---
id: skill-security-main-v1
name: Security Engineering
summary: 安全编码、漏洞防护与安全架构设计指南
type: skill
category: security
tags: [security, vulnerability, encryption, authentication, authorization,渗透测试]
keywords: [安全, 漏洞, 加密, 身份验证, 授权, 渗透测试]
intent: 提供安全编码实践、漏洞防护措施和安全架构设计的完整指导
use_cases:
  - 需要进行安全审计时
  - 需要修复安全漏洞时
  - 需要设计安全架构时
  - 需要实现加密功能时
inputs:
  - name: task_type
    type: string
    required: true
    description: 安全任务类型
  - name: code_or_architecture
    type: string
    required: true
    description: 代码或架构描述
outputs:
  - name: analysis
    type: markdown
    description: 安全分析报告
  - name: recommendations
    type: array
    description: 安全建议
prerequisites:
  - 了解基本安全概念
  - 熟悉目标编程语言
steps:
  - step: 1
    action: 识别安全需求和威胁模型
  - step: 2
    action: 分析代码或架构
  - step: 3
    action: 识别潜在漏洞
  - step: 4
    action: 提供修复建议
examples:
  - input: "task_type: code_review, language: python, code: SQL query with string concatenation"
    output: "SQL injection vulnerability identified with parameterized query fix"
    notes: 展示安全代码审查
related_skills:
  - skill-coding-v1
  - skill-coding-code-review-v1
related_prompts:
  - prompt-task-security-scan-for-vulnerabilities
  - prompt-task-security-design-authentication-system
  - prompt-task-security-implement-encryption
notes: |
  重要原则：
  - 安全是纵深防御
  - 最小权限原则
  - 默认安全
  - 防御优先于检测
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
deprecated: false
---

# Security Engineering Skill

安全编码、漏洞防护与安全架构设计的完整指南。

## OWASP Top 10 漏洞

### 1. SQL注入

```python
# ❌ 危险: 字符串拼接
def get_user_unsafe(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

# ✅ 安全: 参数化查询
def get_user_safe(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

# ✅ 更安全: 使用ORM
def get_user_orm(user_id):
    return User.query.filter_by(id=user_id).first()
```

### 2. 跨站脚本(XSS)

```javascript
// ❌ 危险: 直接输出用户输入
app.get('/profile', (req, res) => {
    res.send(`<h1>Welcome ${req.query.name}</h1>`);
});

// ✅ 安全: HTML转义
const escapeHtml = (str) => {
    return str.replace(/[&<>"']/g, (c) => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[c]));
};

app.get('/profile', (req, res) => {
    res.send(`<h1>Welcome ${escapeHtml(req.query.name)}</h1>`);
});

// ✅ 更好: 使用模板引擎
app.set('view engine', 'ejs');
app.get('/profile', (req, res) => {
    res.render('profile', { name: req.query.name }); // 自动转义
});
```

### 3. 敏感数据泄露

```python
# ❌ 危险: 硬编码密钥
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgresql://user:password@localhost/db"

// ✅ 安全: 使用环境变量
import os
API_KEY = os.environ.get('API_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

# ✅ 更好: 使用密钥管理服务
from keyring import get_password
API_KEY = get_password('myapp', 'api_key')
```

### 4. 不安全的认证

```python
# ❌ 危险: 简单密码比较
def authenticate_unsafe(username, password):
    user = db.get_user(username)
    return user.password == password  # 时间常量比较

# ✅ 安全: 使用bcrypt
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def authenticate_safe(username, password):
    user = db.get_user(username)
    if not user:
        return False
    return verify_password(password, user.password_hash)

# ✅ 使用JWT
import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.environ.get('JWT_SECRET')

def create_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None  # Token过期
```

### 5. 访问控制失效

```python
# ❌ 危险: 缺少权限检查
@app.route('/admin/delete_user')
def delete_user():
    # 任何人都可以删除用户！
    user_id = request.args.get('id')
    db.delete_user(user_id)
    return "User deleted"

// ✅ 安全: 检查权限
from functools import wraps

def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)  # Forbidden
            return f(*args, **kwargs)
        return decorated
    return decorator

@app.route('/admin/delete_user')
@login_required
@require_permission('user:delete')
def delete_user():
    user_id = request.args.get('id')
    db.delete_user(user_id)
    return "User deleted"
```

## 加密最佳实践

### 对称加密 (AES)

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class AESCipher:
    def __init__(self, key):
        self.key = key  # 必须是16, 24, 或 32字节
    
    def encrypt(self, plaintext):
        # 生成随机IV
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # PKCS7填充
        padded = self._pad(plaintext)
        ciphertext = cipher.encrypt(padded)
        
        # 返回 IV + 密文
        return base64.b64encode(iv + ciphertext).decode()
    
    def decrypt(self, encrypted):
        data = base64.b64decode(encrypted)
        iv = data[:AES.block_size]
        ciphertext = data[AES.block_size:]
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded = cipher.decrypt(ciphertext)
        
        return self._unpad(padded).decode()
    
    def _pad(self, data):
        padding = AES.block_size - len(data) % AES.block_size
        return data + bytes([padding] * padding)
    
    def _unpad(self, data):
        return data[:-data[-1]]

# 使用示例
key = get_random_bytes(32)  # 256位密钥
cipher = AESCipher(key)

encrypted = cipher.encrypt("Sensitive data")
decrypted = cipher.decrypt(encrypted)
```

### 非对称加密 (RSA)

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# 生成密钥对
def generate_rsa_keypair(bits=2048):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# 加密 (使用公钥)
def encrypt_with_public(public_key_pem, data):
    key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = cipher.encrypt(data.encode())
    return base64.b64encode(ciphertext).decode()

# 解密 (使用私钥)
def decrypt_with_private(private_key_pem, encrypted_data):
    key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(key)
    ciphertext = base64.b64decode(encrypted_data)
    return cipher.decrypt(ciphertext).decode()

# 签名和验签
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def sign_data(private_key_pem, data):
    key = RSA.import_key(private_key_pem)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return base64.b64encode(signature).decode()

def verify_signature(public_key_pem, data, signature):
    key = RSA.import_key(public_key_pem)
    h = SHA256.new(data.encode())
    try:
        pkcs1_15.new(key).verify(h, base64.b64decode(signature))
        return True
    except ValueError:
        return False
```

## 安全架构设计

### 零信任架构

```markdown
## 零信任核心原则

```
用户 ──► 身份提供商 ──► 设备验证 ──► 策略引擎 ──► 资源访问
                  │              │              │
                  ▼              ▼              ▼
              MFA验证      设备健康检查    最小权限
```

### 实施要点

1. **永不信任，始终验证**
   - 所有请求都要认证和授权
   - 不基于网络位置授予信任

2. **最小权限原则**
   - 只授予完成任务所需的最小权限
   - 定期审查和清理权限

3. **微分段**
   - 网络划分为细粒度段
   - 段间通信需要显式授权

4. **持续监控**
   - 实时安全事件监控
   - 异常行为检测
```

### 安全开发生命周期

```markdown
## SDL流程

┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   设计   │───►│   开发   │───►│   测试   │───►│   部署   │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │                                                 │
     ▼                                                 ▼
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 威胁建模 │    │ 代码审计 │    │ 渗透测试 │    │ 监控响应 │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

## 渗透测试清单

### 信息收集

```markdown
## 侦察阶段

### 被动信息收集
- [ ] DNS查询
- [ ] WHOIS查询
- [ ] 子域名枚举
- [ ] 公开数据泄露检查
- [ ] 技术栈识别

### 主动信息收集
- [ ] 端口扫描 (nmap)
- [ ] 服务指纹识别
- [ ] 目录扫描
- [ ] 参数发现
```

### 漏洞利用

```markdown
## 常见漏洞测试

### Web应用
- [ ] SQL注入
- [ ] XSS (反射/存储/DOM)
- [ ] CSRF
- [ ] SSRF
- [ ] 文件上传
- [ ] 认证缺陷

### API
- [ ] 对象级授权缺失
- [ ] 认证绕过
- [ ] 过度数据暴露
- [ ] 缺乏速率限制
- [ ] 注入漏洞

### 云配置
- [ ] S3 bucket权限
- [ ] IAM角色过度权限
- [ ] 公开数据库
- [ ] 密钥泄露
```

## 安全监控与响应

### SIEM集成

```python
# 安全事件日志格式
SECURITY_EVENT_SCHEMA = {
    "timestamp": "ISO8601",
    "event_type": "authentication|authorization|access|data",
    "severity": "low|medium|high|critical",
    "source_ip": "ip_address",
    "user_id": "user_identifier",
    "resource": "affected_resource",
    "action": "action_taken",
    "result": "success|failure",
    "metadata": {}
}

# 关键事件
CRITICAL_EVENTS = [
    "failed_login_attempts > 5",
    "privilege_escalation",
    "sensitive_data_access",
    "config_change",
    "new_user_creation",
    "api_key_generated"
]
```

### 应急响应流程

```markdown
## 事件响应流程

### 1. 检测 (Detect)
- 识别异常行为
- 验证告警真实性

### 2. 分析 (Analyze)
- 确定事件范围
- 评估影响程度
- 保留证据

### 3. 遏制 (Contain)
- 隔离受影响系统
- 阻止横向移动
- 保护关键资产

### 4. 根除 (Eradicate)
- 移除威胁
- 修复漏洞
- 加强防御

### 5. 恢复 (Recover)
- 系统恢复
- 验证完整性
- 恢复服务

### 6. 复盘 (Lessons)
- 事件总结
- 改进措施
- 更新流程
```

## 安全编码检查清单

### 输入验证

- [ ] 验证所有输入数据
- [ ] 使用白名单验证
- [ ] 验证数据类型和范围
- [ ] 验证长度限制
- [ ] 转义输出

### 认证与会话

- [ ] 使用强密码策略
- [ ] 实现多因素认证
- [ ] 安全会话管理
- [ ] 令牌有过期时间
- [ ] 防止会话固定攻击

### 加密

- [ ] 使用现代加密算法
- [ ] 密钥安全管理
- [ ] 敏感数据加密存储
- [ ] TLS用于传输
- [ ] 安全的随机数生成

### 日志与监控

- [ ] 记录安全事件
- [ ] 保护日志完整性
- [ ] 实时监控告警
- [ ] 定期安全审计
