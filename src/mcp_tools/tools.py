import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class CodeQualityCheckerTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._issues_found: List[Dict[str, Any]] = []

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="code_quality_checker",
            description="Performs static analysis on code to identify issues related to code quality, style, potential bugs, and security vulnerabilities",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The source code to analyze"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language (python, javascript, typescript, java, go, rust)",
                        "enum": ["python", "javascript", "typescript", "java", "go", "rust"]
                    },
                    "check_security": {
                        "type": "boolean",
                        "description": "Enable security checks",
                        "default": True
                    },
                    "check_style": {
                        "type": "boolean",
                        "description": "Enable style checks",
                        "default": True
                    },
                    "check_performance": {
                        "type": "boolean",
                        "description": "Enable performance checks",
                        "default": True
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "quality_score": {"type": "number"},
                    "grade": {"type": "string"},
                    "issues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "line": {"type": "integer"},
                                "severity": {"type": "string"},
                                "category": {"type": "string"},
                                "message": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "summary": {"type": "object"}
                }
            },
            tags={"code", "quality", "analysis", "lint"},
            category="coding"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        check_security = params.get("check_security", True)
        check_style = params.get("check_style", True)
        check_performance = params.get("check_performance", True)

        try:
            issues = self._analyze_code(code, language, check_security, check_style, check_performance)

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
                metadata={"language": language}
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
        check_performance: bool
    ) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        lines = code.split("\n")

        for i, line in enumerate(lines, 1):
            if check_security:
                issues.extend(self._check_security_issues(line, i))

            if check_style:
                issues.extend(self._check_style_issues(line, i, language))

            if check_performance:
                issues.extend(self._check_performance_issues(line, i))

        return issues

    def _check_security_issues(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        issues = []

        if re.search(r"(password|passwd|secret|api_key)\s*=\s*['\"][^'\"']+['\"]", line, re.IGNORECASE):
            issues.append({
                "line": line_num,
                "severity": "error",
                "category": "security",
                "message": "Hardcoded credentials detected",
                "suggestion": "Use environment variables or a secure secrets manager"
            })

        if re.search(r"eval\s*\(", line):
            issues.append({
                "line": line_num,
                "severity": "error",
                "category": "security",
                "message": "Use of eval() is a security risk",
                "suggestion": "Avoid eval() - use safer alternatives like ast.literal_eval"
            })

        if re.search(r"(execute|cursor)\s*\(\s*['\"].*%s.*['\"]", line):
            issues.append({
                "line": line_num,
                "severity": "error",
                "category": "security",
                "message": "Potential SQL injection vulnerability",
                "suggestion": "Use parameterized queries instead of string formatting"
            })

        if re.search(r"subprocess\s*\.\s*(run|call|popen)\s*\([^,]+,\s*shell\s*=\s*True", line):
            issues.append({
                "line": line_num,
                "severity": "warning",
                "category": "security",
                "message": "Shell injection risk with shell=True",
                "suggestion": "Avoid shell=True, use list of arguments instead"
            })

        return issues

    def _check_style_issues(self, line: str, line_num: int, language: str) -> List[Dict[str, Any]]:
        issues = []

        if language == "python":
            if re.match(r"^\s+except\s*:", line):
                issues.append({
                    "line": line_num,
                    "severity": "warning",
                    "category": "style",
                    "message": "Bare except clause",
                    "suggestion": "Specify exception type to catch"
                })

            if len(line) > 120:
                issues.append({
                    "line": line_num,
                    "severity": "info",
                    "category": "style",
                    "message": "Line exceeds 120 characters",
                    "suggestion": "Consider breaking long lines"
                })

            if re.match(r"^\s*def\s+\w+\s*\([^)]*=\s*\[\s*\]", line):
                issues.append({
                    "line": line_num,
                    "severity": "warning",
                    "category": "style",
                    "message": "Mutable default argument",
                    "suggestion": "Use None as default and initialize inside function"
                })

        if line.strip().endswith("  ") and not line.strip().startswith("#"):
            issues.append({
                "line": line_num,
                "severity": "info",
                "category": "style",
                "message": "Trailing whitespace",
                "suggestion": "Remove trailing whitespace"
            })

        return issues

    def _check_performance_issues(self, line: str, line_num: int) -> List[Dict[str, Any]]:
        issues = []

        if re.search(r"\+=\s*str\(", line):
            issues.append({
                "line": line_num,
                "severity": "info",
                "category": "performance",
                "message": "Inefficient string concatenation",
                "suggestion": "Use join() or f-string instead of +="
            })

        if re.search(r"for\s+\w+\s+in\s+range\s*\(\s*len\s*\(\s*\w+\s*\)\s*\)", line):
            issues.append({
                "line": line_num,
                "severity": "info",
                "category": "performance",
                "message": "Using range(len()) pattern",
                "suggestion": "Use enumerate() for index and value"
            })

        if re.search(r"\.append\(\)\s*\n\s*for\s+", line):
            issues.append({
                "line": line_num,
                "severity": "info",
                "category": "performance",
                "message": "Using append in loop",
                "suggestion": "Use list comprehension instead"
            })

        return issues


class UnitTestGeneratorTool(MCPTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="test_generator",
            description="Automatically generates unit tests for code based on function signatures and implementation",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {
                        "type": "string",
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "test_framework": {
                        "type": "string",
                        "enum": ["pytest", "unittest", "jest", "mocha"],
                        "default": "pytest"
                    },
                    "include_edge_cases": {
                        "type": "boolean",
                        "default": True
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "test_code": {"type": "string"},
                    "test_count": {"type": "integer"},
                    "coverage_estimate": {"type": "number"}
                }
            },
            tags={"testing", "code", "generation", "automation"},
            category="coding"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        test_framework = params.get("test_framework", "pytest")
        include_edge_cases = params.get("include_edge_cases", True)

        try:
            test_code = self._generate_tests(code, language, test_framework, include_edge_cases)
            test_count = test_code.count("def test_")

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="test_generator",
                success=True,
                data={
                    "test_code": test_code,
                    "test_count": test_count,
                    "coverage_estimate": min(95.0, 60.0 + (test_count * 5))
                },
                execution_time_ms=execution_time,
                metadata={"language": language, "framework": test_framework}
            )

        except Exception as e:
            return ToolResult(
                tool_name="test_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_tests(
        self,
        code: str,
        language: str,
        framework: str,
        include_edge_cases: bool
    ) -> str:
        if language == "python":
            return self._generate_python_tests(code, framework, include_edge_cases)
        elif language in ("javascript", "typescript"):
            return self._generate_js_tests(code, framework, include_edge_cases)
        return ""

    def _generate_python_tests(self, code: str, framework: str, include_edge_cases: bool) -> str:
        functions = re.findall(r"def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?\s*:", code)

        if framework == "pytest":
            test_lines = ["import pytest", ""]
        else:
            test_lines = ["import unittest", ""]

        for func_name, params, return_type in functions:
            param_names = [p.strip().split(":")[0].strip() for p in params.split(",") if p.strip()]

            test_lines.append(f"class Test{func_name.title()}(unittest.TestCase):" if framework != "pytest" else "")
            test_lines.append(f"    def test_{func_name}_basic(self):")
            test_lines.append(f'        result = {func_name}({", ".join(["None" if not p else f'"{p}"' for p in param_names])})')
            test_lines.append("        assert result is not None")
            test_lines.append("")

            if include_edge_cases:
                test_lines.append(f"    def test_{func_name}_edge_cases(self):")
                test_lines.append(f'        with pytest.raises(Exception):')
                test_lines.append(f'            {func_name}({", ".join(["None"] * len(param_names))})')
                test_lines.append("")

        return "\n".join(test_lines)

    def _generate_js_tests(self, code: str, framework: str, include_edge_cases: bool) -> str:
        functions = re.findall(r"function\s+(\w+)\s*\(([^)]*)\)", code)
        if framework == "jest":
            test_lines = ["describe('Tests', () => {"]
            for func_name, params in functions:
                param_names = [p.strip().split(":")[0].strip() for p in params.split(",") if p.strip()]
                test_lines.append(f"  test('{func_name}', () => {{")
                test_lines.append(f"    const result = {func_name}({', '.join([f'null' for _ in param_names])});")
                test_lines.append("    expect(result).toBeDefined();")
                test_lines.append("  });")
            test_lines.append("});")
        else:
            test_lines = ["// Mocha tests not implemented yet"]
        return "\n".join(test_lines)


class APIDocGeneratorTool(MCPTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="api_doc_generator",
            description="Generates OpenAPI documentation from code or function signatures",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {
                        "type": "string",
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "title": {"type": "string", "default": "My API"},
                    "version": {"type": "string", "default": "1.0.0"}
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "openapi_spec": {"type": "object"},
                    "markdown_doc": {"type": "string"}
                }
            },
            tags={"documentation", "api", "openapi", "generation"},
            category="documentation"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        title = params.get("title", "My API")
        version = params.get("version", "1.0.0")

        try:
            openapi_spec = self._generate_openapi_spec(code, language, title, version)
            markdown_doc = self._generate_markdown(code, language, title)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="api_doc_generator",
                success=True,
                data={
                    "openapi_spec": openapi_spec,
                    "markdown_doc": markdown_doc
                },
                execution_time_ms=execution_time,
                metadata={"language": language}
            )

        except Exception as e:
            return ToolResult(
                tool_name="api_doc_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_openapi_spec(
        self,
        code: str,
        language: str,
        title: str,
        version: str
    ) -> Dict[str, Any]:
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": version,
                "description": "Auto-generated API documentation"
            },
            "paths": {},
            "components": {
                "schemas": {}
            }
        }

        functions = re.findall(
            r"(?:def|function)\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?\s*:?",
            code
        )

        for func_name, params, return_type in functions:
            endpoint = f"/{func_name.replace('_', '-')}"
            param_names = [p.strip().split(":")[0].strip() for p in params.split(",") if p.strip()]

            spec["paths"][endpoint] = {
                "post": {
                    "summary": f"Endpoint for {func_name}",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        p: {"type": "string"} for p in param_names
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "result": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

        return spec

    def _generate_markdown(self, code: str, language: str, title: str) -> str:
        functions = re.findall(
            r"(?:def|function)\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?\s*:?",
            code
        )

        md = [f"# {title}", "", "## API Endpoints", ""]

        for func_name, params, return_type in functions:
            md.append(f"### `{func_name}`")
            md.append("")
            md.append(f"**Description**: {func_name} operation")
            md.append("")
            md.append("**Parameters**:")
            param_names = [p.strip().split(":")[0].strip() for p in params.split(",") if p.strip()]
            for p in param_names:
                md.append(f"- `{p}` (string)")
            md.append("")
            if return_type:
                md.append(f"**Returns**: `{return_type.strip()}`")
            else:
                md.append("**Returns**: `void`")
            md.append("")

        return "\n".join(md)


class RefactoringAssistantTool(MCPTool):
    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="refactoring_assistant",
            description="Analyzes code and suggests refactoring improvements based on design patterns and best practices",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "language": {"type": "string"},
                    "target_pattern": {
                        "type": "string",
                        "enum": ["singleton", "factory", "observer", "strategy", "decorator", "facade", "all"],
                        "default": "all"
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "suggestions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "description": {"type": "string"},
                                "original_code": {"type": "string"},
                                "refactored_code": {"type": "string"},
                                "benefits": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    }
                }
            },
            tags={"refactoring", "code", "improvement", "patterns"},
            category="coding"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        target_pattern = params.get("target_pattern", "all")

        try:
            suggestions = self._analyze_and_suggest(code, language, target_pattern)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="refactoring_assistant",
                success=True,
                data={"suggestions": suggestions},
                execution_time_ms=execution_time,
                metadata={"language": language, "pattern": target_pattern}
            )

        except Exception as e:
            return ToolResult(
                tool_name="refactoring_assistant",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _analyze_and_suggest(
        self,
        code: str,
        language: str,
        target_pattern: str
    ) -> List[Dict[str, Any]]:
        suggestions = []

        if language == "python":
            if target_pattern in ("all", "factory"):
                suggestions.extend(self._check_factory_pattern(code))

            if target_pattern in ("all", "singleton"):
                suggestions.extend(self._check_singleton_pattern(code))

            if target_pattern in ("all", "decorator"):
                suggestions.extend(self._check_decorator_pattern(code))

        return suggestions

    def _check_factory_pattern(self, code: str) -> List[Dict[str, Any]]:
        suggestions = []

        class_ifs = re.findall(r"if\s+isinstance\s*\([^,]+,\s*(\w+)\)\s*:\s*return\s+\1", code)
        if len(class_ifs) >= 3:
            suggestions.append({
                "type": "factory",
                "description": "Detected repeated isinstance checks - consider using Factory pattern",
                "original_code": "\n".join(class_ifs[:3]),
                "refactored_code": """class Factory:
    @staticmethod
    def create(product_type):
        products = {
            'type1': Type1Product,
            'type2': Type2Product,
        }
        return products.get(product_type, DefaultProduct)()""",
                "benefits": [
                    "Eliminates repeated if-isinstance chains",
                    "Easier to add new product types",
                    "Follows Open/Closed Principle"
                ]
            })

        return suggestions

    def _check_singleton_pattern(self, code: str) -> List[Dict[str, Any]]:
        suggestions = []

        global_vars = re.findall(r"^(\w+)\s*=\s*[^{]", code, re.MULTILINE)
        if len(global_vars) >= 5:
            suggestions.append({
                "type": "singleton",
                "description": "Detected multiple global variables - consider grouping into a Singleton class",
                "original_code": "\n".join(global_vars[:3]),
                "refactored_code": """class ConfigManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance""",
                "benefits": [
                    "Reduces global state",
                    "Better encapsulation",
                    "Thread-safe singleton available"
                ]
            })

        return suggestions

    def _check_decorator_pattern(self, code: str) -> List[Dict[str, Any]]:
        suggestions = []

        nested_inheritance = re.findall(r"class\s+\w+\((\w+)\)", code)
        if len(nested_inheritance) >= 3:
            suggestions.append({
                "type": "decorator",
                "description": "Detected deep class inheritance - consider Decorator pattern for flexible behavior",
                "original_code": "class A(B): class C(A): class D(C):",
                "refactored_code": """class Component(ABC):
    @abstractmethod
    def operation(self): pass

class Decorator(Component):
    def __init__(self, component):
        self._component = component""",
                "benefits": [
                    "More flexible than inheritance",
                    "Easy to add/remove behaviors at runtime",
                    "Single Responsibility Principle"
                ]
            })

        return suggestions


__all__ = [
    "CodeQualityCheckerTool",
    "UnitTestGeneratorTool",
    "APIDocGeneratorTool",
    "RefactoringAssistantTool",
]
