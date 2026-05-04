# Thesis Specialist

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](README.md)
[![Platform](https://img.shields.io/badge/platform-Folder--as--Agent-green.svg)](README.md)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![CI Status](https://img.shields.io/github/actions/workflow/status/badhope/Thesis-Specialist-Agent/ci.yml?branch=main)](https://github.com/badhope/Thesis-Specialist-Agent/actions)

---

**🌐 Language:** [English](README.md) | [中文](README_zh.md)

---

# 📖 Table of Contents

- [About](#about)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [File Structure](#file-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

# About

**Thesis Specialist** is an innovative **Folder-as-Agent** platform designed specifically for academic thesis writing. The entire platform can be downloaded and directly submitted to any Large Language Model (LLM) such as Doubao, Claude, GPT, or Gemini for immediate use.

### Core Concept

The **Folder-as-Agent** concept transforms this folder itself into an intelligent agent. Simply download the folder and submit it to any compatible LLM—the agent will automatically execute the complete thesis writing workflow according to predefined processes.

### Platform Positioning

This platform is positioned as a **professional academic writing assistant** that:
- **Out-of-the-box**: No configuration required, ready to use upon download
- **Complete Workflow**: Strictly executes the full 8-phase process
- **Multi-Agent Collaboration**: Coordinates multiple experts for complex tasks
- **Quality Assured**: Includes verification and review mechanisms

[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](README.md)
[![Platform](https://img.shields.io/badge/platform-Folder--as--Agent-green.svg)](README.md)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![CI Status](https://img.shields.io/github/actions/workflow/status/badhope/Thesis-Specialist-Agent/ci.yml?branch=main)](https://github.com/badhope/Thesis-Specialist-Agent/actions)
[![Issues](https://img.shields.io/github/issues/badhope/Thesis-Specialist-Agent)](https://github.com/badhope/Thesis-Specialist-Agent/issues)
[![Stars](https://img.shields.io/github/stars/badhope/Thesis-Specialist-Agent)](https://github.com/badhope/Thesis-Specialist-Agent/stargazers)
[![Forks](https://img.shields.io/github/forks/badhope/Thesis-Specialist-Agent)](https://github.com/badhope/Thesis-Specialist-Agent/network/members)

---

# Features

| Feature | Description |
|---------|-------------|
| **8-Phase Execution** | Strictly follows 8 phases from intent recognition to final output |
| **8 Expert Engines** | Specialized engines for topic, literature, structure, writing, etc. |
| **4 Meta Agents** | Coordination, planning, review, and progress tracking |
| **4 Tools** | Literature search, grammar check, data visualization, format conversion |
| **Memory System** | User preferences, conversation history, project state, knowledge base |
| **Zero Configuration** | Download and use immediately |

---

# Quick Start

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

# Usage Examples

## Example 1: Topic Selection

**Input:**
```
Help me come up with a research topic in computer vision for my master's thesis.
```

**Output:** The Topic Expert provides:
- 3-5 candidate topics with detailed analysis
- Evaluation scores (innovation, feasibility, research value)
- Recommended ranking with reasoning
- Suggested next steps

---

## Example 2: Literature Review

**Input:**
```
I need help writing the literature review chapter for my thesis on machine learning in healthcare.
```

**Output:** The Literature Expert provides:
- Search strategy for multiple databases
- Organized literature structure
- Summary of key findings
- Citation recommendations

---

## Example 3: Thesis Planning

**Input:**
```
Help me plan the entire workflow for writing my thesis. It's due in 3 months.
```

**Output:** The Task Planner provides:
- Task decomposition into manageable phases
- Timeline with milestones
- Expert allocation for each phase
- Progress tracking checkpoints

---

## Example 4: Multi-Expert Coordination

**Input:**
```
I need to complete my entire thesis. Can you coordinate multiple experts?
```

**Output:** The Coordinator Agent:
1. Analyzes the complex task
2. Decomposes into subtasks
3. Assigns appropriate experts
4. Coordinates execution sequence
5. Integrates all outputs
6. Performs quality verification

---

# Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Thesis Specialist                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │   Intent    │ →  │   Expert    │ →  │    Tool     │       │
│  │ Recognition │    │  Matching   │    │   Calling   │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
│         ↓                  ↓                  ↓              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │              8-Phase Execution Flow                  │     │
│  │  1. Intent Recognition → 2. Expert Matching         │     │
│  │  3. Task Planning → 4. Expert Execution            │     │
│  │  5. Tool Calling → 6. Result Integration           │     │
│  │  7. Quality Check → 8. Final Output               │     │
│  └─────────────────────────────────────────────────────┘     │
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
│  ├─ Project State     └─ Knowledge Base                    │
└─────────────────────────────────────────────────────────────┘
```

---

# File Structure

```
thesis-specialist/
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT License
├── README.md                      # English documentation
├── README_zh.md                   # 中文文档
├── CONTRIBUTING.md                # Contributing guidelines
├── CODE_OF_CONDUCT.md             # Code of conduct
├── SUPPORT.md                     # Support information
├── SECURITY.md                    # Security policy
├── agent.yaml                     # Platform configuration
├── system-prompt.md              # System prompt
├── config-validator.py            # Config validator
├── logger.py                     # Logger system
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
│       ├── task-planner/    # Workflow planning
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

# Development

## Requirements

- Python 3.10+
- PyYAML

## Installation

```bash
pip install pyyaml
```

## Running Tests

```bash
python -m unittest tests.test_agent -v
```

## Configuration Validation

```bash
python config-validator.py
```

---

# Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

---

# Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating in this project.

---

# Security

For security vulnerabilities, please read our [Security Policy](SECURITY.md).

---

# Support

If you need help, please read our [Support Guide](SUPPORT.md).

---

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

# Platform Comparison

| Feature | Traditional LLM | Thesis Specialist |
|---------|----------------|-------------------|
| Configuration | Manual setup required | Zero configuration |
| Workflow | Ad-hoc, may skip steps | Strict 8-phase process |
| Expertise | General purpose | Domain-specific experts |
| Output Quality | Variable | Verified and structured |
| Learning Curve | Steep | Minimal |
| Productivity | Moderate | High |

---

# Technical Specifications

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

# Contact

- GitHub Issues: [https://github.com/badhope/Thesis-Specialist-Agent/issues](https://github.com/badhope/Thesis-Specialist-Agent/issues)

---

**Last Updated: 2026-05-04**
