# MCP Deployment & Operations

## Description
MCP 部署与运维专家。帮助部署 MCP 服务器到各种环境，包括本地、云端、Docker 容器，以及监控和维护。

## Details

### 功能特性
- 本地部署配置
- 云平台部署 (AWS, GCP, Azure)
- Docker 容器化
- Kubernetes 编排
- 监控与日志
- 自动化运维

### 本地部署

#### 配置文件
```json
// mcp-config.json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/workspace"],
      "env": {
        "NODE_ENV": "production"
      }
    },
    "database": {
      "command": "node",
      "args": ["dist/db-server.js"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

#### Claude Desktop 配置
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
// %APPDATA%\Claude\claude_desktop_config.json (Windows)
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

### Docker 部署

#### Dockerfile
```dockerfile
# Node.js MCP Server
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist ./dist

# 非根用户
RUN addgroup -g 1001 -S mcp && \
    adduser -S mcp -u 1001 -G mcp
USER mcp

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "console.log('healthy')" || exit 1

CMD ["node", "dist/server.js"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    container_name: mcp-server
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=info
    volumes:
      - ./data:/app/data:ro
    networks:
      - mcp-network
    healthcheck:
      test: ["CMD", "node", "-e", "console.log('healthy')"]
      interval: 30s
      timeout: 3s
      retries: 3

  mcp-gateway:
    image: nginx:alpine
    container_name: mcp-gateway
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - mcp-server
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### 云平台部署

#### AWS EC2 部署
```bash
# 1. 创建 EC2 实例
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --count 1 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-12345678

# 2. SSH 连接
ssh -i my-key.pem ec2-user@<public-ip>

# 3. 安装依赖
sudo yum update -y
sudo yum install -y nodejs npm

# 4. 部署应用
git clone <repository>
cd <repository>
npm install
npm run build

# 5. 使用 PM2 管理
sudo npm install -g pm2
pm2 start dist/server.js --name mcp-server
pm2 startup
pm2 save
```

#### AWS ECS 部署
```yaml
# task-definition.json
{
  "family": "mcp-server",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "mcp-server",
      "image": "<account>.dkr.ecr.<region>.amazonaws.com/mcp-server:latest",
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/mcp-server",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### Google Cloud Run
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/mcp-server', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/mcp-server']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'mcp-server'
      - '--image'
      - 'gcr.io/$PROJECT_ID/mcp-server'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
```

### Kubernetes 部署

#### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
  labels:
    app: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: mcp-server:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          exec:
            command:
            - node
            - -e
            - "console.log('healthy')"
          initialDelaySeconds: 10
          periodSeconds: 30
        env:
        - name: NODE_ENV
          value: "production"
        - name: LOG_LEVEL
          value: "info"
```

#### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
spec:
  selector:
    app: mcp-server
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

### 监控与日志

#### Prometheus 指标
```typescript
import client from 'prom-client';

// 创建注册表
const register = new client.Registry();

// 默认指标
client.collectDefaultMetrics({ register });

// 自定义指标
const toolCallsCounter = new client.Counter({
  name: 'mcp_tool_calls_total',
  help: 'Total number of tool calls',
  labelNames: ['tool_name', 'status'],
  registers: [register]
});

const toolDurationHistogram = new client.Histogram({
  name: 'mcp_tool_duration_seconds',
  help: 'Duration of tool calls in seconds',
  labelNames: ['tool_name'],
  buckets: [0.1, 0.5, 1, 2, 5, 10],
  registers: [register]
});

// 在工具调用中使用
async function executeTool(name: string, args: any) {
  const end = toolDurationHistogram.startTimer({ tool_name: name });
  try {
    const result = await doExecute(name, args);
    toolCallsCounter.inc({ tool_name: name, status: 'success' });
    return result;
  } catch (error) {
    toolCallsCounter.inc({ tool_name: name, status: 'error' });
    throw error;
  } finally {
    end();
  }
}

// 暴露指标端点
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

#### 结构化日志
```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: { colorize: true }
  }
});

// 使用示例
logger.info({ tool: 'read_file', path: '/test.txt' }, 'Tool called');
logger.error({ error: err.message, stack: err.stack }, 'Tool failed');
```

### 健康检查

```typescript
// 健康检查端点
app.get('/health', async (req, res) => {
  const checks = {
    server: true,
    database: await checkDatabase(),
    filesystem: await checkFilesystem()
  };
  
  const healthy = Object.values(checks).every(v => v === true);
  
  res.status(healthy ? 200 : 503).json({
    status: healthy ? 'healthy' : 'unhealthy',
    checks,
    timestamp: new Date().toISOString()
  });
});

// 就绪检查端点
app.get('/ready', async (req, res) => {
  const ready = await isReady();
  res.status(ready ? 200 : 503).json({
    ready,
    timestamp: new Date().toISOString()
  });
});
```

### 自动扩展

```yaml
# Kubernetes HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mcp-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mcp-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 备份与恢复

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/mcp-server"

# 备份配置
cp -r /app/config "$BACKUP_DIR/config_$DATE"

# 备份数据
pg_dump $DATABASE_URL > "$BACKUP_DIR/db_$DATE.sql"

# 压缩
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$BACKUP_DIR/config_$DATE" "$BACKUP_DIR/db_$DATE.sql"

# 清理旧备份
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete
```

### 运维清单

#### 部署前检查
- [ ] 代码已通过测试
- [ ] 依赖已锁定
- [ ] 环境变量已配置
- [ ] 密钥已安全存储
- [ ] 监控已配置

#### 部署后验证
- [ ] 服务健康检查通过
- [ ] 工具调用正常
- [ ] 日志正常输出
- [ ] 指标正常收集
- [ ] 告警规则生效

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `docker-containerization` - Docker 容器化
- `kubernetes-orchestration` - Kubernetes 编排
- `observability-monitoring` - 可观测性监控
