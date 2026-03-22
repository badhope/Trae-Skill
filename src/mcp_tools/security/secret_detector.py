"""Secret Detector Tool"""

import re
from datetime import datetime
from typing import Any, Dict, List
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class SecretDetectorTool(MCPTool):
    SECRET_PATTERNS = [
        (r"api[_-]?key\s*=\s*['\"][^'\"]{8,}", "API Key", "high"),
        (r"secret[_-]?key\s*=\s*['\"][^'\"]{8,}", "Secret Key", "high"),
        (r"password\s*=\s*['\"][^'\"]{4,}", "Password", "high"),
        (r"token\s*=\s*['\"][^'\"]{8,}", "Token", "high"),
        (r"aws[_-]?access[_-]?key", "AWS Access Key", "critical"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token", "critical"),
        (r"xox[baprs]-[a-zA-Z0-9]{10,}", "Slack Token", "high"),
        (r"sk-[a-zA-Z0-9]{48}", "OpenAI API Key", "critical"),
    ]

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="secret_detector",
            description="Detects hardcoded secrets, API keys, and credentials in code.",
            input_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "include_filenames": {"type": "boolean", "default": True}
                },
                "required": ["code"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "secrets": {"type": "array"},
                    "severity_counts": {"type": "object"}
                }
            },
            tags={"code", "security", "secret", "detector", "api-key"},
            category="security",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        code = params["code"]

        secrets = []
        for pattern, name, severity in self.SECRET_PATTERNS:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                secrets.append({
                    "type": name,
                    "severity": severity,
                    "line": code[:match.start()].count("\n") + 1,
                    "placeholder": self._mask_secret(match.group())
                })

        counts = {}
        for s in secrets:
            counts[s["severity"]] = counts.get(s["severity"], 0) + 1

        return ToolResult(
            tool_name="secret_detector",
            success=True,
            data={
                "secrets": secrets,
                "severity_counts": counts
            },
            execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
        )

    def _mask_secret(self, secret: str) -> str:
        if len(secret) <= 8:
            return "***"
        return secret[:4] + "*" * (len(secret) - 8) + secret[-4:]
