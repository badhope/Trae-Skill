"""Unit Test Generator Tool - Automatically generate unit tests for source code"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class UnitTestGeneratorTool(MCPTool):
    TEST_FRAMEWORKS = {
        "python": {
            "pytest": {
                "imports": ["import pytest", "from {module} import {function}"],
                "test_template": '''
def test_{function_name}_basic():
    """Test basic functionality of {function_name}"""
    result = {function_name}({test_inputs})
    assert result == {expected}
'''
            },
            "unittest": {
                "imports": ["import unittest", "from {module} import {function}"],
                "test_template": '''
class Test{ClassName}(unittest.TestCase):
    def test_{function_name}_basic(self):
        """Test basic functionality"""
        result = {function_name}({test_inputs})
        self.assertEqual(result, {expected})
'''
            }
        },
        "javascript": {
            "jest": {
                "imports": ["const {function} = require('{module}');"],
                "test_template": '''
describe('{function_name}', () => {{
    test('should work correctly', () => {{
        const result = {function_name}({test_inputs});
        expect(result).toBe({expected});
    }});
}});
'''
            },
            "mocha": {
                "imports": ["const {{ {function} }} = require('{module}');"],
                "test_template": '''
describe('{function_name}', () => {{
    it('should work correctly', () => {{
        const result = {function_name}({test_inputs});
        assert.equal(result, {expected});
    }});
}});
'''
            }
        },
        "typescript": {
            "jest": {
                "imports": ["import {{ {function} }} from '{module}';"],
                "test_template": '''
describe('{function_name}', () => {{
    it('should work correctly', () => {{
        const result = {function_name}({test_inputs});
        expect(result).toBe({expected});
    }});
}});
'''
            }
        }
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="unit_test_generator",
            description="Automatically generates unit tests for source code. Supports pytest, unittest for Python and Jest, Mocha for JavaScript/TypeScript.",
            input_schema={
                "type": "object",
                "properties": {
                    "source_code": {
                        "type": "string",
                        "description": "The source code to generate tests for"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                        "enum": ["python", "javascript", "typescript"]
                    },
                    "framework": {
                        "type": "string",
                        "description": "Testing framework",
                        "enum": ["pytest", "unittest", "jest", "mocha"]
                    },
                    "coverage_target": {
                        "type": "integer",
                        "description": "Target test coverage percentage",
                        "default": 80
                    },
                    "include_edge_cases": {
                        "type": "boolean",
                        "description": "Include edge case tests",
                        "default": True
                    }
                },
                "required": ["source_code", "language", "framework"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "test_code": {"type": "string", "description": "Generated test code"},
                    "test_cases": {
                        "type": "array",
                        "description": "List of generated test cases",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "inputs": {"type": "array"},
                                "expected": {"type": "string"}
                            }
                        }
                    },
                    "coverage_estimate": {"type": "number"},
                    "missing_cases": {"type": "array", "items": {"type": "string"}},
                    "module_name": {"type": "string"}
                }
            },
            tags={"code", "generation", "testing", "unit-test", "automation"},
            category="generators",
            version="2.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        source_code = params["source_code"]
        language = params["language"]
        framework = params["framework"]
        coverage_target = params.get("coverage_target", 80)
        include_edge_cases = params.get("include_edge_cases", True)

        try:
            result = self._generate_tests(
                source_code, language, framework, coverage_target, include_edge_cases
            )
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="unit_test_generator",
                success=True,
                data=result,
                execution_time_ms=execution_time,
                metadata={"language": language, "framework": framework}
            )

        except Exception as e:
            return ToolResult(
                tool_name="unit_test_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_tests(
        self,
        source_code: str,
        language: str,
        framework: str,
        coverage_target: int,
        include_edge_cases: bool
    ) -> Dict[str, Any]:
        functions = self._extract_functions(source_code, language)

        test_cases = []
        generated_tests = []

        for func in functions:
            cases = self._generate_test_cases(func, language, include_edge_cases)
            test_cases.extend(cases)

            framework_templates = self.TEST_FRAMEWORKS.get(language, {}).get(framework, {})
            if framework_templates:
                test_code = self._render_tests(func, cases, framework_templates, language)
                generated_tests.append(test_code)

        test_code = "\n\n".join(generated_tests)

        coverage_estimate = min(100, len(test_cases) * 15 + 20)

        missing_cases = []
        if len(test_cases) < 5:
            missing_cases.append("Consider adding more edge case tests")
        if not any(tc["type"] == "edge_case" for tc in test_cases) and include_edge_cases:
            missing_cases.append("No edge cases generated - add tests for boundary conditions")

        return {
            "test_code": test_code,
            "test_cases": test_cases,
            "coverage_estimate": coverage_estimate,
            "missing_cases": missing_cases,
            "module_name": self._extract_module_name(source_code, language)
        }

    def _extract_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        functions = []

        if language == "python":
            func_pattern = re.compile(r'^def\s+(\w+)\s*\((.*?)\)\s*:(.*?)(?=^def\s|\Z)', re.MULTILINE | re.DOTALL)
            for match in func_pattern.finditer(code):
                functions.append({
                    "name": match.group(1),
                    "params": match.group(2),
                    "body": match.group(3).strip(),
                    "is_async": False
                })

            async_func_pattern = re.compile(r'^async def\s+(\w+)\s*\((.*?)\)\s*:(.*?)(?=^async def\s|^def\s|\Z)', re.MULTILINE | re.DOTALL)
            for match in async_func_pattern.finditer(code):
                functions.append({
                    "name": match.group(1),
                    "params": match.group(2),
                    "body": match.group(3).strip(),
                    "is_async": True
                })

        elif language in ("javascript", "typescript"):
            func_patterns = [
                re.compile(r'function\s+(\w+)\s*\((.*?)\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'),
                re.compile(r'const\s+(\w+)\s*=\s*(?:async\s+)?\((.*?)\)\s*=>\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', re.MULTILINE),
                re.compile(r'(?:async\s+)?(\w+)\s*\((.*?)\)\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}'),
            ]

            for pattern in func_patterns:
                for match in pattern.finditer(code):
                    functions.append({
                        "name": match.group(1),
                        "params": match.group(2),
                        "body": match.group(3).strip(),
                        "is_async": "async" in code[match.start():match.start()+50]
                    })

        return functions

    def _generate_test_cases(
        self,
        func: Dict[str, Any],
        language: str,
        include_edge_cases: bool
    ) -> List[Dict[str, Any]]:
        cases = []

        cases.append({
            "name": f"test_{func['name']}_basic",
            "type": "basic",
            "inputs": self._get_default_inputs(func["params"], language),
            "expected": self._get_expected_output(func, "basic"),
            "description": f"Basic test for {func['name']}"
        })

        if include_edge_cases:
            cases.append({
                "name": f"test_{func['name']}_edge_empty",
                "type": "edge_case",
                "inputs": self._get_edge_inputs(func["params"], "empty"),
                "expected": self._get_expected_output(func, "empty"),
                "description": f"Edge case: empty input for {func['name']}"
            })

            cases.append({
                "name": f"test_{func['name']}_edge_large",
                "type": "edge_case",
                "inputs": self._get_edge_inputs(func["params"], "large"),
                "expected": self._get_expected_output(func, "large"),
                "description": f"Edge case: large input for {func['name']}"
            })

            cases.append({
                "name": f"test_{func['name']}_edge_null",
                "type": "edge_case",
                "inputs": self._get_edge_inputs(func["params"], "null"),
                "expected": self._get_expected_output(func, "null"),
                "description": f"Edge case: null input for {func['name']}"
            })

        return cases

    def _get_default_inputs(self, params: str, language: str) -> str:
        if not params.strip():
            return ""

        if language == "python":
            param_list = [p.strip().split(":")[0].strip() for p in params.split(",") if p.strip()]
            defaults = {
                "str": '""',
                "int": "0",
                "float": "0.0",
                "bool": "True",
                "list": "[]",
                "dict": "{}",
                "tuple": "()",
                "str | None": "None",
                "int | None": "None",
            }
            inputs = []
            for p in param_list:
                param_name = p.split("=")[0].strip()
                param_type = p.split("=")[1].strip() if "=" in p else "str"
                default_val = defaults.get(param_type, '""')
                inputs.append(default_val)
            return ", ".join(inputs)

        elif language in ("javascript", "typescript"):
            param_list = [p.strip().split(":")[0].strip() for p in params.split(",") if p.strip()]
            inputs = ['null'] * len(param_list)
            return ", ".join(inputs)

        return ""

    def _get_edge_inputs(self, params: str, edge_type: str) -> str:
        if not params.strip():
            return ""

        if edge_type == "empty":
            if "python" in params:
                return ", ".join(["None"] * max(1, params.count(",")))
            return ", ".join(["null"] * max(1, params.count(",")))
        elif edge_type == "large":
            if "python" in params:
                return ", ".join(["[]"] * max(1, params.count(",")))
            return ", ".join(["[]"] * max(1, params.count(",")))
        elif edge_type == "null":
            return ", ".join(["None"] * max(1, params.count(",")))

        return ""

    def _get_expected_output(self, func: Dict[str, Any], test_type: str) -> str:
        return "expected_output"

    def _render_tests(
        self,
        func: Dict[str, Any],
        cases: List[Dict[str, Any]],
        framework_template: Dict[str, str],
        language: str
    ) -> str:
        test_lines = []

        imports = framework_template.get("imports", [])
        module_name = self._extract_module_name_from_func(func, language)

        for imp in imports:
            test_lines.append(imp.format(module=module_name, function=func["name"]))

        test_lines.append("")

        template = framework_template.get("test_template", "")

        for case in cases:
            test_code = template.format(
                function_name=func["name"],
                test_inputs=case["inputs"],
                expected=case["expected"],
                ClassName=func["name"].title().replace("_", "")
            )
            test_lines.append(test_code)

        return "\n".join(test_lines)

    def _extract_module_name(self, code: str, language: str) -> str:
        if language == "python":
            module_match = re.search(r'^module\s*=\s*["\']([^"\']+)["\']', code, re.MULTILINE)
            if module_match:
                return module_match.group(1)
            return "my_module"

        return "myModule"

    def _extract_module_name_from_func(self, func: Dict[str, Any], language: str) -> str:
        return "my_module" if language == "python" else "myModule"
