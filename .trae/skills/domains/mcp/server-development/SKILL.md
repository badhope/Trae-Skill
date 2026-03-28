---
name: mcp-server-development
description: "MCP server development expert for building Model Context Protocol servers with tools, resources, and prompts. Keywords: mcp, server, protocol, tools, resources, stdio, http"
layer: domain
role: specialist
version: 2.0.0
domain: mcp
invoked_by:
  - coding-workflow
  - api-integrator
capabilities:
  - server_architecture
  - tools_implementation
  - resources_exposure
  - prompts_management
  - security_control
---

# MCP Server Development

Model Context Protocol (MCP) 服务器开发专家，帮助设计、实现和部署 MCP 服务器。

## 适用场景

- MCP 服务器架构设计
- 工具 (Tools) 实现
- 资源 (Resources) 暴露
- 提示词 (Prompts) 管理
- 传输层配置 (stdio, HTTP, SSE)
- 安全与权限控制

## MCP 协议核心概念

### 服务器组件

```
MCP Server
├── Tools        # 可执行的函数/操作
├── Resources    # 可读取的数据源
├── Prompts      # 预定义的提示词模板
└── Capabilities # 服务器能力声明
```

### 传输协议

- **stdio**: 标准输入输出，适合本地进程
- **HTTP**: HTTP/HTTPS，适合远程服务
- **SSE**: Server-Sent Events，适合实时推送

## 实现模式

### TypeScript/Node.js

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "echo",
    description: "Echo a message",
    inputSchema: {
      type: "object",
      properties: { message: { type: "string" } },
      required: ["message"]
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  if (name === "echo") {
    return { content: [{ type: "text", text: args.message }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [{
        "name": "echo",
        "description": "Echo a message",
        "inputSchema": {
            "type": "object",
            "properties": {"message": {"type": "string"}},
            "required": ["message"]
        }
    }]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "echo":
        return {"content": [{"type": "text", "text": arguments["message"]}]}

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)
```

## 工具设计最佳实践

### 输入验证

```typescript
inputSchema: {
  type: "object",
  properties: {
    path: { type: "string", description: "File path to read" },
    encoding: { type: "string", enum: ["utf-8", "binary"], default: "utf-8" }
  },
  required: ["path"],
  additionalProperties: false
}
```

### 错误处理

```typescript
try {
  const result = await performOperation(args);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
} catch (error) {
  return {
    isError: true,
    content: [{ type: "text", text: `Error: ${error.message}` }]
  };
}
```

## 资源暴露模式

### 静态资源

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [{
    uri: "file:///config.json",
    name: "Configuration",
    mimeType: "application/json"
  }]
}));
```

### 动态资源

```typescript
server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [{
    uriTemplate: "file:///{path}",
    name: "File by path",
    mimeType: "application/octet-stream"
  }]
}));
```

## 安全考虑

1. **输入验证**: 严格验证所有输入参数
2. **路径遍历**: 防止目录遍历攻击
3. **权限控制**: 限制可访问的资源
4. **速率限制**: 防止资源滥用
5. **日志记录**: 记录所有操作

## 调试技巧

```bash
# 启用调试日志
DEBUG=mcp:* node server.js

# 使用 MCP Inspector
npx @modelcontextprotocol/inspector node dist/server.js
```

## 相关技能

- [mcp-tool-creation](../tools) - MCP 工具创建
- [mcp-client-integration](../client-integration) - MCP 客户端集成
- [api-design](../../actions/code/api-design) - API 设计
