# Architecture

This document explains **why** this repository is structured the way it is, and **how** the different parts work together.

---

## Design Philosophy

This repository follows five core principles:

1. **Enhanced HCSA v5.0 Fusion Architecture**: 6-layer system with Lead-Worker + Handoff collaboration
2. **Tiered Complexity**: Not all skills need multi-agent - use single/chain/fusion as needed
3. **AI-First Discoverability**: Routing system enables AI to autonomously find, select, and compose skills
4. **Human-Friendly Index**: Dual views (by layer + by function) for easy navigation
5. **Self-Improvement**: Built-in learning and reflection capabilities

---

## HCSA v5.0 Fusion Architecture

The fusion architecture combines the best of:
- **Anthropic**: Lead-Worker structure with parallel sub-agents
- **OpenAI**: Handoff (移交) mechanism for seamless collaboration
- **Google Research**: Avoid multi-agent overhead for simple tasks

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEAD AGENT (Meta Layer)                      │
│  • Task planning & decomposition                                │
│  • Worker team assembly & assignment                            │
│  • Final result review & quality check                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼────────┐ ┌───▼────────┐ ┌──▼──────────┐
│ WORKER TEAM 1   │ │ WORKER TEAM 2│ │ WORKER TEAM N│
│  • Expert 1     │ │  • Expert A  │ │  • Expert X │
│  • Expert 2 ━━┓ │ │  • Expert B ━━┓│ │  • Expert Y ━━┓│
│  • Expert 3 ◀━┛ │ │  • Expert C ◀━┛│ │  • Expert Z ◀━┛│
│    (Handoff)     │ │   (Handoff)    │ │   (Handoff)     │
└────────┬─────────┘ └──────┬───────┘ └──────┬────────┘
         │                    │                 │
         └────────────────────┼─────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   RESULT AGGREGATOR │
                    │   (Workflow Layer) │
                    └─────────┬─────────┘
                              │
                              ▼
                 (6-layer HCSA pipeline)
```

---

## Tier Classification (When to Use What)

Based on Google 2026 research, we don't use multi-agent for everything.

| Tier | Name | Architecture | Use Case | Skill Count |
|------|------|--------------|----------|-------------|
| **Tier 1** | Atomic Skills | Single Agent | Simple, focused tasks | ~58 |
| **Tier 2** | Composite Skills | Handoff Chain | Multi-step sequential | ~7 |
| **Tier 3** | Complex Skills | Lead-Worker + Handoff | Complex, parallel, need QC | ~6 |

---

## Handoff Mechanism (OpenAI Style)

The handoff is a core innovation: Agent passes the baton like a relay race.

```
┌─────────────┐    handoff     ┌─────────────┐    handoff     ┌─────────────┐
│   Expert A  │ ━━━━━━━━━━━━━► │   Expert B  │ ━━━━━━━━━━━━━► │   Expert C  │
│  (Designer) │                │  (Coder)    │                │  (Tester)   │
└─────────────┘                └─────────────┘                └─────────────┘
       │                              │                              │
  context +                      context +                      context +
  partial result                 partial result                 final result
```

---

## Enhanced HCSA 6-Layer Pipeline

---

## Enhanced HCSA Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Learning Layer (学习层)                        │
│   reflector | strategy-learner | self-enhancer | knowledge-base│
│   - Execution analysis    - Pattern recognition              │
│   - Self-improvement      - Knowledge accumulation           │
│   - Feedback learning     - Strategy optimization            │
├─────────────────────────────────────────────────────────────┤
│               Meta Layer (战略层)                            │
│   task-planner | decomposition-planner | task-registry       │
│   - Strategic planning    - Task decomposition               │
│   - Dependency analysis   - Task tracking                    │
│   - Complexity assessment - Execution planning               │
├─────────────────────────────────────────────────────────────┤
│            Dispatcher Layer (调度层)                         │
│   model-router | concurrency-manager                         │
│   - Model routing         - Cost optimization                │
│   - Rate limiting         - Parallel execution               │
│   - Load balancing        - Circuit breaking                 │
├─────────────────────────────────────────────────────────────┤
│               Workflow Layer (战术层)                        │
│   coding-workflow | debugging-workflow | aggregation-processor│
│   - Process coordination  - State management                │
│   - Result aggregation    - Error recovery                  │
│   - Conflict resolution   - Consistency checking            │
├─────────────────────────────────────────────────────────────┤
│               Action Layer (执行层)                          │
│   code-generator | test-generator | documentation | ...     │
│   - Specific operations    - Tool calls                     │
│   - Data processing        - Code generation                │
├─────────────────────────────────────────────────────────────┤
│               Domain Layer (领域层)                          │
│   AI | Backend | Frontend | DevOps | Database | Security    │
│   - Domain-specific expertise                               │
│   - Best practices & patterns                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Learning Layer (学习层) - NEW
The Learning Layer enables self-improvement and knowledge accumulation:

| Component | Responsibility |
|-----------|---------------|
| **Reflector** | Post-execution analysis, issue identification, insight generation |
| **Strategy Learner** | Pattern recognition, strategy optimization from feedback |
| **Self-Enhancer** | Capability enhancement, prompt optimization, workflow improvement |
| **Knowledge Base** | Knowledge storage, semantic search, knowledge graph |

### Meta Layer (战略层) - ENHANCED
The Meta Layer handles strategic planning and task management:

| Component | Responsibility |
|-----------|---------------|
| **Task Planner** | Task decomposition, complexity assessment, execution planning |
| **Decomposition Planner** | Advanced decomposition with dependency analysis |
| **Task Registry** | Task tracking, status management, history persistence |
| **Orchestrator** | Workflow coordination, state management, error recovery |

### Dispatcher Layer (调度层) - NEW
The Dispatcher Layer manages model routing and resource allocation:

| Component | Responsibility |
|-----------|---------------|
| **Model Router** | Complexity assessment, model selection, cost optimization |
| **Concurrency Manager** | Rate limiting, request queuing, parallel execution |

### Workflow Layer (战术层) - ENHANCED
The Workflow Layer coordinates process execution:

| Component | Responsibility |
|-----------|---------------|
| **Coding Workflow** | Code implementation process |
| **Debugging Workflow** | Bug fixing process |
| **Aggregation Processor** | Result aggregation, conflict resolution, consistency checking |

### Action Layer (执行层)
The Action Layer executes specific operations:

| Component | Responsibility |
|-----------|---------------|
| **Code Generator** | Code generation |
| **Test Generator** | Test generation |
| **Documentation** | Documentation generation |
| **Code Search** | Code search and navigation |

### Domain Layer (领域层)
The Domain Layer provides domain-specific expertise:

| Domain | Skills |
|--------|--------|
| **AI/LLM** | langchain, prompt-engineering, rag-system, agent-development |
| **Backend** | python, nodejs, go, rust, graphql |
| **Frontend** | react, vue, nextjs, tailwind |
| **DevOps** | docker, kubernetes, ci-cd-pipeline |
| **Database** | mongodb, redis, sql-optimization |
| **Security** | prompt-injection-defense, security-auditor |

---

## Directory Structure

```
.trae/skills/
├── learning/           # Self-improvement skills (NEW)
│   ├── reflector/      # Execution reflection
│   ├── strategy-learner/ # Strategy optimization
│   ├── self-enhancer/  # Capability enhancement
│   └── knowledge-base/ # Knowledge storage
├── meta/               # Strategic planning skills
│   ├── task-planner/   # Task decomposition
│   ├── decomposition-planner/ # Advanced decomposition
│   ├── task-registry/  # Task tracking
│   └── orchestrator/   # Execution coordination
├── dispatcher/         # Model routing skills (NEW)
│   ├── model-router/   # Model selection
│   └── concurrency-manager/ # Concurrent execution
├── workflows/          # Process coordination skills
│   ├── coding-workflow/
│   ├── debugging-workflow/
│   ├── aggregation-processor/ # Result aggregation
│   └── ...
├── actions/            # Execution skills
│   ├── code-generator/
│   ├── test/
│   ├── documentation/
│   └── tools/
├── domains/            # Domain-specific skills
│   ├── ai/
│   ├── backend/
│   ├── frontend/
│   ├── devops/
│   ├── database/
│   ├── testing/
│   ├── mobile/
│   ├── data/
│   ├── security/
│   ├── performance/
│   └── mcp/
├── config/             # Configuration files
│   ├── routing.yaml    # Routing rules (v3.0)
│   └── storage-schema.yaml # Database schema
└── shared/             # Shared resources
    └── schemas/        # JSON schemas
```

---

## Why This Structure?

### Layer Separation

| Layer | Responsibility | When to Use |
|-------|---------------|-------------|
| **Learning** | Self-improvement | Post-execution, periodic optimization |
| **Meta** | Strategic decisions | Complex tasks (complexity > 5) |
| **Dispatcher** | Resource allocation | Model selection, concurrent execution |
| **Workflow** | Process coordination | Medium tasks (complexity 3-5) |
| **Action** | Execute operations | Simple tasks (complexity < 3) |
| **Domain** | Domain expertise | Domain-specific tasks |

### Routing System

The `config/routing.yaml` file defines:
- Layer execution order
- Complexity thresholds for each layer
- Keyword-based routing rules
- Model routing matrix
- Learning configuration

### Skill Composition

Skills can invoke other skills:
```
Learning Layer → Meta Layer → Dispatcher Layer → Workflow Layer → Action Layer → Domain Layer
```

---

## Model Routing

The Dispatcher Layer implements intelligent model routing:

```yaml
complexity_levels:
  LOW:      → gpt-3.5-turbo    (simple tasks, cost-efficient)
  MEDIUM:   → gpt-4o-mini      (balanced performance)
  HIGH:     → gpt-4o           (complex reasoning)
  CRITICAL: → claude-3-opus    (expert-level tasks)
```

### Routing Factors
- Task complexity score
- Token estimation
- Cost optimization
- Latency requirements
- Model availability

---

## Learning System

The Learning Layer implements a continuous improvement cycle:

```
┌─────────────────────────────────────────────────────────┐
│                    Learning Cycle                        │
│                                                          │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │ Execute  │───▶│ Reflect  │───▶│  Learn   │         │
│   └──────────┘    └──────────┘    └──────────┘         │
│        ▲                                 │              │
│        └─────────────────────────────────┘              │
│                    Improve                               │
└─────────────────────────────────────────────────────────┘
```

### Learning Components
1. **Reflection**: Analyze execution results
2. **Pattern Recognition**: Identify success/failure patterns
3. **Strategy Optimization**: Update strategies based on feedback
4. **Knowledge Accumulation**: Store and retrieve knowledge

---

## Skill Metadata

Each skill has standardized frontmatter:

```yaml
---
name: skill-name
description: "Description of the skill"
layer: learning | meta | dispatcher | workflow | action | domain
role: learner | planner | router | coordinator | executor | expert
version: 2.0.0
invokes: []        # Skills this skill calls
invoked_by: []     # Skills that call this skill
capabilities: []   # What this skill can do
triggers:
  keywords: []     # Keywords that trigger this skill
metrics: {}        # Performance metrics
---
```

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config/routing.yaml` | Task routing rules (v3.0) |
| `config/storage-schema.yaml` | Database schema for persistence |
| `shared/schemas/task.json` | Task schema |
| `shared/schemas/result.json` | Result schema |

---

## Persistent Storage

The system uses SQLite for persistent storage:

| Database | Purpose |
|----------|---------|
| `tasks.db` | Task registry and history |
| `knowledge.db` | Knowledge base and learning records |
| `metrics.db` | Performance metrics and analytics |

### Key Features
- Task status tracking
- Knowledge item storage with embeddings
- Learning record persistence
- Cost and performance metrics

---

## Comparison with Original HCSA

| Feature | Original HCSA | Enhanced HCSA |
|---------|---------------|---------------|
| Layers | 4 | 6 |
| Learning | None | Dedicated layer |
| Model Routing | None | Dedicated layer |
| Task Tracking | Basic | Full registry |
| Knowledge Storage | None | Persistent KB |
| Self-Improvement | None | Built-in |
| Cost Optimization | None | Model routing |
