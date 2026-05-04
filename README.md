# 🚀 DevFlow Agent - 开发工作流智能体

---

## 🇺🇸 English

**Development Workflow Agent - 7 Core Skills + 16 Workflows for AI Platforms**

> ✅ Works on ALL AI Platforms: Doubao • Claude Desktop • Cursor • Windsurf • Trae

### 📖 Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Core Skills](#core-skills)
5. [Workflows](#workflows)
6. [Platform Support](#platform-support)
7. [Architecture](#architecture)
8. [Examples](#examples)
9. [Contributing](#contributing)
10. [License](#license)

---

### Overview

DevFlow Agent is a folder-based agent that defines development workflows with simple YAML and Markdown files. Just upload the folder to any AI platform, and it will execute predefined workflows strictly following the specifications.

**Why DevFlow Agent?**
- 📁 **Folder as Agent**: No complex setup required
- 📝 **Simple Configuration**: YAML + Markdown only
- 🚀 **Drag & Drop**: Upload to any AI platform
- 🔧 **Pre-built Workflows**: 16 common development workflows
- 🌍 **Multi-platform**: Works everywhere

---

### Key Features

| Feature | Description |
|---------|-------------|
| **7 Core Skills** | Task planning, fullstack development, testing, security, etc. |
| **16 Workflows** | Cover the entire development lifecycle |
| **50+ Tools** | Professional developer tools mapped to skills |
| **RAG Support** | Knowledge retrieval with vector search |
| **Knowledge Graph** | Entity relationship and reasoning |
| **Memory System** | Context-aware memory management |

---

### Quick Start

#### Option 1: Drag & Drop (Recommended)

1. Download `example-agents/full-stack-assistant/`
2. Upload folder to your AI platform
3. Describe your task in natural language

#### Option 2: Programmatic Usage

```typescript
import { globalNewSkillOrchestrator, loadAgentFromFolder } from '@devflow-agent/core';

const agent = await loadAgentFromFolder('./my-agent');
const result = await globalNewSkillOrchestrator.executeWorkflow(
  { name: 'New Project', stages: [...] },
  'Create a React todo app'
);
```

---

### Core Skills

| Skill | ID | Purpose |
|--------|------|--------|
| **Task Planner** | `task-planner` | Analyze requirements, break down tasks |
| **Fullstack Engine** | `fullstack-engine` | End-to-end application development |
| **Testing Master** | `testing-master` | Comprehensive testing strategies |
| **Security Auditor** | `security-auditor` | Security scanning and risk assessment |
| **Code Quality Expert** | `code-quality-expert` | Code review and quality assessment |
| **Bug Hunter** | `bug-hunter` | Bug analysis and fixing recommendations |
| **DevOps Engineer** | `devops-engineer` | Deployment and CI/CD operations |

---

### Workflows

#### Development Lifecycle

| Workflow | Purpose | Stages |
|----------|---------|--------|
| `new-project` | Initialize new project | 8 stages |
| `feature-implementation` | Build new features | 5 stages |
| `bug-fixing` | Fix bugs and issues | 5 stages |
| `code-review` | Code quality review | 4 stages |
| `technical-design` | Architecture and design | 3 stages |
| `deployment` | Application deployment | 4 stages |
| `security-audit` | Security assessment | 4 stages |
| `database-task` | Database operations | 4 stages |
| `testing-task` | Testing activities | 4 stages |
| `refactoring` | Code refactoring | 4 stages |
| `documentation` | Documentation creation | 3 stages |
| `analysis` | Code and data analysis | 3 stages |
| `data-processing` | Data processing tasks | 3 stages |
| `web-search` | Information retrieval | 2 stages |
| `containerization` | Docker and container tasks | 3 stages |
| `api-development` | API development tasks | 4 stages |

---

### Platform Support

| Platform | Status | How to Use |
|----------|--------|-----------|
| 🫘 **Doubao** | ✅ Native Support | Upload folder directly |
| 🤖 **Claude Desktop** | ✅ Native Support | Add folder to config |
| ✨ **Cursor** | ✅ Full Integration | `@load ./folder` |
| 🌊 **Windsurf** | ✅ Full Integration | Add to workspace |
| 🚀 **Trae** | ✅ Native Support | Best experience |

---

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Request Layer                  │
│                  (Natural Language Input)                │
└─────────────────────────────┬───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│              Intent Recognition & Workflow Router        │
└─────────────────────────────┬───────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌──────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     🎯 Skills   │ │   📋 Workflows  │ │  🛠️ Tools      │
│     (7 Core)    │ │   (16 Defined)  │ │   (50+)         │
└──────────────────┘ └─────────────────┘ └─────────────────┘
```

---

### Examples

#### Example 1: New Project

**Input**: "Create a React todo application with TypeScript"

**Execution Flow**:
1. **Intent Recognition**: `new-project`
2. **Workflow**: `full-project-workflow` (8 stages)
3. **Skills**: Task Planner → Fullstack Engine → Testing Master
4. **Output**: Complete project structure

#### Example 2: Bug Fix

**Input**: "Fix the null pointer exception when submitting the form"

**Execution Flow**:
1. **Intent Recognition**: `bug-fixing`
2. **Workflow**: `bug-fix-workflow` (5 stages)
3. **Skills**: Bug Hunter → Security Auditor
4. **Output**: Root cause + fix

---

### Contributing

Please see the [Contribution Guide](CONTRIBUTING.md) for details.

---

### License

MIT License - See [LICENSE](LICENSE) file for details.

---

---

## 🇨🇳 简体中文

**开发工作流智能体 - 7个核心技能 + 16个工作流，支持所有AI平台**

> ✅ 适用于所有AI平台: 豆包 • Claude Desktop • Cursor • Windsurf • Trae

### 📖 目录
1. [概述](#概述)
2. [核心特性](#核心特性)
3. [快速开始](#快速开始)
4. [核心技能](#核心技能)
5. [工作流](#工作流)
6. [平台支持](#平台支持)
7. [架构](#架构)
8. [使用示例](#使用示例)
9. [贡献指南](#贡献指南)
10. [许可证](#许可证)

---

### 概述

DevFlow Agent 是一个基于文件夹的智能体，通过简单的 YAML 和 Markdown 文件定义开发工作流。只需将文件夹上传到任何 AI 平台，它就会严格按照规范执行预定义的工作流程。

**为什么选择 DevFlow Agent?**
- 📁 **文件夹即智能体**: 无需复杂配置
- 📝 **简单配置**: 仅需 YAML + Markdown
- 🚀 **拖放即用**: 上传到任何AI平台即可
- 🔧 **预设工作流**: 16个常见开发工作流
- 🌍 **多平台兼容**: 所有平台都能用

---

### 核心特性

| 特性 | 描述 |
|---------|-------------|
| **7个核心技能** | 任务规划、全栈开发、测试、安全等 |
| **16个工作流** | 覆盖完整开发生命周期 |
| **50+工具** | 专业开发工具映射到技能 |
| **RAG支持** | 向量搜索知识检索 |
| **知识图谱** | 实体关系和推理 |
| **记忆系统** | 上下文感知记忆管理 |

---

### 快速开始

#### 方式1: 拖放使用（推荐）

1. 下载 `example-agents/full-stack-assistant/`
2. 上传文件夹到您的AI平台
3. 用自然语言描述任务

#### 方式2: 编程使用

```typescript
import { globalNewSkillOrchestrator, loadAgentFromFolder } from '@devflow-agent/core';

const agent = await loadAgentFromFolder('./my-agent');
const result = await globalNewSkillOrchestrator.executeWorkflow(
  { name: 'New Project', stages: [...] },
  'Create a React todo app'
);
```

---

### 核心技能

| 技能 | ID | 用途 |
|--------|------|--------|
| **任务规划师** | `task-planner` | 分析需求、分解任务 |
| **全栈引擎** | `fullstack-engine` | 端到端应用开发 |
| **测试大师** | `testing-master` | 全面测试策略 |
| **安全审计师** | `security-auditor` | 安全扫描和风险评估 |
| **代码质量专家** | `code-quality-expert` | 代码审查和质量评估 |
| **Bug猎手** | `bug-hunter` | Bug分析和修复建议 |
| **DevOps工程师** | `devops-engineer` | 部署和CI/CD操作 |

---

### 工作流

#### 开发生命周期

| 工作流 | 用途 | 阶段数 |
|----------|---------|--------|
| `new-project` | 新项目初始化 | 8个阶段 |
| `feature-implementation` | 功能实现 | 5个阶段 |
| `bug-fixing` | Bug修复 | 5个阶段 |
| `code-review` | 代码质量审查 | 4个阶段 |
| `technical-design` | 架构和设计 | 3个阶段 |
| `deployment` | 应用部署 | 4个阶段 |
| `security-audit` | 安全评估 | 4个阶段 |
| `database-task` | 数据库操作 | 4个阶段 |
| `testing-task` | 测试任务 | 4个阶段 |
| `refactoring` | 代码重构 | 4个阶段 |
| `documentation` | 文档创建 | 3个阶段 |
| `analysis` | 代码和数据分析 | 3个阶段 |
| `data-processing` | 数据处理任务 | 3个阶段 |
| `web-search` | 信息检索 | 2个阶段 |
| `containerization` | Docker和容器任务 | 3个阶段 |
| `api-development` | API开发任务 | 4个阶段 |

---

### 平台支持

| 平台 | 状态 | 使用方式 |
|----------|--------|-----------|
| 🫘 **豆包** | ✅ 原生支持 | 直接上传文件夹 |
| 🤖 **Claude Desktop** | ✅ 原生支持 | 添加到配置 |
| ✨ **Cursor** | ✅ 完整集成 | `@load ./folder` |
| 🌊 **Windsurf** | ✅ 完整集成 | 添加到工作区 |
| 🚀 **Trae** | ✅ 原生支持 | 最佳体验 |

---

### 架构

```
┌─────────────────────────────────────────────────────────┐
│                      用户请求层                            │
│                  (自然语言输入)                           │
└─────────────────────────────┬───────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────┐
│              意图识别和工作流路由器                        │
└─────────────────────────────┬───────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌──────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│     🎯 技能      │ │   📋 工作流     │ │  🛠️ 工具        │
│     (7个核心)    │ │   (16个已定义)  │ │   (50+)         │
└──────────────────┘ └─────────────────┘ └─────────────────┘
```

---

### 使用示例

#### 示例1: 新项目

**输入**: "Create a React todo application with TypeScript"

**执行流程**:
1. **意图识别**: `new-project`
2. **工作流**: `full-project-workflow` (8个阶段)
3. **技能**: 任务规划师 → 全栈引擎 → 测试大师
4. **输出**: 完整项目结构

#### 示例2: Bug修复

**输入**: "Fix the null pointer exception when submitting the form"

**执行流程**:
1. **意图识别**: `bug-fixing`
2. **工作流**: `bug-fix-workflow` (5个阶段)
3. **技能**: Bug猎手 → 安全审计师
4. **输出**: 根因分析 + 修复

---

### 贡献指南

请查看 [贡献指南](CONTRIBUTING.md) 获取详细信息。

---

### 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件。

---

**为 AI 开发者社区构建** ❤️
