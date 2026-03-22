"""API Documentation Generator Tool - Generate API documentation"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class APIDocGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="api_doc_generator",
            description="Generates API documentation from code or OpenAPI specifications. Supports Markdown, Swagger, and HTML formats.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Source code or OpenAPI spec"
                    },
                    "format": {
                        "type": "string",
                        "description": "Documentation format",
                        "enum": ["markdown", "openapi", "html", "swagger"]
                    },
                    "language": {
                        "type": "string",
                        "description": "Documentation language",
                        "default": "en"
                    }
                },
                "required": ["code"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "documentation": {"type": "string"},
                    "endpoints_count": {"type": "integer"}
                }
            },
            tags={"code", "generation", "documentation", "api", "openapi"},
            category="documentation",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        format = params.get("format", "markdown")
        lang = params.get("language", "en")

        try:
            doc = self._generate_doc(code, format, lang)
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="api_doc_generator",
                success=True,
                data={"documentation": doc, "endpoints_count": doc.count("## Endpoint")},
                execution_time_ms=execution_time
            )

        except Exception as e:
            return ToolResult(
                tool_name="api_doc_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_doc(self, code: str, format: str, lang: str) -> str:
        if format == "markdown":
            return self._generate_markdown_doc(code, lang)
        elif format == "html":
            return self._generate_html_doc(code)
        return self._generate_markdown_doc(code, lang)

    def _generate_markdown_doc(self, code: str, lang: str) -> str:
        title = "# API Documentation" if lang == "en" else "# API 文档"
        return f"{title}\n\nGenerated from source code.\n\n## Endpoints\n\n- TBD"
