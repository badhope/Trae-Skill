# AI Skill & Prompt Repository

[English](README.md) · [中文](README.zh-CN.md)

---

[![Version](https://img.shields.io/badge/version-v4.0.0-blue.svg)](https://github.com/badhope/skill)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellowgreen.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/badhope/skill?style=social)](https://github.com/badhope/skill)
[![GitHub forks](https://img.shields.io/github/forks/badhope/skill?style=social)](https://github.com/badhope/skill)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/badhope/skill/graphs/commit-activity)

---

## 🎯 Overview

**AI Skill & Prompt Repository** 采用创新的 **Enhanced HCSA (Hierarchical Collaborative Skill Architecture)** 六层协作架构，将传统扁平Skill升级为智能协作系统，实现任务自动分解、多模型路由、自我反思优化、持续学习增强。

| Target Users | Core Value |
|--------------|------------|
| **Developers** | 快速查找、使用高质量技能，智能任务路由 |
| **AI Systems** | 自主理解、路由、选择、组合技能 |
| **Researchers** | 学术写作、研究辅助、文献检索 |
| **Creators** | 创意写作、内容生成、灵感激发 |

**Core Tech Stack:** GPT-4 · Claude · LangChain · RAG · MCP Tools

---

## ⭐ Why Choose This Project?

| Feature | Description |
|---------|-------------|
| 🏗️ **Enhanced HCSA六层架构** | Learning → Meta → Dispatcher → Workflow → Action → Domain 层级协作 |
| 🧠 **Learning Layer** | 反思学习、策略优化、自我增强、知识积累 |
| 🔀 **Dispatcher Layer** | 智能模型路由、并发管理、成本优化 |
| 🎯 **68+ 标准化Skills** | 模块化设计，即插即用 |
| 🤖 **多模型路由** | 根据任务复杂度自动选择最优模型 |
| 📱 **全栈开发覆盖** | 前端、后端、移动端、DevOps全覆盖 |
| 💾 **持久化存储** | 任务追踪、知识库、学习记录持久化 |
| 🌐 **双语支持** | 完整中英文文档 |

---

## 🚀 Enhanced HCSA Architecture

### 六层协作架构

```
┌─────────────────────────────────────────────────────────────┐
│                  Learning Layer (学习层)                     │
│   执行分析 → 模式识别 → 策略优化 → 知识积累                     │
│   reflector | strategy-learner | self-enhancer | knowledge-base│
├─────────────────────────────────────────────────────────────┤
│                    Meta Layer (战略层)                       │
│   任务规划 → 复杂度评估 → 任务分解 → 执行计划                   │
│   task-planner | decomposition-planner | task-registry       │
├─────────────────────────────────────────────────────────────┤
│                 Dispatcher Layer (调度层)                    │
│   模型路由 → 成本优化 → 并发管理 → 限流控制                     │
│   model-router | concurrency-manager                         │
├─────────────────────────────────────────────────────────────┤
│                  Workflow Layer (战术层)                     │
│   流程编排 → 状态管理 → 结果聚合 → 冲突解决                     │
│   coding-workflow | debugging-workflow | aggregation-processor│
├─────────────────────────────────────────────────────────────┤
│                   Action Layer (执行层)                      │
│   代码生成 → 测试生成 → 文档生成 → 代码搜索                     │
│   code-generator | test-generator | documentation | search  │
├─────────────────────────────────────────────────────────────┤
│                   Domain Layer (领域层)                      │
│   AI领域 → 后端开发 → 前端开发 → 移动开发 → DevOps             │
│   langchain | react | python | docker | kubernetes          │
└─────────────────────────────────────────────────────────────┘
```

### 智能模型路由

```yaml
# 根据任务复杂度自动选择模型
complexity_levels:
  LOW:      → gpt-3.5-turbo    # 简单任务，成本优先
  MEDIUM:   → gpt-4o-mini      # 平衡性能
  HIGH:     → gpt-4o           # 复杂推理
  CRITICAL: → claude-3-opus    # 专家级任务

# 路由示例
用户输入: "实现一个RAG系统"
→ 复杂度评估: HIGH
→ 模型路由: gpt-4o
→ 选择Domain Skill: rag-system
→ 执行Workflow: coding-workflow
→ 执行后反思: reflector分析
→ 学习记录: knowledge-base存储
```

### 学习循环

```
┌─────────────────────────────────────────────────────────┐
│                    Learning Cycle                        │
│                                                          │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │ Execute  │───▶│ Reflect  │───▶│  Learn   │         │
│   └──────────┘    └──────────┘    └──────────┘         │
│        ▲                                 │              │
│        └─────────────────────────────────┘              │
│                    Improve                               │
└─────────────────────────────────────────────────────────┘
```

---

## 🆕 New Features in v4.0

### Learning Layer (学习层)
| Skill | 功能 |
|-------|------|
| **reflector** | 执行后分析、问题识别、洞察生成 |
| **strategy-learner** | 模式识别、策略优化、反馈学习 |
| **self-enhancer** | 能力增强、Prompt优化、工作流改进 |
| **knowledge-base** | 知识存储、语义搜索、知识图谱 |

### Dispatcher Layer (调度层)
| Skill | 功能 |
|-------|------|
| **model-router** | 复杂度评估、模型选择、成本优化 |
| **concurrency-manager** | 限流控制、请求队列、并行执行 |

### Enhanced Meta Layer
| Skill | 功能 |
|-------|------|
| **decomposition-planner** | 高级任务分解、依赖分析 |
| **task-registry** | 任务追踪、状态管理、历史持久化 |

### Enhanced Workflow Layer
| Skill | 功能 |
|-------|------|
| **aggregation-processor** | 结果聚合、冲突解决、一致性检查 |

---

## 📚 Skill Categories

### AI领域 (AI Domain)

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [langchain](.trae/skills/domains/ai/langchain) | LangChain框架专家 | Chain, Agent, RAG |
| [prompt-engineering](.trae/skills/domains/ai/prompt-engineering) | Prompt工程专家 | CoT, Few-shot, 结构化输出 |
| [rag-system](.trae/skills/domains/ai/rag-system) | RAG系统开发 | 向量数据库, Embeddings, 检索策略 |
| [agent-development](.trae/skills/domains/ai/agent-development) | AI Agent开发 | Multi-Agent, Tool Use |
| [llm-evaluation](.trae/skills/domains/ai/llm-evaluation) | LLM评估 | Benchmarks, Metrics |

### 后端开发 (Backend)

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [python](.trae/skills/domains/backend/python) | Python后端开发 | FastAPI, Django, Flask |
| [nodejs](.trae/skills/domains/backend/nodejs) | Node.js后端开发 | Express, NestJS |
| [go](.trae/skills/domains/backend/go) | Go后端开发 | Gin, Echo, gRPC |
| [rust](.trae/skills/domains/backend/rust) | Rust系统编程 | Tokio, Actix, Axum |
| [graphql](.trae/skills/domains/backend/graphql) | GraphQL API开发 | Apollo, Schema设计 |
| [typescript](.trae/skills/domains/backend/typescript) | TypeScript开发 | 类型设计, 泛型编程 |

### 前端开发 (Frontend)

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [react](.trae/skills/domains/frontend/react) | React开发 | React, TypeScript |
| [nextjs](.trae/skills/domains/frontend/nextjs) | Next.js全栈 | SSR, SSG, App Router |
| [vue](.trae/skills/domains/frontend/vue) | Vue开发 | Vue3, Nuxt, TypeScript |
| [css-tailwind](.trae/skills/domains/frontend/css-tailwind) | Tailwind CSS | 响应式设计、暗黑模式 |

### 移动开发 (Mobile)

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [react-native](.trae/skills/domains/mobile/react-native) | React Native开发 | iOS, Android, Expo |
| [flutter](.trae/skills/domains/mobile/flutter) | Flutter开发 | Dart, Widget, 跨平台 |

### 测试领域 (Testing)

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [unit-test](.trae/skills/domains/testing/unit-test) | 单元测试 | Jest, pytest, Go test |
| [integration-test](.trae/skills/domains/testing/integration-test) | 集成测试 | Supertest, TestContainers |
| [e2e-test](.trae/skills/domains/testing/e2e-test) | 端到端测试 | Playwright, Cypress |

### 数据库 (Database)

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [mongodb](.trae/skills/domains/database/mongodb) | MongoDB开发 | Mongoose, 聚合管道 |
| [redis-caching](.trae/skills/domains/database/redis-caching) | Redis缓存 | 缓存策略、限流、分布式锁 |
| [sql-optimization](.trae/skills/domains/database/sql-optimization) | SQL优化 | 索引设计、查询优化 |
| [database-migration](.trae/skills/domains/database/database-migration) | 数据库迁移 | Prisma, Flyway, Django |

### DevOps

| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [docker](.trae/skills/domains/devops/docker) | Docker容器化 | Dockerfile, Compose |
| [kubernetes](.trae/skills/domains/devops/kubernetes) | K8s编排 | Deployment, Service, Helm |
| [ci-cd-pipeline](.trae/skills/domains/devops/ci-cd-pipeline) | CI/CD流水线 | GitHub Actions, GitLab CI |

---

## 📁 Project Structure

```
skill/
├── .trae/
│   └── skills/                    # Enhanced HCSA架构技能库
│       ├── learning/              # 学习层 (NEW)
│       │   ├── reflector/         # 执行反思
│       │   ├── strategy-learner/  # 策略学习
│       │   ├── self-enhancer/     # 自我增强
│       │   └── knowledge-base/    # 知识库
│       ├── meta/                  # 战略层
│       │   ├── task-planner/      # 任务规划
│       │   ├── decomposition-planner/ # 任务分解
│       │   └── task-registry/     # 任务注册
│       ├── dispatcher/            # 调度层 (NEW)
│       │   ├── model-router/      # 模型路由
│       │   └── concurrency-manager/ # 并发管理
│       ├── workflows/             # 战术层
│       │   ├── coding-workflow/
│       │   ├── debugging-workflow/
│       │   └── aggregation-processor/ # 结果聚合
│       ├── actions/               # 执行层
│       ├── domains/               # 领域层
│       ├── shared/                # 共享资源
│       └── config/                # 配置文件
│           ├── routing.yaml       # 路由配置 (v3.0)
│           └── storage-schema.yaml # 存储schema
│
├── docs/                          # 文档
│   └── HIERARCHICAL-SKILL-ARCHITECTURE.md
│
└── README.md                      # 本文件
```

---

## 🔧 Quick Start

### 简单任务 (复杂度 < 3)

直接调用Action层或Domain层skill：

```
用户: "给这个函数添加注释"
→ 直接调用 code-generator
```

### 中等任务 (复杂度 3-5)

使用Workflow层skill：

```
用户: "实现用户登录功能"
→ coding-workflow 协调多个action
```

### 复杂任务 (复杂度 > 5)

完整六层流程：

```
用户: "实现完整的用户认证系统"
→ model-router 选择最优模型
→ task-planner 分解任务
→ decomposition-planner 分析依赖
→ orchestrator 协调执行
→ coding-workflow 执行
→ aggregation-processor 聚合结果
→ reflector 评估优化
→ knowledge-base 存储知识
```

---

## 📊 Statistics

| 层级 | 数量 | 说明 |
|------|------|------|
| Learning | 4 | 自我学习层 (NEW) |
| Meta | 4 | 战略规划层 |
| Dispatcher | 2 | 模型调度层 (NEW) |
| Workflow | 5 | 流程编排层 |
| Action | 14 | 执行操作层 |
| Domain | 39 | 领域专用层 |
| **总计** | **68** | 持续扩展中 |

---

## 🤝 Contributing

欢迎贡献新的Skill或改进现有Skill！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/new-skill`)
3. 提交更改 (`git commit -m 'Add new skill'`)
4. 推送到分支 (`git push origin feature/new-skill`)
5. 创建 Pull Request

### Skill开发规范

```yaml
---
name: skill-name
description: "简短描述，包含关键词"
layer: learning | meta | dispatcher | workflow | action | domain
role: learner | planner | router | coordinator | executor | specialist
version: 2.0.0
invoked_by:
  - parent-skill
capabilities:
  - capability1
  - capability2
metrics:
  success_rate: 0.95
  avg_latency: 1.2s
---
```

---

## 📄 License

- **Code**: Apache-2.0 License
- **Content**: CC BY 4.0 License

---

## 🔗 Related Links

- [HCSA架构规范](docs/HIERARCHICAL-SKILL-ARCHITECTURE.md)
- [Skill索引](SKILLS-INDEX.md)
- [架构文档](ARCHITECTURE.md)
- [路由配置](.trae/skills/config/routing.yaml)
- [存储Schema](.trae/skills/config/storage-schema.yaml)
