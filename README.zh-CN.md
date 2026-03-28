# AI Skill & Prompt 仓库

[English](README.md) · [中文](README.zh-CN.md)

---

[![版本](https://img.shields.io/badge/version-v3.0.0-blue.svg)](https://github.com/badhope/skill)
[![许可证: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellowgreen.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/badhope/skill?style=social)](https://github.com/badhope/skill)
[![GitHub forks](https://img.shields.io/github/forks/badhope/skill?style=social)](https://github.com/badhope/skill)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![维护状态](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/badhope/skill/graphs/commit-activity)

---

## 🎯 项目概述

**AI Skill & Prompt Repository** 采用创新的 **HCSA (Hierarchical Collaborative Skill Architecture)** 四层协作架构，将传统扁平Skill升级为智能协作系统，实现任务自动分解、多Skill协调、自我反思优化。

| 适用对象 | 核心价值 |
|----------|----------|
| **开发者** | 快速查找、使用高质量技能，智能任务路由 |
| **AI 系统** | 自主理解、路由、选择、组合技能 |
| **研究者** | 学术写作、研究辅助、文献检索 |
| **创作者** | 创意写作、内容生成、灵感激发 |

**核心技术栈:** GPT-4 · Claude · LangChain · RAG · MCP Tools

---

## ⭐ 为什么选择本项目？

| 特性 | 说明 |
|------|------|
| 🏗️ **HCSA四层架构** | Meta → Workflow → Action → Domain 层级协作 |
| 🎯 **60+ 标准化Skills** | 模块化设计，即插即用 |
| 🧠 **智能任务路由** | 自动识别任务类型，路由到最佳Skill |
| 🤖 **AI领域专用** | LangChain、RAG、Prompt工程完整支持 |
| 📱 **全栈开发覆盖** | 前端、后端、移动端、DevOps全覆盖 |
| 🔧 **测试领域完善** | 单元测试、集成测试、E2E测试专家 |
| 🌐 **双语支持** | 完整中英文文档 |

---

## 🚀 HCSA 架构

### 四层协作架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Meta Layer (战略层)                       │
│   任务规划 → 复杂度评估 → 执行计划 → 反思优化                   │
│   task-planner | orchestrator | reflector                   │
├─────────────────────────────────────────────────────────────┤
│                  Workflow Layer (战术层)                     │
│   流程编排 → 状态管理 → 错误恢复 → 结果聚合                     │
│   coding-workflow | debugging-workflow                      │
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

### 智能路由系统

```yaml
# 任务自动路由示例
用户输入: "实现一个RAG系统"
→ 路由规则匹配: ai_llm_task
→ 选择Domain Skill: rag-system
→ 执行Workflow: coding-workflow
→ 调用Action: code-generator

用户输入: "修复这个bug"
→ 路由规则匹配: debugging_task
→ 选择Workflow: debugging-workflow
→ 自动分析错误栈
→ 生成修复方案
```

---

## 📚 技能分类

### AI领域 (AI Domain)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [langchain](.trae/skills/domains/ai/langchain) | LangChain框架专家 | Chain, Agent, RAG |
| [prompt-engineering](.trae/skills/domains/ai/prompt-engineering) | Prompt工程专家 | CoT, Few-shot, 结构化输出 |
| [rag-system](.trae/skills/domains/ai/rag-system) | RAG系统开发 | 向量数据库, Embeddings, 检索策略 |
| [openai](.trae/skills/domains/ai/openai) | OpenAI API集成 | GPT-4, DALL-E, Whisper |
| [claude-api](.trae/skills/domains/ai/claude-api) | Claude API集成 | Claude-3, Messages API |
| [agent-development](.trae/skills/domains/ai/agent-development) | AI代理开发 | Multi-agent, 自主代理 |
| [llm-evaluation](.trae/skills/domains/ai/llm-evaluation) | LLM评估 | RAGAS, DeepEval, 基准测试 |

### 后端开发 (Backend)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [python](.trae/skills/domains/backend/python) | Python后端开发 | FastAPI, Django, Flask |
| [nodejs](.trae/skills/domains/backend/nodejs) | Node.js后端开发 | Express, NestJS |
| [go](.trae/skills/domains/backend/go) | Go后端开发 | Gin, Echo, gRPC |
| [rust](.trae/skills/domains/backend/rust) | Rust系统编程 | Tokio, Actix, Axum |
| [graphql](.trae/skills/domains/backend/graphql) | GraphQL API开发 | Apollo, Schema设计 |
| [typescript](.trae/skills/domains/backend/typescript) | TypeScript开发 | 类型设计, 泛型编程 |

### 前端开发 (Frontend)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [react](.trae/skills/domains/frontend/react) | React开发 | React, TypeScript |
| [nextjs](.trae/skills/domains/frontend/nextjs) | Next.js全栈 | SSR, SSG, App Router |
| [vue](.trae/skills/domains/frontend/vue) | Vue开发 | Vue3, Nuxt, TypeScript |
| [css-tailwind](.trae/skills/domains/frontend/css-tailwind) | Tailwind CSS | 响应式设计、暗黑模式 |
| [accessibility](.trae/skills/domains/frontend/accessibility) | 网页无障碍 | WCAG, ARIA |
| [i18n](.trae/skills/domains/frontend/i18n) | 国际化 | 多语言, 本地化 |

### 移动开发 (Mobile)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [react-native](.trae/skills/domains/mobile/react-native) | React Native开发 | iOS, Android, Expo |
| [flutter](.trae/skills/domains/mobile/flutter) | Flutter开发 | Dart, Widget, 跨平台 |

### 测试领域 (Testing)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [unit-test](.trae/skills/domains/testing/unit-test) | 单元测试 | Jest, pytest, Go test |
| [integration-test](.trae/skills/domains/testing/integration-test) | 集成测试 | Supertest, TestContainers |
| [e2e-test](.trae/skills/domains/testing/e2e-test) | 端到端测试 | Playwright, Cypress |

### 数据库 (Database)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [mongodb](.trae/skills/domains/database/mongodb) | MongoDB开发 | Mongoose, 聚合管道 |
| [redis-caching](.trae/skills/domains/database/redis-caching) | Redis缓存 | 缓存策略、限流、分布式锁 |
| [sql-optimization](.trae/skills/domains/database/sql-optimization) | SQL优化 | 索引设计、查询优化 |
| [database-migration](.trae/skills/domains/database/database-migration) | 数据库迁移 | Prisma, Flyway, Django |

### DevOps

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [docker](.trae/skills/domains/devops/docker) | Docker容器化 | Dockerfile, Compose |
| [kubernetes](.trae/skills/domains/devops/kubernetes) | K8s编排 | Deployment, Service, Helm |
| [ci-cd-pipeline](.trae/skills/domains/devops/ci-cd-pipeline) | CI/CD流水线 | GitHub Actions, GitLab CI |
| [monitoring](.trae/skills/domains/devops/monitoring) | 系统监控 | Prometheus, Grafana |

### 安全 (Security)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [security-auditor](.trae/skills/domains/security/security-auditor) | 安全审计 | 漏洞扫描, 渗透测试 |
| [prompt-injection-defense](.trae/skills/domains/security/prompt-injection-defense) | Prompt注入防御 | 输入验证, 越狱防护 |

### 数据处理 (Data)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [etl](.trae/skills/domains/data/etl) | ETL管道 | Airflow, Spark |
| [data-validation](.trae/skills/domains/data/data-validation) | 数据验证 | Schema验证, 质量检查 |

### 性能优化 (Performance)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [performance-optimizer](.trae/skills/domains/performance/performance-optimizer) | 性能优化 | 性能分析, 瓶颈定位 |

### MCP (Model Context Protocol)

| 技能 | 描述 | 技术栈 |
|------|------|--------|
| [mcp-server-development](.trae/skills/domains/mcp/server-development) | MCP服务器开发 | 工具, 资源, 提示词 |
| [mcp-tools](.trae/skills/domains/mcp/tools) | MCP工具创建 | 工具设计, 验证 |

---

## 📈 统计数据

| 层级 | 数量 |
|------|------|
| Meta | 3 |
| Workflow | 4 |
| Action | 14 |
| Domain | 39 |
| **总计** | **60** |

---

## 🚀 快速开始

### AI系统启动序列

按顺序阅读以下文件：

```
1. ARCHITECTURE.md      → 设计理念
2. INDEX.md             → 结构概览
3. AI-USAGE.md          → 使用模式
4. AI-ROUTING.md        → 路由逻辑
5. AI-BOOTSTRAP.md      → 初始设置
6. SKILLS-INDEX.md      → 技能目录
```

### 目录结构

```
.trae/skills/
├── meta/                    # 战略层
│   ├── task-planner/        # 任务规划
│   ├── orchestrator/        # 执行协调
│   └── reflector/           # 反思优化
├── workflows/               # 战术层
│   ├── coding-workflow/     # 编码工作流
│   ├── debugging-workflow/  # 调试工作流
│   ├── research-workflow/   # 研究工作流
│   └── refactoring-workflow/# 重构工作流
├── actions/                 # 执行层
│   ├── code-generator/      # 代码生成
│   ├── test-generator/      # 测试生成
│   ├── documentation/       # 文档生成
│   └── ...                  # 更多Action
├── domains/                 # 领域层
│   ├── ai/                  # AI领域
│   ├── backend/             # 后端开发
│   ├── frontend/            # 前端开发
│   ├── devops/              # DevOps
│   └── ...                  # 更多领域
└── config/
    └── routing.yaml         # 路由配置
```

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

**如何贡献:**

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多详情。

---

## 📄 许可证

本项目采用 [Apache-2.0 许可证](LICENSE)。

---

## 🔗 相关链接

| 链接 | 描述 |
|------|------|
| [📋 技能索引](SKILLS-INDEX.md) | 完整技能目录 |
| [📖 架构文档](ARCHITECTURE.md) | 架构设计说明 |
| [🔧 扩展指南](EXTENSION-GUIDE.md) | 技能扩展指南 |
| [🐛 问题追踪](https://github.com/badhope/skill/issues) | Bug 报告 |

---

## 📬 联系方式

- **GitHub**: [badhope](https://github.com/badhope)
- **项目链接**: [https://github.com/badhope/skill](https://github.com/badhope/skill)

---

<div align="center">
  <strong>如果这个项目对你有帮助，请给一个 ⭐</strong>
  <br>
  <em>由 badhope 用 ❤️ 构建</em>
</div>
