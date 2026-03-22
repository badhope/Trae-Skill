"""Code Smell Detector Tool - Detect code smells"""

import re
from datetime import datetime
from typing import Any, Dict, List
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CodeSmellDetectorTool(MCPTool):
    SMELLS = {
        "long_method": {"threshold": 50, "weight": 3},
        "large_class": {"threshold": 500, "weight": 3},
        "long_parameter_list": {"threshold": 4, "weight": 2},
        "too_many_conditionals": {"threshold": 3, "weight": 2},
        "duplicated_code": {"threshold": 3, "weight": 3},
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="code_smell_detector",
            description="Detects code smells and provides suggestions for improvement.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {"type": "string"}
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "smells": {"type": "array"},
                    "smell_count": {"type": "integer"},
                    "overall_health": {"type": "string"}
                }
            },
            tags={"code", "analysis", "code-smell", "quality"},
            category="refactoring",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]

        try:
            smells = self._detect_smells(code, language)
            health = "Good" if len(smells) < 3 else "Needs Attention" if len(smells) < 5 else "Critical"

            return ToolResult(
                tool_name="code_smell_detector",
                success=True,
                data={
                    "smells": smells,
                    "smell_count": len(smells),
                    "overall_health": health
                },
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

        except Exception as e:
            return ToolResult(
                tool_name="code_smell_detector",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _detect_smells(self, code: str, language: str) -> List[Dict[str, Any]]:
        smells = []
        lines = code.split("\n")

        if len(lines) > self.SMELLS["long_method"]["threshold"]:
            smells.append({
                "type": "long_method",
                "severity": "warning",
                "message": f"Code has {len(lines)} lines, consider splitting"
            })

        return smells
