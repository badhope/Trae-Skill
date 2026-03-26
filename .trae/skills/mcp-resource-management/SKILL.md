# MCP Resource Management

## Description
MCP 资源管理专家。帮助设计、实现和管理 MCP 资源，包括静态资源、动态资源和资源订阅。

## Details

### 功能特性
- 资源定义与暴露
- 资源模板设计
- 资源订阅与通知
- 资源缓存策略
- 大文件处理
- 资源安全控制

### 资源类型

#### 1. 静态资源
预定义的固定资源，URI 不会改变。

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: "config:///app.json",
      name: "Application Configuration",
      description: "Main application configuration file",
      mimeType: "application/json"
    },
    {
      uri: "docs:///readme.md",
      name: "README",
      mimeType: "text/markdown"
    }
  ]
}));
```

#### 2. 动态资源
通过模板生成的资源，支持参数化访问。

```typescript
server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [
    {
      uriTemplate: "file:///{path}",
      name: "File by Path",
      description: "Access any file by its path",
      mimeType: "application/octet-stream"
    },
    {
      uriTemplate: "db:///{table}/{id}",
      name: "Database Record",
      mimeType: "application/json"
    }
  ]
}));
```

### 资源读取实现

#### 基础读取
```typescript
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  
  // 解析 URI
  const parsed = parseUri(uri);
  
  // 读取资源
  const content = await readResourceContent(parsed);
  
  return {
    contents: [{
      uri,
      mimeType: content.mimeType,
      text: content.text,  // 文本内容
      // 或 blob: content.blob  // 二进制内容
    }]
  };
});
```

#### 文件系统资源
```typescript
async function handleFileResource(uri: string) {
  const path = uri.replace("file:///", "/");
  
  // 安全检查
  if (!isPathAllowed(path)) {
    throw new Error("Access denied");
  }
  
  const stats = await fs.stat(path);
  const mimeType = getMimeType(path);
  
  // 大文件处理
  if (stats.size > 10 * 1024 * 1024) {
    return {
      contents: [{
        uri,
        mimeType,
        text: `[File too large: ${formatSize(stats.size)}]`
      }]
    };
  }
  
  const content = await fs.readFile(path);
  
  return {
    contents: [{
      uri,
      mimeType,
      ...(isTextFile(mimeType) 
        ? { text: content.toString('utf-8') }
        : { blob: content.toString('base64') }
      )
    }]
  };
}
```

#### 数据库资源
```typescript
async function handleDatabaseResource(uri: string) {
  const match = uri.match(/db:\/\/([^/]+)\/([^/]+)/);
  if (!match) throw new Error("Invalid database URI");
  
  const [, table, id] = match;
  
  const record = await db.query(
    `SELECT * FROM ${table} WHERE id = $1`,
    [id]
  );
  
  if (!record) {
    throw new Error("Record not found");
  }
  
  return {
    contents: [{
      uri,
      mimeType: "application/json",
      text: JSON.stringify(record, null, 2)
    }]
  };
}
```

### 资源订阅

#### 实现订阅
```typescript
const subscriptions = new Map<string, Set<string>>();  // uri -> clientIds
const watchers = new Map<string, FSWatcher>();         // path -> watcher

server.setRequestHandler(SubscribeResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const clientId = request.clientId;
  
  // 添加订阅
  if (!subscriptions.has(uri)) {
    subscriptions.set(uri, new Set());
  }
  subscriptions.get(uri)!.add(clientId);
  
  // 设置文件监视
  if (!watchers.has(uri)) {
    const path = uriToPath(uri);
    const watcher = fs.watch(path, (eventType) => {
      if (eventType === 'change') {
        notifyResourceUpdated(uri);
      }
    });
    watchers.set(uri, watcher);
  }
  
  return {};
});

server.setRequestHandler(UnsubscribeResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const clientId = request.clientId;
  
  subscriptions.get(uri)?.delete(clientId);
  
  // 如果没有订阅者，关闭监视器
  if (subscriptions.get(uri)?.size === 0) {
    watchers.get(uri)?.close();
    watchers.delete(uri);
    subscriptions.delete(uri);
  }
  
  return {};
});
```

#### 发送更新通知
```typescript
function notifyResourceUpdated(uri: string) {
  server.notification({
    method: "notifications/resources/updated",
    params: { uri }
  });
}
```

### 资源缓存

#### 缓存策略
```typescript
interface CacheEntry {
  content: ResourceContents;
  etag: string;
  lastModified: Date;
  maxAge: number;
}

class ResourceCache {
  private cache = new Map<string, CacheEntry>();
  
  async get(uri: string, ifNoneMatch?: string): Promise<CacheEntry | null> {
    const entry = this.cache.get(uri);
    
    if (!entry) return null;
    
    // 检查过期
    if (Date.now() > entry.lastModified.getTime() + entry.maxAge * 1000) {
      this.cache.delete(uri);
      return null;
    }
    
    // 检查 ETag
    if (ifNoneMatch === entry.etag) {
      return null;  // 未修改
    }
    
    return entry;
  }
  
  set(uri: string, content: ResourceContents, maxAge: number = 300) {
    this.cache.set(uri, {
      content,
      etag: generateETag(content),
      lastModified: new Date(),
      maxAge
    });
  }
  
  invalidate(uri: string) {
    this.cache.delete(uri);
  }
}
```

#### 条件读取
```typescript
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const ifNoneMatch = request.headers?.['if-none-match'];
  
  // 检查缓存
  const cached = await cache.get(uri, ifNoneMatch);
  if (cached === null && ifNoneMatch) {
    return { contents: [] };  // 304 Not Modified
  }
  
  if (cached) {
    return { contents: [cached.content] };
  }
  
  // 读取新内容
  const content = await readResource(uri);
  cache.set(uri, content);
  
  return { contents: [content] };
});
```

### 大文件处理

#### 分块读取
```typescript
interface ChunkedResource {
  totalSize: number;
  chunkSize: number;
  chunks: number;
}

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const range = request.headers?.range;
  
  const stats = await getResourceStats(uri);
  
  // 大于 10MB 的文件需要分块
  if (stats.size > 10 * 1024 * 1024 && !range) {
    return {
      contents: [{
        uri,
        mimeType: "application/json",
        text: JSON.stringify({
          type: "chunked",
          totalSize: stats.size,
          chunkSize: 1024 * 1024,  // 1MB chunks
          chunks: Math.ceil(stats.size / (1024 * 1024))
        })
      }]
    };
  }
  
  // 处理范围请求
  if (range) {
    const [start, end] = parseRange(range, stats.size);
    const chunk = await readChunk(uri, start, end);
    
    return {
      contents: [{
        uri,
        mimeType: stats.mimeType,
        blob: chunk.toString('base64'),
        range: { start, end, total: stats.size }
      }]
    };
  }
  
  // 普通读取
  const content = await readResource(uri);
  return { contents: [content] };
});
```

### 资源列表

#### 分页支持
```typescript
server.setRequestHandler(ListResourcesRequestSchema, async (request) => {
  const { cursor, limit = 100 } = request.params || {};
  
  const allResources = await listAllResources();
  
  let startIndex = 0;
  if (cursor) {
    startIndex = parseInt(Buffer.from(cursor, 'base64').toString());
  }
  
  const resources = allResources.slice(startIndex, startIndex + limit);
  const nextCursor = startIndex + limit < allResources.length
    ? Buffer.from(String(startIndex + limit)).toString('base64')
    : undefined;
  
  return {
    resources,
    nextCursor
  };
});
```

### 安全控制

#### 访问控制
```typescript
class ResourceAccessControl {
  private allowedPaths: string[];
  private deniedPatterns: RegExp[];
  
  constructor(config: {
    allowedPaths: string[];
    deniedPatterns: string[];
  }) {
    this.allowedPaths = config.allowedPaths;
    this.deniedPatterns = config.deniedPatterns.map(p => new RegExp(p));
  }
  
  canAccess(uri: string): boolean {
    const path = uriToPath(uri);
    
    // 检查是否在允许路径内
    const isAllowed = this.allowedPaths.some(
      allowed => path.startsWith(allowed)
    );
    if (!isAllowed) return false;
    
    // 检查是否匹配拒绝模式
    const isDenied = this.deniedPatterns.some(
      pattern => pattern.test(path)
    );
    if (isDenied) return false;
    
    return true;
  }
}
```

#### 敏感信息过滤
```typescript
function sanitizeContent(content: string, mimeType: string): string {
  if (mimeType !== "application/json") return content;
  
  const data = JSON.parse(content);
  
  // 过滤敏感字段
  const sensitiveFields = ['password', 'token', 'secret', 'apiKey'];
  
  function redact(obj: any): any {
    if (typeof obj !== 'object') return obj;
    
    const result = Array.isArray(obj) ? [] : {};
    
    for (const [key, value] of Object.entries(obj)) {
      if (sensitiveFields.some(f => key.toLowerCase().includes(f))) {
        result[key] = '[REDACTED]';
      } else {
        result[key] = redact(value);
      }
    }
    
    return result;
  }
  
  return JSON.stringify(redact(data), null, 2);
}
```

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `mcp-tool-creation` - MCP 工具创建
- `security-auditor` - 安全审计
- `document-processor` - 文档处理
