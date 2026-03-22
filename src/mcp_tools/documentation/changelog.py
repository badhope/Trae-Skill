"""Changelog Generator Tool - Generate changelog from git commits"""

from datetime import datetime
from typing import Any, Dict, List
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class ChangelogGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="changelog_generator",
            description="Generates changelog files from git commits or release notes. Supports conventional commits format.",
            input_schema={
                "type": "object",
                "properties": {
                    "commits": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Git commit messages"
                    },
                    "version": {"type": "string"},
                    "format": {
                        "type": "string",
                        "enum": ["keepachangelog", "conventional", "simple"]
                    }
                },
                "required": ["commits", "version"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "changelog": {"type": "string"},
                    "changes_by_type": {"type": "object"}
                }
            },
            tags={"code", "generation", "documentation", "changelog", "git"},
            category="documentation",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        commits = params["commits"]
        version = params["version"]
        format = params.get("format", "keepachangelog")

        try:
            changelog, by_type = self._generate_changelog(commits, version, format)

            return ToolResult(
                tool_name="changelog_generator",
                success=True,
                data={"changelog": changelog, "changes_by_type": by_type},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

        except Exception as e:
            return ToolResult(
                tool_name="changelog_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_changelog(self, commits: List[str], version: str, format: str) -> tuple:
        by_type = {"added": [], "changed": [], "fixed": [], "removed": []}

        for commit in commits:
            lower = commit.lower()
            if any(k in lower for k in ["add", "feat", "new"]):
                by_type["added"].append(commit)
            elif any(k in lower for k in ["change", "update", "modify"]):
                by_type["changed"].append(commit)
            elif any(k in lower for k in ["fix", "bug", "patch"]):
                by_type["fixed"].append(commit)
            elif any(k in lower for k in ["remove", "delete", "deprecate"]):
                by_type["removed"].append(commit)
            else:
                by_type["changed"].append(commit)

        lines = [f"# Changelog - v{version}", f"\n## [{version}] - {datetime.now().strftime('%Y-%m-%d')}", ""]

        for change_type, items in by_type.items():
            if items:
                lines.append(f"### {change_type.title()}")
                lines.extend([f"- {item}" for item in items])
                lines.append("")

        return "\n".join(lines), by_type
