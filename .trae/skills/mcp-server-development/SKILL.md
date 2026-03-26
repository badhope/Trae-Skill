# MCP Server Development

## Description
Model Context Protocol (MCP) 服务器开发专家。帮助设计、实现和部署 MCP 服务器，让 AI 模型能够与外部工具、资源和数据源进行标准化交互。

## Details

### 功能特性
- MCP 服务器架构设计
- 工具 (Tools) 实现
- 资源 (Resources) 暴露
- 提示词 (Prompts) 管理
- 传输层配置 (stdio, HTTP, SSE)
- 安全与权限控制

### MCP 协议核心概念

#### 1. 服务器组件
```
MCP Server
├── Tools        # 可执行的函数/操作
├── Resources    # 可读取的数据源
├── Prompts      # 预定义的提示词模板
└── Capabilities # 服务器能力声明
```

#### 2. 传输协议
- **stdio**: 标准输入输出，适合本地进程
- **HTTP**: HTTP/HTTPS，适合远程服务
- **SSE**: Server-Sent Events，适合实时推送

#### 3. 消息类型
- `request`: 客户端请求
- `response`: 服务器响应
- `notification`: 单向通知

### 实现模式

#### TypeScript/Node.js
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

// 注册工具
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "echo",
    description: "Echo a message",
    inputSchema: {
      type: "object",
      properties: {
        message: { type: "string" }
      },
      required: ["message"]
    }
  }]
}));

// 处理工具调用
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  if (name === "echo") {
    return { content: [{ type: "text", text: args.message }] };
  }
});

// 启动服务器
const transport = new StdioServerTransport();
await server.connect(transport);
```

#### Python
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
            "properties": {
                "message": {"type": "string"}
            },
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

### 工具设计最佳实践

#### 输入验证
```typescript
inputSchema: {
  type: "object",
  properties: {
    path: { 
      type: "string",
      description: "File path to read"
    },
    encoding: { 
      type: "string",
      enum: ["utf-8", "binary"],
      default: "utf-8"
    }
  },
  required: ["path"],
  additionalProperties: false
}
```

#### 错误处理
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

### 资源暴露模式

#### 静态资源
```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [{
    uri: "file:///config.json",
    name: "Configuration",
    mimeType: "application/json"
  }]
}));
```

#### 动态资源
```typescript
server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [{
    uriTemplate: "file:///{path}",
    name: "File by path",
    mimeType: "application/octet-stream"
  }]
}));
```

### 安全考虑

1. **输入验证**: 严格验证所有输入参数
2. **路径遍历**: 防止目录遍历攻击
3. **权限控制**: 限制可访问的资源
4. **速率限制**: 防止资源滥用
5. **日志记录**: 记录所有操作

### 调试技巧

```typescript
// 启用调试日志
process.env.DEBUG = "mcp:*";

// 使用 MCP Inspector
npx @modelcontextprotocol/inspector node dist/server.js
```

### 常见问题

1. **连接失败**: 检查传输层配置
2. **工具未找到**: 验证工具名称和注册
3. **参数错误**: 检查 inputSchema 定义
4. **超时**: 增加超时时间或优化操作

## Related Skills
- `mcp-client-integration` - MCP 客户端集成
- `mcp-tool-creation` - MCP 工具创建
- `api-design` - API 设计
- `security-auditor` - 安全审计
