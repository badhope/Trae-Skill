# MCP Error Handling

## Description
MCP 错误处理专家。帮助设计和实现健壮的 MCP 错误处理机制，包括错误分类、恢复策略和日志记录。

## Details

### 功能特性
- 错误分类与映射
- 错误恢复策略
- 重试机制
- 优雅降级
- 错误日志记录
- 错误通知

### 错误类型

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
  ContentTooLarge = -32900,
  
  // 工具错误
  ToolNotFound = -33001,
  ToolExecutionError = -33002,
  ToolTimeout = -33003,
  
  // 资源错误
  ResourceNotFound = -34001,
  ResourceAccessDenied = -34002,
  ResourceTooLarge = -34003
}

class MCPError extends Error {
  constructor(
    public code: MCPErrorCode,
    message: string,
    public data?: any
  ) {
    super(message);
    this.name = "MCPError";
  }
  
  toJSON() {
    return {
      code: this.code,
      message: this.message,
      data: this.data
    };
  }
}
```

### 错误处理器

```typescript
class ErrorHandler {
  private handlers: Map<MCPErrorCode, (error: MCPError) => any> = new Map();
  private fallbackHandler: (error: Error) => any;
  
  constructor() {
    this.setupDefaultHandlers();
  }
  
  private setupDefaultHandlers() {
    this.handlers.set(MCPErrorCode.ParseError, (error) => ({
      isError: true,
      content: [{ type: "text", text: "Failed to parse request. Please check the format." }]
    }));
    
    this.handlers.set(MCPErrorCode.InvalidParams, (error) => ({
      isError: true,
      content: [{ type: "text", text: `Invalid parameters: ${error.message}` }]
    }));
    
    this.handlers.set(MCPErrorCode.ToolNotFound, (error) => ({
      isError: true,
      content: [{ type: "text", text: `Tool not found: ${error.data?.toolName}` }]
    }));
    
    this.handlers.set(MCPErrorCode.ToolExecutionError, (error) => ({
      isError: true,
      content: [{ type: "text", text: `Tool execution failed: ${error.message}` }]
    }));
    
    this.handlers.set(MCPErrorCode.ToolTimeout, (error) => ({
      isError: true,
      content: [{ type: "text", text: `Tool execution timed out after ${error.data?.timeout}ms` }]
    }));
    
    this.fallbackHandler = (error) => ({
      isError: true,
      content: [{ type: "text", text: `An unexpected error occurred: ${error.message}` }]
    });
  }
  
  register(code: MCPErrorCode, handler: (error: MCPError) => any) {
    this.handlers.set(code, handler);
  }
  
  handle(error: Error): any {
    if (error instanceof MCPError) {
      const handler = this.handlers.get(error.code);
      if (handler) {
        return handler(error);
      }
    }
    
    return this.fallbackHandler(error);
  }
}
```

### 重试机制

```typescript
interface RetryConfig {
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
  backoffFactor: number;
  retryableErrors: MCPErrorCode[];
}

class RetryManager {
  private defaultConfig: RetryConfig = {
    maxAttempts: 3,
    initialDelay: 1000,
    maxDelay: 30000,
    backoffFactor: 2,
    retryableErrors: [
      MCPErrorCode.InternalError,
      MCPErrorCode.ToolTimeout
    ]
  };
  
  async execute<T>(
    fn: () => Promise<T>,
    config: Partial<RetryConfig> = {}
  ): Promise<T> {
    const cfg = { ...this.defaultConfig, ...config };
    let lastError: Error | null = null;
    let delay = cfg.initialDelay;
    
    for (let attempt = 1; attempt <= cfg.maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error: any) {
        lastError = error;
        
        if (!this.shouldRetry(error, cfg.retryableErrors)) {
          throw error;
        }
        
        if (attempt < cfg.maxAttempts) {
          await this.sleep(delay);
          delay = Math.min(delay * cfg.backoffFactor, cfg.maxDelay);
        }
      }
    }
    
    throw lastError;
  }
  
  private shouldRetry(error: any, retryableErrors: MCPErrorCode[]): boolean {
    if (error instanceof MCPError) {
      return retryableErrors.includes(error.code);
    }
    return false;
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### 优雅降级

```typescript
class GracefulDegradation {
  private fallbacks: Map<string, () => Promise<any>> = new Map();
  
  register(toolName: string, fallback: () => Promise<any>) {
    this.fallbacks.set(toolName, fallback);
  }
  
  async executeWithFallback(
    toolName: string,
    primary: () => Promise<any>
  ): Promise<any> {
    try {
      return await primary();
    } catch (error) {
      const fallback = this.fallbacks.get(toolName);
      if (fallback) {
        console.warn(`Primary execution failed, using fallback for ${toolName}`);
        return await fallback();
      }
      throw error;
    }
  }
}

// 使用示例
const degradation = new GracefulDegradation();

degradation.register("search_web", async () => ({
  content: [{ type: "text", text: "Web search is temporarily unavailable. Please try again later." }]
}));

degradation.register("read_database", async () => ({
  content: [{ type: "text", text: "Database is currently offline. Using cached data." }]
}));
```

### 错误日志

```typescript
interface ErrorLog {
  timestamp: Date;
  errorCode: MCPErrorCode;
  message: string;
  stack?: string;
  context: {
    toolName?: string;
    params?: any;
    sessionId?: string;
  };
}

class ErrorLogger {
  private logs: ErrorLog[] = [];
  private maxLogs: number = 1000;
  
  log(error: Error, context: ErrorLog["context"] = {}) {
    const entry: ErrorLog = {
      timestamp: new Date(),
      errorCode: error instanceof MCPError ? error.code : MCPErrorCode.UnknownErrorCode,
      message: error.message,
      stack: error.stack,
      context
    };
    
    this.logs.push(entry);
    
    // 限制日志数量
    if (this.logs.length > this.maxLogs) {
      this.logs = this.logs.slice(-this.maxLogs);
    }
    
    // 输出到控制台
    console.error(`[${entry.timestamp.toISOString()}] Error ${entry.errorCode}: ${entry.message}`);
    
    // 发送到外部日志系统
    this.sendToExternal(entry);
  }
  
  private async sendToExternal(entry: ErrorLog) {
    // 发送到日志聚合系统
  }
  
  getRecent(count: number = 10): ErrorLog[] {
    return this.logs.slice(-count);
  }
  
  getByCode(code: MCPErrorCode): ErrorLog[] {
    return this.logs.filter(log => log.errorCode === code);
  }
  
  getStats(): Record<number, number> {
    const stats: Record<number, number> = {};
    for (const log of this.logs) {
      stats[log.errorCode] = (stats[log.errorCode] || 0) + 1;
    }
    return stats;
  }
}
```

### 错误通知

```typescript
class ErrorNotifier {
  private subscribers: Map<string, (error: ErrorLog) => void> = new Map();
  
  subscribe(id: string, handler: (error: ErrorLog) => void) {
    this.subscribers.set(id, handler);
  }
  
  unsubscribe(id: string) {
    this.subscribers.delete(id);
  }
  
  notify(error: ErrorLog) {
    for (const handler of this.subscribers.values()) {
      try {
        handler(error);
      } catch (e) {
        console.error("Error in notification handler:", e);
      }
    }
  }
}

// MCP 通知
server.notification({
  method: "notifications/error",
  params: {
    code: MCPErrorCode.ToolExecutionError,
    message: "Tool execution failed",
    timestamp: new Date().toISOString()
  }
});
```

### 验证错误

```typescript
import Ajv from "ajv";

class ValidationError extends MCPError {
  constructor(errors: Ajv.ErrorObject[]) {
    super(
      MCPErrorCode.InvalidParams,
      "Validation failed",
      { errors: errors.map(e => ({
        path: e.instancePath,
        message: e.message,
        params: e.params
      }))}
    );
  }
}

function validateOrThrow(schema: object, data: unknown) {
  const ajv = new Ajv({ allErrors: true });
  const validate = ajv.compile(schema);
  
  if (!validate(data)) {
    throw new ValidationError(validate.errors!);
  }
}
```

### 工具错误处理

```typescript
async function safeToolExecution(
  toolName: string,
  params: any,
  handler: (params: any) => Promise<any>
): Promise<any> {
  const errorHandler = new ErrorHandler();
  const retryManager = new RetryManager();
  
  try {
    return await retryManager.execute(
      () => handler(params),
      { maxAttempts: 3 }
    );
  } catch (error: any) {
    errorLogger.log(error, { toolName, params });
    return errorHandler.handle(error);
  }
}

// 使用示例
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  return safeToolExecution(name, args, async (params) => {
    switch (name) {
      case "read_file":
        return await readFile(params.path);
      case "write_file":
        return await writeFile(params.path, params.content);
      default:
        throw new MCPError(MCPErrorCode.ToolNotFound, `Unknown tool: ${name}`, { toolName: name });
    }
  });
});
```

### 最佳实践

1. **明确错误类型**: 使用具体的错误代码
2. **提供有用信息**: 错误消息应包含修复建议
3. **记录上下文**: 记录错误发生时的上下文信息
4. **优雅降级**: 提供备用方案
5. **监控告警**: 对关键错误设置告警

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `error-recovery` - 错误恢复
- `mcp-debugging-testing` - MCP 调试与测试
