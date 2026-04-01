# Skills Index

Complete index of all 70 skills organized in two views:
1. **By Layer**: Enhanced HCSA 6-layer architecture (AI-friendly)
2. **By Function**: Functional categories (human-friendly)
3. **By Tier**: Complexity tier (for collaboration mode)

---

## HCSA v5.0 Fusion Architecture Overview

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

## Tier Classification

| Tier | Name | Architecture | Skill Count |
|------|------|--------------|-------------|
| **Tier 1** | Atomic Skills | Single Agent | ~40 |
| **Tier 2** | Composite Skills | Handoff Chain | ~20 |
| **Tier 3** | Complex Skills | Lead-Worker + Handoff | ~9 |


---

## Learning Layer (学习层) - NEW

Self-improvement and knowledge accumulation skills.

| Skill | Description | Location |
|-------|-------------|----------|
| reflector | Execution analysis and reflection | [learning/reflector](.trae/skills/learning/reflector) |
| strategy-learner | Strategy optimization from feedback | [learning/strategy-learner](.trae/skills/learning/strategy-learner) |
| self-enhancer | Capability enhancement and evolution | [learning/self-enhancer](.trae/skills/learning/self-enhancer) |
| knowledge-base | Knowledge storage and retrieval | [learning/knowledge-base](.trae/skills/learning/knowledge-base) |

---

## Meta Layer (战略层) - ENHANCED

Strategic planning and coordination skills.

| Skill | Description | Location |
|-------|-------------|----------|
| task-planner | Task decomposition and planning | [meta/task-planner](.trae/skills/meta/task-planner) |
| orchestrator | Execution coordination | [meta/orchestrator](.trae/skills/meta/orchestrator) |
| decomposition-planner | Advanced task decomposition | [meta/decomposition-planner](.trae/skills/meta/decomposition-planner) |
| task-registry | Task tracking and history | [meta/task-registry](.trae/skills/meta/task-registry) |

---

## Dispatcher Layer (调度层) - NEW

Model routing and resource management skills.

| Skill | Description | Location |
|-------|-------------|----------|
| model-router | Intelligent model routing | [dispatcher/model-router](.trae/skills/dispatcher/model-router) |
| concurrency-manager | Concurrent task management | [dispatcher/concurrency-manager](.trae/skills/dispatcher/concurrency-manager) |

---

## Workflow Layer (战术层) - ENHANCED

Process coordination skills.

| Skill | Description | Location |
|-------|-------------|----------|
| coding-workflow | Code implementation workflow | [workflows/coding-workflow](.trae/skills/workflows/coding-workflow) |
| debugging-workflow | Bug fixing workflow | [workflows/debugging-workflow](.trae/skills/workflows/debugging-workflow) |
| research-workflow | Systematic research workflow | [workflows/research-workflow](.trae/skills/workflows/research-workflow) |
| refactoring-workflow | Code refactoring workflow | [workflows/refactoring-workflow](.trae/skills/workflows/refactoring-workflow) |
| aggregation-processor | Result aggregation and conflict resolution | [workflows/aggregation-processor](.trae/skills/workflows/aggregation-processor) |
| hierarchical-debugger | Multi-granularity hierarchical debugger (MGDebugger) | [workflows/hierarchical-debugger](.trae/skills/workflows/hierarchical-debugger) |
| delta-debugger | Delta debugging - binary search for minimal failing input | [workflows/delta-debugger](.trae/skills/workflows/delta-debugger) |
| problem-decomposer | Systematic problem decomposition (Divide & Conquer) | [workflows/problem-decomposer](.trae/skills/workflows/problem-decomposer) |
| solution-merger | Merge subproblem solutions into final solution | [workflows/solution-merger](.trae/skills/workflows/solution-merger) |
| git-bisect-debugger | Git bisect - binary search commit history | [workflows/git-bisect-debugger](.trae/skills/workflows/git-bisect-debugger) |
| code-modularizer | Break monolithic code into clean modules | [workflows/code-modularizer](.trae/skills/workflows/code-modularizer) |
| iteration-controller | Control iterations, prevent infinite loops | [workflows/iteration-controller](.trae/skills/workflows/iteration-controller) |
| content-generator | Generate content - blogs, product descriptions | [workflows/content-generator](.trae/skills/workflows/content-generator) |
| progress-reporter | Report progress, show status, estimate ETA | [workflows/progress-reporter](.trae/skills/workflows/progress-reporter) |
| fallback-manager | Handle failures gracefully with fallback strategies | [workflows/fallback-manager](.trae/skills/workflows/fallback-manager) |
| human-in-the-loop | Involve human in decision making | [workflows/human-in-the-loop](.trae/skills/workflows/human-in-the-loop) |

---

## Action Layer (执行层)

Execution and operation skills.

| Skill | Description | Location |
|-------|-------------|----------|
| code-generator | Code generation | [actions/code-generator](.trae/skills/actions/code-generator) |
| test-generator | Test generation | [actions/test/test-generator](.trae/skills/actions/test/test-generator) |
| code-coverage | Coverage analysis | [actions/test/code-coverage](.trae/skills/actions/test/code-coverage) |
| documentation | Doc generation | [actions/documentation](.trae/skills/actions/documentation) |
| code-search | Code search | [actions/search](.trae/skills/actions/search) |
| api-design | API design | [actions/code/api-design](.trae/skills/actions/code/api-design) |
| code-formatting | Code formatting | [actions/code/code-formatting](.trae/skills/actions/code/code-formatting) |
| linting-config | Lint configuration | [actions/code/linting-config](.trae/skills/actions/code/linting-config) |
| cross-file-refactor | Cross-file refactoring | [actions/code/cross-file-refactor](.trae/skills/actions/code/cross-file-refactor) |
| git-operations | Git operations | [actions/tools/git-operations](.trae/skills/actions/tools/git-operations) |
| tool-use | Tool usage | [actions/tools/tool-use](.trae/skills/actions/tools/tool-use) |
| code-review | Code review | [actions/code-review](.trae/skills/actions/code-review) |
| dependency-analyzer | Dependency analysis | [actions/analysis/dependency-analyzer](.trae/skills/actions/analysis/dependency-analyzer) |
| error-analyzer | Error analysis | [actions/analysis/error-analyzer](.trae/skills/actions/analysis/error-analyzer) |

---

## Domain Layer (领域层)

Domain-specific expertise skills.

### AI/LLM

| Skill | Description | Location |
|-------|-------------|----------|
| langchain | LangChain framework | [domains/ai/langchain](.trae/skills/domains/ai/langchain) |
| prompt-engineering | Prompt optimization | [domains/ai/prompt-engineering](.trae/skills/domains/ai/prompt-engineering) |
| rag-system | RAG implementation | [domains/ai/rag-system](.trae/skills/domains/ai/rag-system) |
| openai | OpenAI API | [domains/ai/openai](.trae/skills/domains/ai/openai) |
| claude-api | Claude API | [domains/ai/claude-api](.trae/skills/domains/ai/claude-api) |
| agent-development | AI agent development | [domains/ai/agent-development](.trae/skills/domains/ai/agent-development) |
| llm-evaluation | LLM evaluation | [domains/ai/llm-evaluation](.trae/skills/domains/ai/llm-evaluation) |

### Backend

| Skill | Description | Location |
|-------|-------------|----------|
| python | Python development | [domains/backend/python](.trae/skills/domains/backend/python) |
| nodejs | Node.js development | [domains/backend/nodejs](.trae/skills/domains/backend/nodejs) |
| go | Go development | [domains/backend/go](.trae/skills/domains/backend/go) |
| rust | Rust development | [domains/backend/rust](.trae/skills/domains/backend/rust) |
| graphql | GraphQL API | [domains/backend/graphql](.trae/skills/domains/backend/graphql) |
| typescript | TypeScript | [domains/backend/typescript](.trae/skills/domains/backend/typescript) |

### Frontend

| Skill | Description | Location |
|-------|-------------|----------|
| react | React development | [domains/frontend/react](.trae/skills/domains/frontend/react) |
| vue | Vue development | [domains/frontend/vue](.trae/skills/domains/frontend/vue) |
| nextjs | Next.js framework | [domains/frontend/nextjs](.trae/skills/domains/frontend/nextjs) |
| css-tailwind | Tailwind CSS | [domains/frontend/css-tailwind](.trae/skills/domains/frontend/css-tailwind) |
| accessibility | Web accessibility | [domains/frontend/accessibility](.trae/skills/domains/frontend/accessibility) |
| i18n | Internationalization | [domains/frontend/i18n](.trae/skills/domains/frontend/i18n) |

### DevOps

| Skill | Description | Location |
|-------|-------------|----------|
| docker | Docker containerization | [domains/devops/docker](.trae/skills/domains/devops/docker) |
| kubernetes | K8s orchestration | [domains/devops/kubernetes](.trae/skills/domains/devops/kubernetes) |
| ci-cd-pipeline | CI/CD workflows | [domains/devops/ci-cd-pipeline](.trae/skills/domains/devops/ci-cd-pipeline) |
| monitoring | System monitoring | [domains/devops/monitoring](.trae/skills/domains/devops/monitoring) |

### Database

| Skill | Description | Location |
|-------|-------------|----------|
| sql-optimization | SQL optimization | [domains/database/sql-optimization](.trae/skills/domains/database/sql-optimization) |
| mongodb | MongoDB | [domains/database/mongodb](.trae/skills/domains/database/mongodb) |
| redis-caching | Redis caching | [domains/database/redis-caching](.trae/skills/domains/database/redis-caching) |
| database-migration | DB migration | [domains/database/database-migration](.trae/skills/domains/database/database-migration) |

### Testing

| Skill | Description | Location |
|-------|-------------|----------|
| unit-test | Unit testing | [domains/testing/unit-test](.trae/skills/domains/testing/unit-test) |
| integration-test | Integration testing | [domains/testing/integration-test](.trae/skills/domains/testing/integration-test) |
| e2e-test | E2E testing | [domains/testing/e2e-test](.trae/skills/domains/testing/e2e-test) |

### Mobile

| Skill | Description | Location |
|-------|-------------|----------|
| react-native | React Native | [domains/mobile/react-native](.trae/skills/domains/mobile/react-native) |
| flutter | Flutter | [domains/mobile/flutter](.trae/skills/domains/mobile/flutter) |

### Data

| Skill | Description | Location |
|-------|-------------|----------|
| etl | ETL pipeline | [domains/data/etl](.trae/skills/domains/data/etl) |
| data-validation | Data validation | [domains/data/data-validation](.trae/skills/domains/data/data-validation) |

### Security

| Skill | Description | Location |
|-------|-------------|----------|
| security-auditor | Security auditing | [domains/security/security-auditor](.trae/skills/domains/security/security-auditor) |
| prompt-injection-defense | Prompt injection defense | [domains/security/prompt-injection-defense](.trae/skills/domains/security/prompt-injection-defense) |

### Performance

| Skill | Description | Location |
|-------|-------------|----------|
| performance-optimizer | Performance optimization | [domains/performance/performance-optimizer](.trae/skills/domains/performance/performance-optimizer) |

### MCP

| Skill | Description | Location |
|-------|-------------|----------|
| mcp-server-development | MCP server dev | [domains/mcp/server-development](.trae/skills/domains/mcp/server-development) |
| mcp-tools | MCP tools | [domains/mcp/tools](.trae/skills/domains/mcp/tools) |

---

## By Function (Functional Categories) - Human-Friendly View

Skills organized by what they do, not by architecture layer.

### Code Development
| Skill | Description | Tier |
|-------|-------------|------|
| code-generator | Code generation | Tier 1 |
| api-design | API design | Tier 1 |
| code-formatting | Code formatting | Tier 1 |
| linting-config | Lint configuration | Tier 1 |
| cross-file-refactor | Cross-file refactoring | Tier 1 |
| code-review | Code review | Tier 1 |
| coding-workflow | Code implementation workflow | Tier 2 |
| refactoring-workflow | Code refactoring workflow | Tier 2 |
| problem-decomposer | Problem decomposition (Divide & Conquer) | Tier 2 |
| solution-merger | Merge subproblem solutions | Tier 2 |
| code-modularizer | Break monolith into modules | Tier 2 |

### Testing & Quality
| Skill | Description | Tier |
|-------|-------------|------|
| test-generator | Test generation | Tier 1 |
| code-coverage | Coverage analysis | Tier 1 |
| unit-test | Unit testing | Tier 1 |
| integration-test | Integration testing | Tier 1 |
| e2e-test | E2E testing | Tier 1 |
| debugging-workflow | Bug fixing workflow | Tier 2 |
| hierarchical-debugger | Multi-granularity hierarchical debugger | Tier 2 |
| delta-debugger | Delta debugging (binary search) | Tier 2 |
| git-bisect-debugger | Git bisect (commit binary search) | Tier 1 |
| error-analyzer | Error analysis | Tier 1 |

### AI & Agents
| Skill | Description | Tier |
|-------|-------------|------|
| langchain | LangChain framework | Tier 1 |
| prompt-engineering | Prompt optimization | Tier 1 |
| rag-system | RAG implementation | Tier 1 |
| openai | OpenAI API | Tier 1 |
| claude-api | Claude API | Tier 1 |
| agent-development | AI agent development | Tier 1 |
| llm-evaluation | LLM evaluation | Tier 1 |
| research-workflow | Systematic research workflow | Tier 2 |
| full-stack-development | Full stack project (NEW) | Tier 3 |
| enterprise-project | Enterprise project (NEW) | Tier 3 |
| research-paper-writing | Research paper writing (NEW) | Tier 3 |

### DevOps & Infrastructure
| Skill | Description | Tier |
|-------|-------------|------|
| docker | Docker containerization | Tier 1 |
| kubernetes | K8s orchestration | Tier 1 |
| ci-cd-pipeline | CI/CD workflows | Tier 1 |
| monitoring | System monitoring | Tier 1 |
| git-operations | Git operations | Tier 1 |
| tool-use | Tool usage | Tier 1 |

### Data & Database
| Skill | Description | Tier |
|-------|-------------|------|
| sql-optimization | SQL optimization | Tier 1 |
| mongodb | MongoDB | Tier 1 |
| redis-caching | Redis caching | Tier 1 |
| database-migration | DB migration | Tier 1 |
| etl | ETL pipeline | Tier 1 |
| data-validation | Data validation | Tier 1 |

### Frontend
| Skill | Description | Tier |
|-------|-------------|------|
| react | React development | Tier 1 |
| vue | Vue development | Tier 1 |
| nextjs | Next.js framework | Tier 1 |
| css-tailwind | Tailwind CSS | Tier 1 |
| accessibility | Web accessibility | Tier 1 |
| i18n | Internationalization | Tier 1 |

### Backend
| Skill | Description | Tier |
|-------|-------------|------|
| python | Python development | Tier 1 |
| nodejs | Node.js development | Tier 1 |
| go | Go development | Tier 1 |
| rust | Rust development | Tier 1 |
| graphql | GraphQL API | Tier 1 |
| typescript | TypeScript | Tier 1 |

### Security & Performance
| Skill | Description | Tier |
|-------|-------------|------|
| security-auditor | Security auditing | Tier 1 |
| prompt-injection-defense | Prompt injection defense | Tier 1 |
| performance-optimizer | Performance optimization | Tier 1 |

### Documentation & Search
| Skill | Description | Tier |
|-------|-------------|------|
| documentation | Doc generation | Tier 1 |
| code-search | Code search | Tier 1 |

### MCP
| Skill | Description | Tier |
|-------|-------------|------|
| mcp-server-development | MCP server dev | Tier 1 |
| mcp-tools | MCP tools | Tier 1 |

### Mobile
| Skill | Description | Tier |
|-------|-------------|------|
| react-native | React Native | Tier 1 |
| flutter | Flutter | Tier 1 |

---

## By Tier (Complexity Level)

### Tier 3: Complex Skills - Lead-Worker + Handoff
| Skill | Description | Layer |
|-------|-------------|-------|
| full-stack-development | Full stack project development (NEW) | Workflow |
| enterprise-project | Enterprise software project (NEW) | Workflow |
| research-paper-writing | Academic research paper writing (NEW) | Workflow |
| decomposition-planner | Advanced task decomposition | Meta |
| orchestrator | Multi-agent orchestration | Meta |
| aggregation-processor | Result aggregation with conflict resolution | Workflow |

### Tier 2: Composite Skills - Handoff Chain
| Skill | Description | Layer |
|-------|-------------|-------|
| coding-workflow | Code implementation workflow | Workflow |
| debugging-workflow | Bug fixing workflow | Workflow |
| research-workflow | Systematic research workflow | Workflow |
| refactoring-workflow | Code refactoring workflow | Workflow |
| hierarchical-debugger | Multi-granularity hierarchical debugger | Workflow |
| delta-debugger | Delta debugging (binary search) | Workflow |
| problem-decomposer | Problem decomposition (Divide & Conquer) | Workflow |
| solution-merger | Merge subproblem solutions | Workflow |
| code-modularizer | Break monolith into modules | Workflow |
| task-planner | Task decomposition and planning | Meta |
| model-router | Intelligent model routing | Dispatcher |
| concurrency-manager | Concurrent task management | Dispatcher |

### Tier 1: Atomic Skills - Single Agent
All remaining 58 skills (Actions, Domains, most Learning) are Tier 1 - single agent, focused, tool-light operations.

---

## Statistics

### By Layer
| Layer | Count |
|-------|-------|
| Learning | 4 |
| Meta | 4 |
| Dispatcher | 2 |
| Workflow | 19 (14 + 5 NEW) |
| Action | 14 |
| Domain | 39 |
| **Total** | **82** |

### By Tier
| Tier | Count |
|------|-------|
| Tier 1 | ~61 |
| Tier 2 | ~15 |
| Tier 3 | ~6 |
| **Total** | **82** |

---

## New Features in v5.0 - Fusion Architecture

### Learning Layer
- **Reflector**: Post-execution analysis and insight generation
- **Strategy Learner**: Pattern recognition and strategy optimization
- **Self-Enhancer**: Capability enhancement and prompt optimization
- **Knowledge Base**: Persistent knowledge storage with semantic search

### Dispatcher Layer
- **Model Router**: Intelligent model selection based on task complexity
- **Concurrency Manager**: Rate limiting, queuing, and parallel execution

### Enhanced Meta Layer
- **Decomposition Planner**: Advanced task decomposition with dependency analysis
- **Task Registry**: Persistent task tracking with history

### Enhanced Workflow Layer
- **Aggregation Processor**: Result aggregation with conflict resolution
