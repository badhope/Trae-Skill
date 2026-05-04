# Full Stack Development Assistant

**English** | [简体中文](#简体中文)

## Overview

The Full Stack Development Assistant is a folder-based agent designed to help developers build high-quality web applications. This agent can be uploaded to any AI platform (such as Doubao, Claude, Cursor, etc.) and will execute predefined workflows following strict protocols.

## Features

- **Requirements Analysis**: Systematically understand and document project requirements
- **Architecture Design**: Create robust technical architectures
- **Code Implementation**: Write clean, maintainable code
- **Quality Assurance**: Implement comprehensive testing strategies
- **Deployment Support**: Prepare applications for production

## Quick Start

1. Download or copy this entire folder
2. Upload to your preferred AI platform
3. Provide a task description in natural language
4. The agent will execute according to the defined workflow

## Folder Structure

```
full-stack-assistant/
├── agent.yaml          # Agent configuration and capabilities
├── system-prompt.md    # Agent personality and operational guidelines
├── README.md           # This file
├── workflow/           # Workflow definitions
│   ├── intent.yaml     # Intent recognition rules
│   ├── stages.yaml     # Workflow stages and outputs
│   └── tools.yaml      # Available tools and parameters
├── knowledge/          # Domain knowledge base
│   └── tech-stack.md   # Technology stack recommendations
├── tests/              # Test cases
│   └── test_cases.yaml # Validation test cases
└── outputs/            # Generated outputs (created at runtime)
```

## Supported Workflows

| Workflow ID | Name | Description |
|-------------|------|-------------|
| `new-project` | New Project Setup | Create a new software project from scratch |
| `feature-implementation` | Feature Implementation | Implement a specific feature |
| `bug-fixing` | Bug Fixing | Identify and fix bugs |
| `code-review` | Code Review | Review code for quality and security |
| `technical-design` | Technical Design | Create technical design documents |

## Usage Examples

```
Input: "Create a simple React Todo application with TypeScript"
→ Matches: new-project intent
→ Executes: full-project-workflow (8 stages)
→ Outputs: Complete project structure with all necessary files

Input: "Implement user login feature with email authentication"
→ Matches: feature-implementation intent
→ Executes: feature-workflow (5 stages)
→ Outputs: Login component, auth service, validation, tests

Input: "Fix the null pointer exception when submitting empty form"
→ Matches: bug-fixing intent
→ Executes: bug-fix-workflow (5 stages)
→ Outputs: Root cause analysis, fix implementation, verification
```

## Configuration

Key configuration options in `agent.yaml`:

- `capabilities`: Defines what the agent can do
- `tools`: Required tools and fallbacks
- `execution.maxIterations`: Maximum execution iterations
- `execution.defaultTimeout`: Default timeout per stage (ms)
- `output.format`: Output format (markdown)

## Output Standards

All outputs follow strict standards:
- Markdown format with clear headings
- Confidence scores for each stage
- Complete audit trail of decisions
- Actionable recommendations

---

---

# 简体中文

## 概述

全栈开发助手是一个基于文件夹的智能体，旨在帮助开发者构建高质量的Web应用程序。该智能体可以上传到任何AI平台（如豆包、Claude、Cursor等），并按照严格的协议执行预定义的工作流程。

## 功能特性

- **需求分析**: 系统地理解和记录项目需求
- **架构设计**: 创建健壮的技术架构
- **代码实现**: 编写干净、可维护的代码
- **质量保证**: 实施全面的测试策略
- **部署支持**: 准备生产环境部署

## 快速开始

1. 下载或复制整个文件夹
2. 上传到您喜欢的AI平台
3. 用自然语言描述任务
4. 智能体将按照定义的工作流程执行

## 文件夹结构

```
full-stack-assistant/
├── agent.yaml          # 智能体配置和能力定义
├── system-prompt.md    # 智能体角色和操作指南
├── README.md           # 本文档
├── workflow/           # 工作流定义
│   ├── intent.yaml     # 意图识别规则
│   ├── stages.yaml     # 工作流程阶段和输出
│   └── tools.yaml      # 可用工具和参数
├── knowledge/          # 领域知识库
│   └── tech-stack.md   # 技术栈建议
├── tests/              # 测试用例
│   └── test_cases.yaml # 验证测试用例
└── outputs/            # 生成的输出文件（运行时创建）
```

## 支持的工作流程

| 工作流程ID | 名称 | 描述 |
|-------------|------|-------------|
| `new-project` | 新项目设置 | 从头创建一个新的软件项目 |
| `feature-implementation` | 功能实现 | 实现特定功能 |
| `bug-fixing` | Bug修复 | 识别并修复Bug |
| `code-review` | 代码审查 | 审查代码质量和安全性 |
| `technical-design` | 技术设计 | 创建技术设计文档 |

## 使用示例

```
输入: "创建一个简单的React Todo应用程序，使用TypeScript"
→ 匹配: new-project 意图
→ 执行: full-project-workflow (8个阶段)
→ 输出: 完整的项目结构，包含所有必要文件

输入: "实现用户登录功能，支持邮箱认证"
→ 匹配: feature-implementation 意图
→ 执行: feature-workflow (5个阶段)
→ 输出: 登录组件、认证服务、验证逻辑、测试

输入: "修复提交空表单时的空指针异常"
→ 匹配: bug-fixing 意图
→ 执行: bug-fix-workflow (5个阶段)
→ 输出: 根本原因分析、修复实现、验证报告
```

## 配置

`agent.yaml` 中的关键配置选项：

- `capabilities`: 定义智能体的能力
- `tools`: 必需的工具和备用方案
- `execution.maxIterations`: 最大执行次数
- `execution.defaultTimeout`: 每个阶段的默认超时时间（毫秒）
- `output.format`: 输出格式（markdown）

## 输出标准

所有输出遵循严格的标准：
- Markdown格式，带有清晰的标题
- 每个阶段的置信度分数
- 完整的决策审计记录
- 可操作的建议
