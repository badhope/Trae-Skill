# Full Stack Development Assistant

**English** | [简体中文](#简体中文)

## Overview

The Full Stack Development Assistant is a DevFlow Agent designed to help developers build high-quality web applications. Simply upload this folder to any AI platform (Doubao, Claude, Cursor, etc.) and it will execute predefined workflows following strict protocols.

## Quick Start

1. Download or copy this folder
2. Upload to your AI platform
3. Describe your task in natural language
4. Agent executes according to defined workflow

## Folder Structure

```
full-stack-assistant/
├── agent.yaml          # Agent configuration
├── system-prompt.md    # Role definition
├── workflow/           # Workflow definitions
│   ├── intent.yaml     # Intent recognition
│   ├── stages.yaml     # Workflow stages
│   └── tools.yaml      # Tool list
├── knowledge/          # Knowledge base
└── tests/             # Test cases
```

## Supported Workflows

| Workflow | Description |
|----------|-------------|
| `new-project` | New Project Setup |
| `feature-implementation` | Feature Implementation |
| `bug-fixing` | Bug Fixing |
| `code-review` | Code Review |
| `technical-design` | Technical Design |

## Usage Examples

```
Input: "Create a React Todo application with TypeScript"
→ Intent: new-project
→ Workflow: full-project-workflow (8 stages)
→ Output: Complete project structure
```

---

---

# 简体中文

## 概述

全栈开发助手是一个 DevFlow Agent，旨在帮助开发者构建高质量的Web应用程序。只需将此文件夹上传到任何AI平台（豆包、Claude、Cursor等），它将按照严格的协议执行预定义的工作流程。

## 快速开始

1. 下载或复制此文件夹
2. 上传到您的AI平台
3. 用自然语言描述任务
4. 智能体按定义的工作流程执行

## 文件夹结构

```
full-stack-assistant/
├── agent.yaml          # 智能体配置
├── system-prompt.md    # 角色定义
├── workflow/           # 工作流定义
│   ├── intent.yaml     # 意图识别
│   ├── stages.yaml     # 工作流程阶段
│   └── tools.yaml      # 工具列表
├── knowledge/          # 知识库
└── tests/             # 测试用例
```

## 支持的工作流程

| 工作流程 | 描述 |
|----------|-------------|
| `new-project` | 新项目设置 |
| `feature-implementation` | 功能实现 |
| `bug-fixing` | Bug修复 |
| `code-review` | 代码审查 |
| `technical-design` | 技术设计 |

## 使用示例

```
输入: "创建一个React Todo应用，使用TypeScript"
→ 意图: new-project
→ 工作流: full-project-workflow (8个阶段)
→ 输出: 完整的项目结构
```
