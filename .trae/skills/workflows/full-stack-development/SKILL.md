---
name: full-stack-development
description: "Tier 3: Lead-Worker + Handoff architecture for full stack project development. Keywords: full stack, web app, frontend backend, vue react go node, 全栈, 前后端"
layer: workflow
role: lead-coordinator
tier: 3
version: 5.0.0
architecture: lead-worker-handoff
invokes:
  - decomposition-planner
  - orchestrator
  - coding-workflow
  - api-design
  - research-workflow
  - aggregation-processor
  - task-registry
  - model-router
invoked_by:
  - meta-layer-orchestrator
  - lead-agent
capabilities:
  - lead_worker_coordination
  - parallel_worker_teams
  - handoff_mechanism
  - quality_review
  - result_integration
triggers:
  keywords:
    - full stack
    - web application
    - frontend backend
    - fullstack
    - vue go
    - react node
    - 全栈
    - 前后端
    - 网站开发
  conditions:
    - "task requires both frontend and backend"
    - "project involves multiple technologies"
    - "needs end-to-end delivery"
metrics:
  avg_execution_time: 45m
  success_rate: 0.85
  worker_teams: 3
  handoffs_per_team: 2-3
---

# Full Stack Development - Tier 3

> **Tier 3 Complex Skill**: Lead-Worker + Handoff architecture for full stack projects.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  LEAD AGENT (This Skill)                     │
│  • Task planning & decomposition                              │
│  • Worker team assembly & assignment                          │
│  • Final result review & quality check                        │
└──────────────────────┬────────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼────────┐ ┌──▼──────────┐ ┌──▼──────────────┐
│ WORKER TEAM 1   │ │ WORKER TEAM 2│ │ WORKER TEAM 3   │
│  Backend        │ │  Frontend    │ │  DevOps/Testing  │
│  • API Design  ━━┓│  • UI Design ━━┓│  • CI/CD Setup  ━━┓│
│  • Code Gen    ◀━┛│  • Components ◀━┛│  • Tests        ◀━┛│
│  • Testing       │ │  • Integration │ │  • Deployment    │
│    (Handoff)     │ │    (Handoff)   │ │    (Handoff)     │
└────────┬─────────┘ └──────┬─────────┘ └──────┬───────────┘
         │                    │                   │
         └────────────────────┼───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   RESULT AGGREGATOR │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │   LEAD REVIEW       │
                    │   (Quality Check)   │
                    └─────────────────────┘
```

## Lead Agent Responsibilities

You are the **Lead Agent** for full stack development. Your job:

1. **Decompose** the full stack task into backend, frontend, and devops sub-tasks
2. **Assign** Worker Teams to each sub-task
3. **Coordinate** parallel execution of Worker Teams
4. **Review** all outputs and ensure quality
5. **Integrate** results into a coherent final deliverable

## Worker Teams Definition

### Team 1: Backend (Handoff Chain)

| Expert | Responsibility | Handoff To |
|--------|----------------|------------|
| **API Designer** | Design REST/GraphQL API | Backend Coder |
| **Backend Coder** | Implement API logic | Backend Tester |
| **Backend Tester** | Write & run tests | Lead Agent |

### Team 2: Frontend (Handoff Chain)

| Expert | Responsibility | Handoff To |
|--------|----------------|------------|
| **UI Designer** | Design UI/UX & components | Frontend Coder |
| **Frontend Coder** | Implement UI & integration | Frontend Tester |
| **Frontend Tester** | Write & run tests | Lead Agent |

### Team 3: DevOps & Integration (Handoff Chain)

| Expert | Responsibility | Handoff To |
|--------|----------------|------------|
| **CI/CD Specialist** | Setup build pipeline | Integration Tester |
| **Integration Tester** | E2E testing | Deployment Specialist |
| **Deployment Specialist** | Final deployment | Lead Agent |

## Execution Flow

### Phase 1: Task Decomposition (Lead Only)

```yaml
purpose: "Decompose full stack task"
state: "decomposing"
actions:
  - skill: decomposition-planner
    task: "Break down into backend/frontend/devops"
    output: "TaskBreakdown"
    
  - skill: orchestrator
    task: "Assign worker teams"
    output: "TeamAssignment"
```

### Phase 2: Parallel Worker Teams Execution

```yaml
purpose: "Execute all worker teams in parallel"
state: "worker_execution"
parallel: true
teams:
  - name: "Backend Team"
    handoff_chain: ["api-design", "code-generator", "test-generator"]
    
  - name: "Frontend Team"
    handoff_chain: ["ui-design", "code-generator", "test-generator"]
    
  - name: "DevOps Team"
    handoff_chain: ["ci-cd-pipeline", "integration-test", "deployment"]
```

### Phase 3: Result Aggregation

```yaml
purpose: "Collect all worker team outputs"
state: "aggregating"
actions:
  - skill: aggregation-processor
    task: "Aggregate backend/frontend/devops results"
    output: "AggregatedResults"
```

### Phase 4: Lead Review & Quality Check

```yaml
purpose: "Final quality review and integration"
state: "reviewing"
quality_gate:
  checks:
    - "Backend API complete"
    - "Frontend UI complete"
    - "All tests pass"
    - "Integration works"
  on_failure: "send_back_to_team"
```

## Handoff Mechanism

### Handoff Protocol

```python
async def handoff(from_expert, to_expert, context, partial_result):
    """
    Transfer the baton from one expert to the next
    """
    handoff_payload = {
        "from": from_expert,
        "to": to_expert,
        "context": context,
        "partial_result": partial_result,
        "next_steps": get_next_steps(to_expert)
    }
    
    return await invoke_skill(to_expert, handoff_payload)
```

### Example Handoff (Backend Team)

```
1. API Designer finishes → handoff to Backend Coder
   ├─ context: API spec + requirements
   └─ partial_result: OpenAPI/Swagger document

2. Backend Coder finishes → handoff to Backend Tester
   ├─ context: API spec + implementation
   └─ partial_result: Code files + DB schema

3. Backend Tester finishes → handoff to Lead Agent
   ├─ context: Everything
   └─ partial_result: Test results + coverage report
```

## Quality Gates

| Gate | Phase | Checks |
|------|-------|--------|
| **Decomposition Gate** | Phase 1 | Task breakdown makes sense, teams properly assigned |
| **Backend Gate** | Phase 2 | API working, tests pass, coverage >= 80% |
| **Frontend Gate** | Phase 2 | UI functional, responsive, tests pass |
| **Integration Gate** | Phase 3 | Frontend ↔ Backend communication works |
| **Final Gate** | Phase 4 | Everything works, documented, deployable |

## Example Usage

### Task: "Build a todo app with Vue3 frontend and Go backend"

```
LEAD AGENT:
  ✓ Decomposed into Backend/Frontend/DevOps
  ✓ Assigned Worker Teams

WORKER TEAMS (in parallel):
  Backend Team:
    API Designer → handoff → Backend Coder → handoff → Backend Tester
    ✓ API spec (OpenAPI)
    ✓ Go backend (150 lines)
    ✓ Tests (12 unit, 85% coverage)
  
  Frontend Team:
    UI Designer → handoff → Frontend Coder → handoff → Frontend Tester
    ✓ UI design (Figma-like spec)
    ✓ Vue3 app (200 lines)
    ✓ Tests (10 unit)
  
  DevOps Team:
    CI/CD Specialist → handoff → Integration Tester → handoff → Deployment
    ✓ GitHub Actions workflow
    ✓ E2E tests pass
    ✓ Local deployment working

LEAD REVIEW:
  ✓ All outputs collected
  ✓ Integration verified (Vue ↔ Go works)
  ✓ Quality checks pass
  ✓ Documentation complete

RESULT: Full stack todo app delivered!
```

## Related Skills

### Lead Skills
- **decomposition-planner** - Task decomposition
- **orchestrator** - Execution coordination

### Worker Skills
- **coding-workflow** - Code generation workflow
- **api-design** - API design
- **research-workflow** - Research tasks

### Aggregation
- **aggregation-processor** - Result aggregation
