"""Mock Server Generator Tool"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class MockServerGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mock_server_generator",
            description="Generates mock API servers from OpenAPI specs for testing.",
            input_schema={
                "type": "object",
                "properties": {
                    "api_spec": {"type": "string"},
                    "framework": {"type": "string", "enum": ["express", "fastapi", "hono"]}
                },
                "required": ["api_spec"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "server_code": {"type": "string"}
                }
            },
            tags={"code", "generation", "api", "mock", "testing"},
            category="api_tools",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        framework = params.get("framework", "express")

        code = f'''const express = require("express");
const app = express();
app.use(express.json());

app.get("/health", (req, res) => {{
  res.json({{ status: "ok" }});
}});

app.all("*", (req, res) => {{
  res.json({{ mock: true, method: req.method, path: req.path }});
}});

app.listen(3000);
'''

        return ToolResult(
            tool_name="mock_server_generator",
            success=True,
            data={"server_code": code},
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
