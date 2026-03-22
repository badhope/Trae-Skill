"""README Generator Tool - Generate README documentation"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class READMEGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="readme_generator",
            description="Generates comprehensive README.md files for projects with badges, installation instructions, and usage examples.",
            input_schema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "description": {"type": "string"},
                    "language": {"type": "string"},
                    "features": {"type": "array", "items": {"type": "string"}},
                    "include_badges": {"type": "boolean", "default": True}
                },
                "required": ["project_name", "description"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "readme_content": {"type": "string"}
                }
            },
            tags={"code", "generation", "documentation", "readme"},
            category="documentation",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        name = params["project_name"]
        desc = params["description"]
        lang = params.get("language", "python")
        features = params.get("features", [])
        badges = params.get("include_badges", True)

        try:
            readme = self._generate_readme(name, desc, lang, features, badges)

            return ToolResult(
                tool_name="readme_generator",
                success=True,
                data={"readme_content": readme},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

        except Exception as e:
            return ToolResult(
                tool_name="readme_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_readme(self, name: str, desc: str, lang: str, features: list, badges: bool) -> str:
        badge_section = """[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
""" if badges else ""

        features_section = "\n".join([f"- {f}" for f in features]) if features else "- Feature 1\n- Feature 2"

        return f"""# {name}

{badge_section}

{description}

## Features

{features_section}

## Installation

```bash
pip install {name}
```

## Usage

```python
import {name}

# Example usage
result = {name}.main()
print(result)
```

## License

MIT License
"""
