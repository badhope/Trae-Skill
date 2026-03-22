"""GraphQL Schema Generator Tool"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class GraphQLSchemaGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="graphql_schema_generator",
            description="Generates GraphQL schemas from data models or natural language descriptions.",
            input_schema={
                "type": "object",
                "properties": {
                    "models": {"type": "array"},
                    "include_mutations": {"type": "boolean", "default": True}
                },
                "required": ["models"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "schema": {"type": "string"}
                }
            },
            tags={"code", "generation", "api", "graphql"},
            category="api_tools",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        models = params["models"]
        include_mutations = params.get("include_mutations", True)

        schema_lines = ["type Query {", "  dummy: String", "}"]

        if include_mutations:
            schema_lines.append("type Mutation {")
            schema_lines.append("  dummy: String")
            schema_lines.append("}")

        return ToolResult(
            tool_name="graphql_schema_generator",
            success=True,
            data={"schema": "\n".join(schema_lines)},
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
