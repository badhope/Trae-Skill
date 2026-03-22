"""Code Comment Generator Tool - Generate code comments"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CodeCommentGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="code_comment_generator",
            description="Generates documentation comments for source code. Supports docstrings, JSDoc, and various comment styles.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Source code"},
                    "language": {
                        "type": "string",
                        "enum": ["python", "javascript", "typescript", "java", "go"]
                    },
                    "style": {
                        "type": "string",
                        "enum": ["docstring", "jsdoc", "google", "numpy"]
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "commented_code": {"type": "string"},
                    "comments_added": {"type": "integer"}
                }
            },
            tags={"code", "generation", "documentation", "comments", "docstring"},
            category="documentation",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        style = params.get("style", "docstring" if language == "python" else "jsdoc")

        try:
            commented = self._add_comments(code, language, style)
            count = commented.count('"""') + commented.count("'''") + commented.count("/**")

            return ToolResult(
                tool_name="code_comment_generator",
                success=True,
                data={"commented_code": commented, "comments_added": count},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

        except Exception as e:
            return ToolResult(
                tool_name="code_comment_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _add_comments(self, code: str, language: str, style: str) -> str:
        lines = code.split("\n")
        result = []
        for i, line in enumerate(lines):
            if f"def " in line or f"function " in line or f"class " in line:
                indent = len(line) - len(line.lstrip())
                prefix = line[:indent] if indent > 0 else ""
                if language == "python":
                    result.append(f'{prefix}"""Function description."""')
                else:
                    result.append(f'{prefix}/**\n{prefix} * @description Function description\n{prefix} */')
            result.append(line)
        return "\n".join(result)
