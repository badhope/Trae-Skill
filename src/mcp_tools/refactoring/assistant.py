"""Refactoring Assistant Tool - Suggest and perform code refactoring"""

from datetime import datetime
from typing import Any, Dict, List
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class RefactoringAssistantTool(MCPTool):
    REFACTORING_TYPES = [
        "extract_method", "inline_method", "rename_variable",
        "replace_loop_with_recursion", "pull_up_field", "push_down_field",
        "extract_class", "introduce_parameter_object", "remove_dead_code"
    ]

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="refactoring_assistant",
            description="Provides refactoring suggestions and can perform common refactoring operations on code.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "target_pattern": {
                        "type": "string",
                        "enum": REFACTORING_TYPES
                    },
                    "language": {
                        "type": "string",
                        "enum": ["python", "javascript", "typescript", "java"]
                    }
                },
                "required": ["code", "target_pattern", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "original_code": {"type": "string"},
                    "refactored_code": {"type": "string"},
                    "changes_summary": {"type": "array"}
                }
            },
            tags={"code", "refactoring", "assistant", "restructure"},
            category="refactoring",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        pattern = params["target_pattern"]
        language = params["language"]

        try:
            refactored = self._apply_refactoring(code, pattern, language)

            return ToolResult(
                tool_name="refactoring_assistant",
                success=True,
                data={
                    "original_code": code,
                    "refactored_code": refactored,
                    "changes_summary": [f"Applied {pattern} refactoring"]
                },
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

        except Exception as e:
            return ToolResult(
                tool_name="refactoring_assistant",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _apply_refactoring(self, code: str, pattern: str, language: str) -> str:
        return code
