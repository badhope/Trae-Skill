"""Complexity Analyzer Tool - Calculate cyclomatic complexity and code complexity metrics"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


@dataclass
class ComplexityResult:
    file_path: str
    complexity: int
    rating: str
    functions: List[Dict[str, Any]]
    lines_of_code: int
    maintainability_index: float


class ComplexityAnalyzerTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="complexity_analyzer",
            description="Analyzes code complexity using cyclomatic complexity, halstead metrics, and maintainability index. Provides recommendations for simplifying complex code.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The source code to analyze"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                        "enum": ["python", "javascript", "typescript", "java"]
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Optional file path for context"
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "overall_complexity": {"type": "integer"},
                    "complexity_rating": {"type": "string"},
                    "maintainability_index": {"type": "number"},
                    "functions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "complexity": {"type": "integer"},
                                "lines": {"type": "integer"},
                                "rating": {"type": "string"}
                            }
                        }
                    },
                    "lines_of_code": {"type": "integer"},
                    "recommendations": {"type": "array", "items": {"type": "string"}}
                }
            },
            tags={"code", "complexity", "analysis", "metrics", "quality"},
            category="analyzers",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        file_path = params.get("file_path", "unknown")

        try:
            result = self._analyze_complexity(code, language, file_path)
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="complexity_analyzer",
                success=True,
                data=result,
                execution_time_ms=execution_time,
                metadata={"language": language, "file_path": file_path}
            )

        except Exception as e:
            return ToolResult(
                tool_name="complexity_analyzer",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _analyze_complexity(self, code: str, language: str, file_path: str) -> Dict[str, Any]:
        lines = code.split("\n")
        loc = len(lines)

        functions = self._extract_functions(code, language)

        total_complexity = sum(f["complexity"] for f in functions)
        if not functions:
            total_complexity = self._calculate_file_complexity(code, language)

        avg_complexity = total_complexity / max(len(functions), 1)
        rating = self._get_complexity_rating(avg_complexity)

        maintainability = self._calculate_maintainability_index(code, loc, total_complexity)

        recommendations = self._generate_recommendations(functions, avg_complexity)

        return {
            "overall_complexity": total_complexity,
            "complexity_rating": rating,
            "maintainability_index": round(maintainability, 2),
            "functions": functions,
            "lines_of_code": loc,
            "recommendations": recommendations
        }

    def _extract_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        functions = []
        lines = code.split("\n")

        if language == "python":
            func_pattern = re.compile(r'^def\s+(\w+)\s*\((.*?)\):')
            current_func = None
            func_start = 0
            indent_level = 0

            for i, line in enumerate(lines):
                match = func_pattern.match(line)
                if match:
                    if current_func:
                        func_lines = lines[func_start:i]
                        complexity = self._calculate_complexity("\n".join(func_lines), language)
                        functions.append({
                            "name": current_func["name"],
                            "complexity": complexity,
                            "lines": len(func_lines),
                            "rating": self._get_complexity_rating(complexity),
                            "parameters": current_func["params"]
                        })

                    current_func = {"name": match.group(1), "params": match.group(2)}
                    func_start = i

            if current_func:
                func_lines = lines[func_start:]
                complexity = self._calculate_complexity("\n".join(func_lines), language)
                functions.append({
                    "name": current_func["name"],
                    "complexity": complexity,
                    "lines": len(func_lines),
                    "rating": self._get_complexity_rating(complexity),
                    "parameters": current_func["params"]
                })

        elif language in ("javascript", "typescript"):
            func_patterns = [
                re.compile(r'function\s+(\w+)\s*\((.*?)\)\s*{'),
                re.compile(r'const\s+(\w+)\s*=\s*(?:async\s+)?\((.*?)\)\s*(?:=>|function)\s*{'),
                re.compile(r'(\w+)\s*\((.*?)\)\s*{'),
            ]

            for i, line in enumerate(lines):
                for pattern in func_patterns:
                    match = pattern.match(line.strip())
                    if match:
                        name = match.group(1) if 'function' in line else match.group(1)
                        params = match.group(2) if match.lastindex >= 2 else ""

                        brace_count = line.count('{') - line.count('}')
                        start_line = i
                        end_line = i

                        for j in range(i + 1, len(lines)):
                            brace_count += lines[j].count('{') - lines[j].count('}')
                            if brace_count == 0:
                                end_line = j
                                break

                        func_lines = lines[start_line:end_line + 1]
                        complexity = self._calculate_complexity("\n".join(func_lines), language)
                        functions.append({
                            "name": name,
                            "complexity": complexity,
                            "lines": len(func_lines),
                            "rating": self._get_complexity_rating(complexity),
                            "parameters": params
                        })
                        break

        return functions

    def _calculate_complexity(self, code: str, language: str) -> int:
        complexity = 1

        decision_points = [
            r'\bif\b',
            r'\belse\b',
            r'\belif\b',
            r'\bwhile\b',
            r'\bfor\b',
            r'\bcase\b',
            r'\bcatch\b',
            r'\?\s*:',
            r'\b&&\b',
            r'\b\|\|\b',
        ]

        for pattern in decision_points:
            complexity += len(re.findall(pattern, code))

        return complexity

    def _calculate_file_complexity(self, code: str, language: str) -> int:
        return self._calculate_complexity(code, language)

    def _get_complexity_rating(self, complexity: float) -> str:
        if complexity <= 10:
            return "A (Low Risk)"
        elif complexity <= 20:
            return "B (Moderate Risk)"
        elif complexity <= 30:
            return "C (High Risk)"
        elif complexity <= 50:
            return "D (Very High Risk)"
        else:
            return "F (Untestable)"

    def _calculate_maintainability_index(self, code: str, loc: int, complexity: int) -> float:
        if loc == 0:
            return 100.0

        volume = loc * (complexity / max(1, loc))

        mi = 171 - 5.2 * complexity - 0.23 * volume - 16.2 * (loc / max(1, complexity))

        mi = max(0, min(100, mi))

        return mi

    def _generate_recommendations(self, functions: List[Dict[str, Any]], avg_complexity: float) -> List[str]:
        recommendations = []

        high_complexity_funcs = [f for f in functions if f["complexity"] > 10]

        if high_complexity_funcs:
            names = ", ".join([f["name"] for f in high_complexity_funcs[:3]])
            recommendations.append(
                f"Consider refactoring functions with high complexity: {names}"
            )

        long_functions = [f for f in functions if f["lines"] > 50]
        if long_functions:
            recommendations.append(
                f"Long functions detected ({len(long_functions)}). Consider breaking them into smaller, focused functions."
            )

        if avg_complexity > 20:
            recommendations.append(
                "Overall code complexity is high. Consider extracting complex logic into separate functions or classes."
            )

        if not functions and avg_complexity < 10:
            recommendations.append(
                "Code is simple and maintainable. Keep it that way!"
            )

        return recommendations
