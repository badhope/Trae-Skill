# Hierarchical Collaborative Skill Architecture (HCSA)

> **创新架构**: 将传统扁平Skill升级为四层协作系统，实现智能任务分解、自动协调、自我反思

## 目录结构

```
.trae/skills/
├── meta/                          # 战略层 (任务规划、协调、反思)
│   ├── task-planner/              # 任务规划器
│   ├── orchestrator/              # 执行协调器
│   └── reflector/                 # 反思学习器
│
├── workflows/                     # 战术层 (流程编排)
│   ├── coding-workflow/           # 编码工作流
│   └── debugging-workflow/        # 调试工作流
│
├── actions/                       # 执行层 (具体操作)
│   ├── code/                      # 代码操作
│   │   ├── api-design/            # API设计
│   │   ├── code-formatting/       # 代码格式化
│   │   ├── cross-file-refactor/   # 跨文件重构
│   │   └── linting-config/        # Lint配置
│   ├── code-generator/            # 代码生成
│   ├── documentation/             # 文档生成
│   ├── search/                    # 代码搜索
│   ├── test/                      # 测试操作
│   │   ├── code-coverage/         # 覆盖率分析
│   │   └── test-generator/        # 测试生成
│   └── tools/                     # 工具操作
│       ├── git-operations/        # Git操作
│       └── tool-use/              # 工具使用
│
├── domains/                       # 领域专用技能
│   ├── ai/                        # AI领域
│   │   ├── langchain/             # LangChain框架
│   │   ├── prompt-engineering/    # Prompt工程
│   │   └── rag-system/            # RAG系统
│   ├── backend/                   # 后端开发
│   │   ├── go/                    # Go后端
│   │   ├── graphql/               # GraphQL API
│   │   ├── nodejs/                # Node.js后端
│   │   ├── python/                # Python后端
│   │   └── typescript/            # TypeScript开发
│   ├── data/                      # 数据处理
│   │   ├── data-validation/       # 数据验证
│   │   └── etl/                   # ETL管道
│   ├── database/                  # 数据库
│   │   ├── database-migration/    # 数据库迁移
│   │   ├── mongodb/               # MongoDB
│   │   ├── redis-caching/         # Redis缓存
│   │   └── sql-optimization/      # SQL优化
│   ├── devops/                    # DevOps
│   │   ├── ci-cd-pipeline/        # CI/CD流水线
│   │   ├── docker/                # Docker容器化
│   │   └── kubernetes/            # K8s编排
│   ├── frontend/                  # 前端开发
│   │   ├── css-tailwind/          # Tailwind CSS
│   │   ├── nextjs/                # Next.js全栈
│   │   ├── react/                 # React开发
│   │   └── vue/                   # Vue开发
│   ├── infrastructure/            # 基础设施
│   │   ├── docker/                # Docker容器化
│   │   └── kubernetes/            # K8s编排
│   ├── mcp/                       # MCP集成
│   │   ├── server-development/    # MCP服务器开发
│   │   └── tools/                 # MCP工具
│   ├── mobile/                    # 移动开发
│   │   ├── flutter/               # Flutter开发
│   │   └── react-native/          # React Native开发
│   ├── performance/               # 性能优化
│   │   └── performance-optimizer/ # 性能优化器
│   ├── security/                  # 安全
│   │   └── security-auditor/      # 安全审计
│   └── testing/                   # 测试领域
│       ├── e2e-test/              # 端到端测试
│       ├── integration-test/      # 集成测试
│       └── unit-test/             # 单元测试
│
├── shared/                        # 共享资源
│   └── schemas/                   # JSON Schema
│
└── config/                        # 配置文件
```

## 快速索引

### 按层级查找

#### Meta层 (战略规划)
| Skill | 描述 | 触发场景 |
|-------|------|----------|
| [task-planner](meta/task-planner) | 任务分解与规划 | 复杂任务、多步骤任务 |
| [orchestrator](meta/orchestrator) | 执行协调与调度 | 多skill协作 |
| [reflector](meta/reflector) | 反思与学习优化 | 任务完成后评估 |

#### Workflow层 (流程编排)
| Skill | 描述 | 触发场景 |
|-------|------|----------|
| [coding-workflow](workflows/coding-workflow) | 编码任务流程 | 功能开发、代码实现 |
| [debugging-workflow](workflows/debugging-workflow) | 调试任务流程 | Bug修复、问题排查 |

#### Action层 (执行操作)
| Skill | 描述 | 触发场景 |
|-------|------|----------|
| [code-generator](actions/code-generator) | 代码生成 | 编写新代码 |
| [documentation](actions/documentation) | 文档生成 | README、API文档 |
| [code-search](actions/search) | 代码搜索 | 查找定义、用法分析 |
| [api-design](actions/code/api-design) | API设计 | RESTful/GraphQL设计 |
| [code-formatting](actions/code/code-formatting) | 代码格式化 | Prettier/Black配置 |
| [linting-config](actions/code/linting-config) | Lint配置 | ESLint/Ruff配置 |
| [cross-file-refactor](actions/code/cross-file-refactor) | 跨文件重构 | 重命名、移动代码 |
| [test-generator](actions/test/test-generator) | 测试生成 | 创建测试用例 |
| [code-coverage](actions/test/code-coverage) | 覆盖率分析 | 测试覆盖率 |
| [git-operations](actions/tools/git-operations) | Git操作 | 分支管理、合并冲突 |
| [tool-use](actions/tools/tool-use) | 工具使用 | 文件读取、命令执行 |

### 按领域查找

#### AI领域
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [langchain](domains/ai/langchain) | LangChain框架 | Chain, Agent, RAG |
| [prompt-engineering](domains/ai/prompt-engineering) | Prompt工程 | CoT, Few-shot, 结构化输出 |
| [rag-system](domains/ai/rag-system) | RAG系统 | 向量数据库, Embeddings, 检索策略 |

#### 后端开发
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [backend-python](domains/backend/python) | Python后端开发 | FastAPI, Django, Flask |
| [backend-nodejs](domains/backend/nodejs) | Node.js后端开发 | Express, NestJS |
| [backend-go](domains/backend/go) | Go后端开发 | Gin, Echo, gRPC |
| [graphql](domains/backend/graphql) | GraphQL API开发 | Apollo, Schema设计 |
| [typescript](domains/backend/typescript) | TypeScript开发 | 类型设计, 泛型编程 |

#### 前端开发
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [frontend-react](domains/frontend/react) | React开发 | React, TypeScript |
| [nextjs](domains/frontend/nextjs) | Next.js全栈 | SSR, SSG, App Router |
| [frontend-vue](domains/frontend/vue) | Vue开发 | Vue3, Nuxt, TypeScript |
| [css-tailwind](domains/frontend/css-tailwind) | Tailwind CSS | 响应式设计、暗黑模式 |

#### 移动开发
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [react-native](domains/mobile/react-native) | React Native开发 | iOS, Android, Expo |
| [flutter](domains/mobile/flutter) | Flutter开发 | Dart, Widget, 跨平台 |

#### 测试领域
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [unit-test](domains/testing/unit-test) | 单元测试 | Jest, pytest, Go test |
| [integration-test](domains/testing/integration-test) | 集成测试 | Supertest, TestContainers |
| [e2e-test](domains/testing/e2e-test) | 端到端测试 | Playwright, Cypress |

#### 数据库
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [mongodb](domains/database/mongodb) | MongoDB开发 | Mongoose, 聚合管道 |
| [database-migration](domains/database/database-migration) | 数据库迁移 | Prisma, Flyway, Django |
| [redis-caching](domains/database/redis-caching) | Redis缓存 | 缓存策略、限流、分布式锁 |
| [sql-optimization](domains/database/sql-optimization) | SQL优化 | 索引设计、查询优化 |

#### 数据处理
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [etl](domains/data/etl) | ETL管道开发 | Airflow, Spark, dbt |
| [data-validation](domains/data/data-validation) | 数据验证 | Pydantic, Great Expectations |

#### DevOps
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [docker](domains/devops/docker) | Docker容器化 | Dockerfile, Compose |
| [kubernetes](domains/devops/kubernetes) | K8s编排 | Deployment, Service, Helm |
| [ci-cd-pipeline](domains/devops/ci-cd-pipeline) | CI/CD流水线 | GitHub Actions, GitLab CI |

#### 安全与性能
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [security-auditor](domains/security/security-auditor) | 安全审计 | 漏洞扫描、认证审查 |
| [performance-optimizer](domains/performance/performance-optimizer) | 性能优化 | 瓶颈分析、算法优化 |

#### MCP集成
| Skill | 描述 | 技术栈 |
|-------|------|--------|
| [mcp-server](domains/mcp/server-development) | MCP服务器开发 | TypeScript, MCP SDK |
| [mcp-tools](domains/mcp/tools) | MCP工具创建 | Tool定义, 资源管理 |

## 使用指南

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

完整三层流程：

```
用户: "实现完整的用户认证系统"
→ task-planner 分解任务
→ orchestrator 协调执行
→ coding-workflow 执行
→ reflector 评估优化
```

## Frontmatter规范

```yaml
---
name: skill-name
description: "简短描述，包含关键词"
layer: meta | workflow | action | domain
role: planner | orchestrator | coordinator | executor | specialist
version: 2.0.0
invoked_by:
  - parent-skill
capabilities:
  - capability1
  - capability2
---
```

## 统计信息

| 层级 | 数量 | 说明 |
|------|------|------|
| Meta | 3 | 战略规划层 |
| Workflow | 2 | 流程编排层 |
| Action | 11 | 执行操作层 |
| Domain | 30+ | 领域专用层 |
| **总计** | **46+** | 持续扩展中 |

## 相关文档

- [HCSA架构规范](../../docs/HIERARCHICAL-SKILL-ARCHITECTURE.md)
