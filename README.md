# Thesis Specialist

## 论文专家智能体 | Academic Thesis Writing Agent

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](README.md)
[![Platform](https://img.shields.io/badge/platform-Folder--as--Agent-green.svg)](README.md)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

# 📖 目录 | Table of Contents

- [English Description](#english)
- [中文介绍](#中文)
- [快速开始 | Quick Start](#quick-start)
- [完整使用指南 | Complete Usage Guide](#usage-guide)
- [架构说明 | Architecture](#architecture)
- [示例 | Examples](#examples)

---

# English

## Platform Overview

**Thesis Specialist** is an innovative **Folder-as-Agent** platform designed specifically for academic thesis writing. The entire platform can be downloaded and directly submitted to any Large Language Model (LLM) such as Doubao, Claude, GPT, or Gemini for immediate use.

### Core Concept

The **Folder-as-Agent** concept transforms this folder itself into an intelligent agent. Simply download the folder and submit it to any compatible LLM—the agent will automatically execute the complete thesis writing workflow according to predefined processes.

### Key Features

| Feature | Description |
|---------|-------------|
| **8-Phase Execution** | Strictly follows 8 phases from intent recognition to final output |
| **8 Expert Engines** | Specialized engines for topic, literature, structure, writing, etc. |
| **4 Meta Agents** | Coordination, planning, review, and progress tracking |
| **4 Tools** | Literature search, grammar check, data visualization, format conversion |
| **Memory System** | User preferences, conversation history, project state, knowledge base |
| **No Configuration** | Download and use immediately |

### Platform Positioning

This platform is positioned as a **professional academic writing assistant** that:

1. **Out-of-the-box**: No configuration required, ready to use upon download
2. **Complete Workflow**: Strictly executes the full 8-phase process
3. **Multi-Agent Collaboration**: Coordinates multiple experts for complex tasks
4. **Quality Assured**: Includes verification and review mechanisms

---

# 中文

## 平台概述

**Thesis Specialist（论文专家智能体）** 是一个创新的 **"文件夹即智能体"（Folder-as-Agent）** 平台，专为学术论文写作而设计。整个平台可以下载后直接提交给任何大语言模型（LLM），如豆包、Claude、GPT或Gemini，立即使用。

### 核心概念

**"文件夹即智能体"** 概念将整个文件夹转变为一个智能体。只需下载文件夹并提交给任何兼容的LLM，智能体会自动按照预定义的流程执行完整的论文写作工作流。

### 核心特性

| 特性 | 描述 |
|------|------|
| **8阶段执行流程** | 从意图识别到最终输出的严格8阶段流程 |
| **8个专家引擎** | 主题、文献、结构、写作等专业化引擎 |
| **4个元智能体** | 协调、规划、评审、进度追踪 |
| **4个工具** | 文献检索、语法检查、数据可视化、格式转换 |
| **记忆系统** | 用户偏好、会话历史、项目状态、知识库 |
| **零配置** | 下载即用 |

### 平台定位

本平台定位为**专业学术写作助手**，具备以下特点：

1. **开箱即用**：无需配置，下载即可使用
2. **完整流程**：严格遵循8阶段工作流程
3. **多智能体协作**：协调多个专家完成复杂任务
4. **质量保障**：包含验证和评审机制

---

# Quick Start | 快速开始

## Method 1: Direct LLM Submission (Recommended)

```
1. Download this folder
2. Submit the entire folder to Doubao, Claude, GPT, or Gemini
3. Describe your thesis requirements in natural language
4. The agent automatically executes the complete workflow
```

## Method 2: Reference Files

```
1. Read agent.yaml for platform configuration
2. Read system-prompt.md for system instructions
3. Select appropriate SKILL.md for your task
4. Submit to LLM with specific requirements
```

---

# Usage Guide | 完整使用指南

## Step 1: Understand Your Needs

Before starting, clarify:

| Question | Purpose |
|----------|---------|
| What is your research field? | Match with expert engine |
| What stage of writing are you at? | Determine workflow phase |
| Do you need a single expert or multiple? | Single expert vs coordinator |

## Step 2: Choose Interaction Mode

### Single Expert Mode
For specific tasks:
- Topic selection → Topic Expert
- Literature review → Literature Expert
- Writing assistance → Writing Expert

### Multi-Expert Mode
For complex tasks requiring coordination:
- Complete thesis → Coordinator Agent
- Full workflow planning → Task Planner

## Step 3: Describe Your Requirements

Example inputs:

| English | 中文 |
|---------|------|
| "Help me find a research topic in computer vision" | "帮我找一个计算机视觉的研究方向" |
| "Write the literature review chapter" | "帮我写文献综述章节" |
| "Plan my thesis writing workflow" | "帮我规划论文写作流程" |
| "Polish my abstract" | "帮我润色摘要" |

## Step 4: Receive Expert Output

Each expert provides structured output:
- Topic Expert → Topic proposals with evaluation
- Literature Expert → Search strategy + review outline
- Writing Expert → Chapter content with formatting
- Reviewer → Quality assessment + improvement suggestions

---

# Architecture | 架构说明

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Thesis Specialist                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Intent    │ →  │   Expert    │ →  │    Tool     │     │
│  │ Recognition │    │  Matching   │    │   Calling   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         ↓                  ↓                  ↓              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              8-Phase Execution Flow                  │    │
│  │  1. Intent Recognition → 2. Expert Matching         │    │
│  │  3. Task Planning → 4. Expert Execution            │    │
│  │  5. Tool Calling → 6. Result Integration           │    │
│  │  7. Quality Check → 8. Final Output               │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  Expert Engines (8)    │  Meta Agents (4)  │  Tools (4)   │
│  ├─ Topic Expert       │  ├─ Coordinator   │  ├─ Search   │
│  ├─ Literature Expert  │  ├─ Task Planner │  ├─ Grammar  │
│  ├─ Structure Expert   │  ├─ Reviewer     │  ├─ Visual   │
│  ├─ Writing Expert     │  └─ Progress     │  └─ Format   │
│  ├─ English Expert     │                   │              │
│  ├─ Data Analysis     │                   │              │
│  ├─ Reference Expert  │                   │              │
│  └─ Format Expert     │                   │              │
├─────────────────────────────────────────────────────────────┤
│                    Memory System                             │
│  ├─ User Preferences  ├─ Conversation History               │
│  ├─ Project State     └─ Knowledge Base                   │
└─────────────────────────────────────────────────────────────┘
```

## File Structure

```
thesis-specialist/
├── agent.yaml                 # Platform configuration
├── system-prompt.md          # System prompt for LLM
├── README.md                 # This file
│
├── skills/
│   ├── engines/            # 8 Expert Engines
│   │   ├── topic-expert/   # Topic selection
│   │   ├── literature-expert/  # Literature review
│   │   ├── structure-expert/   # Structure planning
│   │   ├── writing-expert/     # Content writing
│   │   ├── english-expert/     # English polishing
│   │   ├── data-analysis-expert/  # Data analysis
│   │   ├── reference-expert/   # Reference management
│   │   └── format-expert/      # Format compliance
│   └── meta/                # Meta Agents
│       ├── coordinator/    # Multi-expert coordination
│       ├── task-planner/   # Workflow planning
│       ├── reviewer/       # Quality review
│       └── progress-tracker/  # Progress tracking
│
├── tools/                   # Tools
│   ├── literature-search/  # Academic database search
│   ├── grammar-checker/    # Grammar & style check
│   ├── data-visualizer/    # Chart generation
│   └── format-converter/   # Format conversion
│
├── memory/                  # Memory System
│   ├── memory-system.yaml  # Memory configuration
│   └── stores/            # Data stores
│       ├── user-preferences.json
│       ├── conversation-history.json
│       ├── project-state.json
│       └── knowledge-base.json
│
├── utils/                  # Utilities
│   ├── routing_optimizer.py   # Smart routing
│   ├── error_handler.py       # Error handling
│   └── performance.py         # Performance optimization
│
└── tests/                  # Tests
    └── test_agent.py      # Unit tests
```

---

# Examples | 示例

## Example 1: Topic Selection

**Input | 输入:**
```
Help me come up with a research topic in computer vision for my master's thesis.
帮我找一个计算机视觉方向的硕士论文研究方向。
```

**Output | 输出:**
The Topic Expert provides:
- 3-5 candidate topics with detailed analysis
- Evaluation scores (innovation, feasibility, research value)
- Recommended ranking with reasoning
- Suggested next steps

---

## Example 2: Literature Review

**Input | 输入:**
```
I need help writing the literature review chapter for my thesis on machine learning in healthcare.
帮我写一篇关于机器学习在医疗领域应用的文献综述。
```

**Output | 输出:**
The Literature Expert provides:
- Search strategy for multiple databases
- Organized literature structure
- Summary of key findings
- Citation recommendations

---

## Example 3: Thesis Planning

**Input | 输入:**
```
Help me plan the entire workflow for writing my thesis. It's due in 3 months.
帮我规划一下论文写作的整体流程，我需要在3个月内完成。
```

**Output | 输出:**
The Task Planner provides:
- Task decomposition into manageable phases
- Timeline with milestones
- Expert allocation for each phase
- Progress tracking checkpoints

---

## Example 4: Multi-Expert Coordination

**Input | 输入:**
```
I need to complete my entire thesis. Can you coordinate multiple experts?
我需要完成一篇完整的论文，你能协调多个专家吗？
```

**Output | 输出:**
The Coordinator Agent:
1. Analyzes the complex task
2. Decomposes into subtasks
3. Assigns appropriate experts
4. Coordinates execution sequence
5. Integrates all outputs
6. Performs quality verification

---

# Platform Comparison | 平台对比

| Feature | Traditional LLM | Thesis Specialist |
|---------|-----------------|-------------------|
| Configuration | Manual setup required | Zero configuration |
| Workflow | Ad-hoc, may skip steps | Strict 8-phase process |
| Expertise | General purpose | Domain-specific experts |
| Output Quality | Variable | Verified and structured |
| Learning Curve | Steep | Minimal |
| Productivity | Moderate | High |

---

# 技术规格 | Technical Specifications

| Item | Value |
|------|-------|
| Version | 2.2.0 |
| Release Date | 2026-05-04 |
| Protocol | MCP (Model Context Protocol) |
| Configuration | YAML-based |
| Languages | EN (core), ZH (README) |
| Testing | Unit tests included |
| Validation | Config validator included |

---

# 许可证 | License

MIT License - Free for academic and commercial use.

---

# 联系方式 | Contact

For issues and suggestions, please refer to the project repository.

---

**Last Updated: 2026-05-04 | 最后更新：2026-05-04**
