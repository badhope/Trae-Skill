---
name: security-auditor
description: "Security auditing expert for vulnerability identification, risk assessment, and remediation guidance. Keywords: security, audit, vulnerability, xss, sql-injection, authentication"
layer: domain
role: specialist
version: 2.0.0
domain: security
invoked_by:
  - coding-workflow
  - code-review-workflow
capabilities:
  - vulnerability_scanning
  - code_audit
  - authentication_review
  - data_protection
  - compliance_check
---

# Security Auditor

代码安全审计专家。

## 适用场景

- 代码安全审查
- 处理敏感数据
- 认证授权实现
- API安全
- 合规要求

## 常见漏洞

### SQL注入

```typescript
// 危险
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// 安全
const query = 'SELECT * FROM users WHERE id = ?';
await db.query(query, [userId]);
```

### XSS

```typescript
// 危险
element.innerHTML = userInput;

// 安全
element.textContent = userInput;
// 或使用DOMPurify
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 命令注入

```typescript
// 危险
exec(`convert ${filename} output.png`);

// 安全
execFile('convert', [filename, 'output.png']);
```

## 认证安全

### 密码存储

```typescript
import bcrypt from 'bcrypt';

const saltRounds = 12;
const hash = await bcrypt.hash(password, saltRounds);
const valid = await bcrypt.compare(password, hash);
```

### JWT最佳实践

```typescript
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '1h', algorithm: 'HS256' }
);
```

### 限流

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100
});
```

## 安全头

```typescript
import helmet from 'helmet';

app.use(helmet());
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "trusted.cdn.com"]
  }
}));
```

## 相关技能

- [dependency-analyzer](../tools/dependency-analyzer) - 依赖分析
- [api-design](../../actions/code/api-design) - API设计
- [auth-implementation](../auth/auth-implementation) - 认证实现
