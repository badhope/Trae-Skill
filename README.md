<div align="center">
  <h1>🚀 DevFlow Agent</h1>
  <p>Development Workflow Agent - 开发工作流智能体</p>
  
  <!-- Language Switcher -->
  <div style="margin-bottom: 20px;">
    <a href="#english" style="padding: 8px 16px; background: #4CAF50; color: white; border-radius: 4px; text-decoration: none; margin-right: 8px;">🇺🇸 English</a>
    <a href="#chinese" style="padding: 8px 16px; background: #2196F3; color: white; border-radius: 4px; text-decoration: none;">🇨🇳 简体中文</a>
  </div>
</div>

---

## 📌 Quick Links | 快速链接

| Category | English | 中文 |
|----------|---------|------|
| **GitHub** | [![GitHub Stars](https://img.shields.io/github/stars/badhope/devflow-agent.svg)](https://github.com/badhope/devflow-agent) | ⭐ 收藏项目 |
| **License** | [![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) | 📄 MIT许可证 |
| **Version** | [![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](package.json) | 🔢 版本 1.0.0 |
| **Platforms** | Doubao • Claude • Cursor • Windsurf • Trae | 🖥️ 多平台支持 |

---

## 🇺🇸 English <a name="english"></a>

**Development Workflow Agent with 7 Core Skills and 16 Workflows**

### 📖 Table of Contents
1. [Overview](#overview-en)
2. [Key Features](#features-en)
3. [Quick Start](#quickstart-en)
4. [Core Skills](#skills-en)
5. [Workflows](#workflows-en)
6. [Installation](#install-en)
7. [Usage](#usage-en)
8. [Platform Support](#platform-en)
9. [Contributing](#contributing-en)
10. [License](#license-en)

---

### Overview <a name="overview-en"></a>

DevFlow Agent is a folder-based development workflow agent. Simply define your workflows with YAML and Markdown files, then upload the folder to any AI platform. The agent will execute according to your predefined specifications.

**Features:**
- 📁 **Folder as Agent**: Complete agent definition in a folder
- 📝 **Simple Configuration**: YAML + Markdown only
- 🚀 **Drag & Drop**: Works on any AI platform
- 🔧 **16 Pre-built Workflows**: Covering entire development lifecycle
- 🌍 **Multi-platform**: Doubao, Claude, Cursor, Windsurf, Trae

---

### Key Features <a name="features-en"></a>

| Feature | Description |
|---------|-------------|
| **7 Core Skills** | Task Planner, Fullstack Engine, Testing Master, Security Auditor, Code Quality Expert, Bug Hunter, DevOps Engineer |
| **16 Workflows** | New project, feature implementation, bug fixing, code review, deployment, security audit, etc. |
| **50+ Tools** | Professional developer tools mapped to skills |
| **RAG Integration** | Knowledge retrieval with semantic search |
| **Knowledge Graph** | Entity relationships and reasoning |
| **Memory System** | Context-aware memory management |

---

### Quick Start <a name="quickstart-en"></a>

#### Option 1: Drag & Drop (Recommended)
```
1. Download example-agents/full-stack-assistant/ folder
2. Upload to your AI platform (Doubao, Claude, Cursor, etc.)
3. Describe your task in natural language
4. Agent executes automatically!
```

#### Option 2: Programmatic Usage
```typescript
import { loadAgentFromFolder, AgentFolderExecutor } from '@devflow-agent/core';

// Load agent from folder
const agent = await loadAgentFromFolder('./my-agent');

// Execute workflow
const executor = new AgentFolderExecutor(agent);
const result = await executor.execute('Create a React todo app');
```

---

### Core Skills <a name="skills-en"></a>

| Skill | ID | Description |
|--------|------|-------------|
| **Task Planner** | `task-planner` | Analyze requirements, decompose tasks, create timelines |
| **Fullstack Engine** | `fullstack-engine` | End-to-end application development |
| **Testing Master** | `testing-master` | Comprehensive testing strategies |
| **Security Auditor** | `security-auditor` | Security scanning and vulnerability detection |
| **Code Quality Expert** | `code-quality-expert` | Code review and quality assessment |
| **Bug Hunter** | `bug-hunter` | Root cause analysis and bug fixing |
| **DevOps Engineer** | `devops-engineer` | Deployment and CI/CD operations |

---

### Workflows <a name="workflows-en"></a>

| Workflow | Stages | Description |
|----------|--------|-------------|
| `new-project` | 8 stages | Initialize new software project |
| `feature-implementation` | 5 stages | Implement new features |
| `bug-fixing` | 5 stages | Identify and fix bugs |
| `code-review` | 4 stages | Review code quality |
| `technical-design` | 3 stages | Create technical design docs |
| `deployment` | 4 stages | Deploy applications |
| `security-audit` | 4 stages | Security vulnerability scan |
| `database-task` | 4 stages | Database operations |
| `testing-task` | 4 stages | Testing activities |
| `refactoring` | 4 stages | Code refactoring |
| `documentation` | 3 stages | Documentation creation |
| `analysis` | 3 stages | Code and data analysis |
| `data-processing` | 3 stages | Data processing tasks |
| `web-search` | 2 stages | Information retrieval |
| `containerization` | 3 stages | Docker and container tasks |
| `api-development` | 4 stages | API development |

---

### Installation <a name="install-en"></a>

```bash
# Install from npm
npm install @devflow-agent/core

# Or clone the repository
git clone https://github.com/badhope/devflow-agent.git
cd devflow-agent
npm install
```

---

### Usage <a name="usage-en"></a>

#### CLI Commands
```bash
# Create a new agent
npx devflow create my-agent

# Validate agent folder
npx devflow validate ./my-agent

# Run agent
npx devflow run ./my-agent -t "Create React app"

# List available agents
npx devflow list
```

---

### Platform Support <a name="platform-en"></a>

| Platform | Status | Usage |
|----------|--------|-------|
| 🫘 **Doubao** | ✅ Native | Upload folder directly |
| 🤖 **Claude Desktop** | ✅ Native | Add folder to config |
| ✨ **Cursor** | ✅ Full | `@load ./folder` command |
| 🌊 **Windsurf** | ✅ Full | Add to workspace |
| 🚀 **Trae** | ✅ Native | Best experience |

---

### Contributing <a name="contributing-en"></a>

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

---

### License <a name="license-en"></a>

MIT License - See [LICENSE](LICENSE) for details.

---

---

## 🇨🇳 简体中文 <a name="chinese"></a>

**开发工作流智能体 - 7个核心技能 + 16个工作流**

### 📖 目录
1. [概述](#overview-cn)
2. [核心特性](#features-cn)
3. [快速开始](#quickstart-cn)
4. [核心技能](#skills-cn)
5. [工作流](#workflows-cn)
6. [安装](#install-cn)
7. [使用](#usage-cn)
8. [平台支持](#platform-cn)
9. [贡献指南](#contributing-cn)
10. [许可证](#license-cn)

---

### 概述 <a name="overview-cn"></a>

DevFlow Agent 是一个基于文件夹的开发工作流智能体。只需用 YAML 和 Markdown 文件定义工作流，然后将文件夹上传到任何 AI 平台，智能体就会按照您预定义的规范执行。

**特性:**
- 📁 **文件夹即智能体**: 在文件夹中定义完整智能体
- 📝 **简单配置**: 仅需 YAML + Markdown
- 🚀 **拖放即用**: 适用于任何 AI 平台
- 🔧 **16个预设工作流**: 覆盖完整开发生命周期
- 🌍 **多平台兼容**: 豆包、Claude、Cursor、Windsurf、Trae

---

### 核心特性 <a name="features-cn"></a>

| 特性 | 描述 |
|---------|-------------|
| **7个核心技能** | 任务规划师、全栈引擎、测试大师、安全审计师、代码质量专家、Bug猎手、DevOps工程师 |
| **16个工作流** | 新项目、功能实现、Bug修复、代码审查、部署、安全审计等 |
| **50+工具** | 专业开发工具映射到技能 |
| **RAG集成** | 语义搜索知识检索 |
| **知识图谱** | 实体关系和推理 |
| **记忆系统** | 上下文感知记忆管理 |

---

### 快速开始 <a name="quickstart-cn"></a>

#### 方式1: 拖放使用（推荐）
```
1. 下载 example-agents/full-stack-assistant/ 文件夹
2. 上传到您的 AI 平台（豆包、Claude、Cursor等）
3. 用自然语言描述任务
4. 智能体自动执行！
```

#### 方式2: 编程使用
```typescript
import { loadAgentFromFolder, AgentFolderExecutor } from '@devflow-agent/core';

// 从文件夹加载智能体
const agent = await loadAgentFromFolder('./my-agent');

// 执行工作流
const executor = new AgentFolderExecutor(agent);
const result = await executor.execute('创建一个React待办应用');
```

---

### 核心技能 <a name="skills-cn"></a>

| 技能 | ID | 描述 |
|--------|------|-------------|
| **任务规划师** | `task-planner` | 分析需求、分解任务、创建时间线 |
| **全栈引擎** | `fullstack-engine` | 端到端应用开发 |
| **测试大师** | `testing-master` | 全面测试策略 |
| **安全审计师** | `security-auditor` | 安全扫描和漏洞检测 |
| **代码质量专家** | `code-quality-expert` | 代码审查和质量评估 |
| **Bug猎手** | `bug-hunter` | 根本原因分析和Bug修复 |
| **DevOps工程师** | `devops-engineer` | 部署和CI/CD操作 |

---

### 工作流 <a name="workflows-cn"></a>

| 工作流 | 阶段数 | 描述 |
|----------|--------|-------------|
| `new-project` | 8个阶段 | 初始化新软件项目 |
| `feature-implementation` | 5个阶段 | 实现新功能 |
| `bug-fixing` | 5个阶段 | 识别并修复Bug |
| `code-review` | 4个阶段 | 代码质量审查 |
| `technical-design` | 3个阶段 | 创建技术设计文档 |
| `deployment` | 4个阶段 | 部署应用 |
| `security-audit` | 4个阶段 | 安全漏洞扫描 |
| `database-task` | 4个阶段 | 数据库操作 |
| `testing-task` | 4个阶段 | 测试任务 |
| `refactoring` | 4个阶段 | 代码重构 |
| `documentation` | 3个阶段 | 文档创建 |
| `analysis` | 3个阶段 | 代码和数据分析 |
| `data-processing` | 3个阶段 | 数据处理任务 |
| `web-search` | 2个阶段 | 信息检索 |
| `containerization` | 3个阶段 | Docker和容器任务 |
| `api-development` | 4个阶段 | API开发 |

---

### 安装 <a name="install-cn"></a>

```bash
# 从npm安装
npm install @devflow-agent/core

# 或者克隆仓库
git clone https://github.com/badhope/devflow-agent.git
cd devflow-agent
npm install
```

---

### 使用 <a name="usage-cn"></a>

#### CLI命令
```bash
# 创建新智能体
npx devflow create my-agent

# 验证智能体文件夹
npx devflow validate ./my-agent

# 运行智能体
npx devflow run ./my-agent -t "创建React应用"

# 列出可用智能体
npx devflow list
```

---

### 平台支持 <a name="platform-cn"></a>

| 平台 | 状态 | 使用方式 |
|----------|--------|-------|
| 🫘 **豆包** | ✅ 原生 | 直接上传文件夹 |
| 🤖 **Claude Desktop** | ✅ 原生 | 添加到配置 |
| ✨ **Cursor** | ✅ 完整 | `@load ./folder` 命令 |
| 🌊 **Windsurf** | ✅ 完整 | 添加到工作区 |
| 🚀 **Trae** | ✅ 原生 | 最佳体验 |

---

### 贡献指南 <a name="contributing-cn"></a>

请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 获取贡献详情。

---

### 许可证 <a name="license-cn"></a>

MIT License - 查看 [LICENSE](LICENSE) 获取详情。

---

<div align="center">
  <p>Made with ❤️ for the AI Developer Community</p>
  <p>为 AI 开发者社区构建</p>
</div>
