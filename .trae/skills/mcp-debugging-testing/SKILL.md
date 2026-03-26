# MCP Debugging & Testing

## Description
MCP 调试与测试专家。帮助调试 MCP 服务器和客户端，使用 MCP Inspector 等工具进行测试和验证。

## Details

### 功能特性
- MCP Inspector 使用
- 服务器调试技巧
- 客户端调试方法
- 协议消息追踪
- 错误诊断与修复
- 自动化测试

### MCP Inspector

#### 安装与启动
```bash
# 使用 npx 直接运行
npx @modelcontextprotocol/inspector node dist/server.js

# 或全局安装
npm install -g @modelcontextprotocol/inspector
mcp-inspector node dist/server.js

# Python 服务器
npx @modelcontextprotocol/inspector python server.py
```

#### Inspector 功能
- **工具列表**: 查看所有可用工具
- **工具调用**: 测试工具执行
- **资源浏览**: 查看可用资源
- **提示词查看**: 查看提示词模板
- **消息日志**: 查看协议消息

### 调试技巧

#### 1. 启用调试日志
```typescript
// 环境变量方式
process.env.DEBUG = "mcp:*";

// 或在代码中
import debug from "debug";
debug.enable("mcp:*");
```

#### 2. 消息追踪
```typescript
// 拦截所有请求
const originalRequest = server.request.bind(server);
server.request = async (request: any) => {
  console.log("[REQUEST]", JSON.stringify(request, null, 2));
  const response = await originalRequest(request);
  console.log("[RESPONSE]", JSON.stringify(response, null, 2));
  return response;
};

// 拦截所有通知
server.onnotification = (notification: any) => {
  console.log("[NOTIFICATION]", JSON.stringify(notification, null, 2));
};
```

#### 3. 错误捕获
```typescript
// 全局错误处理
process.on("uncaughtException", (error) => {
  console.error("[UNCAUGHT]", error);
});

process.on("unhandledRejection", (reason, promise) => {
  console.error("[UNHANDLED]", reason);
});

// 服务器错误处理
server.onerror = (error: Error) => {
  console.error("[SERVER ERROR]", error);
};
```

### 常见问题诊断

#### 连接问题
```typescript
// 问题：服务器无法启动
// 诊断步骤：

// 1. 检查端口占用
const net = require("net");
const tester = net.createServer()
  .once("error", (err: any) => {
    if (err.code === "EADDRINUSE") {
      console.error("Port is already in use");
    }
  })
  .once("listening", () => tester.close());

// 2. 检查传输层配置
const transport = new StdioServerTransport();
console.log("Transport created:", transport);

// 3. 检查服务器配置
const server = new Server(
  { name: "test-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);
console.log("Server capabilities:", server.capabilities);
```

#### 工具调用问题
```typescript
// 问题：工具调用失败
// 诊断步骤：

// 1. 验证工具注册
server.setRequestHandler(ListToolsRequestSchema, async () => {
  const tools = [
    { name: "test_tool", description: "Test", inputSchema: {} }
  ];
  console.log("Registered tools:", tools);
  return { tools };
});

// 2. 验证工具处理
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  console.log("Tool call request:", request.params);
  
  try {
    const result = await executeTool(request.params.name, request.params.arguments);
    console.log("Tool call result:", result);
    return result;
  } catch (error) {
    console.error("Tool call error:", error);
    return {
      isError: true,
      content: [{ type: "text", text: error.message }]
    };
  }
});
```

### 单元测试

#### Jest 测试示例
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

describe("MCP Server", () => {
  let server: Server;
  
  beforeEach(() => {
    server = new Server(
      { name: "test-server", version: "1.0.0" },
      { capabilities: { tools: {} } }
    );
  });
  
  describe("tools/list", () => {
    it("should return list of tools", async () => {
      const handler = server.getRequestHandler(ListToolsRequestSchema);
      const result = await handler({});
      
      expect(result.tools).toBeDefined();
      expect(Array.isArray(result.tools)).toBe(true);
    });
  });
  
  describe("tools/call", () => {
    it("should execute tool successfully", async () => {
      const handler = server.getRequestHandler(CallToolRequestSchema);
      const result = await handler({
        params: {
          name: "echo",
          arguments: { message: "test" }
        }
      });
      
      expect(result.isError).toBeUndefined();
      expect(result.content).toBeDefined();
    });
    
    it("should handle unknown tool", async () => {
      const handler = server.getRequestHandler(CallToolRequestSchema);
      const result = await handler({
        params: {
          name: "unknown_tool",
          arguments: {}
        }
      });
      
      expect(result.isError).toBe(true);
    });
  });
});
```

#### Python pytest 测试
```python
import pytest
from mcp.server import Server

@pytest.fixture
def server():
    return Server("test-server")

@pytest.mark.asyncio
async def test_list_tools(server):
    tools = await server.list_tools()
    assert isinstance(tools, list)

@pytest.mark.asyncio
async def test_call_tool(server):
    result = await server.call_tool("echo", {"message": "test"})
    assert "content" in result
    assert not result.get("isError", False)
```

### 集成测试

#### 端到端测试
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

describe("MCP Integration", () => {
  let client: Client;
  
  beforeAll(async () => {
    client = new Client({ name: "test-client", version: "1.0.0" }, {});
    const transport = new StdioClientTransport({
      command: "node",
      args: ["dist/server.js"]
    });
    await client.connect(transport);
  });
  
  afterAll(async () => {
    await client.close();
  });
  
  it("should connect to server", () => {
    expect(client.isConnected()).toBe(true);
  });
  
  it("should list tools", async () => {
    const result = await client.request(
      { method: "tools/list" },
      ListToolsResultSchema
    );
    expect(result.tools.length).toBeGreaterThan(0);
  });
  
  it("should call tool", async () => {
    const result = await client.request({
      method: "tools/call",
      params: { name: "test_tool", arguments: {} }
    }, CallToolResultSchema);
    
    expect(result.content).toBeDefined();
  });
});
```

### 性能测试

```typescript
import { performance } from "perf_hooks";

async function benchmarkToolCalls(client: Client, toolName: string, iterations: number) {
  const times: number[] = [];
  
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    await client.request({
      method: "tools/call",
      params: { name: toolName, arguments: {} }
    }, CallToolResultSchema);
    times.push(performance.now() - start);
  }
  
  return {
    avg: times.reduce((a, b) => a + b) / times.length,
    min: Math.min(...times),
    max: Math.max(...times),
    p95: times.sort((a, b) => a - b)[Math.floor(times.length * 0.95)]
  };
}
```

### 调试清单

#### 服务器启动检查
- [ ] 依赖已正确安装
- [ ] 入口文件路径正确
- [ ] 环境变量已配置
- [ ] 端口/stdio 配置正确
- [ ] 权限设置正确

#### 工具注册检查
- [ ] 工具名称唯一
- [ ] inputSchema 格式正确
- [ ] 处理函数已注册
- [ ] 错误处理已实现

#### 客户端连接检查
- [ ] 服务器命令正确
- [ ] 参数格式正确
- [ ] 连接超时设置
- [ ] 错误处理已实现

### 日志分析

```typescript
// 结构化日志
interface LogEntry {
  timestamp: string;
  level: "debug" | "info" | "warn" | "error";
  component: string;
  message: string;
  data?: any;
}

function log(entry: LogEntry) {
  console.log(JSON.stringify({
    ...entry,
    timestamp: new Date().toISOString()
  }));
}

// 使用示例
log({
  level: "info",
  component: "tool-executor",
  message: "Tool called",
  data: { tool: "read_file", args: { path: "/test.txt" } }
});
```

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `mcp-client-integration` - MCP 客户端集成
- `test-generator` - 测试生成
- `error-recovery` - 错误恢复
