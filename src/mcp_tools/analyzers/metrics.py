"""Code Metrics Collector Tool - Collect various code metrics and measurements"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


@dataclass
class CodeMetrics:
    loc: int
    sloc: int
    comments: int
    blank_lines: int
    comment_ratio: float
    average_line_length: float
    max_line_length: int


class CodeMetricsCollectorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="code_metrics_collector",
            description="Collects comprehensive code metrics including lines of code, comment ratio, complexity metrics, and Halstead measurements.",
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
                        "enum": ["python", "javascript", "typescript", "java", "go", "rust"]
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "loc": {"type": "integer", "description": "Total lines of code"},
                    "sloc": {"type": "integer", "description": "Source lines of code (non-blank, non-comment)"},
                    "comments": {"type": "integer", "description": "Lines of comments"},
                    "blank_lines": {"type": "integer", "description": "Blank lines"},
                    "comment_ratio": {"type": "number", "description": "Comment to code ratio"},
                    "average_line_length": {"type": "number", "description": "Average line length"},
                    "max_line_length": {"type": "integer", "description": "Maximum line length"},
                    "functions": {"type": "integer", "description": "Number of functions"},
                    "classes": {"type": "integer", "description": "Number of classes"},
                    "files": {"type": "integer", "description": "Number of files (if multi-file)"},
                    "halstead": {
                        "type": "object",
                        "description": "Halstead metrics",
                        "properties": {
                            "volume": {"type": "number"},
                            "difficulty": {"type": "number"},
                            "effort": {"type": "number"}
                        }
                    }
                }
            },
            tags={"code", "metrics", "analysis", "measurement", "halstead"},
            category="analyzers",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]

        try:
            metrics = self._collect_metrics(code, language)
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="code_metrics_collector",
                success=True,
                data=metrics,
                execution_time_ms=execution_time,
                metadata={"language": language}
            )

        except Exception as e:
            return ToolResult(
                tool_name="code_metrics_collector",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _collect_metrics(self, code: str, language: str) -> Dict[str, Any]:
        lines = code.split("\n")
        total_lines = len(lines)

        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = self._count_comment_lines(lines, language)

        sloc = total_lines - blank_lines - comment_lines
        comment_ratio = (comment_lines / sloc * 100) if sloc > 0 else 0

        line_lengths = [len(line) for line in lines if line.strip()]
        avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
        max_line_length = max(line_lengths) if line_lengths else 0

        function_count = self._count_functions(code, language)
        class_count = self._count_classes(code, language)

        halstead = self._calculate_halstead(code, language)

        return {
            "loc": total_lines,
            "sloc": sloc,
            "comments": comment_lines,
            "blank_lines": blank_lines,
            "comment_ratio": round(comment_ratio, 2),
            "average_line_length": round(avg_line_length, 2),
            "max_line_length": max_line_length,
            "functions": function_count,
            "classes": class_count,
            "files": 1,
            "halstead": halstead
        }

    def _count_comment_lines(self, lines: List[str], language: str) -> int:
        comment_lines = 0
        in_block_comment = False

        for line in lines:
            stripped = line.strip()

            if language == "python":
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                        comment_lines += 1
                    else:
                        in_block_comment = not in_block_comment
                        comment_lines += 1
                elif in_block_comment:
                    comment_lines += 1
                elif stripped.startswith('#'):
                    comment_lines += 1

            elif language in ("javascript", "typescript", "java", "go", "rust"):
                if '/*' in line:
                    in_block_comment = True
                    comment_lines += 1
                elif '*/' in line:
                    in_block_comment = False
                    comment_lines += 1
                elif in_block_comment:
                    comment_lines += 1
                elif stripped.startswith('//'):
                    comment_lines += 1

        return comment_lines

    def _count_functions(self, code: str, language: str) -> int:
        if language == "python":
            pattern = r'^def\s+\w+\s*\('
        elif language in ("javascript", "typescript"):
            pattern = r'(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s+)?\(|(?:async\s+)?\w+\s*\([^)]*\)\s*{)'
        elif language == "java":
            pattern = r'(?:public|private|protected)?\s*(?:static)?\s+\w+\s+\w+\s*\([^)]*\)'
        elif language in ("go", "rust"):
            pattern = r'func\s+\w+'
        else:
            pattern = r'\w+\s*\([^)]*\)\s*{'

        return len(re.findall(pattern, code, re.MULTILINE))

    def _count_classes(self, code: str, language: str) -> int:
        if language == "python":
            pattern = r'^class\s+\w+'
        elif language in ("javascript", "typescript"):
            pattern = r'class\s+\w+'
        elif language == "java":
            pattern = r'class\s+\w+'
        elif language == "go":
            pattern = r'type\s+\w+\s+struct'
        elif language == "rust":
            pattern = r'struct\s+\w+'
        else:
            pattern = r'class\s+\w+'

        return len(re.findall(pattern, code, re.MULTILINE))

    def _calculate_halstead(self, code: str, language: str) -> Dict[str, float]:
        operators = set()
        operands = set()

        operator_patterns = [
            r'[+\-*/%=<>!&|^~]',
            r'\b(if|else|while|for|return|try|catch|throw|class|def|import|from|as|and|or|not|in|is)\b',
        ]

        for pattern in operator_patterns:
            operators.update(re.findall(pattern, code))

        operand_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        reserved_words = {'if', 'else', 'while', 'for', 'return', 'try', 'catch', 'throw', 'class', 'def', 'import', 'from', 'as', 'and', 'or', 'not', 'in', 'is', 'true', 'false', 'null', 'none', 'undefined'}
        all_identifiers = re.findall(operand_pattern, code)
        operands = {word for word in all_identifiers if word not in reserved_words}

        n1 = len(operators)
        n2 = len(operands)
        N1 = len([op for op in re.findall(r'[+\-*/%=<>!&|^~]', code)])
        N2 = len(operands)

        N = N1 + N2
        n = n1 + n2

        if n1 > 0 and n2 > 0:
            volume = N * (n ** 0.5) if n > 0 else 0
            difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
            effort = volume * difficulty
        else:
            volume = 0
            difficulty = 0
            effort = 0

        return {
            "volume": round(volume, 2),
            "difficulty": round(difficulty, 2),
            "effort": round(effort, 2)
        }
