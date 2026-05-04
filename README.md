# 🚀 Mega-Agent Developer Platform
---
## 🌐 简介
**Mega-Agent Developer Platform** 是世界上首个基于MCP标准的智能体开发平台，包含 **13个专家引擎** 和 **96+个专业工具**。

**一次构建，全平台兼容！** ✨

### 核心特色
- 🎯 **多专家引擎**: 13个专业领域专家，覆盖全栈开发
- 🤖 **元智能体协调**: 5个协调智能体，自动分解复杂任务
- 🔧 **MCP标准工具**: 96+专业工具，开箱即用
- 🌍 **全平台兼容**: Claude Desktop, Cursor, Windsurf, Cline, Trae等

---
## 📦 快速开始（仅需3步！）
### 第一步：克隆项目
```bash
git clone https://github.com/badhope/skills.git
cd skills
```

### 第二步：加载到AI平台
根据你使用的平台，选择合适的加载方式：

| 平台 | 加载方式 |
|------|---------|
| **Trae** | 将文件夹添加为项目目录 |
| **Cursor** | 使用 `@load ./skills` 命令 |
| **Claude Desktop** | 设置中添加文件夹路径 |
| **Windsurf** | 添加为工作区目录 |
| **Cline** | 配置MCP服务器指向 `skills/mcp` |

### 第三步：开始使用！
用自然语言描述你的需求即可：
- "帮我创建一个React待办应用"
- "调试我的API返回500错误"
- "部署Node.js应用到AWS"
- "重构代码提高可读性"

---
## 🏗️ 架构概览
```
┌─────────────────────────────────────────────────────────────┐
│                   用户请求入口层                             │
│                   (自然语言输入)                            │
└───────────────────────────────┬───────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              智能路由层 (根据关键词匹配)                      │
└───────────────────────────────┬───────────────────────────────┘
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
┌────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   👥 专家引擎     │ │   🧠 元智能体    │ │  🛠️ MCP工具库    │
│   (13个)         │ │   (5个)         │ │   (96+)         │
│                  │ │                 │ │                 │
└────────────────────┘ └──────────────────┘ └──────────────────┘
```

---
## 👥 专家引擎团队
### 🔧 全栈开发工程师
完整应用开发，从数据库到部署
- **适用**: 构建新应用、完整功能开发
- **关键词**: 开发、构建、创建、应用

### 🎨 前端大师
React/Vue等前端开发专家
- **适用**: UI开发、组件设计、前端优化
- **关键词**: 前端、React、Vue、UI、CSS

### ⚡ 后端大师
多语言后端开发与微服务
- **适用**: API开发、微服务设计、认证
- **关键词**: 后端、API、Server、微服务

### 🗄️ 数据库专家
数据库建模、优化与迁移
- **适用**: 数据库设计、性能优化、迁移
- **关键词**: 数据库、MySQL、PostgreSQL、MongoDB

### 📦 DevOps工程师
Docker/K8s/CI/CD/多云部署
- **适用**: 容器化、部署、CI/CD、云服务
- **关键词**: 部署、Docker、K8s、云、CI/CD

### 🔒 安全审计官
安全审计与漏洞检测
- **适用**: 安全检查、渗透测试、漏洞修复
- **关键词**: 安全、漏洞、审计、Security

### ♻️ 代码质量专家
重构、设计模式与规范评审
- **适用**: 代码审查、重构、优化
- **关键词**: 重构、代码审查、质量

### 🧪 测试大师
全层级测试与性能压测
- **适用**: 单元测试、集成测试、性能测试
- **关键词**: 测试、单元测试、E2E

### 🤖 AI智能体架构师
Agent/MCP/RAG/提示词工程
- **适用**: 智能体开发、RAG、提示词优化
- **关键词**: Agent、MCP、RAG、提示词

### 📚 文档写作大师
技术文档与API文档
- **适用**: README、API文档、技术文档
- **关键词**: 文档、Readme、API文档

### 🐛 调试捉虫专家
系统性根因分析与Bug修复
- **适用**: 调试、错误排查、问题定位
- **关键词**: 调试、Bug、错误、Fix

### 🎮 游戏开发工具包
游戏开发专用工具
- **适用**: 游戏开发、Unity、Unreal
- **关键词**: 游戏、Unity、Unreal

---
## 🧠 元智能体（协调层）
### 🎯 任务编排器
复杂任务分解与多引擎协调
- **触发词**: 编排、协调、Workflow

### 📋 任务规划师
大任务分解为可执行的小任务
- **触发词**: 规划、分解、计划

### 🔍 反思器
任务复盘与经验沉淀
- **触发词**: 复盘、反思、改进

### 🛠️ 技能工匠
创建和升级智能体定义
- **触发词**: 创建技能、Skill、新技能

### 📈 持续学习器
从执行中学习，不断优化输出质量

---
## 🛠️ MCP工具分类
### 🔧 核心工具
- `filesystem` - 文件读写
- `terminal` - 终端命令
- `git` - Git操作
- `diff` - 对比差异
- `env` - 环境变量

### 🎨 前端工具
- `frontend-dev-kit` - 前端开发工具包
- `react` - React专用
- `typescript` - TypeScript支持
- `ui-design-kit` - UI设计工具

### ⚡ 后端工具
- `backend-dev-kit` - 后端开发工具包
- `api-dev` - API开发
- `code-generator` - 代码生成
- `auth` - 认证授权

### 🗄️ 数据库工具
- `database` - 通用数据库
- `mongodb` - MongoDB
- `redis` - Redis
- `json` - JSON数据处理
- `csv` - CSV数据处理

### ☁️ DevOps工具
- `docker` - Docker容器
- `kubernetes` - K8s集群
- `aws` - AWS服务
- `aliyun` - 阿里云
- `github` - GitHub集成
- `gitlab` - GitLab集成
- `gitee` - Gitee集成

### 🔒 安全工具
- `security-auditor` - 安全审计
- `secrets` - 密钥管理
- `auth` - 认证模块

### 🧪 测试工具
- `testing-toolkit` - 测试工具包
- `test-generator` - 测试用例生成
- `performance-optimizer` - 性能优化

### 🤖 Agent工具
- `agent-dev-kit` - Agent开发工具包
- `agent-coordinator` - 智能体协调
- `agent-multi` - 多智能体系统
- `agent-reflection` - 反思机制
- `agent-persistence` - 持久化

---
## 📂 项目结构
```
skills/
├── agent.yaml                      # 智能体配置文件
├── system-prompt.md                # 系统提示词
├── README.md                       # 项目说明（本文件）
│
├── .agent-skills/skills/          # 专家引擎目录
│   ├── config/routing.yaml         # 路由配置
│   ├── engines/                   # 13个专家引擎
│   │   ├── fullstack-engine/
│   │   ├── frontend-master/
│   │   ├── backend-master/
│   │   ├── database-specialist/
│   │   ├── devops-engineer/
│   │   ├── security-auditor/
│   │   ├── code-quality-expert/
│   │   ├── testing-master/
│   │   ├── ai-agent-architect/
│   │   ├── documentation-suite/
│   │   ├── bug-hunter/
│   │   └── game-dev-toolkit/
│   └── meta/                      # 5个元智能体
│       ├── orchestrator/
│       ├── task-planner/
│       ├── reflector/
│       ├── skill-crafter/
│       └── continuous-learning/
│
└── mcp/                           # 96+ MCP工具
    ├── core-dev-kit/
    ├── frontend-dev-kit/
    ├── backend-dev-kit/
    ├── api-dev/
    ├── database/
    ├── docker/
    ├── kubernetes/
    ├── github/
    ├── gitlab/
    ├── security-auditor/
    └── ... (更多工具)
```

---
## 💡 使用示例
### 示例1：构建React应用
```
用户: "创建一个React待办应用，带本地存储"

系统自动:
- 选择前端大师引擎
- 调用frontend-dev-kit + react工具
- 生成完整组件代码
- 包含本地存储功能
```

### 示例2：调试问题
```
用户: "我的API返回500错误，帮我调试"

系统自动:
- 选择调试捉虫专家
- 调用debugging-workflow工具
- 分析日志和错误堆栈
- 定位根因并修复
```

### 示例3：部署应用
```
用户: "部署Node.js应用到AWS"

系统自动:
- 选择DevOps工程师
- 调用docker + aws工具
- 生成Dockerfile和CI/CD配置
- 提供部署步骤
```

---
## 🔌 平台兼容性
| 平台 | 状态 | 说明 |
|------|------|------|
| ✅ Trae | 原生支持 | 最佳体验 |
| ✅ Claude Desktop | 原生支持 | MCP标准 |
| ✅ Cursor | 完全兼容 | 深度集成 |
| ✅ Windsurf | 完全兼容 | Cascade支持 |
| ✅ Cline / Roo Code | 完全兼容 | MCP工具 |
| ✅ 任何支持MCP的平台 | 完全兼容 | 标准协议 |

---
## 📊 项目统计
| 指标 | 数值 |
|------|------|
| **专家引擎** | 13个 |
| **元智能体** | 5个 |
| **MCP工具** | 96+个 |
| **架构版本** | 3.1.0 |
| **标准协议** | MCP v1.0 |
| **兼容性** | 全平台 |

---
## 🤝 贡献指南
欢迎贡献！请参考以下步骤：
1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 提交Pull Request

---
## 📄 许可证
MIT License - 详见LICENSE文件

---
## 🚀 开始使用
准备好开始了吗？只需：
1. 将此文件夹复制到你的项目中
2. 在你的AI平台中加载
3. 开始用自然语言描述需求！

**一次构建，处处运行！** 🌍✨
