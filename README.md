# AI Skill & Prompt Repository

[English](README.md) · [中文](README.zh-CN.md)

---

[![Version](https://img.shields.io/badge/version-v2.0.0-blue.svg)](https://github.com/badhope/skill)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellowgreen.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-orange.svg)](LICENSE-CONTENT)
[![GitHub stars](https://img.shields.io/github/stars/badhope/skill?style=social)](https://github.com/badhope/skill)
[![GitHub forks](https://img.shields.io/github/forks/badhope/skill?style=social)](https://github.com/badhope/skill)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/badhope/skill/graphs/commit-activity)

---

## 🎯 Overview

**AI Skill & Prompt Repository** is a modular **AI Skill/Prompt/Workflow** knowledge base designed for developers seeking efficient programming and intelligent workflows.

| Target Users | Core Value |
|--------------|------------|
| **Developers** | Quickly find, copy, and use high-quality prompts |
| **AI Systems** | Autonomously understand, route, select, and combine skills |
| **Researchers** | Academic writing, research assistance, literature retrieval |
| **Creators** | Creative writing, content generation, inspiration |

**Core Tech Stack:** GPT-4 · Claude · Reinforcement Learning · Context Memory · MCP Tools

---

## ⭐ Why Choose This Project?

| Feature | Description |
|---------|-------------|
| 🏆 **132+ Curated Prompts** | Covering coding, debugging, learning, creative scenarios |
| 🎯 **78+ Standardized Skills** | Modular design, plug-and-play |
| 🔧 **10+ Pre-built Workflows** | Ready-to-use multi-step task flows |
| 🧠 **Context Memory System** | <100ms semantic search response |
| 🤖 **Reinforcement Learning Engine** | Adaptive workflow optimization |
| 🔌 **MCP Tool Framework** | Extensible code quality detection, document generation |
| 📚 **Academic Writing Suite** | Literature search, paper optimization, plagiarism detection |
| 🎨 **Creative Content Generation** | Novel writing, professional copy, multimodal generation |
| 🌐 **Bilingual Support** | Complete Chinese and English documentation |

---

## 🚀 Core Capabilities

### 🧠 Context Memory System

Hierarchical memory architecture with semantic search:

| Memory Type | TTL | Capacity | Use Case |
|-------------|-----|----------|----------|
| **Short-term** | 1 hour | 100 items | Current conversation context |
| **Medium-term** | 2 hours | Unlimited | Session-level information |
| **Long-term** | Permanent | Unlimited | Cross-session knowledge |

**Core Features:**
- Semantic similarity search (response time <100ms)
- Importance scoring and decay mechanism
- Timestamp version control for conflict resolution
- Tag and embedding vector-based search

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

**Capability Matrix:**
- Multi-dimensional reward functions (code quality, solution efficiency, user satisfaction)
- Priority sampling experience replay
- Dynamic ε decay for exploration-exploitation balance
- Code simulation and execution environment

### 🔧 MCP Tools Framework

Extensible tool framework with professional modules:

| Tool | Description |
|------|-------------|
| **CodeQualityCheckerTool** | Static code analysis, style checking |
| **UnitTestGeneratorTool** | Automated test generation |
| **APIDocGeneratorTool** | OpenAPI/Swagger documentation generation |
| **RefactoringAssistantTool** | Code smell detection and refactoring suggestions |
| **CodeGeneratorTool** | MCU code generation |
| **PeripheralDriverTool** | GPIO, UART, SPI, I2C driver generation |

---

## 📚 Academic & Professional Tools

### 🔬 Academic Writing Suite

| Module | Function |
|--------|----------|
| **Context-Aware Literature Search** | Semantic search of research databases |
| **Research Paper Enhancement** | Structure optimization, clarity improvement |
| **Plagiarism Detection** | Originality verification and citation checking |
| **Academic Integrity Verification** | Academic integrity verification |

### 🎓 Learning Support Modules

- Adaptive learning path recommendation
- Knowledge gap identification
- Spaced repetition scheduling
- Progress tracking and assessment

### ✍️ Professional Writing Tools

- Multi-audience tone adaptation (formal/casual/technical)
- Brand voice consistency checking
- A/B title optimization
- Call-to-action effectiveness analysis

---

## 🎨 Creative Content Generation

### 📖 Fiction & Story Development

| Feature | Description |
|---------|-------------|
| **Narrative Structure Assistance** | Three-act, Hero's Journey, Save the Cat |
| **Character Development** | Archetype mapping, motivation analysis |
| **Worldbuilding** | Consistency checking, world management |
| **Dialogue Generation** | Tone adaptation, character voice maintenance |

### 🎬 Multimodal Content Generation

| Modality | Capability |
|----------|------------|
| **Text-to-Image** | Stable Diffusion integration ready |
| **Text-to-Video** | Storyboard generation, scene description |
| **Audio-Visual** | Subtitle sync, audio description |

### 🤖 Intelligent Agent Toolkit

- Customizable behavior patterns
- Persona configuration
- Memory and context management
- Tool use workflow integration

---

## 🏗️ Architecture

### 📦 Modular Architecture

```
src/
├── context_memory/     # Layered memory + semantic search
│   ├── stores.py       # Short/medium/long-term storage
│   ├── semantic_search.py  # Vector operations, similarity
│   └── manager.py      # Memory orchestration
├── rl_engine/          # Reinforcement learning
│   ├── engine.py       # RL core implementation
│   ├── ppo.py          # Policy/Value networks
│   └── reward.py       # Reward calculation
├── coding_engine/      # Code analysis and generation
│   ├── analyzer.py     # Syntax analysis
│   ├── quality.py      # Code quality checking
│   ├── patterns.py     # Design pattern library
│   └── algorithms.py   # Algorithm implementation
├── network/            # Distributed communication
│   └── communication.py  # Service mesh, load balancing
├── mcp_tools/          # MCP tool framework
│   ├── framework.py    # Tool orchestration
│   ├── tools.py        # Built-in tools
│   └── mcu_tools.py    # MCU code generation
└── special/            # Special function modules
    └── modules.py      # Animation, games, simulation, etc.
```

---

## ✨ Repository at a Glance

| Category | Count | Description |
|----------|:-----:|-------------|
| **Prompts** | 132+ | Coding, debugging, planning, research prompts |
| **Skills** | 78+ | AI task routing capability definitions |
| **Workflows** | 10+ | Multi-step execution flows |
| **Tool-Use Guides** | 8+ | File reading, command execution methods |
| **Output Formats** | 6+ | JSON, YAML, Markdown, Table, Checklist, Report |
| **Meta Prompts** | 8+ | Prompt engineering tools |
| **Special Modules** | 6 | Animation, games, simulation, etc. |

---

## 🚀 Quick Navigation

### For Human Users

> **"I want AI to..."**

| Task | Link |
|------|------|
| 🔨 Generate or modify code | [prompts/task/coding/](prompts/task/coding/) |
| 🐛 Debug and fix bugs | [prompts/task/debugging/](prompts/task/debugging/) |
| 📊 Understand code repository | [prompts/task/repo-analysis/](prompts/task/repo-analysis/) |
| 📋 Create execution plans | [prompts/task/planning/](prompts/task/planning/) |
| 🔬 Conduct research | [prompts/task/research/](prompts/task/research/) |
| 🔄 Execute multi-step workflows | [prompts/workflow/](prompts/workflow/) |
| 📤 Output specific formats | [prompts/output/](prompts/output/) |
| 🛠️ Optimize prompts | [prompts/meta/](prompts/meta/) |
| 📧 Daily email writing | [prompts/everyday/](prompts/everyday/) |
| ✅ Checklist generation | [prompts/everyday/prompt-everyday-checklist.md](prompts/everyday/) |

---

### For AI Systems

**Bootstrap Sequence** — Read files in this order:

```
1. START-HERE.md              → Entry point
2. ARCHITECTURE.md            → Design philosophy
3. ASSET-MAP.md               → Complete inventory
4. INDEX.md                   → Structure overview
5. registry/prompts-registry.yaml  → Discover prompts
6. registry/routes-registry.yaml   → Learn routing
7. AI-USAGE.md                → Usage patterns
8. AI-ROUTING.md              → Routing logic
9. AI-BOOTSTRAP.md            → Initial setup
```

---

## 📈 Statistics

| Metric | Value |
|--------|-------|
| 📝 Prompts | 132+ |
| 🎯 Skills | 78+ |
| 🔧 Workflows | 10+ |
| ⚙️ Source Modules | 6 |
| 📚 Documentation | 50+ |
| 🌍 Languages | 2 (EN/ZH) |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**How to Contribute:**

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 📄 License

This project uses dual licensing:

- **Code**: [Apache-2.0 License](LICENSE-CODE)
- **Content**: [CC BY 4.0 License](LICENSE-CONTENT)

---

## 🔗 Related Links

| Link | Description |
|------|-------------|
| [📦 NPM Package](https://npmjs.com/) | Frontend component package (coming soon) |
| [🐍 PyPI Package](https://pypi.org/) | Python SDK (coming soon) |
| [📖 Documentation](https://github.com/badhope/skill/wiki) | Full documentation |
| [🐛 Issue Tracker](https://github.com/badhope/skill/issues) | Bug reports |
| [💬 Discussions](https://github.com/badhope/skill/discussions) | Community discussions |

---

## 📬 Contact

- **GitHub**: [badhope](https://github.com/badhope)
- **Project Link**: [https://github.com/badhope/skill](https://github.com/badhope/skill)

---

<div align="center">
  <strong>If this project helps you, please give it a ⭐</strong>
  <br>
  <em>Built with ❤️ by badhope</em>
</div>
