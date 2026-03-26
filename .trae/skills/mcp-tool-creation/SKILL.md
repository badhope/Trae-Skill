# MCP Tool Creation

## Description
MCP 工具创建专家。帮助设计、实现和优化 MCP 工具，确保工具具有良好的可用性、安全性和性能。

## Details

### 功能特性
- 工具设计与架构
- 输入模式定义
- 输出格式规范
- 错误处理策略
- 性能优化
- 安全最佳实践

### 工具设计原则

#### 1. 单一职责
每个工具应该只做一件事，并且做好它。

```typescript
// 好的设计 - 单一职责
const readFileTool = {
  name: "read_file",
  description: "Read the contents of a file",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string", description: "File path" }
    },
    required: ["path"]
  }
};

// 不好的设计 - 职责过多
const fileTool = {
  name: "file_operations",
  description: "Read, write, or delete files",
  // ... 混合了多种操作
};
```

#### 2. 清晰的描述
工具描述应该清楚地说明：
- 工具做什么
- 什么时候使用
- 有什么限制

```typescript
const searchTool = {
  name: "search_files",
  description: `Search for files matching a pattern.
    
Use this tool when you need to find files by name or content.
Supports glob patterns and regular expressions.

Limitations:
- Maximum 1000 results
- Searches within allowed directories only`,
  // ...
};
```

#### 3. 完整的输入模式

```typescript
inputSchema: {
  type: "object",
  properties: {
    path: {
      type: "string",
      description: "Absolute path to the file",
      pattern: "^/([a-zA-Z0-9_-]+/)*[a-zA-Z0-9_-]+$"
    },
    encoding: {
      type: "string",
      enum: ["utf-8", "utf-16", "binary"],
      default: "utf-8",
      description: "Character encoding for text files"
    },
    maxSize: {
      type: "integer",
      minimum: 1,
      maximum: 10485760,  // 10MB
      default: 1048576,   // 1MB
      description: "Maximum file size in bytes"
    }
  },
  required: ["path"],
  additionalProperties: false
}
```

### 工具实现模式

#### 基础工具
```typescript
async function executeTool(name: string, args: Record<string, any>) {
  switch (name) {
    case "read_file":
      return await readFile(args.path, args.encoding);
    case "write_file":
      return await writeFile(args.path, args.content);
    case "list_directory":
      return await listDirectory(args.path);
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
```

#### 流式工具
```typescript
// 对于长时间运行的操作，使用进度通知
async function executeLongRunningTool(name: string, args: any, progress: (msg: string) => void) {
  progress("Starting operation...");
  
  const items = await getItems(args);
  const results = [];
  
  for (let i = 0; i < items.length; i++) {
    progress(`Processing item ${i + 1}/${items.length}`);
    results.push(await processItem(items[i]));
  }
  
  progress("Operation complete");
  return results;
}
```

#### 批量工具
```typescript
const batchReadTool = {
  name: "batch_read_files",
  description: "Read multiple files in a single operation",
  inputSchema: {
    type: "object",
    properties: {
      paths: {
        type: "array",
        items: { type: "string" },
        maxItems: 100,
        description: "Array of file paths to read"
      }
    },
    required: ["paths"]
  }
};

async function executeBatchRead(paths: string[]) {
  const results = await Promise.allSettled(
    paths.map(path => readFile(path))
  );
  
  return results.map((result, index) => ({
    path: paths[index],
    status: result.status,
    content: result.status === 'fulfilled' ? result.value : null,
    error: result.status === 'rejected' ? result.reason.message : null
  }));
}
```

### 输出格式规范

#### 文本输出
```typescript
return {
  content: [{
    type: "text",
    text: "File contents here..."
  }]
};
```

#### 结构化输出
```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({
      success: true,
      data: result,
      metadata: {
        timestamp: new Date().toISOString(),
        duration: elapsed
      }
    }, null, 2)
  }]
};
```

#### 多部分输出
```typescript
return {
  content: [
    { type: "text", text: "# Summary\n\nOperation completed successfully." },
    { type: "text", text: "```json\n" + JSON.stringify(data) + "\n```" },
    { type: "image", data: imageBase64, mimeType: "image/png" }
  ]
};
```

### 错误处理

#### 错误类型
```typescript
enum ToolErrorType {
  VALIDATION_ERROR = "validation_error",
  NOT_FOUND = "not_found",
  PERMISSION_DENIED = "permission_denied",
  TIMEOUT = "timeout",
  INTERNAL_ERROR = "internal_error"
}

class ToolError extends Error {
  constructor(
    public type: ToolErrorType,
    message: string,
    public details?: any
  ) {
    super(message);
  }
}
```

#### 错误响应
```typescript
function createErrorResponse(error: Error) {
  if (error instanceof ToolError) {
    return {
      isError: true,
      content: [{
        type: "text",
        text: JSON.stringify({
          error: error.type,
          message: error.message,
          details: error.details
        })
      }]
    };
  }
  
  return {
    isError: true,
    content: [{
      type: "text",
      text: JSON.stringify({
        error: "internal_error",
        message: "An unexpected error occurred"
      })
    }]
  };
}
```

### 安全最佳实践

#### 输入验证
```typescript
import Ajv from 'ajv';

const ajv = new Ajv({ strict: true });

function validateInput(schema: object, input: unknown) {
  const validate = ajv.compile(schema);
  if (!validate(input)) {
    throw new ToolError(
      ToolErrorType.VALIDATION_ERROR,
      "Invalid input",
      validate.errors
    );
  }
}
```

#### 路径安全
```typescript
import path from 'path';

function sanitizePath(baseDir: string, userPath: string): string {
  const absolutePath = path.resolve(baseDir, userPath);
  
  if (!absolutePath.startsWith(baseDir)) {
    throw new ToolError(
      ToolErrorType.PERMISSION_DENIED,
      "Path traversal detected"
    );
  }
  
  return absolutePath;
}
```

#### 速率限制
```typescript
class RateLimiter {
  private requests: Map<string, number[]> = new Map();
  
  constructor(
    private maxRequests: number,
    private windowMs: number
  ) {}
  
  check(key: string): boolean {
    const now = Date.now();
    const requests = this.requests.get(key) || [];
    const recent = requests.filter(t => t > now - this.windowMs);
    
    if (recent.length >= this.maxRequests) {
      return false;
    }
    
    recent.push(now);
    this.requests.set(key, recent);
    return true;
  }
}
```

### 性能优化

#### 缓存
```typescript
const cache = new Map<string, { value: any; expiry: number }>();

async function cachedOperation(key: string, fn: () => Promise<any>, ttlMs: number) {
  const cached = cache.get(key);
  if (cached && cached.expiry > Date.now()) {
    return cached.value;
  }
  
  const value = await fn();
  cache.set(key, { value, expiry: Date.now() + ttlMs });
  return value;
}
```

#### 并发控制
```typescript
import pLimit from 'p-limit';

const limit = pLimit(5);  // 最大并发数

async function processBatch(items: string[]) {
  return Promise.all(
    items.map(item => limit(() => processItem(item)))
  );
}
```

### 工具测试

```typescript
describe('read_file tool', () => {
  it('should read a file successfully', async () => {
    const result = await executeTool('read_file', {
      path: '/test/file.txt'
    });
    
    expect(result.isError).toBeUndefined();
    expect(result.content[0].type).toBe('text');
  });
  
  it('should fail for non-existent file', async () => {
    const result = await executeTool('read_file', {
      path: '/nonexistent.txt'
    });
    
    expect(result.isError).toBe(true);
  });
  
  it('should reject path traversal', async () => {
    const result = await executeTool('read_file', {
      path: '../../../etc/passwd'
    });
    
    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain('permission');
  });
});
```

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `mcp-client-integration` - MCP 客户端集成
- `api-design` - API 设计
- `security-auditor` - 安全审计
