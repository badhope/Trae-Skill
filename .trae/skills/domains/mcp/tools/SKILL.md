---
name: mcp-tool-creation
description: "MCP tool creation expert for designing, implementing and optimizing MCP tools with best practices. Keywords: mcp, tool, schema, validation, security"
layer: domain
role: specialist
version: 2.0.0
domain: mcp
invoked_by:
  - mcp-server-development
  - coding-workflow
capabilities:
  - tool_design
  - input_schema
  - output_format
  - error_handling
  - security
---

# MCP Tool Creation

MCP 工具创建专家，帮助设计、实现和优化 MCP 工具。

## 适用场景

- 工具设计与架构
- 输入模式定义
- 输出格式规范
- 错误处理策略
- 性能优化
- 安全最佳实践

## 工具设计原则

### 1. 单一职责

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
```

### 2. 清晰的描述

```typescript
const searchTool = {
  name: "search_files",
  description: `Search for files matching a pattern.
    
Use this tool when you need to find files by name or content.
Supports glob patterns and regular expressions.

Limitations:
- Maximum 1000 results
- Searches within allowed directories only`,
};
```

### 3. 完整的输入模式

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
      default: "utf-8"
    }
  },
  required: ["path"],
  additionalProperties: false
}
```

## 输出格式规范

### 文本输出

```typescript
return {
  content: [{
    type: "text",
    text: "File contents here..."
  }]
};
```

### 结构化输出

```typescript
return {
  content: [{
    type: "text",
    text: JSON.stringify({
      success: true,
      data: result,
      metadata: { timestamp: new Date().toISOString() }
    }, null, 2)
  }]
};
```

## 错误处理

```typescript
enum ToolErrorType {
  VALIDATION_ERROR = "validation_error",
  NOT_FOUND = "not_found",
  PERMISSION_DENIED = "permission_denied",
  TIMEOUT = "timeout",
  INTERNAL_ERROR = "internal_error"
}

function createErrorResponse(error: ToolError) {
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
```

## 安全最佳实践

### 输入验证

```typescript
import Ajv from 'ajv';

const ajv = new Ajv({ strict: true });

function validateInput(schema: object, input: unknown) {
  const validate = ajv.compile(schema);
  if (!validate(input)) {
    throw new ToolError(ToolErrorType.VALIDATION_ERROR, "Invalid input", validate.errors);
  }
}
```

### 路径安全

```typescript
import path from 'path';

function sanitizePath(baseDir: string, userPath: string): string {
  const absolutePath = path.resolve(baseDir, userPath);
  if (!absolutePath.startsWith(baseDir)) {
    throw new ToolError(ToolErrorType.PERMISSION_DENIED, "Path traversal detected");
  }
  return absolutePath;
}
```

## 性能优化

### 缓存

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

### 并发控制

```typescript
import pLimit from 'p-limit';

const limit = pLimit(5);

async function processBatch(items: string[]) {
  return Promise.all(items.map(item => limit(() => processItem(item))));
}
```

## 相关技能

- [mcp-server-development](../server-development) - MCP 服务器开发
- [mcp-client-integration](../client-integration) - MCP 客户端集成
- [security-auditor](../../actions/analysis/security-auditor) - 安全审计
