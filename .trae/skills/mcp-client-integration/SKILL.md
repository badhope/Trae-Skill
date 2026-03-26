# MCP Client Integration

## Description
Model Context Protocol (MCP) 客户端集成专家。帮助将 MCP 客户端集成到应用程序中，连接 MCP 服务器，发现和使用工具、资源和提示词。

## Details

### 功能特性
- MCP 客户端配置与连接
- 工具发现与调用
- 资源读取与订阅
- 提示词获取与使用
- 多服务器管理
- 错误处理与重连

### MCP 客户端架构

```
MCP Client
├── Connection Manager  # 连接管理
├── Tool Registry       # 工具注册表
├── Resource Cache      # 资源缓存
├── Prompt Library      # 提示词库
└── Transport Layer     # 传输层
```

### 客户端实现

#### TypeScript/Node.js
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

// 创建客户端
const client = new Client(
  { name: "my-client", version: "1.0.0" },
  { capabilities: {} }
);

// 连接到服务器
const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"]
});
await client.connect(transport);

// 列出可用工具
const tools = await client.request({
  method: "tools/list"
}, ListToolsResultSchema);

// 调用工具
const result = await client.request({
  method: "tools/call",
  params: {
    name: "read_file",
    arguments: { path: "/example.txt" }
  }
}, CallToolResultSchema);
```

#### Python
```python
from mcp import Client
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client("node", ["server.js"]) as client:
        # 列出工具
        tools = await client.list_tools()
        
        # 调用工具
        result = await client.call_tool("read_file", {"path": "/example.txt"})
```

### 工具发现与调用

#### 发现工具
```typescript
async function discoverTools(client: Client) {
  const response = await client.request(
    { method: "tools/list" },
    ListToolsResultSchema
  );
  
  return response.tools.map(tool => ({
    name: tool.name,
    description: tool.description,
    parameters: tool.inputSchema
  }));
}
```

#### 调用工具
```typescript
async function callTool(
  client: Client,
  name: string,
  args: Record<string, any>
) {
  try {
    const result = await client.request({
      method: "tools/call",
      params: { name, arguments: args }
    }, CallToolResultSchema);
    
    if (result.isError) {
      throw new Error(result.content[0].text);
    }
    
    return result.content;
  } catch (error) {
    console.error(`Tool call failed: ${error.message}`);
    throw error;
  }
}
```

### 资源管理

#### 读取资源
```typescript
async function readResource(client: Client, uri: string) {
  const result = await client.request({
    method: "resources/read",
    params: { uri }
  }, ReadResourceResultSchema);
  
  return result.contents;
}
```

#### 订阅资源更新
```typescript
// 订阅资源
await client.request({
  method: "resources/subscribe",
  params: { uri: "file:///config.json" }
}, SubscribeResultSchema);

// 监听更新通知
client.onNotification("notifications/resources/updated", (params) => {
  console.log("Resource updated:", params.uri);
});
```

### 提示词使用

#### 获取提示词
```typescript
async function getPrompt(
  client: Client,
  name: string,
  args: Record<string, any>
) {
  const result = await client.request({
    method: "prompts/get",
    params: { name, arguments: args }
  }, GetPromptResultSchema);
  
  return result.messages;
}
```

### 多服务器管理

```typescript
class MCPClientManager {
  private clients: Map<string, Client> = new Map();
  
  async connect(name: string, config: ServerConfig) {
    const client = new Client(
      { name: `${name}-client`, version: "1.0.0" },
      { capabilities: {} }
    );
    
    const transport = this.createTransport(config);
    await client.connect(transport);
    this.clients.set(name, client);
  }
  
  async callTool(server: string, tool: string, args: any) {
    const client = this.clients.get(server);
    if (!client) {
      throw new Error(`Server ${server} not connected`);
    }
    return client.request({
      method: "tools/call",
      params: { name: tool, arguments: args }
    }, CallToolResultSchema);
  }
  
  async listAllTools() {
    const allTools = [];
    for (const [name, client] of this.clients) {
      const result = await client.request(
        { method: "tools/list" },
        ListToolsResultSchema
      );
      allTools.push(...result.tools.map(t => ({ ...t, server: name })));
    }
    return allTools;
  }
}
```

### 错误处理与重连

```typescript
class ResilientMCPClient {
  private client: Client;
  private config: ServerConfig;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  
  async connect() {
    try {
      await this.client.connect(this.createTransport());
      this.reconnectAttempts = 0;
    } catch (error) {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        await new Promise(r => setTimeout(r, 1000 * this.reconnectAttempts));
        return this.connect();
      }
      throw error;
    }
  }
  
  setupErrorHandling() {
    this.client.onerror = (error) => {
      console.error("MCP client error:", error);
      this.handleDisconnect();
    };
  }
  
  async handleDisconnect() {
    console.log("Attempting to reconnect...");
    await this.connect();
  }
}
```

### 与 AI 模型集成

```typescript
async function useMCPWithAI(client: Client, userQuery: string) {
  // 1. 获取可用工具
  const tools = await client.request(
    { method: "tools/list" },
    ListToolsResultSchema
  );
  
  // 2. 将 MCP 工具转换为 AI 可用格式
  const aiTools = tools.tools.map(tool => ({
    type: "function",
    function: {
      name: tool.name,
      description: tool.description,
      parameters: tool.inputSchema
    }
  }));
  
  // 3. 调用 AI 模型
  const response = await ai.chat({
    messages: [{ role: "user", content: userQuery }],
    tools: aiTools
  });
  
  // 4. 处理工具调用
  if (response.toolCalls) {
    for (const call of response.toolCalls) {
      const result = await client.request({
        method: "tools/call",
        params: { name: call.function.name, arguments: call.function.arguments }
      }, CallToolResultSchema);
      
      // 将结果返回给 AI
      await ai.chat({
        messages: [
          { role: "tool", tool_call_id: call.id, content: JSON.stringify(result) }
        ]
      });
    }
  }
}
```

### 最佳实践

1. **连接池**: 复用连接，避免频繁创建
2. **超时设置**: 设置合理的超时时间
3. **错误重试**: 实现指数退避重试
4. **资源缓存**: 缓存不常变化的资源
5. **日志记录**: 记录所有操作便于调试

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `mcp-tool-creation` - MCP 工具创建
- `api-integrator` - API 集成
- `error-recovery` - 错误恢复
