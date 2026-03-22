"""Bug Pattern Scanner Tool - Detect common bug patterns in code"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class BugPatternScannerTool(MCPTool):
    BUG_PATTERNS = {
        "python": [
            {
                "id": "PY001",
                "name": "Mutable Default Argument",
                "pattern": r"def\s+\w+\s*\([^)]*=\s*\[\s*\]",
                "severity": "error",
                "description": "Using mutable default argument can cause unexpected behavior",
                "example": "def foo(items=[]): # BAD\ndef foo(items=None): # GOOD",
                "suggestion": "Use None as default and create new list inside function"
            },
            {
                "id": "PY002",
                "name": "Comparison to None using ==",
                "pattern": r"[=!]=\s*None(?!\s*is)",
                "severity": "warning",
                "description": "Use 'is' for None comparison",
                "example": "if x == None: # BAD\nif x is None: # GOOD",
                "suggestion": "Replace '==' with 'is' for None comparisons"
            },
            {
                "id": "PY003",
                "name": "Shadowing Built-in",
                "pattern": r"\b(list|dict|str|int|float|set|tuple)\s*=\s*",
                "severity": "warning",
                "description": "Shadowing built-in names reduces code clarity",
                "example": "list = [1, 2, 3] # Shadows built-in",
                "suggestion": "Use different variable name"
            },
            {
                "id": "PY004",
                "name": "Empty Exception Block",
                "pattern": r"except[^:]*:\s*\n\s*pass",
                "severity": "warning",
                "description": "Empty exception block silently ignores errors",
                "example": "except:\n    pass # Silent failure",
                "suggestion": "Log the exception or handle it appropriately"
            },
            {
                "id": "PY005",
                "name": "Import Star Usage",
                "pattern": r"from\s+\w+\s+import\s+\*",
                "severity": "info",
                "description": "Using import * makes code harder to understand",
                "example": "from module import * # Unclear what is imported",
                "suggestion": "Explicitly import only what is needed"
            },
            {
                "id": "PY006",
                "name": "Bare except Clause",
                "pattern": r"except\s*:",
                "severity": "warning",
                "description": "Bare except catches all exceptions including KeyboardInterrupt",
                "example": "except: # Catches everything",
                "suggestion": "Catch specific exceptions"
            },
            {
                "id": "PY007",
                "name": "Incorrect __init__ vs __new__",
                "pattern": r"def\s+__init__\s*\([^)]*cls[^)]*\)",
                "severity": "error",
                "description": "__init__ receives instance, not class. Use __new__ for class creation.",
                "example": "def __init__(self, cls): # Wrong\ndef __new__(cls): # Correct for class creation",
                "suggestion": "Use 'self' as first parameter for __init__"
            },
            {
                "id": "PY008",
                "name": "Boolean comparison to True",
                "pattern": r"[=!]=\s*True(?! is)",
                "severity": "info",
                "description": "Redundant boolean comparison",
                "example": "if x == True: # Redundant\nif x: # Better",
                "suggestion": "Remove redundant comparison to True/False"
            },
        ],
        "javascript": [
            {
                "id": "JS001",
                "name": " == vs === ",
                "pattern": r"(?<![=!])={2}(?![=])",
                "severity": "warning",
                "description": "Use === instead of == for type-safe comparison",
                "example": "if (x == '1') // Use === instead",
                "suggestion": "Use === for comparisons"
            },
            {
                "id": "JS002",
                "name": "Assignment in Condition",
                "pattern": r"if\s*\(\s*\w+\s*=\s*[^=]",
                "severity": "error",
                "description": "Assignment in if condition - likely intended comparison",
                "example": "if (x = 5) // Assignment! Did you mean ===?",
                "suggestion": "Check if assignment was intended or should be comparison"
            },
            {
                "id": "JS003",
                "name": "Empty Catch Block",
                "pattern": r"catch\s*\([^)]*\)\s*{\s*}",
                "severity": "warning",
                "description": "Empty catch block silently ignores errors",
                "example": "catch (e) {} // Silent failure",
                "suggestion": "Log error or handle appropriately"
            },
            {
                "id": "JS004",
                "name": "Unused Variable",
                "pattern": r"const\s+\w+\s*=.*;(?:\s*\/\/[^\n]*)?(?:\s*(?!const|let|var|function)\w+\s*=)?(?:\s*\/\/[^\n]*)?(?:\s*\n(?:(?!\w+\s*=).)*$){0,2}",
                "severity": "info",
                "description": "Variable declared but may not be used",
                "example": "const unused = 5; // Not referenced",
                "suggestion": "Remove unused variable or use it"
            },
            {
                "id": "JS005",
                "name": "Console.log in Production",
                "pattern": r"console\.(log|debug|info|warn|error)\s*\(",
                "severity": "info",
                "description": "Console statements should be removed in production",
                "example": "console.log(debugInfo) // Remove in production",
                "suggestion": "Use proper logging framework with level control"
            },
        ],
        "typescript": [
            {
                "id": "TS001",
                "name": "Any Type Usage",
                "pattern": r":\s*any\b",
                "severity": "warning",
                "description": "Using 'any' defeats TypeScript type checking",
                "example": "const x: any = 5; // Avoid",
                "suggestion": "Use specific type or unknown if type is truly unknown"
            },
            {
                "id": "TS002",
                "name": "Non-null Assertion",
                "pattern": r"![.\w]",
                "severity": "info",
                "description": "Non-null assertion bypasses type checking",
                "example": "const x = value!; // May cause runtime error",
                "suggestion": "Use proper null checking instead"
            },
        ]
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="bug_pattern_scanner",
            description="Scans code for common bug patterns and potential issues. Supports Python, JavaScript, and TypeScript with detailed fix suggestions.",
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
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "severity_filter": {
                        "type": "array",
                        "description": "Filter by severity levels",
                        "items": {"type": "string", "enum": ["error", "warning", "info"]}
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "bugs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "name": {"type": "string"},
                                "line": {"type": "integer"},
                                "severity": {"type": "string"},
                                "description": {"type": "string"},
                                "example": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "summary": {
                        "type": "object",
                        "properties": {
                            "total": {"type": "integer"},
                            "errors": {"type": "integer"},
                            "warnings": {"type": "integer"},
                            "info": {"type": "integer"}
                        }
                    }
                }
            },
            tags={"code", "bug", "scanner", "analysis", "quality", "security"},
            category="analyzers",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        severity_filter = params.get("severity_filter", ["error", "warning", "info"])

        try:
            bugs = self._scan_for_bugs(code, language, severity_filter)

            error_count = len([b for b in bugs if b["severity"] == "error"])
            warning_count = len([b for b in bugs if b["severity"] == "warning"])
            info_count = len([b for b in bugs if b["severity"] == "info"])

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="bug_pattern_scanner",
                success=True,
                data={
                    "bugs": bugs,
                    "summary": {
                        "total": len(bugs),
                        "errors": error_count,
                        "warnings": warning_count,
                        "info": info_count
                    }
                },
                execution_time_ms=execution_time,
                metadata={"language": language}
            )

        except Exception as e:
            return ToolResult(
                tool_name="bug_pattern_scanner",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _scan_for_bugs(self, code: str, language: str, severity_filter: List[str]) -> List[Dict[str, Any]]:
        bugs = []
        lines = code.split("\n")

        patterns = self.BUG_PATTERNS.get(language, [])

        for pattern_info in patterns:
            if pattern_info["severity"] not in severity_filter:
                continue

            for line_num, line in enumerate(lines, 1):
                if re.search(pattern_info["pattern"], line):
                    bugs.append({
                        "id": pattern_info["id"],
                        "name": pattern_info["name"],
                        "line": line_num,
                        "severity": pattern_info["severity"],
                        "description": pattern_info["description"],
                        "example": pattern_info["example"],
                        "suggestion": pattern_info["suggestion"]
                    })

        return bugs
