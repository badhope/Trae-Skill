# MCP Protocol Deep Dive

## Description
MCP 协议深度解析专家。深入理解 MCP 协议规范，包括消息格式、传输层、能力协商等核心概念。

## Details

### 功能特性
- 协议规范解读
- 消息格式详解
- 传输层实现
- 能力协商机制
- 版本兼容性
- 协议扩展

### 协议概述

MCP (Model Context Protocol) 是一个开放协议，用于标准化 AI 模型与外部工具、资源和数据源的交互。

```
┌─────────────┐                    ┌─────────────┐
│   Client    │◄────── JSON-RPC ───►│   Server    │
│  (AI App)   │                    │  (MCP)      │
└─────────────┘                    └─────────────┘
      │                                  │
      │  Tools: 可执行函数               │
      │  Resources: 可读数据源           │
      │  Prompts: 提示词模板            │
      └──────────────────────────────────┘
```

### 消息格式

#### 请求 (Request)
```typescript
interface JSONRPCRequest {
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: object;
}

// 示例
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

#### 响应 (Response)
```typescript
interface JSONRPCResponse {
  jsonrpc: "2.0";
  id: string | number;
  result?: object;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}

// 成功响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [...]
  }
}

// 错误响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

#### 通知 (Notification)
```typescript
interface JSONRPCNotification {
  jsonrpc: "2.0";
  method: string;
  params?: object;
}

// 示例
{
  "jsonrpc": "2.0",
  "method": "notifications/resources/updated",
  "params": {
    "uri": "file:///example.txt"
  }
}
```

### 核心方法

#### 初始化
```typescript
// 客户端请求
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "clientInfo": {
      "name": "my-client",
      "version": "1.0.0"
    },
    "capabilities": {
      "roots": { "listChanged": true }
    }
  }
}

// 服务器响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "serverInfo": {
      "name": "my-server",
      "version": "1.0.0"
    },
    "capabilities": {
      "tools": {},
      "resources": { "subscribe": true },
      "prompts": {}
    }
  }
}
```

#### 工具操作
```typescript
// 列出工具
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}

// 调用工具
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/example.txt"
    }
  }
}
```

#### 资源操作
```typescript
// 列出资源
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/list"
}

// 读取资源
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "resources/read",
  "params": {
    "uri": "file:///example.txt"
  }
}

// 订阅资源
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "resources/subscribe",
  "params": {
    "uri": "file:///example.txt"
  }
}
```

### 传输层

#### stdio 传输
```typescript
import { stdin, stdout } from "process";
import { Readable, Writable } from "stream";

class StdioTransport {
  private buffer: string = "";
  
  constructor(
    private input: Readable = stdin,
    private output: Writable = stdout
  ) {}
  
  async send(message: object) {
    const content = JSON.stringify(message);
    this.output.write(`Content-Length: ${content.length}\r\n\r\n`);
    this.output.write(content);
  }
  
  onMessage(handler: (message: object) => void) {
    this.input.on("data", (data: Buffer) => {
      this.buffer += data.toString();
      this.processBuffer(handler);
    });
  }
  
  private processBuffer(handler: (message: object) => void) {
    while (true) {
      const headerEnd = this.buffer.indexOf("\r\n\r\n");
      if (headerEnd === -1) break;
      
      const header = this.buffer.slice(0, headerEnd);
      const match = header.match(/Content-Length: (\d+)/);
      if (!match) break;
      
      const contentLength = parseInt(match[1]);
      const contentStart = headerEnd + 4;
      const contentEnd = contentStart + contentLength;
      
      if (this.buffer.length < contentEnd) break;
      
      const content = this.buffer.slice(contentStart, contentEnd);
      this.buffer = this.buffer.slice(contentEnd);
      
      try {
        const message = JSON.parse(content);
        handler(message);
      } catch (error) {
        console.error("Failed to parse message:", error);
      }
    }
  }
}
```

#### HTTP 传输
```typescript
import express from "express";

class HTTPTransport {
  private app = express();
  private messageHandler?: (message: object) => Promise<object>;
  
  constructor(private port: number) {
    this.app.use(express.json());
    this.setupRoutes();
  }
  
  private setupRoutes() {
    this.app.post("/mcp", async (req, res) => {
      try {
        if (!this.messageHandler) {
          return res.status(500).json({ error: "No handler registered" });
        }
        
        const response = await this.messageHandler(req.body);
        res.json(response);
      } catch (error) {
        res.status(500).json({
          jsonrpc: "2.0",
          id: req.body.id,
          error: {
            code: -32603,
            message: "Internal error"
          }
        });
      }
    });
  }
  
  onMessage(handler: (message: object) => Promise<object>) {
    this.messageHandler = handler;
  }
  
  async send(message: object) {
    // HTTP 传输通常不主动发送，而是通过 SSE
  }
  
  start() {
    this.app.listen(this.port);
  }
}
```

#### SSE 传输
```typescript
import express from "express";

class SSETransport {
  private clients: Set<express.Response> = new Set();
  
  setupSSE(app: express.Application, path: string) {
    app.get(path, (req, res) => {
      res.setHeader("Content-Type", "text/event-stream");
      res.setHeader("Cache-Control", "no-cache");
      res.setHeader("Connection", "keep-alive");
      
      this.clients.add(res);
      
      req.on("close", () => {
        this.clients.delete(res);
      });
    });
  }
  
  send(message: object) {
    const data = JSON.stringify(message);
    const event = `data: ${data}\n\n`;
    
    for (const client of this.clients) {
      client.write(event);
    }
  }
  
  sendToClient(clientId: string, message: object) {
    // 发送给特定客户端
  }
}
```

### 能力协商

```typescript
interface ClientCapabilities {
  roots?: {
    listChanged?: boolean;
  };
  sampling?: {};
}

interface ServerCapabilities {
  tools?: {
    listChanged?: boolean;
  };
  resources?: {
    subscribe?: boolean;
    listChanged?: boolean;
  };
  prompts?: {
    listChanged?: boolean;
  };
  logging?: {};
}

// 能力检查
function hasCapability(
  capabilities: ServerCapabilities | undefined,
  feature: string
): boolean {
  if (!capabilities) return false;
  
  const parts = feature.split(".");
  let current: any = capabilities;
  
  for (const part of parts) {
    if (!current[part]) return false;
    current = current[part];
  }
  
  return true;
}

// 使用示例
if (hasCapability(serverCapabilities, "resources.subscribe")) {
  await subscribeToResource(uri);
}
```

### 错误代码

```typescript
enum MCPErrorCode {
  // JSON-RPC 标准错误
  ParseError = -32700,
  InvalidRequest = -32600,
  MethodNotFound = -32601,
  InvalidParams = -32602,
  InternalError = -32603,
  
  // MCP 特定错误
  ServerNotInitialized = -32002,
  UnknownErrorCode = -32001,
  
  // 请求错误
  Cancelled = -32800,
  ContentTooLarge = -32900
}

function createError(code: MCPErrorCode, message: string, id?: string | number) {
  return {
    jsonrpc: "2.0",
    id: id ?? null,
    error: {
      code,
      message
    }
  };
}
```

### 版本兼容

```typescript
const SUPPORTED_VERSIONS = ["2024-11-05", "2024-10-07"];

function checkVersion(clientVersion: string): boolean {
  return SUPPORTED_VERSIONS.includes(clientVersion);
}

function negotiateVersion(clientVersions: string[]): string | null {
  for (const version of clientVersions) {
    if (SUPPORTED_VERSIONS.includes(version)) {
      return version;
    }
  }
  return null;
}
```

### 协议扩展

```typescript
// 自定义方法
interface CustomMethods {
  "custom/sync": {
    params: { force?: boolean };
    result: { synced: boolean; timestamp: string };
  };
}

// 注册自定义方法
server.setRequestHandler("custom/sync", async (request) => {
  const { force = false } = request.params;
  
  // 执行同步
  const result = await performSync(force);
  
  return {
    synced: true,
    timestamp: new Date().toISOString()
  };
});
```

### 最佳实践

1. **版本检查**: 始终检查协议版本兼容性
2. **错误处理**: 提供清晰的错误信息
3. **超时处理**: 设置合理的请求超时
4. **消息验证**: 验证所有传入消息格式
5. **日志记录**: 记录协议交互便于调试

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `mcp-client-integration` - MCP 客户端集成
- `api-design` - API 设计
