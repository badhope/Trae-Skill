import asyncio
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rl_engine.reward import (
    CodeAction,
    CodeActionType,
    ExecutionResult,
    RewardCalculator,
    Experience,
    ExperienceBuffer,
    PrioritizedReplayBuffer,
)
from rl_engine.ppo import PolicyNetwork, ValueNetwork, PPOTrainer
from rl_engine.engine import RLEngine, RLConfig, ExplorationStrategy, CodeSimulator


class TestRewardCalculation(unittest.TestCase):
    def test_basic_reward_calculation(self):
        calculator = RewardCalculator()

        action = CodeAction(
            action_type=CodeActionType.GENERATE,
            code='def hello():\n    """Say hello."""\n    print("Hello")',
            language="python",
        )

        result = ExecutionResult(
            success=True,
            output="Hello",
            execution_time=0.5,
            test_passed=True,
            user_rating=0.9,
            task_completion_rate=1.0,
        )

        reward = calculator.calculate(action, result)

        self.assertGreater(reward, 0.5)
        self.assertLessEqual(reward, 1.0)

    def test_failed_execution_reward(self):
        calculator = RewardCalculator()

        action = CodeAction(
            action_type=CodeActionType.GENERATE,
            code="invalid code here",
            language="python",
        )

        result = ExecutionResult(
            success=False,
            output="",
            error="SyntaxError",
            execution_time=0.1,
            test_passed=False,
            task_completion_rate=0.0,
        )

        reward = calculator.calculate(action, result)
        self.assertIsInstance(reward, float)

    def test_code_quality_reward(self):
        calculator = RewardCalculator()

        good_code = '''def add(a, b):
    """Add two numbers."""
    try:
        return int(a) + int(b)
    except ValueError:
        return 0
'''
        bad_code = "def add(a,b):return a+b"

        action_good = CodeAction(CodeActionType.GENERATE, good_code, "python")
        action_bad = CodeAction(CodeActionType.GENERATE, bad_code, "python")
        result = ExecutionResult(success=True, output="", execution_time=1.0)

        reward_good = calculator._calculate_code_quality(action_good)
        reward_bad = calculator._calculate_code_quality(action_bad)

        self.assertGreater(reward_good, reward_bad)


class TestExperienceBuffer(unittest.TestCase):
    def test_experience_buffer_add(self):
        buffer = ExperienceBuffer(capacity=10)

        experience = Experience(
            state=np.array([1.0, 2.0]),
            action=CodeAction(CodeActionType.GENERATE, "test", "python"),
            reward=0.8,
            next_state=np.array([2.0, 3.0]),
            done=False,
        )

        asyncio.run(buffer.add(experience))
        self.assertEqual(buffer.size(), 1)

    def test_experience_buffer_sample(self):
        buffer = ExperienceBuffer(capacity=100)

        for i in range(20):
            experience = Experience(
                state=np.array([float(i), float(i + 1)]),
                action=CodeAction(CodeActionType.GENERATE, f"code_{i}", "python"),
                reward=float(i) / 20.0,
                next_state=np.array([float(i + 1), float(i + 2)]),
                done=False,
            )
            asyncio.run(buffer.add(experience))

        sampled = asyncio.run(buffer.sample(5))
        self.assertEqual(len(sampled), 5)

    def test_prioritized_replay(self):
        buffer = PrioritizedReplayBuffer(capacity=50, alpha=0.6)

        for i in range(10):
            experience = Experience(
                state=np.array([float(i)]),
                action=CodeAction(CodeActionType.GENERATE, f"code_{i}", "python"),
                reward=float(i) / 10.0,
                next_state=np.array([float(i + 1)]),
                done=False,
                priority=float(i + 1),
            )
            asyncio.run(buffer.add(experience))

        sampled, weights, indices = asyncio.run(buffer.sample(5))

        self.assertEqual(len(sampled), 5)
        self.assertEqual(len(weights), 5)
        self.assertEqual(len(indices), 5)


class TestPolicyNetwork(unittest.TestCase):
    def test_policy_forward(self):
        policy = PolicyNetwork(state_dim=8, action_dim=4, hidden_dims=[16, 8])

        state = np.random.randn(1, 8)
        output = policy.forward(state)

        self.assertEqual(output.shape, (1, 4))

    def test_policy_get_action(self):
        policy = PolicyNetwork(state_dim=8, action_dim=4, hidden_dims=[16, 8])

        state = np.random.randn(1, 8)
        action, log_prob = policy.get_action(state, temperature=1.0)

        self.assertGreaterEqual(action, 0)
        self.assertLess(action, 4)
        self.assertLessEqual(log_prob, 0)


class TestValueNetwork(unittest.TestCase):
    def test_value_forward(self):
        value = ValueNetwork(state_dim=8, hidden_dims=[16, 8])

        state = np.random.randn(1, 8)
        output = value.forward(state)

        self.assertIsInstance(output, float)


class TestPPOTrainer(unittest.TestCase):
    def test_ppo_trainer_add_experience(self):
        policy = PolicyNetwork(state_dim=8, action_dim=4)
        value = ValueNetwork(state_dim=8)
        trainer = PPOTrainer(policy, value, update_interval=5)

        state = np.random.randn(8)
        trainer.add_experience(state, action=1, old_log_prob=-0.5, reward=0.8)

        self.assertEqual(len(trainer._trajectory), 1)


class TestExplorationStrategy(unittest.TestCase):
    def test_exploration_decay(self):
        strategy = ExplorationStrategy(
            initial_epsilon=1.0,
            min_epsilon=0.1,
            decay_rate=0.9
        )

        initial_epsilon = strategy.get_epsilon()
        strategy.decay()
        decayed_epsilon = strategy.get_epsilon()

        self.assertLess(decayed_epsilon, initial_epsilon)
        self.assertGreaterEqual(decayed_epsilon, 0.1)

    def test_exploration_select_action_random(self):
        strategy = ExplorationStrategy(initial_epsilon=1.0, min_epsilon=0.01)
        policy = PolicyNetwork(state_dim=8, action_dim=4)

        state = np.random.randn(1, 8)

        random_actions = set()
        for _ in range(100):
            action, _ = strategy.select_action(policy, state, 4, training=True)
            random_actions.add(action)

        self.assertGreater(len(random_actions), 1)


class TestCodeSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = CodeSimulator()

    def test_supported_languages(self):
        languages = self.simulator.get_supported_languages()

        self.assertIn("python", languages)
        self.assertIn("javascript", languages)

    def test_python_execution_success(self):
        code = "print('Hello, World!')"

        result = asyncio.run(self.simulator.execute(code, "python"))

        self.assertTrue(result.success)
        self.assertIn("Hello", result.output)

    def test_python_execution_error(self):
        code = "print('未闭合的字符串)"

        result = asyncio.run(self.simulator.execute(code, "python"))

        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)

    def test_unsupported_language(self):
        code = "some code"
        result = asyncio.run(self.simulator.execute(code, "cobol"))

        self.assertFalse(result.success)


class TestRLEngine(unittest.TestCase):
    def setUp(self):
        self.config = RLConfig(
            state_dim=16,
            action_dim=6,
            hidden_dims=[32, 16],
            epsilon=1.0,
            epsilon_min=0.1,
            epsilon_decay=0.95,
        )
        self.engine = RLEngine(self.config)

    def test_state_to_embedding(self):
        context = {
            "current_query": "How do I sort a list?",
            "memory_context": {"total_entries": 50},
            "action_type": "generate",
            "language": "python",
        }

        embedding = self.engine.state_to_embedding(context)

        self.assertEqual(embedding.shape[0], 16)

    def test_select_action(self):
        state = np.random.randn(16)

        action, log_prob = asyncio.run(self.engine.select_action(state, training=True))

        self.assertGreaterEqual(action, 0)
        self.assertLess(action, 6)

    def test_engine_statistics(self):
        stats = self.engine.get_statistics()

        self.assertIn("total_experiences", stats)
        self.assertIn("epsilon", stats)
        self.assertEqual(stats["epsilon"], 1.0)


class TestRLIntegration(unittest.TestCase):
    def test_full_training_cycle(self):
        config = RLConfig(
            state_dim=8,
            action_dim=4,
            hidden_dims=[16, 8],
            epsilon=1.0,
            epsilon_min=0.1,
            batch_size=4,
            update_interval=4,
        )
        engine = RLEngine(config)

        for i in range(10):
            state = np.random.randn(8)
            context = {
                "current_query": f"Query {i}",
                "memory_context": {"total_entries": i},
                "action_type": "generate",
                "language": "python",
            }

            action, _ = asyncio.run(engine.select_action(state, training=True))

            code_action = CodeAction(
                action_type=CodeActionType.GENERATE,
                code=f"def function_{i}(): pass",
                language="python",
                step_number=i,
            )

            result = asyncio.run(engine.execute_action(code_action, context))

            self.assertIsNotNone(result)

        for _ in range(5):
            asyncio.run(engine.train_step())

        stats = engine.get_statistics()
        self.assertGreater(stats["total_experiences"], 0)


if __name__ == "__main__":
    unittest.main()
