"""Integration Test Generator Tool - Generate integration tests for APIs and services"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class IntegrationTestGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="integration_test_generator",
            description="Generates integration tests for APIs, services, and database interactions. Supports pytest, Jest, and other testing frameworks.",
            input_schema={
                "type": "object",
                "properties": {
                    "api_spec": {
                        "type": "string",
                        "description": "API specification or endpoint descriptions"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "framework": {
                        "type": "string",
                        "description": "Testing framework",
                        "enum": ["pytest", "jest", "mocha"]
                    },
                    "include_auth": {
                        "type": "boolean",
                        "description": "Include authentication tests",
                        "default": True
                    }
                },
                "required": ["api_spec", "language", "framework"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "test_code": {"type": "string"},
                    "test_count": {"type": "integer"},
                    "endpoints_tested": {"type": "array"}
                }
            },
            tags={"code", "generation", "testing", "integration", "api"},
            category="testing",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        api_spec = params["api_spec"]
        language = params["language"]
        framework = params["framework"]
        include_auth = params.get("include_auth", True)

        try:
            endpoints = self._parse_endpoints(api_spec)
            test_code = self._generate_tests(endpoints, language, framework, include_auth)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="integration_test_generator",
                success=True,
                data={
                    "test_code": test_code,
                    "test_count": len(endpoints) * 3,
                    "endpoints_tested": [e["path"] for e in endpoints]
                },
                execution_time_ms=execution_time,
                metadata={"language": language, "framework": framework}
            )

        except Exception as e:
            return ToolResult(
                tool_name="integration_test_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _parse_endpoints(self, spec: str) -> List[Dict[str, Any]]:
        endpoints = []
        patterns = [
            (r'(GET|POST|PUT|DELETE|PATCH)\s+([/\w{}.-]+)\s*-?\s*([A-Z]\w+(?:\s+[A-Z]\w+)*)?', None)
        ]

        for pattern, _ in patterns:
            for match in re.finditer(pattern, spec, re.IGNORECASE):
                method = match.group(1).upper()
                path = match.group(2)
                description = match.group(3) or ""

                endpoints.append({
                    "method": method,
                    "path": path,
                    "description": description
                })

        if not endpoints:
            endpoints.append({"method": "GET", "path": "/api/resource", "description": "Get resource"})

        return endpoints

    def _generate_tests(self, endpoints: List[Dict[str, Any]], language: str, framework: str, include_auth: bool) -> str:
        if language == "python":
            return self._generate_pytest_tests(endpoints, include_auth)
        elif language in ("javascript", "typescript"):
            return self._generate_jest_tests(endpoints, include_auth)
        return ""

    def _generate_pytest_tests(self, endpoints: List[Dict[str, Any]], include_auth: bool) -> str:
        lines = [
            '"""Integration tests for API endpoints"""',
            "import pytest",
            "from httpx import AsyncClient",
            "from main import app",
            "",
            "",
            "@pytest.mark.asyncio",
            "class TestAPIEndpoints:",
        ]

        if include_auth:
            lines.insert(3, "from unittest.mock import patch")

            lines.extend([
                "",
                "    @pytest.fixture",
                "    async def auth_client():",
                "        \"\"\"Create authenticated test client\"\"\"",
                "        async with AsyncClient(app=app, base_url='http://test') as client:",
                "            with patch('main.authenticate', return_value={'user_id': 1}):",
                "                 yield client",
            ])

        for endpoint in endpoints:
            path = endpoint["path"]
            method = endpoint["method"]
            test_name = f"test_{method.lower()}_{path.replace('/', '_').replace('{{', '').replace('}}', '')}"

            lines.extend([
                "",
                f"    async def {test_name}(self, auth_client):",
                f'        """Test {method} {path}"""',
                f"        response = await auth_client.{method.lower()}({repr(path)})",
                "        assert response.status_code in [200, 201, 400, 401, 404]",
            ])

        lines.extend([
            "",
            "",
            "@pytest.mark.asyncio",
            "class TestHealthChecks:",
            "",
            "    async def test_service_health(self):",
            '        """Test service health endpoint"""',
            "        async with AsyncClient(app=app, base_url='http://test') as client:",
            "            response = await client.get('/health')",
            "            assert response.status_code == 200",
        ])

        return "\n".join(lines)

    def _generate_jest_tests(self, endpoints: List[Dict[str, Any]], include_auth: bool) -> str:
        lines = [
            '"""Integration tests for API endpoints"""',
            "const request = require('supertest');",
            "const app = require('./src/index');",
            "",
            "describe('API Endpoints', () => {",
        ]

        for endpoint in endpoints:
            path = endpoint["path"]
            method = endpoint["method"].toLowerCase()
            test_name = f"test_{method}_{path.replace('/', '_').replace('{', '').replace('}', '')}"

            lines.extend([
                "",
                f"  test('{test_name}', async () => {{",
                f"    const response = await request(app)",
                f"      .{method}({repr(path)})",
                "      .expect((res) => {",
                "        expect([200, 201, 400, 401, 404]).toContain(res.status);",
                "      });",
                "  });",
            ])

        lines.extend([
            "",
            "  describe('Health Checks', () => {",
            "    test('service health', async () => {",
            "      const response = await request(app).get('/health');",
            "      expect(response.status).toBe(200);",
            "    });",
            "  });",
            "});",
        ])

        return "\n".join(lines)
