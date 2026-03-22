"""Pattern Detector Tool - Detect design patterns in code"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


@dataclass
class PatternMatch:
    pattern_name: str
    confidence: float
    locations: List[Tuple[int, int]]
    description: str
    suggestion: str


class PatternDetectorTool(MCPTool):
    DESIGN_PATTERNS = {
        "singleton": {
            "description": "Ensures a class has only one instance",
            "patterns": [
                (r"class\s+\w+.*:\s*.*\n.*_instance\s*=\s*None", "Python singleton"),
                (r"static\s+\w+\s*instance\s*=\s*null", "Java/C# singleton"),
                (r"let\s+instance\s*=\s*null.*\n.*export\s+function\s+getInstance", "JS module singleton"),
            ]
        },
        "factory": {
            "description": "Creates objects without specifying exact class",
            "patterns": [
                (r"def\s+create_\w+\(", "Factory method create_*"),
                (r"class\s+\w+Factory", "Factory class"),
                (r"static\s+\w+\s+create\(", "Static factory method"),
            ]
        },
        "observer": {
            "description": "Notifies observers of state changes",
            "patterns": [
                (r"(add|remove|notify)_observer", "Observer management"),
                (r"def\s+update\s*\(", "Observer update method"),
                (r"Subject|Observer", "Subject/Observer naming"),
            ]
        },
        "strategy": {
            "description": "Defines family of algorithms interchangeably",
            "patterns": [
                (r"class\s+\w+Strategy", "Strategy interface/class"),
                (r"def\s+execute\s*\(", "Strategy execute method"),
                (r"context\.strategy", "Strategy usage"),
            ]
        },
        "decorator": {
            "description": "Adds behavior dynamically",
            "patterns": [
                (r"@classmethod", "Class method decorator"),
                (r"@property", "Property decorator"),
                (r"@wraps\s*\(", "Decorator wrapper"),
            ]
        },
        "adapter": {
            "description": "Converts interface of a class to another",
            "patterns": [
                (r"class\s+\w+Adapter", "Adapter class"),
                (r"def\s+convert\s*\(", "Conversion method"),
            ]
        },
        "facade": {
            "description": "Simplified interface to complex subsystem",
            "patterns": [
                (r"class\s+\w+Facade", "Facade class"),
                (r"def\s+\w+\s*\([^)]*\)\s*:\s*.*\n.*\w+\.\w+\(", "Simplified interface"),
            ]
        },
        "command": {
            "description": "Encapsulates request as an object",
            "patterns": [
                (r"class\s+\w+Command", "Command class"),
                (r"def\s+execute\s*\(", "Command execute method"),
                (r"def\s+undo\s*\(", "Command undo method"),
            ]
        },
    }

    ANTI_PATTERNS = {
        "god_class": {
            "description": "Class with too many responsibilities",
            "patterns": [
                (r"class\s+\w+.*:\s*.*\n(.*\n){200,}", "Very large class"),
            ]
        },
        "spaghetti_code": {
            "description": "Code with tangled control flow",
            "patterns": [
                (r"if\s+.*:\s*\n\s*if\s+.*:\s*\n\s*if\s+.*:", "Deeply nested if statements"),
            ]
        },
        "magic_number": {
            "description": "Hardcoded numbers without explanation",
            "patterns": [
                (r"[=!\)]\s*\d{4,}", "Large magic number"),
                (r"if\s+.*\s*>\s*\d{3,}", "Magic number comparison"),
            ]
        },
        "copy_paste": {
            "description": "Repeated code blocks",
            "patterns": [
                (r"(.{100,})\1", "Repeated code"),
            ]
        },
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="pattern_detector",
            description="Detects software design patterns (GoF patterns) and anti-patterns in code. Helps identify code structure issues and improvement opportunities.",
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
                    "detect_anti_patterns": {
                        "type": "boolean",
                        "description": "Also detect anti-patterns",
                        "default": True
                    }
                },
                "required": ["code", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "design_patterns": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "confidence": {"type": "number"},
                                "locations": {"type": "array"},
                                "description": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "anti_patterns": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "confidence": {"type": "number"},
                                "locations": {"type": "array"},
                                "description": {"type": "string"},
                                "suggestion": {"type": "string"}
                            }
                        }
                    },
                    "summary": {"type": "object"}
                }
            },
            tags={"code", "pattern", "design-pattern", "analysis", "anti-pattern"},
            category="analyzers",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]
        language = params["language"]
        detect_anti_patterns = params.get("detect_anti_patterns", True)

        try:
            result = self._detect_patterns(code, language, detect_anti_patterns)
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="pattern_detector",
                success=True,
                data=result,
                execution_time_ms=execution_time,
                metadata={"language": language}
            )

        except Exception as e:
            return ToolResult(
                tool_name="pattern_detector",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _detect_patterns(self, code: str, language: str, detect_anti_patterns: bool) -> Dict[str, Any]:
        design_patterns = self._find_design_patterns(code, language)
        anti_patterns = []

        if detect_anti_patterns:
            anti_patterns = self._find_anti_patterns(code, language)

        return {
            "design_patterns": design_patterns,
            "anti_patterns": anti_patterns,
            "summary": {
                "total_patterns": len(design_patterns),
                "total_anti_patterns": len(anti_patterns),
                "confidence_average": sum(p["confidence"] for p in design_patterns) / max(len(design_patterns), 1)
            }
        }

    def _find_design_patterns(self, code: str, language: str) -> List[Dict[str, Any]]:
        found_patterns = []
        lines = code.split("\n")

        for pattern_name, pattern_info in self.DESIGN_PATTERNS.items():
            for pattern_regex, description in pattern_info["patterns"]:
                matches = list(re.finditer(pattern_regex, code, re.MULTILINE))
                if matches:
                    locations = [(m.start(), m.end()) for m in matches]
                    confidence = min(1.0, len(matches) * 0.3 + 0.5)

                    found_patterns.append({
                        "name": pattern_name,
                        "confidence": confidence,
                        "locations": locations,
                        "description": pattern_info["description"],
                        "suggestion": self._get_pattern_suggestion(pattern_name)
                    })
                    break

        return found_patterns

    def _find_anti_patterns(self, code: str, language: str) -> List[Dict[str, Any]]:
        found_anti_patterns = []
        lines = code.split("\n")

        for pattern_name, pattern_info in self.ANTI_PATTERNS.items():
            for pattern_regex, description in pattern_info["patterns"]:
                matches = list(re.finditer(pattern_regex, code, re.MULTILINE | re.DOTALL))
                if matches:
                    locations = [(m.start(), m.end()) for m in matches[:5]]
                    confidence = min(1.0, len(matches) * 0.2 + 0.6)

                    found_anti_patterns.append({
                        "name": pattern_name,
                        "confidence": confidence,
                        "locations": locations,
                        "description": pattern_info["description"],
                        "suggestion": self._get_anti_pattern_suggestion(pattern_name)
                    })
                    break

        return found_anti_patterns

    def _get_pattern_suggestion(self, pattern_name: str) -> str:
        suggestions = {
            "singleton": "Consider if a singleton is truly necessary. Dependency injection may be preferable.",
            "factory": "Factory pattern is well implemented. Consider using abstract factory for families of products.",
            "observer": "Good use of observer pattern. Consider using WeakKeyDictionary to prevent memory leaks.",
            "strategy": "Strategy pattern well applied. Consider adding a context class for better encapsulation.",
            "decorator": "Decorator pattern detected. Consider using functools.wraps to preserve metadata.",
            "adapter": "Adapter pattern well implemented. Consider if the existing interface can be refactored instead.",
            "facade": "Facade pattern provides clean interface. Consider if lower-level access is needed.",
            "command": "Command pattern well implemented. Consider adding undo/redo functionality.",
        }
        return suggestions.get(pattern_name, "Pattern well implemented.")

    def _get_anti_pattern_suggestion(self, pattern_name: str) -> str:
        suggestions = {
            "god_class": "Refactor into smaller, focused classes using Single Responsibility Principle.",
            "spaghetti_code": "Refactor using early returns, guard clauses, or extract methods.",
            "magic_number": "Replace magic numbers with named constants with descriptive names.",
            "copy_paste": "Extract repeated code into functions or use inheritance/composition.",
        }
        return suggestions.get(pattern_name, "Refactoring recommended.")
