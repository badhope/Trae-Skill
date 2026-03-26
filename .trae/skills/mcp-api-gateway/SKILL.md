# MCP API Gateway

## Description
MCP API 网关专家。帮助设计和实现 MCP API 网关，统一管理多个 MCP 服务器的访问、路由和负载均衡。

## Details

### 功能特性
- 多服务器路由
- 负载均衡
- 请求转发
- 响应聚合
- 缓存策略
- 限流熔断

### 网关架构

```
                    ┌─────────────────┐
                    │   MCP Client    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   MCP Gateway   │
                    │  - Router       │
                    │  - Load Balance │
                    │  - Cache        │
                    │  - Rate Limit   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
│ MCP Server A  │   │ MCP Server B  │   │ MCP Server C  │
│ (Filesystem)  │   │ (Database)    │   │ (Browser)     │
└───────────────┘   └───────────────┘   └───────────────┘
```

### 网关实现

```typescript
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";

interface MCPServerConfig {
  name: string;
  url: string;
  capabilities: string[];
  weight: number;
  healthCheck?: string;
}

class MCPGateway {
  private servers: Map<string, MCPServerConfig[]> = new Map();
  private app: express.Application;
  
  constructor() {
    this.app = express();
    this.setupMiddleware();
  }
  
  registerServer(config: MCPServerConfig) {
    const capability = config.capabilities[0];
    if (!this.servers.has(capability)) {
      this.servers.set(capability, []);
    }
    this.servers.get(capability)!.push(config);
  }
  
  private setupMiddleware() {
    // JSON 解析
    this.app.use(express.json());
    
    // 请求日志
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
    
    // 健康检查
    this.app.get("/health", (req, res) => {
      res.json({ status: "healthy", timestamp: new Date().toISOString() });
    });
    
    // 工具列表聚合
    this.app.get("/tools", async (req, res) => {
      const allTools = await this.aggregateTools();
      res.json({ tools: allTools });
    });
    
    // 工具调用路由
    this.app.post("/tools/call", async (req, res) => {
      try {
        const result = await this.routeToolCall(req.body);
        res.json(result);
      } catch (error: any) {
        res.status(500).json({ error: error.message });
      }
    });
    
    // 资源列表聚合
    this.app.get("/resources", async (req, res) => {
      const allResources = await this.aggregateResources();
      res.json({ resources: allResources });
    });
  }
  
  private async aggregateTools() {
    const allTools: any[] = [];
    
    for (const [capability, servers] of this.servers) {
      for (const server of servers) {
        try {
          const response = await fetch(`${server.url}/tools`);
          const data = await response.json();
          allTools.push(...data.tools.map((t: any) => ({
            ...t,
            server: server.name
          })));
        } catch (error) {
          console.error(`Failed to get tools from ${server.name}:`, error);
        }
      }
    }
    
    return allTools;
  }
  
  private async routeToolCall(params: { name: string; arguments: any }) {
    // 根据工具名称找到对应的服务器
    const server = this.findServerForTool(params.name);
    if (!server) {
      throw new Error(`No server found for tool: ${params.name}`);
    }
    
    const response = await fetch(`${server.url}/tools/call`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params)
    });
    
    return await response.json();
  }
  
  private findServerForTool(toolName: string): MCPServerConfig | null {
    for (const [_, servers] of this.servers) {
      for (const server of servers) {
        // 简单匹配：工具名前缀匹配服务器能力
        if (toolName.startsWith(server.capabilities[0])) {
          return server;
        }
      }
    }
    return null;
  }
  
  start(port: number) {
    this.app.listen(port, () => {
      console.log(`MCP Gateway running on port ${port}`);
    });
  }
}
```

### 负载均衡

```typescript
class LoadBalancer {
  private roundRobinIndex: Map<string, number> = new Map();
  
  selectServer(servers: MCPServerConfig[]): MCPServerConfig {
    if (servers.length === 1) {
      return servers[0];
    }
    
    // 加权轮询
    const totalWeight = servers.reduce((sum, s) => sum + s.weight, 0);
    let random = Math.random() * totalWeight;
    
    for (const server of servers) {
      random -= server.weight;
      if (random <= 0) {
        return server;
      }
    }
    
    return servers[0];
  }
  
  // 最少连接
  async selectLeastConnected(
    servers: MCPServerConfig[],
    connectionCounter: Map<string, number>
  ): Promise<MCPServerConfig> {
    let minConnections = Infinity;
    let selectedServer = servers[0];
    
    for (const server of servers) {
      const connections = connectionCounter.get(server.name) || 0;
      if (connections < minConnections) {
        minConnections = connections;
        selectedServer = server;
      }
    }
    
    return selectedServer;
  }
}
```

### 缓存层

```typescript
interface CacheEntry {
  data: any;
  expiry: number;
}

class MCPGatewayCache {
  private cache: Map<string, CacheEntry> = new Map();
  private defaultTTL: number = 300000; // 5 分钟
  
  async get<T>(key: string): Promise<T | null> {
    const entry = this.cache.get(key);
    if (!entry) return null;
    
    if (Date.now() > entry.expiry) {
      this.cache.delete(key);
      return null;
    }
    
    return entry.data;
  }
  
  async set(key: string, data: any, ttl: number = this.defaultTTL) {
    this.cache.set(key, {
      data,
      expiry: Date.now() + ttl
    });
  }
  
  async getOrFetch<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl?: number
  ): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached !== null) {
      return cached;
    }
    
    const data = await fetcher();
    await this.set(key, data, ttl);
    return data;
  }
  
  invalidate(pattern: string) {
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }
}

// 使用缓存
const cache = new MCPGatewayCache();

async function aggregateToolsWithCache() {
  return cache.getOrFetch(
    "tools:all",
    () => aggregateTools(),
    60000  // 1 分钟缓存
  );
}
```

### 限流熔断

```typescript
import CircuitBreaker from "opossum";

class MCPCircuitBreaker {
  private breakers: Map<string, CircuitBreaker> = new Map();
  
  createBreaker(
    name: string,
    fn: (...args: any[]) => Promise<any>,
    options: Partial<CircuitBreaker.Options> = {}
  ) {
    const breaker = new CircuitBreaker(fn, {
      timeout: 30000,
      errorThresholdPercentage: 50,
      resetTimeout: 30000,
      ...options
    });
    
    breaker.on("open", () => {
      console.log(`Circuit breaker opened for ${name}`);
    });
    
    breaker.on("halfOpen", () => {
      console.log(`Circuit breaker half-open for ${name}`);
    });
    
    breaker.on("close", () => {
      console.log(`Circuit breaker closed for ${name}`);
    });
    
    this.breakers.set(name, breaker);
    return breaker;
  }
  
  async execute(name: string, ...args: any[]) {
    const breaker = this.breakers.get(name);
    if (!breaker) {
      throw new Error(`No circuit breaker found for ${name}`);
    }
    
    return breaker.fire(...args);
  }
  
  getStats(name: string) {
    const breaker = this.breakers.get(name);
    if (!breaker) return null;
    
    return {
      state: breaker.opened ? "open" : breaker.halfOpen ? "halfOpen" : "closed",
      stats: breaker.stats
    };
  }
}
```

### 请求聚合

```typescript
class RequestAggregator {
  async aggregateResponses(
    requests: Array<{ server: string; endpoint: string; params?: any }>
  ): Promise<Map<string, any>> {
    const results = new Map<string, any>();
    
    await Promise.all(
      requests.map(async (req) => {
        try {
          const response = await fetch(
            `${req.server}${req.endpoint}`,
            req.params ? {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(req.params)
            } : {}
          );
          results.set(req.server, await response.json());
        } catch (error) {
          results.set(req.server, { error: (error as Error).message });
        }
      })
    );
    
    return results;
  }
  
  async parallelToolCalls(
    calls: Array<{ tool: string; args: any; server: string }>
  ): Promise<any[]> {
    return Promise.all(
      calls.map(async (call) => {
        const response = await fetch(`${call.server}/tools/call`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: call.tool,
            arguments: call.args
          })
        });
        return response.json();
      })
    );
  }
}
```

### 配置管理

```yaml
# gateway-config.yaml
gateway:
  port: 8080
  timeout: 30000
  
servers:
  - name: filesystem
    url: http://localhost:3001
    capabilities: [file, filesystem]
    weight: 1
    healthCheck: /health
    
  - name: database
    url: http://localhost:3002
    capabilities: [db, database, sql]
    weight: 1
    healthCheck: /health
    
  - name: browser
    url: http://localhost:3003
    capabilities: [browser, puppeteer]
    weight: 1
    healthCheck: /health

cache:
  enabled: true
  ttl: 300000
  
rateLimit:
  enabled: true
  windowMs: 60000
  max: 100
  
circuitBreaker:
  timeout: 30000
  errorThresholdPercentage: 50
  resetTimeout: 30000
```

### 监控指标

```typescript
import client from "prom-client";

const register = new client.Registry();

const requestCounter = new client.Counter({
  name: "mcp_gateway_requests_total",
  help: "Total requests through gateway",
  labelNames: ["server", "tool", "status"],
  registers: [register]
});

const requestDuration = new client.Histogram({
  name: "mcp_gateway_request_duration_seconds",
  help: "Request duration in seconds",
  labelNames: ["server", "tool"],
  buckets: [0.1, 0.5, 1, 2, 5, 10],
  registers: [register]
});

const activeConnections = new client.Gauge({
  name: "mcp_gateway_active_connections",
  help: "Active connections per server",
  labelNames: ["server"],
  registers: [register]
});

// 暴露指标
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});
```

### 最佳实践

1. **健康检查**: 定期检查后端服务器健康状态
2. **优雅降级**: 服务器不可用时提供备用响应
3. **请求超时**: 设置合理的请求超时时间
4. **日志记录**: 记录所有请求和错误
5. **监控告警**: 监控关键指标并设置告警

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `api-design` - API 设计
- `kubernetes-orchestration` - Kubernetes 编排
- `observability-monitoring` - 可观测性监控
