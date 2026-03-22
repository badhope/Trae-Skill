---
id: skill-devops-main-v1
name: DevOps Engineering
summary: DevOps实践、CI/CD流水线与基础设施自动化指南
type: skill
category: devops
tags: [devops, ci-cd, infrastructure, docker, kubernetes, terraform, ansible]
keywords: [DevOps, 持续集成, Docker, Kubernetes, Terraform, Ansible]
intent: 提供DevOps实践、自动化部署和基础设施即代码的完整指导
use_cases:
  - 需要搭建CI/CD流水线时
  - 需要实现容器化部署时
  - 需要编写基础设施代码时
inputs:
  - name: task_type
    type: string
    required: true
    description: 任务类型
  - name: project_context
    type: object
    required: false
    description: 项目上下文
outputs:
  - name: config
    type: code
    description: 配置文件
  - name: pipeline
    type: code
    description: 流水线代码
prerequisites:
  - 了解Linux基础
  - 了解版本控制
steps:
  - step: 1
    action: 评估项目需求和环境
  - step: 2
    action: 设计CI/CD流程
  - step: 3
    action: 编写配置文件
  - step: 4
    action: 实现自动化
examples:
  - input: "task_type: ci_cd, language: python, platform: github_actions"
    output: "complete GitHub Actions workflow for Python project"
    notes: 展示Python项目CI/CD配置
related_skills:
  - skill-coding-v1
  - skill-security-main-v1
related_prompts:
  - prompt-task-devops-design-ci-cd-pipeline
  - prompt-task-devops-configure-docker
  - prompt-task-devops-setup-kubernetes
notes: |
  关键原则：
  - 自动化一切
  - 基础设施即代码
  - 监控和日志
  - 快速恢复
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
deprecated: false
---

# DevOps Engineering Skill

DevOps实践、CI/CD流水线与基础设施自动化的完整指南。

## CI/CD流水线

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'

jobs:
  lint:
    name: Code Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black isort
          pip install -r requirements.txt
      
      - name: Run flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      
      - name: Run black
        run: |
          black --check .
      
      - name: Run isort
        run: |
          isort --check-only .

  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Run tests with coverage
        run: |
          pytest --cov=. --cov-report=xml --cov-report=html
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  build:
    name: Build & Push
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    environment: production
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.PROD_HOST }}
          username: deploy
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /app
            docker-compose pull
            docker-compose up -d
            docker-compose exec -T app python manage.py migrate
            docker-compose exec -T app python manage.py collectstatic --noinput
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

lint:
  stage: lint
  image: python:3.11
  before_script:
    - pip install flake8 black isort
  script:
    - flake8 . --count --select=E9,F63,F7,F82
    - black --check .
    - isort --check-only .
  only:
    - merge_requests
    - main

test:
  stage: test
  image: python:3.11
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgresql://test:test@postgres:5432/test
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - pytest --cov=. --cov-report=xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main

deploy_production:
  stage: deploy
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add -
  script:
    - ssh -o StrictHostKeyChecking=no $PROD_USER@$PROD_HOST "
      cd /app &&
      docker-compose pull &&
      docker-compose up -d &&
      docker-compose exec -T app python manage.py migrate
    "
  environment:
    name: production
    url: https://example.com
  only:
    - main
```

## Docker容器化

### Dockerfile最佳实践

```dockerfile
# 多阶段构建示例
# 阶段1: 构建
FROM python:3.11-slim as builder

WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装依赖到独立目录
RUN pip install --user --no-cache-dir -r requirements.txt

# 阶段2: 运行
FROM python:3.11-slim

# 创建非root用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# 复制Python包
COPY --from=builder /root/.local /home/appuser/.local

# 复制应用代码
COPY --chown=appuser:appgroup . .

# 设置环境变量
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 切换用户
USER appuser

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    image: myapp:latest
    container_name: myapp
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://cache:6379/0
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - backend

  db:
    image: postgres:15-alpine
    container_name: myapp_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - backend

  cache:
    image: redis:7-alpine
    container_name: myapp_cache
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    networks:
      - backend

  nginx:
    image: nginx:alpine
    container_name: myapp_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - static_volume:/app/static
    depends_on:
      - app
    restart: unless-stopped
    networks:
      - backend

volumes:
  postgres_data:
  redis_data:
  static_volume:

networks:
  backend:
    driver: bridge
```

## Kubernetes部署

### Deployment配置

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      serviceAccountName: myapp
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: myapp
          image: myapp:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 8000
              name: http
          envFrom:
            - secretRef:
                name: myapp-secrets
            - configMapRef:
                name: myapp-config
          resources:
            requests:
              cpu: "100m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 10"]
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - myapp
                topologyKey: kubernetes.io/hostname
```

### Service配置

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  labels:
    app: myapp
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
      name: http
  selector:
    app: myapp
---
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
  labels:
    app: myapp
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
      name: http
    - port: 443
      targetPort: 8000
      protocol: TCP
      name: https
  selector:
    app: myapp
```

### HPA配置

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Pods
          value: 1
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Pods
          value: 2
          periodSeconds: 15
```

## Terraform基础设施

### 主配置

```terraform
# main.tf
terraform {
  required_version = ">= 1.5"
  
  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt = true
  }
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# VPC模块
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  
  name = "myapp-vpc"
  cidr = var.vpc_cidr
  
  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs
  
  enable_nat_gateway = true
  single_nat_gateway = false
  
  tags = {
    Name = "myapp-vpc"
  }
}

# EKS集群
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = "myapp-cluster"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    general = {
      min_size       = 2
      max_size       = 10
      desired_size   = 3
      instance_types = ["t3.medium"]
      
      labels = {
        node-group = "general"
      }
    }
    
    compute = {
      min_size       = 1
      max_size       = 5
      desired_size   = 1
      instance_types = ["t3.large"]
      
      labels = {
        node-group = "compute"
      }
      
      taints = [{
        key    = "workload"
        value  = "compute"
        effect = "NO_SCHEDULE"
      }]
    }
  }
  
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }
}

# RDS数据库
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"
  
  identifier = "myapp-db"
  
  engine            = "postgres"
  engine_version    = "15.4"
  family            = "postgres15"
  instance_class    = "db.t3.medium"
  
  allocated_storage     = 100
  max_allocated_storage = 500
  
  db_name  = var.database_name
  username = var.database_username
  password = var.database_password
  
  vpc_security_group_ids = [module.security_group.security_group_id]
  subnet_ids            = module.vpc.database_subnets
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "mon:04:00-mon:05:00"
  
  deletion_protection = var.environment == "prod" ? true : false
}
```

### 变量和输出

```terraform
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

# outputs.tf
output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "database_endpoint" {
  description = "RDS database endpoint"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}
```

## Ansible配置

### Playbook示例

```yaml
# ansible/playbooks/deploy.yml
---
- name: Deploy Application
  hosts: app_servers
  become: yes
  vars:
    app_path: /opt/myapp
    app_user: myapp
    app_version: "{{ deploy_version }}"

  tasks:
    - name: Ensure application user exists
      user:
        name: "{{ app_user }}"
        system: yes
        shell: /bin/bash
        home: "{{ app_path }}"

    - name: Create application directories
      file:
        path: "{{ item }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
        mode: '0755'
      loop:
        - "{{ app_path }}"
        - "{{ app_path }}/config"
        - "{{ app_path }}/logs"

    - name: Stop application service
      systemd:
        name: myapp
        state: stopped

    - name: Deploy application code
      git:
        repo: "{{ git_repo }}"
        version: "{{ app_version }}"
        dest: "{{ app_path }}/current"
        force: yes
        umask: '0022'
      notify: Restart application

    - name: Create symbolic link
      file:
        src: "{{ app_path }}/current"
        dest: "{{ app_path }}/code"
        state: link

    - name: Install Python dependencies
      pip:
        requirements: "{{ app_path }}/code/requirements.txt"
        virtualenv: "{{ app_path }}/venv"
        virtualenv_command: python3 -m venv

    - name: Run database migrations
      django_migrate:
        project_path: "{{ app_path }}/code"
        settings: settings.production
        pythonpath: "{{ app_path }}/code"
      environment:
        DATABASE_URL: "{{ db_url }}"
      when: migrate | bool

    - name: Collect static files
      django_collectstatic:
        project_path: "{{ app_path }}/code"
        settings: settings.production
        pythonpath: "{{ app_path }}/code"
        noinput: yes
      environment:
        DATABASE_URL: "{{ db_url }}"
      when: collectstatic | bool

    - name: Start application service
      systemd:
        name: myapp
        state: started
        enabled: yes

  handlers:
    - name: Restart application
      systemd:
        name: myapp
        state: restarted
        daemon_reload: yes
```

### 角色结构

```
ansible/
├── roles/
│   ├── common/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   └── templates/
│   │       └── sysctl.conf.j2
│   ├── app/
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   │   └── myapp.service.j2
│   │   └── vars/
│   │       └── main.yml
│   └── nginx/
│       ├── tasks/
│       │   └── main.yml
│       └── templates/
│           └── nginx.conf.j2
├── inventory/
│   ├── production/
│   │   └── hosts.yml
│   └── staging/
│       └── hosts.yml
├── playbooks/
│   ├── site.yml
│   ├── production.yml
│   └── staging.yml
└── ansible.cfg
```

## 监控和日志

### Prometheus + Grafana

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - "alerts/*.yml"

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['myapp:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'postgres_exporter'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

### ELK日志配置

```yaml
# docker-compose.monitoring.yml
version: '3.9'

services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  logstash:
    image: logstash:8.11.0
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    ports:
      - "5044:5044"
    environment:
      - "LS_JAVA_OPTS=-Xmx512m -Xms512m"

  kibana:
    image: kibana:8.11.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:8.11.0
    user: root
    volumes:
      - ./filebeat/filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - logstash
```
