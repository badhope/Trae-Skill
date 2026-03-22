"""CI Config Generator Tool"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CIConfigGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="ci_config_generator",
            description="Generates CI/CD configuration files for GitHub Actions, GitLab CI, etc.",
            input_schema={
                "type": "object",
                "properties": {
                    "platform": {"type": "string", "enum": ["github", "gitlab", "jenkins"]},
                    "language": {"type": "string"},
                    "include_deploy": {"type": "boolean", "default": False}
                },
                "required": ["platform", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "config": {"type": "string"}
                }
            },
            tags={"code", "generation", "ci", "cd", "devops", "automation"},
            category="devops",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        platform = params["platform"]

        if platform == "github":
            config = '''name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pip install pytest && pytest
'''
        else:
            config = "# CI configuration"

        return ToolResult(
            tool_name="ci_config_generator",
            success=True,
            data={"config": config},
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
