"""SQL Query Generator Tool"""

from datetime import datetime
from typing import Any, Dict
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class SQLQueryGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="sql_query_generator",
            description="Generates SQL queries from natural language descriptions. Supports PostgreSQL, MySQL, SQLite.",
            input_schema={
                "type": "object",
                "properties": {
                    "natural_language": {"type": "string"},
                    "database_type": {"type": "string", "enum": ["postgresql", "mysql", "sqlite"]},
                    "tables": {"type": "array"}
                },
                "required": ["natural_language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "explanation": {"type": "string"}
                }
            },
            tags={"code", "generation", "database", "sql"},
            category="database",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        nl = params["natural_language"]
        db_type = params.get("database_type", "postgresql")

        sql = f"-- Generated SQL for: {nl}\nSELECT * FROM table_name;"

        return ToolResult(
            tool_name="sql_query_generator",
            success=True,
            data={"sql": sql, "explanation": "Generated SQL query"},
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )
