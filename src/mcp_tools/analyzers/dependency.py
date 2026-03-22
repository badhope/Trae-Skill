"""Dependency Parser Tool - Parse and analyze code dependencies"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


@dataclass
class DependencyNode:
    name: str
    type: str
    imports: List[str]
    is_external: bool


class DependencyParserTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="dependency_parser",
            description="Parses and analyzes code dependencies across multiple programming languages. Generates dependency trees and identifies unused imports.",
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
                    "project_path": {
                        "type": "string",
                        "description": "Optional project root path for context"
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "dependencies": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"},
                                "imports": {"type": "array"},
                                "is_external": {"type": "boolean"}
                            }
                        }
                    },
                    "external_packages": {"type": "array", "items": {"type": "string"}},
                    "internal_modules": {"type": "array", "items": {"type": "string"}},
                    "unused_imports": {"type": "array", "items": {"type": "string"}},
                    "dependency_count": {"type": "integer"},
                    "warnings": {"type": "array", "items": {"type": "string"}}
                }
            },
            tags={"code", "dependency", "analysis", "imports", "parsing"},
            category="analyzers",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        project_path = params.get("project_path", "")

        try:
            result = self._parse_dependencies(code, language, project_path)
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="dependency_parser",
                success=True,
                data=result,
                execution_time_ms=execution_time,
                metadata={"language": language}
            )

        except Exception as e:
            return ToolResult(
                tool_name="dependency_parser",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _parse_dependencies(self, code: str, language: str, project_path: str) -> Dict[str, Any]:
        dependencies: List[Dict[str, Any]] = []
        external_packages: Set[str] = set()
        internal_modules: Set[str] = set()
        all_imports: Set[str] = set()
        used_names: Set[str] = set()

        imports = self._extract_imports(code, language)
        all_imports.update(imports)

        for imp in imports:
            parts = imp.split(".")
            if language == "python":
                if parts[0] in ("os", "sys", "re", "json", "datetime", "typing", "pathlib", "collections", "itertools", "functools"):
                    external_packages.add(parts[0])
                elif parts[0] in ("pytest", "unittest", "django", "flask", "fastapi", "requests", "numpy", "pandas"):
                    external_packages.add(parts[0])
                else:
                    internal_modules.add(parts[0])

            elif language in ("javascript", "typescript"):
                if imp.startswith(("./", "../", "/")):
                    internal_modules.add(imp)
                elif imp.startswith("@"):
                    external_packages.add(imp.split("/")[0])
                elif imp not in ("react", "react-dom", "node-fetch"):
                    external_packages.add(imp.split("/")[0])

        used_names = self._find_used_names(code, language)

        unused_imports = self._find_unused_imports(imports, used_names, language)

        warnings = []
        if len(external_packages) > 20:
            warnings.append("Large number of external dependencies. Consider reviewing for redundancy.")

        if unused_imports:
            warnings.append(f"Found {len(unused_imports)} unused imports. Consider removing them.")

        return {
            "dependencies": [
                {
                    "name": name,
                    "type": "external" if name in external_packages else "internal",
                    "imports": [],
                    "is_external": name in external_packages
                }
                for name in list(external_packages) + list(internal_modules)
            ],
            "external_packages": sorted(list(external_packages)),
            "internal_modules": sorted(list(internal_modules)),
            "unused_imports": unused_imports,
            "dependency_count": len(external_packages) + len(internal_modules),
            "warnings": warnings
        }

    def _extract_imports(self, code: str, language: str) -> List[str]:
        imports: List[str] = []

        if language == "python":
            import_patterns = [
                r'^import\s+(\w+(?:\.\w+)*)',
                r'^from\s+(\w+(?:\.\w+)*)\s+import',
            ]
            for pattern in import_patterns:
                for match in re.finditer(pattern, code, re.MULTILINE):
                    imports.append(match.group(1))

        elif language in ("javascript", "typescript"):
            import_patterns = [
                r'^import\s+(?:{[^}]+}|\*\s+as\s+\w+|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'^import\s+[\'"]([^\'"]+)[\'"]',
                r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            ]
            for pattern in import_patterns:
                for match in re.finditer(pattern, code, re.MULTILINE):
                    imports.append(match.group(1))

        return imports

    def _find_used_names(self, code: str, language: str) -> Set[str]:
        used = set()

        if language == "python":
            used_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
            used.update(re.findall(used_pattern, code))

            builtin_functions = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
            used = used - builtin_functions - {'import', 'from', 'def', 'class', 'if', 'else', 'elif', 'while', 'for', 'return', 'try', 'except', 'finally', 'with', 'as', 'pass', 'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'lambda', 'yield', 'global', 'nonlocal', 'assert', 'raise', 'del', 'async', 'await']

        elif language in ("javascript", "typescript"):
            used_pattern = r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
            used.update(re.findall(used_pattern, code))
            keywords = {'import', 'export', 'from', 'const', 'let', 'var', 'function', 'class', 'extends', 'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return', 'try', 'catch', 'finally', 'throw', 'new', 'typeof', 'instanceof', 'void', 'delete', 'in', 'of', 'async', 'await', 'yield', 'static', 'get', 'set', 'constructor', 'this', 'super', 'true', 'false', 'null', 'undefined', 'NaN', 'Infinity'}
            used = used - keywords

        return used

    def _find_unused_imports(self, imports: List[str], used_names: Set[str], language: str) -> List[str]:
        unused = []

        for imp in imports:
            base_name = imp.split(".")[0].split("/")[-1]

            if base_name not in used_names:
                unused.append(imp)

            if "." in imp:
                parts = imp.split(".")
                for i in range(1, len(parts)):
                    submodule = ".".join(parts[:i])
                    if submodule not in used_names:
                        if imp not in unused:
                            unused.append(imp)
                        break

        return unused
