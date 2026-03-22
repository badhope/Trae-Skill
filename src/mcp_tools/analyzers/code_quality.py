"""Code Quality Checker Tool - Static code analysis for quality, security, and performance issues"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CodeQualityCheckerTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._issues_found: List[Dict[str, Any]] = []

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="code_quality_checker",
            description="Performs static analysis on code to identify issues related to code quality, style, potential bugs, and security vulnerabilities. Supports Python, JavaScript, TypeScript, Java, Go, and Rust.",
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
                    },
                    "check_security": {
                        "type": "boolean",
                        "description": "Enable security vulnerability checks",
                        "default": True
                    },
                    "check_style": {
                        "type": "boolean",
                        "description": "Enable code style checks",
                        "default": True
                    },
                    "check_performance": {
                        "type": "boolean",
                        "description": "Enable performance issue checks",
                        "default": True
                    },
                    "check_best_practices": {
                        "type": "boolean",
                        "description": "Enable best practices checks",
                        "default": True
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "quality_score": {"type": "number", "description": "Overall quality score 0-100"},
                    "grade": {"type": "string", "description": "Letter grade A/B/C/D/F"},
                    "issues": {
                        "type": "array",
                        "description": "List of identified issues",
                        "items": {
                            "type": "object",
                            "properties": {
                                "line": {"type": "integer", "description": "Line number"},
                                "severity": {"type": "string", "description": "error/warning/info"},
                                "category": {"type": "string", "description": "Issue category"},
                                "message": {"type": "string", "description": "Issue description"},
                                "suggestion": {"type": "string", "description": "How to fix"}
                            }
                        }
                    },
                    "summary": {
                        "type": "object",
                        "properties": {
                            "total_issues": {"type": "integer"},
                            "errors": {"type": "integer"},
                            "warnings": {"type": "integer"},
                            "info": {"type": "integer"}
                        }
                    }
                }
            },
            tags={"code", "quality", "analysis", "lint", "security", "performance"},
            category="analyzers",
            version="2.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        check_security = params.get("check_security", True)
        check_style = params.get("check_style", True)
        check_performance = params.get("check_performance", True)
        check_best_practices = params.get("check_best_practices", True)

        try:
            issues = self._analyze_code(
                code, language,
                check_security,
                check_style,
                check_performance,
                check_best_practices
            )

            error_count = len([i for i in issues if i["severity"] == "error"])
            warning_count = len([i for i in issues if i["severity"] == "warning"])
            info_count = len([i for i in issues if i["severity"] == "info"])

            quality_score = max(0, 100 - (error_count * 20) - (warning_count * 5) - (info_count * 1))

            if quality_score >= 90:
                grade = "A"
            elif quality_score >= 80:
                grade = "B"
            elif quality_score >= 70:
                grade = "C"
            elif quality_score >= 60:
                grade = "D"
            else:
                grade = "F"

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="code_quality_checker",
                success=True,
                data={
                    "quality_score": quality_score,
                    "grade": grade,
                    "issues": issues,
                    "summary": {
                        "total_issues": len(issues),
                        "errors": error_count,
                        "warnings": warning_count,
                        "info": info_count
                    }
                },
                execution_time_ms=execution_time,
                metadata={"language": language, "lines_of_code": len(code.splitlines())}
            )

        except Exception as e:
            return ToolResult(
                tool_name="code_quality_checker",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _analyze_code(
        self,
        code: str,
        language: str,
        check_security: bool,
        check_style: bool,
        check_performance: bool,
        check_best_practices: bool
    ) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        lines = code.split("\n")

        analyzers = {
            "security": self._check_security_issues if check_security else lambda l, n: [],
            "style": self._check_style_issues if check_style else lambda l, n: [],
            "performance": self._check_performance_issues if check_performance else lambda l, n: [],
            "best_practices": self._check_best_practices if check_best_practices else lambda l, n: []
        }

        for i, line in enumerate(lines, 1):
            for check_name, checker in analyzers.items():
                found_issues = checker(line, i)
                issues.extend(found_issues)

        return issues

    def _check_security_issues(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        issues = []
        line_stripped = line.strip()

        patterns = [
            (r"eval\s*\(", "Use of eval() - potential code injection risk"),
            (r"exec\s*\(", "Use of exec() - potential code injection risk"),
            (r"pickle\.loads?", "Pickle deserialization - potential code execution"),
            (r"subprocess\.\w+\s*\(\s*shell\s*=\s*True", "shell=True is a security risk"),
            (r"password\s*=\s*['\"][^'\"]{0,}", "Hardcoded password detected"),
            (r"api[_-]?key\s*=\s*['\"][^'\"]{0,}", "Hardcoded API key detected"),
            (r"secret\s*=\s*['\"][^'\"]{0,}", "Hardcoded secret detected"),
            (r"os\.system\s*\(", "os.system is vulnerable to shell injection"),
            (r"SQL\s*\(", "Raw SQL query - use parameterized queries"),
            (r"\.format\s*\(\s*['\"].*\%", "String formatting for SQL - use parameterized queries"),
            (r"innerHTML\s*=", "innerHTML assignment - potential XSS risk"),
            (r"document\.write\s*\(", "document.write - potential XSS risk"),
            (r"__import__\s*\(", "Dynamic import - potential code injection"),
            (r"yaml\.load\s*\(", "yaml.load without Loader - unsafe"),
        ]

        for pattern, message in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    "line": line_num,
                    "severity": "error",
                    "category": "security",
                    "message": message,
                    "suggestion": "Use secure alternatives and remove hardcoded secrets"
                })

        return issues

    def _check_style_issues(self, line: str, line_num: int, language: str) -> List[Dict[str, Any]]:
        issues = []
        line_stripped = line.strip()

        if language == "python":
            if len(line) > 120:
                issues.append({
                    "line": line_num,
                    "severity": "warning",
                    "category": "style",
                    "message": f"Line too long ({len(line)} > 120 characters)",
                    "suggestion": "Break line to fit within 120 characters"
                })

            if line_stripped and not line_stripped.startswith('#') and not line_stripped.startswith('"""') and not line_stripped.startswith("'''"):
                if re.match(r'^[A-Z][A-Z_]*\s*=', line_stripped):
                    issues.append({
                        "line": line_num,
                        "severity": "info",
                        "category": "style",
                        "message": "Constants should be in SCREAMING_SNAKE_CASE",
                        "suggestion": "Constants are already correctly named"
                    })

                if re.match(r'^def\s+\w+', line_stripped) and '  ' in line_stripped.split('def')[0]:
                    issues.append({
                        "line": line_num,
                        "severity": "warning",
                        "category": "style",
                        "message": "Inconsistent indentation",
                        "suggestion": "Use 4 spaces per indentation level"
                    })

        elif language in ("javascript", "typescript"):
            if len(line) > 140:
                issues.append({
                    "line": line_num,
                    "severity": "warning",
                    "category": "style",
                    "message": f"Line too long ({len(line)} > 140 characters)",
                    "suggestion": "Break line to fit within 140 characters"
                })

            if re.search(r'var\s+\w+', line_stripped):
                issues.append({
                    "line": line_num,
                    "severity": "info",
                    "category": "style",
                    "message": "Use of 'var' instead of 'let' or 'const'",
                    "suggestion": "Prefer 'let' for reassignable or 'const' for immutable variables"
                })

        return issues

    def _check_performance_issues(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        issues = []
        line_stripped = line.strip()

        patterns = [
            (r"for\s+\w+\s+in\s+range\s*\(\s*\d{6,}\s*\)", "Large range iteration - consider generator"),
            (r"\.append\s*\(\s*\)", "Repeated list append in loop - consider list comprehension"),
            (r"re\.compile\s*\(.*\)\s*\n\s*re\.", "Regex compiled inside loop",),
            (r"print\s*\(\s*\)", "Print statement in production code",),
            (r"list\s*\(\s*\[", "Unnecessary list() wrapper around list literal"),
        ]

        for pattern, message in patterns:
            if re.search(pattern, line):
                issues.append({
                    "line": line_num,
                    "severity": "warning",
                    "category": "performance",
                    "message": message,
                    "suggestion": "Optimize for better performance"
                })

        return issues

    def _check_best_practices(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        issues = []
        line_stripped = line.strip()

        patterns = [
            (r"except\s*:\s*$", "Bare except clause - catches all exceptions"),
            (r"pass\s*$", "Empty except/pass block"),
            (r"#\s*TODO", "TODO comment found - should be addressed"),
            (r"#\s*FIXME", "FIXME comment found - should be addressed"),
            (r"#\s*HACK", "HACK comment found - technical debt"),
            (r"raise\s+Exception\s*\(\s*['\"]", "Generic exception - be specific"),
            (r"except\s+Exception\s+as\s+e:\s*\n\s+print\s*\(\s*e\s*\)", "Catching exception and only printing"),
        ]

        for pattern, message in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append({
                    "line": line_num,
                    "severity": "info",
                    "category": "best_practices",
                    "message": message,
                    "suggestion": "Follow best practices for maintainable code"
                })

        return issues
