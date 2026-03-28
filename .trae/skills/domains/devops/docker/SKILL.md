---
name: docker
description: "Docker containerization for application deployment and development. Keywords: docker, container, image, compose, kubernetes, 容器"
layer: domain
role: specialist
version: 2.0.0
domain: devops
languages:
  - dockerfile
  - yaml
frameworks:
  - docker
  - docker-compose
invoked_by:
  - coding-workflow
  - ci-cd-pipeline
capabilities:
  - container_creation
  - image_optimization
  - compose_orchestration
  - multi_stage_builds
  - development_environment
---

# Docker

Docker容器化专家，专注于应用部署、镜像优化和开发环境配置。

## 适用场景

- 应用容器化
- 开发环境标准化
- 微服务部署
- CI/CD流水线
- 多环境一致性

## 核心架构

### 1. Dockerfile最佳实践

```dockerfile
# 多阶段构建 - Node.js应用
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:20-alpine AS runner

WORKDIR /app

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodejs

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

USER nodejs

EXPOSE 3000

ENV NODE_ENV=production
ENV PORT=3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]

# Python应用
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Go应用
FROM golang:1.21-alpine AS builder

WORKDIR /app

RUN apk add --no-cache git

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

COPY --from=builder /app/main .
COPY --from=builder /app/config ./config

EXPOSE 8080

ENV TZ=Asia/Shanghai

CMD ["./main"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runner
      args:
        NODE_ENV: production
    container_name: myapp
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:password@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  postgres:
    image: postgres:15-alpine
    container_name: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

### 3. 开发环境配置

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: myapp-dev
    ports:
      - "3000:3000"
      - "9229:9229"
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev
    networks:
      - dev-network

  postgres:
    image: postgres:15-alpine
    container_name: postgres-dev
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: devdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data
    networks:
      - dev-network

  redis:
    image: redis:7-alpine
    container_name: redis-dev
    ports:
      - "6379:6379"
    networks:
      - dev-network

  adminer:
    image: adminer
    container_name: adminer
    ports:
      - "8080:8080"
    networks:
      - dev-network

networks:
  dev-network:
    driver: bridge

volumes:
  postgres_dev_data:
```

### 4. Docker管理脚本

```bash
#!/bin/bash

set -e

COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="myapp"

build() {
    echo "Building images..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
}

up() {
    echo "Starting services..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d
}

down() {
    echo "Stopping services..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
}

logs() {
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f $@
}

ps() {
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME ps
}

clean() {
    echo "Cleaning up..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down -v --rmi local
    docker system prune -f
}

backup() {
    echo "Backing up database..."
    docker exec postgres pg_dump -U user mydb > backup_$(date +%Y%m%d_%H%M%S).sql
}

restore() {
    if [ -z "$1" ]; then
        echo "Usage: $0 restore <backup_file>"
        exit 1
    fi
    echo "Restoring database..."
    cat $1 | docker exec -i postgres psql -U user mydb
}

case "$1" in
    build) build ;;
    up) up ;;
    down) down ;;
    logs) logs ${@:2} ;;
    ps) ps ;;
    clean) clean ;;
    backup) backup ;;
    restore) restore $2 ;;
    *) echo "Usage: $0 {build|up|down|logs|ps|clean|backup|restore}" ;;
esac
```

### 5. 镜像优化

```bash
# 构建优化镜像
docker build --squash -t myapp:optimized .

# 分析镜像层
docker history myapp:latest

# 查看镜像大小
docker images myapp

# 多平台构建
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:multiarch .

# 安全扫描
docker scout cves myapp:latest

# 清理未使用资源
docker system prune -a --volumes
```

## 最佳实践

1. **多阶段构建**: 减小镜像体积
2. **最小化基础镜像**: 使用alpine
3. **非root用户**: 安全运行容器
4. **健康检查**: 配置健康检查
5. **资源限制**: 设置CPU和内存限制
6. **日志管理**: 配置日志轮转

## 相关技能

- [ci-cd-pipeline](../ci-cd-pipeline) - CI/CD流水线
- [kubernetes](../kubernetes) - Kubernetes编排
- [backend-nodejs](../../backend/nodejs) - Node.js后端
