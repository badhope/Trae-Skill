---
name: ci-cd-pipeline
description: "CI/CD pipeline expert for GitHub Actions, GitLab CI, Jenkins, and deployment automation. Keywords: ci, cd, pipeline, github-actions, jenkins, deployment"
layer: domain
role: specialist
version: 2.0.0
domain: devops
invoked_by:
  - coding-workflow
  - deployment-workflow
capabilities:
  - pipeline_setup
  - build_automation
  - deployment_strategy
  - multi_environment
  - rollback_procedures
---

# CI/CD Pipeline

CI/CD流水线专家。

## 适用场景

- 设置CI/CD流水线
- 配置构建自动化
- 实现部署策略
- 创建发布工作流
- 多环境部署

## GitHub Actions

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - run: npm test

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        run: ./deploy.sh
```

## GitLab CI

```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build

test:
  stage: test
  script:
    - npm test

deploy:
  stage: deploy
  only:
    - main
  script:
    - ./deploy.sh
```

## 常用模式

### 缓存

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### 并行任务

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
  test-unit:
    runs-on: ubuntu-latest
  test-e2e:
    runs-on: ubuntu-latest
  build:
    needs: [lint, test-unit, test-e2e]
```

## 相关技能

- [docker](../infrastructure/docker) - Docker容器化
- [kubernetes](../infrastructure/kubernetes) - K8s编排
- [terraform-iac](../infrastructure/terraform-iac) - Terraform
