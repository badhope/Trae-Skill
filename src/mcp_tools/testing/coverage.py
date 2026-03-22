"""Coverage Analyzer Tool - Analyze test coverage reports"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CoverageAnalyzerTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="coverage_analyzer",
            description="Analyzes test coverage reports and provides recommendations for improving coverage. Supports coverage.py, Istanbul, and other coverage tools.",
            input_schema={
                "type": "object",
                "properties": {
                    "coverage_report": {
                        "type": "string",
                        "description": "Coverage report in text or JSON format"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "target_coverage": {
                        "type": "number",
                        "description": "Target coverage percentage",
                        "default": 80
                    }
                },
                "required": ["coverage_report", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "coverage_percentage": {"type": "number"},
                    "grade": {"type": "string"},
                    "uncovered_lines": {"type": "array"},
                    "recommendations": {"type": "array"}
                }
            },
            tags={"code", "analysis", "testing", "coverage"},
            category="testing",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        coverage_report = params["coverage_report"]
        language = params["language"]
        target = params.get("target_coverage", 80)

        try:
            coverage_pct = self._extract_coverage(coverage_report)
            uncovered = self._find_uncovered_lines(coverage_report)
            recommendations = self._generate_recommendations(coverage_pct, target, uncovered)
            grade = self._calculate_grade(coverage_pct)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="coverage_analyzer",
                success=True,
                data={
                    "coverage_percentage": coverage_pct,
                    "grade": grade,
                    "uncovered_lines": uncovered[:20],
                    "recommendations": recommendations
                },
                execution_time_ms=execution_time,
                metadata={"language": language, "target": target}
            )

        except Exception as e:
            return ToolResult(
                tool_name="coverage_analyzer",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _extract_coverage(self, report: str) -> float:
        import re
        match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', report)
        if match:
            return float(match.group(1))

        match = re.search(r'"percent_covered"\s*:\s*"?(\d+\.?\d*)"?', report)
        if match:
            return float(match.group(1))

        match = re.search(r'(\d+\.?\d*)\s*%', report)
        if match:
            return float(match.group(1))

        return 0.0

    def _find_uncovered_lines(self, report: str) -> list:
        import re
        lines = []

        matches = re.findall(r'SRC.*:(\d+)\s+.*0\s*$', report, re.MULTILINE)
        lines.extend([f"Line {m}" for m in matches[:50]])

        return lines

    def _calculate_grade(self, coverage: float) -> str:
        if coverage >= 90:
            return "A (Excellent)"
        elif coverage >= 80:
            return "B (Good)"
        elif coverage >= 70:
            return "C (Fair)"
        elif coverage >= 60:
            return "D (Poor)"
        else:
            return "F (Fail)"

    def _generate_recommendations(self, coverage: float, target: float, uncovered: list) -> list:
        recommendations = []

        if coverage < target:
            recommendations.append(f"Coverage {coverage}% is below target {target}%. Focus on testing uncovered functions.")

        if coverage < 70:
            recommendations.append("Critical: Test coverage is too low. Prioritize adding tests for critical paths.")

        if len(uncovered) > 10:
            recommendations.append("Consider using @pytest.mark.parametrize for testing multiple inputs efficiently.")

        recommendations.append("Run 'pytest --cov --cov-report=term-missing' to see detailed line-by-line coverage.")

        return recommendations
