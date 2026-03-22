# AI Skill & Prompt Repository

<!-- ==================== METADATA ==================== -->
<!--
  repository: badhope/skill
  version: v2.0.0
  description: Modular AI Skill/Prompt/Workflow repository with advanced technical capabilities
  topics: [ai, prompts, skills, workflows, coding, debugging, mcp, rl-engine, academic, creative]
-->
<!-- ================================================= -->

<!-- Language Switcher -->
[English](README.md) · [中文](README.zh-CN.md)

---

[![Version](https://img.shields.io/badge/version-v2.0.0-blue.svg)](https://github.com/badhope/skill)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellowgreen.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-orange.svg)](LICENSE-CONTENT)
[![GitHub stars](https://img.shields.io/github/stars/badhope/skill?style=social)](https://github.com/badhope/skill)

---

## 🎯 Overview

A modular **AI Skill/Prompt/Workflow** repository with advanced technical capabilities designed for both:

| Audience | Needs |
|----------|-------|
| **Human Users** | Quick find, copy, and use of prompts |
| **AI Systems** | Autonomous understanding, routing, selection, and composition |

This repository integrates cutting-edge AI technologies including reinforcement learning, context memory systems, MCP tools, and specialized modules for academic and creative applications.

---

## 🚀 Core Capabilities

### 🧠 Context Memory System
Hierarchical memory architecture with semantic search capabilities:

| Memory Type | TTL | Capacity | Use Case |
|-------------|-----|----------|----------|
| **Short-Term** | 1 hour | 100 entries | Current conversation context |
| **Medium-Term** | 2 hours | Unlimited | Session-long information |
| **Long-Term** | Permanent | Unlimited | Cross-session knowledge |

**Key Features:**
- Semantic similarity retrieval (<100ms response)
- Importance scoring and decay mechanisms
- Conflict resolution with timestamp versioning
- Tag-based and embedding-based search

### 🤖 Reinforcement Learning Engine
PPO-based RL framework for adaptive workflow optimization:

```python
from rl_engine import RLEngine, RLConfig

config = RLConfig(
    state_dim=128,
    action_dim=10,
    learning_rate=0.001,
    gamma=0.99
)
engine = RLEngine(config)
```

**Capabilities:**
- Multi-dimensional reward functions (code quality, solving efficiency, user satisfaction)
- Experience replay with prioritized sampling
- Exploration-exploitation balance with dynamic epsilon decay
- Code simulation and execution environment

### 🔧 MCP (Model Control Program) Tools
Extensible tool framework with specialized modules:

| Tool | Description |
|------|-------------|
| **CodeQualityCheckerTool** | Static code analysis, style checking |
| **UnitTestGeneratorTool** | Automated test generation |
| **APIDocGeneratorTool** | OpenAPI/Swagger documentation |
| **RefactoringAssistantTool** | Code smell detection and refactoring suggestions |
| **CodeGeneratorTool** | MCU code generation |
| **PeripheralDriverTool** | GPIO, UART, SPI, I2C driver generation |

---

## 📚 Academic & Professional Tools

### 🔬 Academic Writing Suite

| Module | Function |
|--------|----------|
| **Context-Aware Literature Search** | Semantic search across research databases |
| **Research Paper Enhancement** | Structure optimization, clarity improvement |
| **Plagiarism Detection** | Originality verification and citation checking |
| **Academic Integrity Verification** | Integrity validation for scholarly work |

### 🎓 Learning Support Modules

- Adaptive learning path recommendations
- Knowledge gap identification
- Spaced repetition scheduling
- Progress tracking and assessment

---

## 🎨 Creative Content Generation Suite

### ✍️ Fiction & Story Development

| Feature | Description |
|---------|-------------|
| **Narrative Structure Assistance** | Three-act structure, hero's journey, save the cat |
| **Character Development** | Archetype mapping, motivation analysis |
| **World Building** | Consistency checking, lore management |
| **Dialogue Generation** | Tone adaptation, character voice preservation |

### 📝 Professional Copywriting Tools

- Tone adaptation across audiences (formal, casual, technical)
- Brand voice consistency checking
- A/B headline optimization
- Call-to-action effectiveness analysis

### 🎬 Multimodal Content Generation

| Modality | Capability |
|----------|-----------|
| **Text-to-Image** | Stable Diffusion integration ready |
| **Text-to-Video** | Storyboard generation, scene description |
| **Audio-Visual** | Subtitle synchronization, audio description |

### 🤖 Intelligent Agent Development Toolkit

- Customizable behavior patterns
- Personality configuration
- Memory and context management
- Tool-use workflow integration

---

## 🏗️ Architectural Improvements

### 📦 Modular Architecture

```
src/
├── context_memory/     # Hierarchical memory with semantic search
│   ├── stores.py       # Short/Medium/Long-term storage
│   ├── semantic_search.py  # Vector operations, similarity
│   └── manager.py      # Memory orchestration
├── rl_engine/          # Reinforcement learning
│   ├── engine.py       # RL core implementation
│   ├── ppo.py          # Policy/Value networks
│   └── reward.py       # Reward calculation
├── coding_engine/     # Code analysis & generation
│   ├── analyzer.py     # Syntax analysis
│   ├── quality.py      # Code quality checking
│   ├── patterns.py     # Design pattern library
│   └── algorithms.py   # Algorithm implementations
├── network/           # Distributed communication
│   └── communication.py  # Service mesh, load balancing
├── mcp_tools/        # MCP tool framework
│   ├── framework.py    # Tool orchestration
│   ├── tools.py       # Built-in tools
│   └── mcu_tools.py   # MCU code generation
└── special/          # Specialized modules
    └── modules.py     # Animation, Game, Simulation, etc.
```

### ⚡ Performance Optimization

| Optimization | Technique |
|-------------|-----------|
| **Computational Efficiency** | Vectorized operations, async/await patterns |
| **Step Minimization** | Parallel execution, caching |
| **Text Compression** | Token optimization, structured output |
| **Quality Enhancement** | RL-based feedback loops |

---

## ✨ Repository at a Glance

| Category | Count | Description |
|----------|:-----:|-------------|
| **Prompts** | 132+ | Ready-to-use prompts for coding, debugging, planning, research |
| **Skills** | 14 | Capability definitions for AI task routing |
| **Workflows** | 10 | Multi-step execution flows |
| **Tool-Use Guides** | 8 | Systematic approaches to file reading, command execution |
| **Output Formats** | 6 | JSON, YAML, Markdown, tables, checklists, reports |
| **Meta Prompts** | 8 | Prompt engineering tools |

---

## 🚀 Quick Navigation

### For Human Users

> **"I want AI to..."**

| Task | → Go To |
|------|---------|
| 🔨 Generate or modify code | [prompts/task/coding/](prompts/task/coding/) |
| 🐛 Debug and fix bugs | [prompts/task/debugging/](prompts/task/debugging/) |
| 📊 Understand a repository | [prompts/task/repo-analysis/](prompts/task/repo-analysis/) |
| 📋 Create execution plans | [prompts/task/planning/](prompts/task/planning/) |
| 🔬 Conduct research | [prompts/task/research/](prompts/task/research/) |
| 🔄 Execute multi-step workflows | [prompts/workflow/](prompts/workflow/) |
| 📤 Output specific formats | [prompts/output/](prompts/output/) |
| 🛠️ Optimize prompts | [prompts/meta/](prompts/meta/) |

---

### For AI Systems

**Bootstrap Sequence** — Read files in this order:

```
1. START-HERE.md              → Entry point
2. ARCHITECTURE.md            → Design rationale
3. ASSET-MAP.md               → Complete inventory
4. INDEX.md                   → Structure overview
5. registry/prompts-registry.yaml  → Discover prompts
6. registry/routes-registry.yaml   → Learn routing
7. AI-USAGE.md                → Usage patterns
8. AI-ROUTING.md              → Routing logic
9. AI-BOOTSTRAP.md            → First-time setup
```

---

## 📂 Repository Structure

```
skill/
│
├── 🎯 ENTRY DOCUMENTS
├── START-HERE.md              ← Start here (humans & AI)
├── ARCHITECTURE.md            ← Why this structure
├── ASSET-MAP.md               ← Complete asset inventory
├── DECISION-LOG.md            ← Key decisions & rationale
├── EXTENSION-GUIDE.md         ← How to add new assets
├── MAINTENANCE-RULES.md       ← Standards & conventions
├── QUALITY-STANDARDS.md       ← Quality requirements
│
├── 📖 CORE ENTRY
├── README.md                   ← You are here
├── README.zh-CN.md            ← Chinese version
├── INDEX.md                   ← Master index
│
├── 💬 PROMPTS
├── prompts/
│   ├── _routing/              ← AI routing prompts
│   ├── _core/                 ← Standards & specs
│   ├── system/                ← System prompts
│   ├── task/                   │ ← Task-specific
│   │   ├── coding/            │    20 prompts
│   │   ├── debugging/         │    20 prompts
│   │   ├── repo-analysis/     │    10 prompts
│   │   ├── planning/          │    2 prompts
│   │   ├── research/          │    1 prompt
│   │   ├── refactoring/       │    8 prompts
│   │   ├── testing/           │    8 prompts
│   │   ├── engineering-planning/│  8 prompts
│   │   ├── documentation-for-code/│ 6 prompts
│   │   └── code-review/       │    8 prompts
│   ├── general/                │ ← General capabilities
│   │   ├── clarification/     │    8 prompts
│   │   ├── context-memory/    │    8 prompts
│   │   ├── reasoning/         │    7 prompts
│   │   ├── search/            │    7 prompts
│   │   ├── user-style-adaptation/│ 8 prompts
│   │   ├── long-term-assistant/│  8 prompts
│   │   ├── creative-special/  │   10 prompts
│   │   ├── personal/          │    6 prompts
│   │   ├── reflection/        │    6 prompts
│   │   └── learning-support/  │    8 prompts
│   ├── workflow/               │ ← 10 workflows
│   ├── tool-use/               │ ← 8 tool guides
│   ├── output/                  │ ← 6 output formats
│   └── meta/                   │ ← 8 meta prompts
│
├── 🎯 SKILLS
├── skills/                     ← Canonical skill directory
│   ├── ai-routing/
│   ├── routing/
│   ├── coding/
│   ├── debugging/
│   ├── planning/
│   ├── repo-analysis/
│   ├── research/
│   ├── tool-use/
│   ├── prompt-composition/
│   ├── system-prompts/
│   ├── workflows/
│   ├── writing/
│   ├── data-visualization/
│   ├── devops/
│   ├── mcu/
│   ├── security/
│   ├── learning-support/
│   ├── reflection/
│   ├── personal/
│   └── creative-special/
│
├── 🔧 SRC (Technical Implementation)
├── src/
│   ├── context_memory/        # Memory system
│   ├── rl_engine/             # RL framework
│   ├── coding_engine/         # Code analysis
│   ├── network/               # Communication
│   ├── mcp_tools/             # MCP framework
│   └── special/               # Specialized modules
│
├── 📚 REGISTRY (AI-readable)
├── registry/
│   ├── prompts-registry.yaml   ← All prompts metadata
│   ├── skills-registry.yaml    ← All skills metadata
│   ├── routes-registry.yaml    ← Task routing rules
│   ├── relations-registry.yaml ← Asset relationships
│   └── tags-registry.yaml     ← Unified tag dictionary
│
├── 📎 EXAMPLES & CURATIONS
├── examples/                   ← Real-world usage examples
│   ├── coding/
│   ├── debugging/
│   ├── general/
│   └── creative-special/
│
├── author-picks/               ← Maintainer recommendations
│
├── 📚 DOCUMENTATION
├── docs/guides/
│   ├── SPEC.md                ← Complete specification
│   └── templates/             ← Asset templates
│
├── 🤖 AI GUIDES
├── AI-USAGE.md                 ← Usage patterns
├── AI-ROUTING.md               ← Routing logic
├── AI-BOOTSTRAP.md             ← Bootstrap guide
│
└── 📄 PROJECT DOCS
├── CHANGELOG.md               ← Version history
├── PROJECT-PLAN.md            ← Roadmap
├── CONTRIBUTING.md            ← Contribution guide
├── CODE_OF_CONDUCT.md         ← Community code
├── SECURITY.md                ← Security policy
└── LICENSE*                   ← Licensing info
```

---

## 🧪 Testing & Quality Assurance

### Test Coverage

| Module | Tests | Status |
|--------|-------|--------|
| context_memory | 15+ | ✅ Passing |
| rl_engine | 20+ | ✅ Passing |
| coding_engine | 25+ | ✅ Passing |
| network | 15+ | ✅ Passing |
| mcp_tools | 20+ | ✅ Passing |
| special | 26+ | ✅ Passing |
| **Total** | **156** | **✅ All Passing** |

### Run Tests

```bash
# Set PYTHONPATH and run all tests
export PYTHONPATH=src
pytest tests/ -v

# Run specific module tests
pytest tests/test_context_memory.py -v
pytest tests/test_rl_engine.py -v
pytest tests/test_coding_engine.py -v
```

---

## 🔀 How Routing Works

```
1. AI parses user request
       │
       ▼
2. Match against trigger_patterns in routes-registry.yaml
       │
       ▼
3. Select recommended primary_prompt + supporting_prompts
       │
       ▼
4. Check relations-registry.yaml for related assets
       │
       ▼
5. Execute with selected prompts in sequence
```

---

## 🎯 Core Task Coverage

| Task | Primary Prompt | Supporting |
|------|---------------|------------|
| **Coding** | generate-code-from-requirement | read-files, output-markdown |
| **Debugging** | identify-root-cause | generate-plan, fix-bug, verify |
| **Repo Analysis** | analyze-repository-structure | read-files, summarize-arch |
| **Planning** | break-down-task | create-execution-plan, output-checklist |
| **Research** | prepare-research-brief | output-markdown-report |
| **Prompt Eng.** | debug-failing-prompt | shorten, evaluate, adapt |

---

## 🔒 Dual Licensing Model

| License | Applies To |
|---------|------------|
| **Apache-2.0** | Code, scripts, configs (`.trae/skills/`, configs) |
| **CC BY 4.0** | Content assets (prompts, workflows, skills, docs) |

> ℹ️ Use Apache-2.0 content freely. Use CC BY 4.0 content with attribution.

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📌 Version Info

| Item | Value |
|------|-------|
| **Current Version** | **v2.0.0** |
| **Release Date** | 2026-03-22 |

Major additions in v2.0.0:
- Context Memory System with semantic search
- Reinforcement Learning Engine integration
- MCP Tool Framework with MCU support
- Special Modules (Animation, Game, Simulation)
- Academic & Creative tool suites

See [CHANGELOG.md](CHANGELOG.md) for detailed history.

---

## 🔗 Quick Reference

| Need | → Go To |
|------|---------|
| Global index | [INDEX.md](INDEX.md) |
| Prompts index | [prompts/INDEX.md](prompts/INDEX.md) |
| AI usage | [AI-USAGE.md](AI-USAGE.md) |
| AI routing | [AI-ROUTING.md](AI-ROUTING.md) |
| Technical docs | [docs/ARCHITECTURE-DETAILED.md](docs/ARCHITECTURE-DETAILED.md) |
