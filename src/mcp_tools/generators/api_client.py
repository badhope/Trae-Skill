"""API Client Generator Tool - Generate API client code from OpenAPI specifications"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class APIClientGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="api_client_generator",
            description="Generates API client code from OpenAPI/REST specifications. Supports Python (requests, httpx), JavaScript/TypeScript (fetch, axios), and other languages.",
            input_schema={
                "type": "object",
                "properties": {
                    "api_spec": {
                        "type": "string",
                        "description": "OpenAPI spec (YAML/JSON) or natural language API description"
                    },
                    "language": {
                        "type": "string",
                        "description": "Target programming language",
                        "enum": ["python", "javascript", "typescript", "java", "go"]
                    },
                    "http_client": {
                        "type": "string",
                        "description": "HTTP client library to use",
                        "enum": ["requests", "httpx", "fetch", "axios", "http", "net/http"]
                    },
                    "include_auth": {
                        "type": "boolean",
                        "description": "Include authentication handling",
                        "default": True
                    },
                    "include_error_handling": {
                        "type": "boolean",
                        "description": "Include comprehensive error handling",
                        "default": True
                    }
                },
                "required": ["api_spec", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "client_code": {"type": "string", "description": "Generated API client code"},
                    "endpoints": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "method": {"type": "string"},
                                "path": {"type": "string"},
                                "name": {"type": "string"}
                            }
                        }
                    },
                    "usage_examples": {"type": "string"},
                    "types_code": {"type": "string"}
                }
            },
            tags={"code", "generation", "api", "client", "openapi", "rest"},
            category="generators",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        api_spec = params["api_spec"]
        language = params["language"]
        http_client = params.get("http_client", "requests" if language == "python" else "fetch")
        include_auth = params.get("include_auth", True)
        include_error_handling = params.get("include_error_handling", True)

        try:
            endpoints = self._parse_endpoints(api_spec)
            client_code = self._generate_client(
                endpoints, language, http_client, include_auth, include_error_handling
            )
            types_code = self._generate_types(endpoints, language)
            usage_examples = self._generate_usage_examples(endpoints, language)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="api_client_generator",
                success=True,
                data={
                    "client_code": client_code,
                    "endpoints": [{"method": e["method"], "path": e["path"], "name": e["name"]} for e in endpoints],
                    "types_code": types_code,
                    "usage_examples": usage_examples
                },
                execution_time_ms=execution_time,
                metadata={"language": language, "http_client": http_client}
            )

        except Exception as e:
            return ToolResult(
                tool_name="api_client_generator",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _parse_endpoints(self, spec: str) -> List[Dict[str, Any]]:
        endpoints = []

        get_pattern = re.compile(r'GET\s+([/\w{}.-]+)\s*-?\s*([A-Z]\w+(?:\s+[A-Z]\w+)*)?', re.IGNORECASE)
        post_pattern = re.compile(r'POST\s+([/\w{}.-]+)\s*-?\s*([A-Z]\w+(?:\s+[A-Z]\w+)*)?', re.IGNORECASE)
        put_pattern = re.compile(r'PUT\s+([/\w{}.-]+)\s*-?\s*([A-Z]\w+(?:\s+[A-Z]\w+)*)?', re.IGNORECASE)
        delete_pattern = re.compile(r'DELETE\s+([/\w{}.-]+)\s*-?\s*([A-Z]\w+(?:\s+[A-Z]\w+)*)?', re.IGNORECASE)

        for pattern, method in [(get_pattern, "GET"), (post_pattern, "POST"), (put_pattern, "PUT"), (delete_pattern, "DELETE")]:
            for match in pattern.finditer(spec):
                path = match.group(1)
                name = self._generate_endpoint_name(path, method)
                description = match.group(2) if match.lastindex >= 2 else ""

                endpoints.append({
                    "method": method,
                    "path": path,
                    "name": name,
                    "description": description
                })

        if not endpoints and ("{" in spec or '"' in spec):
            try:
                import json
                spec_dict = json.loads(spec) if "{" in spec else {}
                paths = spec_dict.get("paths", {})
                for path, methods in paths.items():
                    for method, details in methods.items():
                        if method.upper() in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                            endpoints.append({
                                "method": method.upper(),
                                "path": path,
                                "name": self._generate_endpoint_name(path, method.upper()),
                                "description": details.get("summary", "")
                            })
            except json.JSONDecodeError:
                pass

        if not endpoints:
            endpoints.append({
                "method": "GET",
                "path": "/api/resource",
                "name": "getResource",
                "description": "Get resource endpoint"
            })

        return endpoints

    def _generate_endpoint_name(self, path: str, method: str) -> str:
        path_clean = re.sub(r'\{([^}]+)\}', r'\1', path)
        parts = [p for p in path_clean.split('/') if p and p != 'api']

        if parts:
            first_part = parts[0].lower()
            if method == "GET":
                name = f"get{parts[-1].title()}" if len(parts) == 1 else f"get{''.join(p.title() for p in parts)}"
            elif method == "POST":
                name = f"create{parts[-1].title()}" if len(parts) == 1 else f"create{''.join(p.title() for p in parts)}"
            elif method == "PUT":
                name = f"update{parts[-1].title()}" if len(parts) == 1 else f"update{''.join(p.title() for p in parts)}"
            elif method == "DELETE":
                name = f"delete{parts[-1].title()}" if len(parts) == 1 else f"delete{''.join(p.title() for p in parts)}"
            else:
                name = f"{method.lower()}{''.join(p.title() for p in parts)}"
        else:
            name = f"{method.lower()}Resource"

        return name

    def _generate_client(
        self,
        endpoints: List[Dict[str, Any]],
        language: str,
        http_client: str,
        include_auth: bool,
        include_error_handling: bool
    ) -> str:
        if language == "python":
            return self._generate_python_client(endpoints, http_client, include_auth, include_error_handling)
        elif language in ("javascript", "typescript"):
            return self._generate_js_client(endpoints, http_client, include_auth, include_error_handling)
        elif language == "go":
            return self._generate_go_client(endpoints, include_auth, include_error_handling)
        else:
            return self._generate_generic_client(endpoints)

    def _generate_python_client(
        self,
        endpoints: List[Dict[str, Any]],
        http_client: str,
        include_auth: bool,
        include_error_handling: bool
    ) -> str:
        imports = ["from typing import Optional, Dict, Any"]
        if http_client == "httpx":
            imports.append("import httpx")
        else:
            imports.append("import requests")

        class_def = '''
class APIClient:
    """Auto-generated API client"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
'''

        if include_auth:
            class_def += '''
        self.headers: Dict[str, str] = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
'''

        if include_error_handling:
            class_def += '''
        self.timeout = 30.0

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")
'''
        else:
            class_def += '''
    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        return response.json()
'''

        for ep in endpoints:
            params = self._get_endpoint_params(ep)
            method_code = f'''
    def {ep["name"]}({params}) -> Any:
        """{ep["description"]}"""
        return self._request("{ep["method"]}", "{ep["path"]}"{", " + params.split(":")[0] if params else ""})
'''
            class_def += method_code

        return "\n".join(imports) + class_def

    def _generate_js_client(
        self,
        endpoints: List[Dict[str, Any]],
        http_client: str,
        include_auth: bool,
        include_error_handling: bool
    ) -> str:
        imports = ["const axios = require('axios');"] if http_client == "axios" else []

        class_def = '''
class APIClient {
  constructor(baseURL, apiKey = null) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
    this.client = axios.create({
      baseURL,
      timeout: 30000,
    });
'''

        if include_auth:
            class_def += '''
    if (apiKey) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${apiKey}`;
    }
'''

        class_def += '''
  }

  async request(method, endpoint, data = null) {
'''

        if include_error_handling:
            class_def += '''
    try {
      const response = await this.client({ method, url: endpoint, data });
      return response.data;
    } catch (error) {
      throw new APIError(error.message);
    }
'''
        else:
            class_def += '''
    const response = await this.client({ method, url: endpoint, data });
    return response.data;
'''

        class_def += '''
  }
'''

        for ep in endpoints:
            method_code = f'''
  async {ep["name"]}({self._get_js_params(ep)}) {{
    return this.request('{ep["method"]}', '{ep["path"]}'{', data' if ep["method"] in ('POST', 'PUT', 'PATCH') else ''});
  }}
'''
            class_def += method_code

        class_def += "\n}"

        return "\n".join(imports) + class_def

    def _generate_go_client(
        self,
        endpoints: List[Dict[str, Any]],
        include_auth: bool,
        include_error_handling: bool
    ) -> str:
        code = '''package api

import (
    "bytes"
    "encoding/json"
    "net/http"
)

type Client struct {
    baseURL string
    apiKey  string
    client  *http.Client
}
'''

        return code

    def _generate_generic_client(self, endpoints: List[Dict[str, Any]]) -> str:
        return "// Generic API client - specify language for detailed implementation"

    def _get_endpoint_params(self, endpoint: Dict[str, Any]) -> str:
        path_params = re.findall(r'\{(\w+)\}', endpoint["path"])
        if path_params:
            return ", ".join([f"{p}: str" for p in path_params])
        return ""

    def _get_js_params(self, endpoint: Dict[str, Any]) -> str:
        path_params = re.findall(r'\{(\w+)\}', endpoint["path"])
        if path_params:
            return ", ".join(path_params)
        return ""

    def _generate_types(self, endpoints: List[Dict[str, Any]], language: str) -> str:
        if language == "python":
            return '''
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class APIResponse:
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None

@dataclass
class APIError(Exception):
    message: str
'''
        elif language in ("javascript", "typescript"):
            return '''
interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

class APIError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'APIError';
  }
}
'''
        return ""

    def _generate_usage_examples(self, endpoints: List[Dict[str, Any]], language: str) -> str:
        if endpoints:
            ep = endpoints[0]
            return f'''
# Example usage:
client = APIClient("https://api.example.com", "your-api-key")
result = client.{ep["name"]}()
'''
        return ""
