# Folder as Agent - Example Agents

**English** | [简体中文](#简体中文)

This directory contains example agents demonstrating the Folder as Agent concept. Each folder represents a complete, self-contained agent that can be uploaded to any AI platform.

## Available Agents

### 1. Full Stack Development Assistant
**Location**: `full-stack-assistant/`

A comprehensive development assistant that helps with:
- New project setup
- Feature implementation
- Bug fixing
- Code review
- Technical design

**Key Features**:
- 5 predefined intents
- 5 complete workflows with 4-8 stages each
- 12+ tools available
- Domain knowledge base
- 5 test cases for validation

## How to Use

1. **Choose an Agent**: Select one of the example agent folders
2. **Upload to Platform**: Copy the entire folder to your AI platform (Doubao, Claude, Cursor, etc.)
3. **Provide Task**: Describe your task in natural language
4. **Execute**: The agent will follow its predefined workflow

## Creating Your Own Agent

See [FOLDER_AGENT_SPEC.md](../FOLDER_AGENT_SPEC.md) for the complete specification.

### Minimum Folder Structure

```
your-agent/
├── agent.yaml          # Required - Agent configuration
├── system-prompt.md    # Required - Agent instructions
├── workflow/           # Required - Workflow definitions
│   ├── intent.yaml     # Intent recognition rules
│   ├── stages.yaml     # Workflow stages
│   └── tools.yaml      # Available tools
├── knowledge/          # Optional - Domain knowledge
├── tests/              # Optional - Test cases
└── outputs/            # Generated outputs (runtime)
```

## Platform Compatibility

These agents are designed to work with:
- **Doubao (豆包)**: Full support
- **Claude Desktop**: Full support
- **Cursor**: Full support
- **Windsurf**: Full support
- **Any MCP Client**: Standardized tool calls

---

---

# 简体中文

## 文件夹即智能体 - 示例智能体

此目录包含展示"文件夹即智能体"概念的示例智能体。每个文件夹代表一个完整的、自包含的智能体，可以上传到任何AI平台使用。

## 可用智能体

### 1. 全栈开发助手
**位置**: `full-stack-assistant/`

一个全面的开发助手，帮助完成以下任务：
- 新项目设置
- 功能实现
- Bug修复
- 代码审查
- 技术设计

**主要特性**:
- 5个预定义意图
- 5个完整工作流程，每个包含4-8个阶段
- 12+可用工具
- 领域知识库
- 5个验证测试用例

## 使用方法

1. **选择智能体**: 选择一个示例智能体文件夹
2. **上传到平台**: 将整个文件夹复制到您的AI平台（豆包、Claude、Cursor等）
3. **提供任务**: 用自然语言描述您的任务
4. **执行**: 智能体将按照预定义的工作流程执行

## 创建您自己的智能体

请参阅 [FOLDER_AGENT_SPEC.md](../FOLDER_AGENT_SPEC.md) 获取完整规范。

### 最小文件夹结构

```
your-agent/
├── agent.yaml          # 必需 - 智能体配置
├── system-prompt.md    # 必需 - 智能体指令
├── workflow/           # 必需 - 工作流定义
│   ├── intent.yaml     # 意图识别规则
│   ├── stages.yaml     # 工作流程阶段
│   └── tools.yaml      # 可用工具
├── knowledge/          # 可选 - 领域知识
├── tests/              # 可选 - 测试用例
└── outputs/            # 生成的输出（运行时）
```

## 平台兼容性

这些智能体设计用于以下平台：
- **豆包**: 完全支持
- **Claude Desktop**: 完全支持
- **Cursor**: 完全支持
- **Windsurf**: 完全支持
- **任何MCP客户端**: 标准化工具调用
