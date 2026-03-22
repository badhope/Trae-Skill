"""Reinforcement Learning Engine - PPO-based RL framework"""

from rl_engine.engine import RLConfig, ExplorationStrategy, CodeSimulator, RLEngine
from rl_engine.ppo import PolicyNetwork, ValueNetwork, PPOTrainer
from rl_engine.reward import (
    CodeActionType,
    CodeAction,
    ExecutionResult,
    RewardCalculator,
    Experience,
    ExperienceBuffer,
    PrioritizedReplayBuffer,
)

__all__ = [
    "RLConfig",
    "ExplorationStrategy",
    "CodeSimulator",
    "RLEngine",
    "PolicyNetwork",
    "ValueNetwork",
    "PPOTrainer",
    "CodeActionType",
    "CodeAction",
    "ExecutionResult",
    "RewardCalculator",
    "Experience",
    "ExperienceBuffer",
    "PrioritizedReplayBuffer",
]

__version__ = "1.1.0"
