"""Performance Test Generator Tool - Generate performance and load tests"""

import re
from datetime import datetime
from typing import Any, Dict, List
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class PerformanceTestGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="performance_test_generator",
            description="Generates performance tests, load tests, and stress tests. Supports k6, Locust, and other performance testing frameworks.",
            input_schema={
                "type": "object",
                "properties": {
                    "endpoints": {
                        "type": "array",
                        "description": "List of endpoints to test",
                        "items": {"type": "string"}
                    },
                    "language": {
                        "type": "string",
                        "description": "Script language",
                        "enum": ["python", "javascript"]
                    },
                    "framework": {
                        "type": "string",
                        "description": "Performance testing framework",
                        "enum": ["locust", "k6", "pytest-benchmark"]
                    },
                    "target_rps": {
                        "type": "integer",
                        "description": "Target requests per second",
                        "default": 100
                    },
                    "duration_seconds": {
                        "type": "integer",
                        "description": "Test duration in seconds",
                        "default": 60
                    }
                },
                "required": ["endpoints", "language", "framework"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "test_code": {"type": "string"},
                    "instructions": {"type": "string"}
                }
            },
            tags={"code", "generation", "testing", "performance", "load", "stress"},
            category="testing",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        endpoints = params["endpoints"]
        language = params["language"]
        framework = params["framework"]
        target_rps = params.get("target_rps", 100)
        duration = params.get("duration_seconds", 60)

        try:
            if framework == "locust":
                test_code = self._generate_locust_test(endpoints, target_rps, duration)
            elif framework == "k6":
                test_code = self._generate_k6_test(endpoints, target_rps, duration)
            elif framework == "pytest-benchmark":
                test_code = self._generate_pytest_benchmark_test(endpoints)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="performance_test_generator",
                success=True,
                data={
                    "test_code": test_code,
                    "instructions": self._get_instructions(framework)
                },
                execution_time_ms=execution_time,
                metadata={"framework": framework, "endpoints_count": len(endpoints)}
            )

        except Exception as e:
            return ToolResult(
                tool_name="performance_test_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_locust_test(self, endpoints: List[str], target_rps: int, duration: int) -> str:
        users = target_rps // 10

        lines = [
            '"""Locust performance test"""',
            "from locust import HttpUser, task, between",
            "",
            "",
            "class WebsiteUser(HttpUser):",
            f"    wait_time = between(1, {max(2, 10 - users // 20)})",
            f"    host = 'http://localhost:8000'",
            "",
        ]

        for i, endpoint in enumerate(endpoints):
            lines.append(f"    @task({max(1, 10 - i)})")
            lines.append(f"    def task_{i}(self):")
            lines.append(f"        self.client.get('{endpoint}')")

        return "\n".join(lines)

    def _generate_k6_test(self, endpoints: List[str], target_rps: int, duration: int) -> str:
        lines = [
            '// k6 performance test',
            "import http from 'k6/http';",
            "import { check, sleep } from 'k6';",
            "",
            f"export const options = {{",
            f"    stages: [",
            f"        {{ duration: '30s', target: {target_rps} }},",
            f"        {{ duration: '{duration - 30}s', target: {target_rps} }},",
            f"        {{ duration: '30s', target: 0 }},",
            f"    ],",
            "};",
            "",
            "export default function () {",
        ]

        for i, endpoint in enumerate(endpoints):
            lines.append(f"    const res{i} = http.get('{endpoint}');")
            lines.append(f"    check(res{i}, {{")
            lines.append(f"        'status is 200': (r) => r.status === 200,")
            lines.append(f"        'response time < 500ms': (r) => r.timings.duration < 500,")
            lines.append("    });")
            lines.append("    sleep(1);")

        lines.append("}")

        return "\n".join(lines)

    def _generate_pytest_benchmark_test(self, endpoints: List[str]) -> str:
        lines = [
            '"""Pytest benchmark tests"""',
            "import pytest",
            "import httpx",
            "",
        ]

        for endpoint in endpoints:
            func_name = f"test_{endpoint.replace('/', '_').replace('{', '').replace('}', '')}_performance"

            lines.extend([
                f"def {func_name}(benchmark):",
                f'    """Benchmark {endpoint}"""',
                "    def fetch():",
                "        response = httpx.get(f'http://localhost:8000{endpoint}')",
                "        return response",
                "",
                f"    result = benchmark(fetch)",
                "    assert result.status_code == 200",
            ])

        return "\n".join(lines)

    def _get_instructions(self, framework: str) -> str:
        instructions = {
            "locust": """
# Locust Instructions:
# 1. pip install locust
# 2. locust -f locust_test.py --host=http://localhost:8000
# 3. Open http://localhost:8089
""",
            "k6": """
# k6 Instructions:
# 1. Install k6: https://k6.io/docs/getting-started/installation/
# 2. k6 run k6_test.js
# 3. For cloud execution: k6 cloud k6_test.js
""",
            "pytest-benchmark": """
# Pytest Benchmark Instructions:
# 1. pip install pytest-benchmark pytest-httpx
# 2. pytest benchmark_test.py --benchmark-only
"""
        }
        return instructions.get(framework, "")
