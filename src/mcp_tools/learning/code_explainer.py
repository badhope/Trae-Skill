"""Code Explainer Tool"""

import re
from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CodeExplainerTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="code_explainer",
            description="Explains code in natural language, breaking down complex logic into understandable parts.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {"type": "string"},
                    "detail_level": {"type": "string", "enum": ["brief", "medium", "detailed"]}
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "explanation": {"type": "string"},
                    "components": {"type": "array"}
                }
            },
            tags={"code", "learning", "explanation", "education"},
            category="learning",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        detail = params.get("detail_level", "medium")

        lines = code.split("\n")
        components = []

        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("def "):
                components.append({"type": "function", "line": i, "content": stripped})
            elif stripped.startswith("class "):
                components.append({"type": "class", "line": i, "content": stripped})
            elif stripped.startswith("#"):
                components.append({"type": "comment", "line": i, "content": stripped})

        explanation = f"This {language} code contains {len(components)} main components. "

        if detail == "detailed":
            explanation += " ".join([f"{c['type']}: {c['content']}" for c in components])

        return ToolResult(
            tool_name="code_explainer",
            success=True,
            data={
                "explanation": explanation,
                "components": components
            },
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
