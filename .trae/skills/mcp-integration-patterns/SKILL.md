# MCP Integration Patterns

## Description
MCP 集成模式专家。帮助设计和实现各种 MCP 集成模式，包括多服务器协调、工具链、事件驱动等。

## Details

### 功能特性
- 多服务器协调模式
- 工具链与流水线
- 事件驱动集成
- 数据同步模式
- 错误传播与恢复
- 性能优化模式

### 多服务器协调

#### 服务器注册表
```typescript
interface MCPServerConfig {
  name: string;
  command: string;
  args: string[];
  env?: Record<string, string>;
  capabilities: string[];
}

class MCPServerRegistry {
  private servers: Map<string, MCPServerConfig> = new Map();
  private clients: Map<string, Client> = new Map();
  
  register(config: MCPServerConfig) {
    this.servers.set(config.name, config);
  }
  
  async connect(name: string): Promise<Client> {
    const config = this.servers.get(name);
    if (!config) throw new Error(`Server ${name} not found`);
    
    const client = new Client(
      { name: `${name}-client`, version: "1.0.0" },
      { capabilities: {} }
    );
    
    const transport = new StdioClientTransport({
      command: config.command,
      args: config.args,
      env: { ...process.env, ...config.env }
    });
    
    await client.connect(transport);
    this.clients.set(name, client);
    return client;
  }
  
  getClient(name: string): Client | undefined {
    return this.clients.get(name);
  }
  
  async disconnectAll() {
    for (const client of this.clients.values()) {
      await client.close();
    }
    this.clients.clear();
  }
}
```

#### 工具路由器
```typescript
interface ToolRoute {
  toolName: string;
  serverName: string;
  transform?: (args: any) => any;
}

class ToolRouter {
  private routes: Map<string, ToolRoute> = new Map();
  private registry: MCPServerRegistry;
  
  constructor(registry: MCPServerRegistry) {
    this.registry = registry;
  }
  
  addRoute(route: ToolRoute) {
    this.routes.set(route.toolName, route);
  }
  
  async callTool(name: string, args: any): Promise<any> {
    const route = this.routes.get(name);
    if (!route) throw new Error(`No route for tool: ${name}`);
    
    const client = this.registry.getClient(route.serverName);
    if (!client) throw new Error(`Server not connected: ${route.serverName}`);
    
    const transformedArgs = route.transform ? route.transform(args) : args;
    
    return client.request({
      method: "tools/call",
      params: { name, arguments: transformedArgs }
    }, CallToolResultSchema);
  }
  
  async listAllTools(): Promise<any[]> {
    const allTools: any[] = [];
    
    for (const [serverName, client] of this.registry.clients) {
      const result = await client.request(
        { method: "tools/list" },
        ListToolsResultSchema
      );
      allTools.push(...result.tools.map(t => ({ ...t, server: serverName })));
    }
    
    return allTools;
  }
}
```

### 工具链模式

#### 顺序执行链
```typescript
interface ChainStep {
  toolName: string;
  argsMapping: (previousResult: any, originalArgs: any) => any;
  onError?: 'stop' | 'continue' | 'retry';
}

class ToolChain {
  private steps: ChainStep[] = [];
  
  addStep(step: ChainStep): this {
    this.steps.push(step);
    return this;
  }
  
  async execute(initialArgs: any, router: ToolRouter): Promise<any> {
    let result: any = null;
    let args = initialArgs;
    
    for (const step of this.steps) {
      const stepArgs = step.argsMapping(result, initialArgs);
      
      try {
        result = await router.callTool(step.toolName, stepArgs);
      } catch (error) {
        if (step.onError === 'stop') {
          throw error;
        } else if (step.onError === 'retry') {
          result = await router.callTool(step.toolName, stepArgs);
        }
        // 'continue' - 忽略错误继续
      }
    }
    
    return result;
  }
}

// 使用示例
const chain = new ToolChain()
  .addStep({
    toolName: 'search_files',
    argsMapping: (_, args) => ({ pattern: args.searchPattern })
  })
  .addStep({
    toolName: 'read_file',
    argsMapping: (result, _) => ({ path: result.files[0] })
  })
  .addStep({
    toolName: 'analyze_content',
    argsMapping: (result, args) => ({ content: result.content, type: args.analysisType })
  });

const result = await chain.execute(
  { searchPattern: '*.ts', analysisType: 'complexity' },
  router
);
```

#### 并行执行
```typescript
class ParallelExecutor {
  constructor(private router: ToolRouter) {}
  
  async executeAll(calls: Array<{ toolName: string; args: any }>): Promise<any[]> {
    return Promise.all(
      calls.map(call => this.router.callTool(call.toolName, call.args))
    );
  }
  
  async executeRace(calls: Array<{ toolName: string; args: any }>): Promise<any> {
    return Promise.race(
      calls.map(call => this.router.callTool(call.toolName, call.args))
    );
  }
  
  async executeWithFallback(
    primary: { toolName: string; args: any },
    fallbacks: Array<{ toolName: string; args: any }>
  ): Promise<any> {
    try {
      return await this.router.callTool(primary.toolName, primary.args);
    } catch {
      for (const fallback of fallbacks) {
        try {
          return await this.router.callTool(fallback.toolName, fallback.args);
        } catch {}
      }
      throw new Error('All fallbacks failed');
    }
  }
}
```

### 事件驱动集成

#### 事件总线
```typescript
interface MCPEvent {
  type: string;
  source: string;
  payload: any;
  timestamp: Date;
}

class EventBus {
  private handlers: Map<string, Set<(event: MCPEvent) => void>> = new Map();
  
  subscribe(eventType: string, handler: (event: MCPEvent) => void): () => void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }
    this.handlers.get(eventType)!.add(handler);
    
    return () => {
      this.handlers.get(eventType)?.delete(handler);
    };
  }
  
  publish(event: Omit<MCPEvent, 'timestamp'>) {
    const fullEvent: MCPEvent = {
      ...event,
      timestamp: new Date()
    };
    
    this.handlers.get(event.type)?.forEach(handler => handler(fullEvent));
    this.handlers.get('*')?.forEach(handler => handler(fullEvent));
  }
}

// 使用示例
const eventBus = new EventBus();

// 订阅工具调用事件
eventBus.subscribe('tool.called', (event) => {
  console.log(`Tool ${event.payload.toolName} called by ${event.source}`);
});

// 发布事件
eventBus.publish({
  type: 'tool.called',
  source: 'client-1',
  payload: { toolName: 'read_file', args: { path: '/test.txt' } }
});
```

#### 资源变更通知
```typescript
class ResourceWatcher {
  private eventBus: EventBus;
  private watchers: Map<string, any> = new Map();
  
  constructor(eventBus: EventBus) {
    this.eventBus = eventBus;
  }
  
  watch(uri: string, client: Client) {
    if (this.watchers.has(uri)) return;
    
    // 订阅资源更新
    client.onnotification('notifications/resources/updated', (params) => {
      if (params.uri === uri) {
        this.eventBus.publish({
          type: 'resource.changed',
          source: 'watcher',
          payload: { uri, changes: params.changes }
        });
      }
    });
    
    this.watchers.set(uri, true);
  }
  
  unwatch(uri: string) {
    this.watchers.delete(uri);
  }
}
```

### 数据同步模式

#### 双向同步
```typescript
interface SyncConfig {
  sourceClient: Client;
  targetClient: Client;
  resourceUri: string;
  interval: number;
  conflictResolution: 'source' | 'target' | 'manual';
}

class ResourceSynchronizer {
  private syncJobs: Map<string, NodeJS.Timeout> = new Map();
  
  startSync(config: SyncConfig): string {
    const jobId = `${config.resourceUri}-${Date.now()}`;
    
    const sync = async () => {
      try {
        const sourceData = await this.readResource(config.sourceClient, config.resourceUri);
        const targetData = await this.readResource(config.targetClient, config.resourceUri);
        
        if (this.hasConflict(sourceData, targetData)) {
          await this.resolveConflict(config, sourceData, targetData);
        } else {
          await this.writeResource(config.targetClient, config.resourceUri, sourceData);
        }
      } catch (error) {
        console.error(`Sync failed for ${config.resourceUri}:`, error);
      }
    };
    
    const intervalId = setInterval(sync, config.interval);
    this.syncJobs.set(jobId, intervalId);
    
    return jobId;
  }
  
  stopSync(jobId: string) {
    const intervalId = this.syncJobs.get(jobId);
    if (intervalId) {
      clearInterval(intervalId);
      this.syncJobs.delete(jobId);
    }
  }
  
  private async readResource(client: Client, uri: string): Promise<any> {
    const result = await client.request({
      method: 'resources/read',
      params: { uri }
    }, ReadResourceResultSchema);
    
    return result.contents[0];
  }
  
  private hasConflict(source: any, target: any): boolean {
    return JSON.stringify(source) !== JSON.stringify(target);
  }
  
  private async resolveConflict(config: SyncConfig, source: any, target: any): Promise<void> {
    switch (config.conflictResolution) {
      case 'source':
        await this.writeResource(config.targetClient, config.resourceUri, source);
        break;
      case 'target':
        await this.writeResource(config.sourceClient, config.resourceUri, target);
        break;
      case 'manual':
        // 触发冲突事件，等待外部处理
        break;
    }
  }
}
```

### 错误传播与恢复

#### 熔断器模式
```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailureTime: Date | null = null;
  private state: 'closed' | 'open' | 'half-open' = 'closed';
  
  constructor(
    private threshold: number = 5,
    private timeout: number = 60000
  ) {}
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailureTime!.getTime() > this.timeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }
    
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }
  
  private onFailure() {
    this.failures++;
    this.lastFailureTime = new Date();
    
    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}
```

#### 重试策略
```typescript
interface RetryConfig {
  maxAttempts: number;
  delay: number;
  backoff: 'fixed' | 'exponential';
  maxDelay: number;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig
): Promise<T> {
  let lastError: Error | null = null;
  let delay = config.delay;
  
  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt < config.maxAttempts) {
        await new Promise(r => setTimeout(r, delay));
        
        if (config.backoff === 'exponential') {
          delay = Math.min(delay * 2, config.maxDelay);
        }
      }
    }
  }
  
  throw lastError;
}
```

### 性能优化

#### 连接池
```typescript
class ConnectionPool {
  private pool: Map<string, Client[]> = new Map();
  private maxConnections: number;
  
  constructor(maxConnections: number = 5) {
    this.maxConnections = maxConnections;
  }
  
  async acquire(serverName: string, factory: () => Promise<Client>): Promise<Client> {
    if (!this.pool.has(serverName)) {
      this.pool.set(serverName, []);
    }
    
    const pool = this.pool.get(serverName)!;
    
    if (pool.length > 0) {
      return pool.pop()!;
    }
    
    return factory();
  }
  
  release(serverName: string, client: Client) {
    const pool = this.pool.get(serverName);
    if (pool && pool.length < this.maxConnections) {
      pool.push(client);
    } else {
      client.close();
    }
  }
}
```

#### 结果缓存
```typescript
class ToolResultCache {
  private cache: Map<string, { result: any; expiry: number }> = new Map();
  private defaultTTL: number;
  
  constructor(defaultTTL: number = 60000) {
    this.defaultTTL = defaultTTL;
  }
  
  private getKey(toolName: string, args: any): string {
    return `${toolName}:${JSON.stringify(args)}`;
  }
  
  get(toolName: string, args: any): any | null {
    const key = this.getKey(toolName, args);
    const entry = this.cache.get(key);
    
    if (entry && entry.expiry > Date.now()) {
      return entry.result;
    }
    
    this.cache.delete(key);
    return null;
  }
  
  set(toolName: string, args: any, result: any, ttl?: number) {
    const key = this.getKey(toolName, args);
    this.cache.set(key, {
      result,
      expiry: Date.now() + (ttl || this.defaultTTL)
    });
  }
  
  invalidate(toolName: string, args?: any) {
    if (args) {
      this.cache.delete(this.getKey(toolName, args));
    } else {
      for (const key of this.cache.keys()) {
        if (key.startsWith(`${toolName}:`)) {
          this.cache.delete(key);
        }
      }
    }
  }
}
```

## Related Skills
- `mcp-client-integration` - MCP 客户端集成
- `mcp-server-development` - MCP 服务器开发
- `error-recovery` - 错误恢复
- `performance-optimizer` - 性能优化
