import asyncio
import time
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from context_memory.manager import MemoryManager, ContextAssembler
from rl_engine.engine import RLEngine, RLConfig
from mcp_tools.framework import MCPFramework
from mcp_tools.tools import CodeQualityCheckerTool, UnitTestGeneratorTool


class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.memory_manager = MemoryManager()
        self.rl_engine = RLEngine(RLConfig())
        self.mcp_framework = MCPFramework()
        self.mcp_framework.register_tool(CodeQualityCheckerTool())
        self.mcp_framework.register_tool(UnitTestGeneratorTool())

    def test_memory_search_performance(self):
        for i in range(100):
            asyncio.run(self.memory_manager.store(
                content=f"Test content {i} with some unique keywords",
                importance_score=0.5 + (i % 50) / 100,
                tags={f"tag{i % 10}"}
            ))

        start_time = time.time()

        for _ in range(20):
            asyncio.run(self.memory_manager.search(
                query_text="keywords",
                threshold=0.3,
                top_k=10
            ))

        elapsed = time.time() - start_time
        avg_time_ms = (elapsed / 20) * 1000

        print(f"\nMemory search average: {avg_time_ms:.2f}ms")
        self.assertLess(avg_time_ms, 100, f"Search took {avg_time_ms}ms, should be <100ms")

    def test_mcp_tool_execution_performance(self):
        code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    return quicksort([x for x in arr if x < pivot]) + \\
           quicksort([x for x in arr if x >= pivot])
'''

        start_time = time.time()

        for _ in range(50):
            asyncio.run(self.mcp_framework.execute_tool(
                "code_quality_checker",
                {"code": code, "language": "python"}
            ))

        elapsed = time.time() - start_time
        avg_time_ms = (elapsed / 50) * 1000

        print(f"\nMCP tool average: {avg_time_ms:.2f}ms")
        self.assertLess(avg_time_ms, 200, f"MCP tool took {avg_time_ms}ms, should be <200ms")

    def test_concurrent_mcp_execution(self):
        code = "def test(): pass"

        async def execute_many():
            tasks = []
            for _ in range(100):
                task = self.mcp_framework.execute_tool(
                    "code_quality_checker",
                    {"code": code, "language": "python"}
                )
                tasks.append(task)
            return await asyncio.gather(*tasks)

        start_time = time.time()
        results = asyncio.run(execute_many())
        elapsed = time.time() - start_time

        success_count = sum(1 for r in results if r.success)

        print(f"\nConcurrent 100 requests: {elapsed:.2f}s, success: {success_count}")
        self.assertGreaterEqual(success_count, 95)

    def test_memory_bulk_operations(self):
        start_time = time.time()

        for i in range(1000):
            asyncio.run(self.memory_manager.store(
                content=f"Bulk content {i}",
                importance_score=0.5
            ))

        store_elapsed = time.time() - start_time

        start_time = time.time()

        for i in range(100):
            asyncio.run(self.memory_manager.search(
                query_text=f"content {i}",
                threshold=0.1,
                top_k=5
            ))

        search_elapsed = time.time() - start_time

        print(f"\nBulk store 1000 entries: {store_elapsed:.2f}s")
        print(f"100 searches: {search_elapsed:.2f}s")

    def test_rl_engine_training_performance(self):
        from rl_engine.reward import CodeAction, CodeActionType

        for i in range(50):
            state = self.rl_engine.state_to_embedding({
                "current_query": f"Query {i}",
                "memory_context": {"total_entries": i},
                "action_type": "generate",
                "language": "python"
            })

            action, _ = asyncio.run(self.rl_engine.select_action(state))

            code_action = CodeAction(
                action_type=CodeActionType.GENERATE,
                code=f"def function_{i}(): return {i}",
                language="python",
                step_number=i
            )

            asyncio.run(self.rl_engine.execute_action(code_action, {}))

        start_time = time.time()

        for _ in range(20):
            asyncio.run(self.rl_engine.train_step())

        elapsed = time.time() - start_time
        avg_time_ms = (elapsed / 20) * 1000

        print(f"\nRL training step average: {avg_time_ms:.2f}ms")

    def test_context_assembly_performance(self):
        for i in range(50):
            asyncio.run(self.memory_manager.store(
                content=f"Session content {i}",
                importance_score=0.5,
                metadata={"session_id": "perf_test"}
            ))

        assembler = ContextAssembler(self.memory_manager)

        start_time = time.time()

        for _ in range(100):
            asyncio.run(assembler.assemble_context(
                current_query="What am I doing?",
                session_id="perf_test"
            ))

        elapsed = time.time() - start_time
        avg_time_ms = (elapsed / 100) * 1000

        print(f"\nContext assembly average: {avg_time_ms:.2f}ms")
        self.assertLess(avg_time_ms, 50)


class TestStress(unittest.TestCase):
    def test_high_concurrency_memory(self):
        manager = MemoryManager()

        async def stress_test():
            async def store_batch(batch_id):
                tasks = []
                for i in range(50):
                    task = manager.store(
                        content=f"Batch {batch_id} item {i}",
                        importance_score=0.5
                    )
                    tasks.append(task)
                await asyncio.gather(*tasks)

            tasks = [store_batch(i) for i in range(20)]
            await asyncio.gather(*tasks)

        start_time = time.time()
        asyncio.run(stress_test())
        elapsed = time.time() - start_time

        print(f"\nStress test (1000 stores): {elapsed:.2f}s")
        self.assertLess(elapsed, 5.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
