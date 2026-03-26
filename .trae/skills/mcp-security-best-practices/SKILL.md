# MCP Security Best Practices

## Description
MCP 安全最佳实践专家。帮助设计和实现安全的 MCP 服务器和客户端，包括认证、授权、输入验证和安全配置。

## Details

### 功能特性
- 身份认证机制
- 权限授权控制
- 输入验证与清理
- 敏感数据保护
- 安全配置指南
- 安全审计检查

### 认证机制

#### API Key 认证
```typescript
import crypto from 'crypto';

interface ApiKeyConfig {
  headerName: string;
  prefix: string;
  hashAlgorithm: string;
}

class ApiKeyAuth {
  private validKeys: Set<string>;
  
  constructor(keys: string[], private config: ApiKeyConfig = {
    headerName: 'X-API-Key',
    prefix: 'Bearer ',
    hashAlgorithm: 'sha256'
  }) {
    this.validKeys = new Set(keys.map(k => this.hash(k)));
  }
  
  private hash(key: string): string {
    return crypto.createHash(this.config.hashAlgorithm).update(key).digest('hex');
  }
  
  validate(authHeader: string | undefined): boolean {
    if (!authHeader) return false;
    
    const key = authHeader.replace(this.config.prefix, '');
    return this.validKeys.has(this.hash(key));
  }
}

// 使用示例
const auth = new ApiKeyAuth([process.env.MCP_API_KEY!]);

server.use((req, res, next) => {
  if (!auth.validate(req.headers['authorization'])) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
});
```

#### JWT 认证
```typescript
import jwt from 'jsonwebtoken';

interface JWTPayload {
  sub: string;
  permissions: string[];
  exp: number;
}

class JWTAuth {
  constructor(
    private secret: string,
    private options: jwt.VerifyOptions = {}
  ) {}
  
  verify(token: string): JWTPayload | null {
    try {
      return jwt.verify(token, this.secret, this.options) as JWTPayload;
    } catch {
      return null;
    }
  }
  
  hasPermission(payload: JWTPayload, permission: string): boolean {
    return payload.permissions.includes(permission);
  }
}

// 使用示例
const jwtAuth = new JWTAuth(process.env.JWT_SECRET!, {
  algorithms: ['HS256'],
  issuer: 'mcp-server'
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const token = request.headers?.authorization?.replace('Bearer ', '');
  const payload = jwtAuth.verify(token || '');
  
  if (!payload) {
    return { isError: true, content: [{ type: 'text', text: 'Unauthorized' }] };
  }
  
  // 检查权限
  if (!jwtAuth.hasPermission(payload, 'tools:execute')) {
    return { isError: true, content: [{ type: 'text', text: 'Forbidden' }] };
  }
  
  // 执行工具
  return executeTool(request.params.name, request.params.arguments);
});
```

### 授权控制

#### 基于角色的访问控制 (RBAC)
```typescript
interface Role {
  name: string;
  permissions: Permission[];
}

interface Permission {
  resource: string;
  actions: ('read' | 'write' | 'execute')[];
}

class RBAC {
  private roles: Map<string, Role> = new Map();
  
  addRole(role: Role) {
    this.roles.set(role.name, role);
  }
  
  hasPermission(roleName: string, resource: string, action: string): boolean {
    const role = this.roles.get(roleName);
    if (!role) return false;
    
    return role.permissions.some(
      p => p.resource === resource && p.actions.includes(action as any)
    );
  }
}

// 配置角色
const rbac = new RBAC();

rbac.addRole({
  name: 'admin',
  permissions: [
    { resource: '*', actions: ['read', 'write', 'execute'] }
  ]
});

rbac.addRole({
  name: 'developer',
  permissions: [
    { resource: 'tools', actions: ['read', 'execute'] },
    { resource: 'resources', actions: ['read'] }
  ]
});

rbac.addRole({
  name: 'readonly',
  permissions: [
    { resource: 'resources', actions: ['read'] }
  ]
});
```

#### 工具级别授权
```typescript
interface ToolPermission {
  toolName: string;
  requiredPermissions: string[];
}

const toolPermissions: Map<string, ToolPermission> = new Map([
  ['read_file', { toolName: 'read_file', requiredPermissions: ['files:read'] }],
  ['write_file', { toolName: 'write_file', requiredPermissions: ['files:write'] }],
  ['execute_command', { toolName: 'execute_command', requiredPermissions: ['commands:execute'] }]
]);

async function checkToolPermission(
  userPermissions: string[],
  toolName: string
): Promise<boolean> {
  const perm = toolPermissions.get(toolName);
  if (!perm) return false;
  
  return perm.requiredPermissions.every(p => userPermissions.includes(p));
}
```

### 输入验证

#### Schema 验证
```typescript
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv({ strict: true, allErrors: true });
addFormats(ajv);

// 工具输入 Schema
const toolSchemas: Map<string, object> = new Map([
  ['read_file', {
    type: 'object',
    properties: {
      path: {
        type: 'string',
        format: 'path',
        pattern: '^/([a-zA-Z0-9_\\-./]+)$',
        maxLength: 4096
      },
      encoding: {
        type: 'string',
        enum: ['utf-8', 'binary'],
        default: 'utf-8'
      }
    },
    required: ['path'],
    additionalProperties: false
  }]
]);

function validateInput(toolName: string, input: unknown): { valid: boolean; errors?: string[] } {
  const schema = toolSchemas.get(toolName);
  if (!schema) {
    return { valid: false, errors: ['Unknown tool'] };
  }
  
  const validate = ajv.compile(schema);
  const valid = validate(input);
  
  if (!valid) {
    return {
      valid: false,
      errors: validate.errors?.map(e => `${e.instancePath} ${e.message}`)
    };
  }
  
  return { valid: true };
}
```

#### 路径安全验证
```typescript
import path from 'path';

class PathValidator {
  private allowedRoots: string[];
  private deniedPatterns: RegExp[];
  
  constructor(config: {
    allowedRoots: string[];
    deniedPatterns?: string[];
  }) {
    this.allowedRoots = config.allowedRoots.map(p => path.resolve(p));
    this.deniedPatterns = (config.deniedPatterns || [
      '\\.\\.',           // 路径遍历
      '\\.env',           // 环境文件
      '\\.git',           // Git 目录
      'node_modules',     // Node 模块
      '\\.ssh',           // SSH 密钥
      '\\.aws',           // AWS 凭证
      'credentials',      // 凭证文件
      'secrets?'          // 密钥文件
    ]).map(p => new RegExp(p, 'i'));
  }
  
  validate(userPath: string): { valid: boolean; resolvedPath?: string; error?: string } {
    // 解析绝对路径
    const resolvedPath = path.resolve(userPath);
    
    // 检查是否在允许的根目录下
    const isAllowed = this.allowedRoots.some(root => 
      resolvedPath.startsWith(root + path.sep) || resolvedPath === root
    );
    
    if (!isAllowed) {
      return { valid: false, error: 'Path outside allowed directories' };
    }
    
    // 检查是否匹配拒绝模式
    for (const pattern of this.deniedPatterns) {
      if (pattern.test(resolvedPath)) {
        return { valid: false, error: 'Path matches denied pattern' };
      }
    }
    
    return { valid: true, resolvedPath };
  }
}

// 使用示例
const pathValidator = new PathValidator({
  allowedRoots: ['/app/workspace', '/app/data'],
  deniedPatterns: ['\\.\\.', '\\.env', '\\.git']
});

const result = pathValidator.validate(userInput.path);
if (!result.valid) {
  return { isError: true, content: [{ type: 'text', text: result.error! }] };
}
```

### 敏感数据保护

#### 数据脱敏
```typescript
interface SensitiveField {
  pattern: RegExp;
  replacement: string;
}

const sensitivePatterns: SensitiveField[] = [
  { pattern: /password["']?\s*[:=]\s*["'][^"']+["']/gi, replacement: 'password: "[REDACTED]"' },
  { pattern: /api[_-]?key["']?\s*[:=]\s*["'][^"']+["']/gi, replacement: 'api_key: "[REDACTED]"' },
  { pattern: /token["']?\s*[:=]\s*["'][^"']+["']/gi, replacement: 'token: "[REDACTED]"' },
  { pattern: /secret["']?\s*[:=]\s*["'][^"']+["']/gi, replacement: 'secret: "[REDACTED]"' },
  { pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, replacement: '[EMAIL]' },
  { pattern: /\b\d{16,19}\b/g, replacement: '[CARD]' }
];

function sanitizeOutput(output: string): string {
  let sanitized = output;
  for (const { pattern, replacement } of sensitivePatterns) {
    sanitized = sanitized.replace(pattern, replacement);
  }
  return sanitized;
}
```

#### 环境变量安全
```typescript
// 安全加载环境变量
import dotenv from 'dotenv';

dotenv.config();

// 验证必需的环境变量
const requiredEnvVars = [
  'MCP_API_KEY',
  'DATABASE_URL'
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

// 敏感环境变量不应暴露
const sensitiveEnvVars = [
  'MCP_API_KEY',
  'DATABASE_URL',
  'JWT_SECRET',
  'AWS_SECRET_ACCESS_KEY'
];

function filterEnvForLogging(env: NodeJS.ProcessEnv): Record<string, string> {
  const filtered: Record<string, string> = {};
  for (const [key, value] of Object.entries(env)) {
    filtered[key] = sensitiveEnvVars.includes(key) ? '[REDACTED]' : value || '';
  }
  return filtered;
}
```

### 安全配置

#### 安全 Headers
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:'],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      frameAncestors: ["'none'"]
    }
  },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: { policy: 'same-origin' },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  noSniff: true,
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' }
}));
```

#### 速率限制
```typescript
import rateLimit from 'express-rate-limit';

// 全局速率限制
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 分钟
  max: 100,                   // 每个 IP 最多 100 请求
  message: { error: 'Too many requests' },
  standardHeaders: true,
  legacyHeaders: false
});

// 工具调用速率限制
const toolLimiter = rateLimit({
  windowMs: 60 * 1000,        // 1 分钟
  max: 30,                     // 每个 IP 最多 30 次工具调用
  keyGenerator: (req) => {
    return req.headers['x-api-key'] as string || req.ip;
  }
});

app.use('/tools', toolLimiter);
```

### 安全审计

#### 审计日志
```typescript
interface AuditLog {
  timestamp: Date;
  userId: string;
  action: string;
  resource: string;
  result: 'success' | 'failure';
  ipAddress: string;
  userAgent: string;
  details?: any;
}

class AuditLogger {
  private logs: AuditLog[] = [];
  
  log(entry: Omit<AuditLog, 'timestamp'>) {
    this.logs.push({
      ...entry,
      timestamp: new Date()
    });
    
    // 发送到外部日志系统
    this.sendToLogSystem(this.logs[this.logs.length - 1]);
  }
  
  private async sendToLogSystem(log: AuditLog) {
    // 发送到 SIEM 或日志聚合系统
  }
  
  getLogs(filter?: Partial<AuditLog>): AuditLog[] {
    if (!filter) return this.logs;
    
    return this.logs.filter(log => {
      return Object.entries(filter).every(([key, value]) => 
        log[key as keyof AuditLog] === value
      );
    });
  }
}
```

#### 安全检查清单
```markdown
## MCP 安全检查清单

### 认证
- [ ] 所有端点都需要认证
- [ ] API Key 安全存储
- [ ] JWT 使用强密钥
- [ ] 会话超时配置

### 授权
- [ ] 实施最小权限原则
- [ ] 工具级别权限控制
- [ ] 资源访问控制
- [ ] 定期权限审计

### 输入验证
- [ ] 所有输入都经过验证
- [ ] 路径遍历防护
- [ ] SQL 注入防护
- [ ] XSS 防护

### 数据保护
- [ ] 敏感数据加密
- [ ] 日志脱敏
- [ ] 安全的密钥管理
- [ ] 数据备份加密

### 网络安全
- [ ] HTTPS 强制
- [ ] 安全 Headers
- [ ] 速率限制
- [ ] CORS 配置

### 监控
- [ ] 审计日志
- [ ] 异常检测
- [ ] 安全告警
- [ ] 定期安全扫描
```

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `security-auditor` - 安全审计
- `secret-management` - 密钥管理
- `api-design` - API 设计
