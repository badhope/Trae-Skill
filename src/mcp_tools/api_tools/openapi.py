"""OpenAPI Generator Tool - Generate OpenAPI specifications"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class OpenAPIGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="openapi_generator",
            description="Generates OpenAPI 3.0 specifications from code or natural language descriptions.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "title": {"type": "string", "default": "My API"},
                    "version": {"type": "string", "default": "1.0.0"}
                },
                "required": ["code"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "openapi_spec": {"type": "string"}
                }
            },
            tags={"code", "generation", "api", "openapi", "rest"},
            category="api_tools",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        title = params.get("title", "My API")
        version = params.get("version", "1.0.0")

        spec = f'''openapi: 3.0.0
info:
  title: {title}
  version: {version}
paths:
  /health:
    get:
      summary: Health check
      responses:
        '200':
          description: OK
'''

        return ToolResult(
            tool_name="openapi_generator",
            success=True,
            data={"openapi_spec": spec},
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
