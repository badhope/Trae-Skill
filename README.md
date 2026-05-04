# 🚀 Folder as Agent Platform

**English** | [简体中文](#简体中文)

---

## 🌐 Overview

**Folder as Agent Platform** is the world's first MCP-standard agent development platform that enables "Folder as Agent" functionality. With **7 core skills** and **50+ professional tools**, you can create complete agent definitions in folders that work across all AI platforms.

**Build once, run everywhere!** ✨

### Key Features
- 📁 **Folder-based Agents**: Complete agent definitions in a folder structure
- 🎯 **7 Core Skills**: Task planning, full-stack development, testing, security auditing, code quality, bug fixing, and DevOps
- 🔧 **MCP Standard Tools**: 50+ professional tools ready to use
- 🌍 **Multi-platform Compatible**: Doubao, Claude Desktop, Cursor, Windsurf, Trae, and more
- 🧠 **AI-Enhanced**: Integrated RAG, Knowledge Graph, and Memory Graph
- ✅ **Quality Assurance**: Comprehensive testing suite with 45+ test cases

---

## 📦 Quick Start (Just 3 Steps!)

### Step 1: Clone the Project
```bash
git clone https://github.com/badhope/skills.git
cd skills
```

### Step 2: Load to AI Platform

| Platform | Loading Method |
|----------|---------------|
| **Trae** | Add folder as project directory |
| **Cursor** | Use `@load ./skills` command |
| **Claude Desktop** | Add folder path in settings |
| **Windsurf** | Add as workspace directory |
| **Doubao** | Upload folder directly |

### Step 3: Start Using!
Describe your requirements in natural language:
- "Create a React Todo application"
- "Debug my API returning 500 error"
- "Deploy Node.js app to production"
- "Refactor code for better readability"

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   User Request Layer                        │
│                  (Natural Language Input)                   │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              Intent Recognition & Workflow Router           │
└───────────────────────────────┬─────────────────────────────┘
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
┌────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│     👥 Skills      │ │   🧠 Workflows   │ │  🛠️ Tools        │
│    (7 Core)       │ │   (16 Defined)   │ │   (50+)          │
│                   │ │                  │ │                  │
└────────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 👥 Core Skills

### 1. Task Planner
Requirements analysis and task decomposition
- **Keywords**: plan, analyze, requirements, design

### 2. Fullstack Engine
Complete application development
- **Keywords**: develop, build, create, application

### 3. Testing Master
Comprehensive testing strategies
- **Keywords**: test, unit test, integration test

### 4. Security Auditor
Security scanning and vulnerability detection
- **Keywords**: security, audit, vulnerability

### 5. Code Quality Expert
Code review and refactoring
- **Keywords**: review, refactor, quality

### 6. Bug Hunter
Root cause analysis and bug fixing
- **Keywords**: debug, bug, fix, error

### 7. DevOps Engineer
Deployment and operations
- **Keywords**: deploy, docker, CI/CD, cloud

---

## 📂 Project Structure

```
skills/
├── agent.yaml                      # Agent configuration
├── system-prompt.md                # System prompt
├── README.md                       # This file
├── FOLDER_AGENT_SPEC.md            # Specification document
├── PROJECT_COMPLETION_SUMMARY.md   # Project summary
│
├── .agent-skills/skills/config/    # Configuration files
│   └── tool-skill-mapping.yaml     # Tool-skill mappings
│
├── example-agents/                 # Example agents
│   └── full-stack-assistant/       # Full-stack development agent
│
└── packages/core/skill/            # Core implementation
    ├── skills/                     # 7 skill implementations
    ├── agentFolderExecutor.ts      # Execution engine
    ├── agentFolderLoader.ts        # Agent loader
    ├── agentPackager.ts            # Packaging utilities
    └── __tests__/                  # Test suite
```

---

## 🚀 Usage Examples

### Example 1: Create React App
```
Input: "Create a simple React Todo application with TypeScript"
→ Intent: new-project
→ Workflow: full-project-workflow (8 stages)
→ Output: Complete project structure
```

### Example 2: Fix Bug
```
Input: "Fix null pointer exception when submitting empty form"
→ Intent: bug-fixing
→ Workflow: bug-fix-workflow (5 stages)
→ Output: Root cause analysis + fix
```

### Example 3: Security Audit
```
Input: "Audit my codebase for security vulnerabilities"
→ Intent: security-audit
→ Workflow: security-workflow (4 stages)
→ Output: Security report with recommendations
```

---

## 🔌 Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| ✅ Doubao | Native Support | Direct folder upload |
| ✅ Claude Desktop | Native Support | MCP standard |
| ✅ Cursor | Full Support | Deep integration |
| ✅ Windsurf | Full Support | Cascade support |
| ✅ Trae | Native Support | Best experience |
| ✅ Any MCP-compliant platform | Full Support | Standard protocol |

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Core Skills** | 7 |
| **Workflows** | 16 |
| **Tools** | 50+ |
| **Test Cases** | 45+ |
| **Version** | 3.1.0 |
| **Protocol** | MCP v1.0 |

---

## 🤝 Contributing
Welcome to contribute! Please follow:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Submit Pull Request

---

## 📄 License
MIT License - See LICENSE file for details

---

---

# 简体中文

## 🌐 简介

**Folder as Agent Platform** 是世界上首个基于MCP标准的智能体开发平台，实现了"文件夹即智能体"功能。拥有 **7个核心技能** 和 **50+个专业工具**，您可以在文件夹中创建完整的智能体定义，跨所有AI平台运行。

**一次构建，全平台兼容！** ✨

### 核心特色
- 📁 **文件夹即智能体**: 在文件夹结构中定义完整智能体
- 🎯 **7个核心技能**: 任务规划、全栈开发、测试、安全审计、代码质量、Bug修复、DevOps
- 🔧 **MCP标准工具**: 50+专业工具，开箱即用
- 🌍 **多平台兼容**: 支持豆包、Claude Desktop、Cursor、Windsurf、Trae等
- 🧠 **AI增强**: 集成RAG、知识图谱、记忆图谱
- ✅ **质量保证**: 45+测试用例的完整测试套件

---

## 📦 快速开始（仅需3步！）

### 第一步：克隆项目
```bash
git clone https://github.com/badhope/skills.git
cd skills
```

### 第二步：加载到AI平台

| 平台 | 加载方式 |
|------|---------|
| **Trae** | 将文件夹添加为项目目录 |
| **Cursor** | 使用 `@load ./skills` 命令 |
| **Claude Desktop** | 设置中添加文件夹路径 |
| **Windsurf** | 添加为工作区目录 |
| **豆包** | 直接上传文件夹 |

### 第三步：开始使用！
用自然语言描述您的需求：
- "创建一个React待办应用"
- "调试我的API返回500错误"
- "部署Node.js应用到生产环境"
- "重构代码提高可读性"

---

## 🏗️ 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    用户请求层                              │
│                   (自然语言输入)                            │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              意图识别与工作流路由层                          │
└───────────────────────────────┬─────────────────────────────┘
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
┌────────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│     👥 技能系统    │ │   🧠 工作流     │ │  🛠️ 工具库        │
│    (7个核心)       │ │   (16个预定义)   │ │   (50+)          │
│                   │ │                  │ │                  │
└────────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## 👥 核心技能

### 1. 任务规划师
需求分析与任务分解
- **关键词**: 规划、分析、需求、设计

### 2. 全栈引擎
完整应用开发
- **关键词**: 开发、构建、创建、应用

### 3. 测试大师
全面测试策略
- **关键词**: 测试、单元测试、集成测试

### 4. 安全审计官
安全扫描与漏洞检测
- **关键词**: 安全、审计、漏洞

### 5. 代码质量专家
代码审查与重构
- **关键词**: 审查、重构、质量

### 6. Bug猎手
根本原因分析与Bug修复
- **关键词**: 调试、Bug、修复、错误

### 7. DevOps工程师
部署与运维
- **关键词**: 部署、Docker、CI/CD、云

---

## 📂 项目结构

```
skills/
├── agent.yaml                      # 智能体配置
├── system-prompt.md                # 系统提示词
├── README.md                       # 本文件
├── FOLDER_AGENT_SPEC.md            # 规范文档
├── PROJECT_COMPLETION_SUMMARY.md   # 项目总结
│
├── .agent-skills/skills/config/    # 配置文件
│   └── tool-skill-mapping.yaml     # 工具-技能映射
│
├── example-agents/                 # 示例智能体
│   └── full-stack-assistant/       # 全栈开发助手
│
└── packages/core/skill/            # 核心实现
    ├── skills/                     # 7个技能实现
    ├── agentFolderExecutor.ts      # 执行引擎
    ├── agentFolderLoader.ts        # 智能体加载器
    ├── agentPackager.ts            # 打包工具
    └── __tests__/                  # 测试套件
```

---

## 🚀 使用示例

### 示例1：创建React应用
```
输入: "创建一个简单的React Todo应用，使用TypeScript"
→ 意图: new-project
→ 工作流: full-project-workflow (8个阶段)
→ 输出: 完整项目结构
```

### 示例2：修复Bug
```
输入: "修复提交空表单时的空指针异常"
→ 意图: bug-fixing
→ 工作流: bug-fix-workflow (5个阶段)
→ 输出: 根本原因分析 + 修复方案
```

### 示例3：安全审计
```
输入: "审计我的代码库查找安全漏洞"
→ 意图: security-audit
→ 工作流: security-workflow (4个阶段)
→ 输出: 安全报告与建议
```

---

## 🔌 平台兼容性

| 平台 | 状态 | 说明 |
|------|------|------|
| ✅ 豆包 | 原生支持 | 直接上传文件夹 |
| ✅ Claude Desktop | 原生支持 | MCP标准 |
| ✅ Cursor | 完全兼容 | 深度集成 |
| ✅ Windsurf | 完全兼容 | Cascade支持 |
| ✅ Trae | 原生支持 | 最佳体验 |
| ✅ 任何支持MCP的平台 | 完全兼容 | 标准协议 |

---

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| **核心技能** | 7个 |
| **工作流** | 16个 |
| **工具** | 50+个 |
| **测试用例** | 45+个 |
| **版本** | 3.1.0 |
| **协议** | MCP v1.0 |

---

## 🤝 贡献指南
欢迎贡献！请遵循以下步骤：
1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 提交Pull Request

---

## 📄 许可证
MIT License - 详见LICENSE文件

---

**Build once, run everywhere!** 🌍✨
