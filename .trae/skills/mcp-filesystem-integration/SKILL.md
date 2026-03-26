# MCP Filesystem Integration

## Description
MCP 文件系统集成专家。帮助实现安全的文件系统访问，包括文件读写、目录操作、文件监视等功能。

## Details

### 功能特性
- 安全文件读写
- 目录浏览与管理
- 文件监视与通知
- 权限控制
- 大文件处理
- 文件搜索

### 基础配置

#### Claude Desktop 配置
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/workspace",
        "/Users/username/projects"
      ]
    }
  }
}
```

#### 自定义服务器实现
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import fs from "fs/promises";
import path from "path";

const ALLOWED_DIRECTORIES = [
  "/Users/username/workspace",
  "/Users/username/projects"
];

const server = new Server(
  { name: "filesystem-server", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);
```

### 工具实现

#### 读取文件
```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "read_file",
      description: "Read the contents of a file",
      inputSchema: {
        type: "object",
        properties: {
          path: {
            type: "string",
            description: "Absolute path to the file"
          },
          encoding: {
            type: "string",
            enum: ["utf-8", "binary"],
            default: "utf-8"
          }
        },
        required: ["path"]
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "read_file") {
    const { path: filePath, encoding = "utf-8" } = request.params.arguments;
    
    // 安全验证
    const validation = validatePath(filePath);
    if (!validation.valid) {
      return {
        isError: true,
        content: [{ type: "text", text: validation.error! }]
      };
    }
    
    try {
      // 检查文件大小
      const stats = await fs.stat(validation.resolvedPath!);
      if (stats.size > 10 * 1024 * 1024) {
        return {
          isError: true,
          content: [{ type: "text", text: `File too large: ${stats.size} bytes` }]
        };
      }
      
      // 读取文件
      if (encoding === "binary") {
        const content = await fs.readFile(validation.resolvedPath!);
        return {
          content: [{
            type: "text",
            text: content.toString("base64")
          }]
        };
      } else {
        const content = await fs.readFile(validation.resolvedPath!, "utf-8");
        return {
          content: [{ type: "text", text: content }]
        };
      }
    } catch (error: any) {
      return {
        isError: true,
        content: [{ type: "text", text: `Error reading file: ${error.message}` }]
      };
    }
  }
});
```

#### 写入文件
```typescript
{
  name: "write_file",
  description: "Write content to a file",
  inputSchema: {
    type: "object",
    properties: {
      path: {
        type: "string",
        description: "Absolute path to the file"
      },
      content: {
        type: "string",
        description: "Content to write"
      },
      mode: {
        type: "string",
        enum: ["write", "append"],
        default: "write"
      }
    },
    required: ["path", "content"]
  }
}

// 实现
async function writeFile(filePath: string, content: string, mode: string = "write") {
  const validation = validatePath(filePath);
  if (!validation.valid) {
    throw new Error(validation.error);
  }
  
  // 确保目录存在
  const dir = path.dirname(validation.resolvedPath!);
  await fs.mkdir(dir, { recursive: true });
  
  // 写入文件
  if (mode === "append") {
    await fs.appendFile(validation.resolvedPath!, content, "utf-8");
  } else {
    await fs.writeFile(validation.resolvedPath!, content, "utf-8");
  }
  
  return { success: true, path: validation.resolvedPath };
}
```

#### 列出目录
```typescript
{
  name: "list_directory",
  description: "List contents of a directory",
  inputSchema: {
    type: "object",
    properties: {
      path: {
        type: "string",
        description: "Absolute path to the directory"
      },
      recursive: {
        type: "boolean",
        default: false
      }
    },
    required: ["path"]
  }
}

// 实现
async function listDirectory(dirPath: string, recursive: boolean = false): Promise<any[]> {
  const validation = validatePath(dirPath);
  if (!validation.valid) {
    throw new Error(validation.error);
  }
  
  const entries = await fs.readdir(validation.resolvedPath!, { withFileTypes: true });
  
  const result = await Promise.all(entries.map(async (entry) => {
    const entryPath = path.join(validation.resolvedPath!, entry.name);
    const stats = await fs.stat(entryPath);
    
    const item: any = {
      name: entry.name,
      path: entryPath,
      type: entry.isDirectory() ? "directory" : "file",
      size: stats.size,
      modified: stats.mtime
    };
    
    if (recursive && entry.isDirectory()) {
      item.children = await listDirectory(entryPath, true);
    }
    
    return item;
  }));
  
  return result;
}
```

#### 搜索文件
```typescript
{
  name: "search_files",
  description: "Search for files matching a pattern",
  inputSchema: {
    type: "object",
    properties: {
      path: {
        type: "string",
        description: "Base directory to search"
      },
      pattern: {
        type: "string",
        description: "Glob pattern or regex"
      },
      type: {
        type: "string",
        enum: ["glob", "regex", "name"],
        default: "glob"
      }
    },
    required: ["path", "pattern"]
  }
}

// 实现
import { glob } from "glob";

async function searchFiles(basePath: string, pattern: string, type: string = "glob"): Promise<string[]> {
  const validation = validatePath(basePath);
  if (!validation.valid) {
    throw new Error(validation.error);
  }
  
  let matches: string[] = [];
  
  if (type === "glob") {
    matches = await glob(pattern, {
      cwd: validation.resolvedPath,
      absolute: true,
      nodir: true
    });
  } else if (type === "regex") {
    const regex = new RegExp(pattern, "i");
    const allFiles = await glob("**/*", {
      cwd: validation.resolvedPath,
      absolute: true,
      nodir: true
    });
    matches = allFiles.filter(f => regex.test(path.basename(f)));
  } else {
    const allFiles = await glob("**/*", {
      cwd: validation.resolvedPath,
      absolute: true,
      nodir: true
    });
    matches = allFiles.filter(f => path.basename(f).includes(pattern));
  }
  
  // 过滤只返回允许路径内的文件
  return matches.filter(f => isPathAllowed(f));
}
```

### 资源暴露

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const resources = [];
  
  for (const dir of ALLOWED_DIRECTORIES) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      resources.push({
        uri: `file://${path.join(dir, entry.name)}`,
        name: entry.name,
        mimeType: entry.isDirectory() 
          ? "application/x-directory" 
          : getMimeType(entry.name)
      });
    }
  }
  
  return { resources };
});

server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [
    {
      uriTemplate: "file://{path}",
      name: "File by Path",
      description: "Access any file within allowed directories",
      mimeType: "application/octet-stream"
    }
  ]
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const filePath = uri.replace("file://", "");
  
  const validation = validatePath(filePath);
  if (!validation.valid) {
    throw new Error(validation.error);
  }
  
  const content = await fs.readFile(validation.resolvedPath!);
  const mimeType = getMimeType(validation.resolvedPath!);
  
  return {
    contents: [{
      uri,
      mimeType,
      ...(isTextFile(mimeType)
        ? { text: content.toString("utf-8") }
        : { blob: content.toString("base64") }
      )
    }]
  };
});
```

### 文件监视

```typescript
import chokidar from "chokidar";

class FileWatcher {
  private watchers: Map<string, chokidar.FSWatcher> = new Map();
  private subscriptions: Map<string, Set<string>> = new Map();
  
  subscribe(clientId: string, filePath: string) {
    if (!this.watchers.has(filePath)) {
      const watcher = chokidar.watch(filePath, {
        persistent: true,
        ignoreInitial: true
      });
      
      watcher.on("change", (path) => {
        this.notifySubscribers(path);
      });
      
      watcher.on("add", (path) => {
        this.notifySubscribers(path, "created");
      });
      
      watcher.on("unlink", (path) => {
        this.notifySubscribers(path, "deleted");
      });
      
      this.watchers.set(filePath, watcher);
    }
    
    if (!this.subscriptions.has(filePath)) {
      this.subscriptions.set(filePath, new Set());
    }
    this.subscriptions.get(filePath)!.add(clientId);
  }
  
  unsubscribe(clientId: string, filePath: string) {
    this.subscriptions.get(filePath)?.delete(clientId);
    
    if (this.subscriptions.get(filePath)?.size === 0) {
      this.watchers.get(filePath)?.close();
      this.watchers.delete(filePath);
      this.subscriptions.delete(filePath);
    }
  }
  
  private notifySubscribers(filePath: string, event: string = "modified") {
    server.notification({
      method: "notifications/resources/updated",
      params: {
        uri: `file://${filePath}`,
        event
      }
    });
  }
}
```

### 路径安全验证

```typescript
class PathValidator {
  private allowedRoots: string[];
  private deniedPatterns: RegExp[];
  
  constructor(allowedRoots: string[]) {
    this.allowedRoots = allowedRoots.map(p => path.resolve(p));
    this.deniedPatterns = [
      /\.\./,                    // 路径遍历
      /\.env/i,                  // 环境文件
      /\.git/i,                  // Git 目录
      /\.ssh/i,                  // SSH 密钥
      /\.aws/i,                  // AWS 凭证
      /credentials/i,            // 凭证文件
      /secrets?/i,               // 密钥文件
      /\.pem$/i,                 // 证书文件
      /\.key$/i                  // 密钥文件
    ];
  }
  
  validate(userPath: string): { valid: boolean; resolvedPath?: string; error?: string } {
    try {
      // 解析绝对路径
      const resolvedPath = path.resolve(userPath);
      
      // 检查路径遍历
      if (userPath.includes("..")) {
        return { valid: false, error: "Path traversal detected" };
      }
      
      // 检查是否在允许的根目录下
      const isAllowed = this.allowedRoots.some(root =>
        resolvedPath.startsWith(root + path.sep) || resolvedPath === root
      );
      
      if (!isAllowed) {
        return { valid: false, error: "Path outside allowed directories" };
      }
      
      // 检查拒绝模式
      for (const pattern of this.deniedPatterns) {
        if (pattern.test(resolvedPath)) {
          return { valid: false, error: "Access to this path is denied" };
        }
      }
      
      return { valid: true, resolvedPath };
    } catch (error) {
      return { valid: false, error: "Invalid path format" };
    }
  }
}

const pathValidator = new PathValidator(ALLOWED_DIRECTORIES);

function validatePath(userPath: string) {
  return pathValidator.validate(userPath);
}
```

### MIME 类型识别

```typescript
import mime from "mime-types";

function getMimeType(filePath: string): string {
  const mimeType = mime.lookup(filePath);
  return mimeType || "application/octet-stream";
}

function isTextFile(mimeType: string): boolean {
  const textMimes = [
    "text/",
    "application/json",
    "application/xml",
    "application/javascript",
    "application/typescript",
    "application/x-yaml"
  ];
  
  return textMimes.some(m => mimeType.startsWith(m) || mimeType === m);
}
```

### 最佳实践

1. **最小权限原则**: 只授予必要的目录访问权限
2. **路径验证**: 始终验证用户提供的路径
3. **大小限制**: 限制可读取的文件大小
4. **日志记录**: 记录所有文件操作
5. **错误处理**: 提供清晰的错误信息
6. **并发控制**: 处理并发文件访问

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `mcp-security-best-practices` - MCP 安全最佳实践
- `document-processor` - 文档处理
