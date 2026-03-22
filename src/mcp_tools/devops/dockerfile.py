"""Dockerfile Generator Tool"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class DockerfileGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="dockerfile_generator",
            description="Generates Docker and Docker Compose configurations for projects.",
            input_schema={
                "type": "object",
                "properties": {
                    "project_type": {"type": "string"},
                    "language": {"type": "string"},
                    "include_compose": {"type": "boolean", "default": False}
                },
                "required": ["project_type", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "dockerfile": {"type": "string"},
                    "docker_compose": {"type": "string"}
                }
            },
            tags={"code", "generation", "docker", "devops", "container"},
            category="devops",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        project_type = params["project_type"]
        language = params["language"]
        include_compose = params.get("include_compose", False)

        dockerfile = f'''FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
'''

        result = {"dockerfile": dockerfile}

        if include_compose:
            compose = f'''version: "3.8"
services:
  app:
    build: .
    ports:
      - "8000:8000"
'''
            result["docker_compose"] = compose

        return ToolResult(
            tool_name="dockerfile_generator",
            success=True,
            data=result,
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
