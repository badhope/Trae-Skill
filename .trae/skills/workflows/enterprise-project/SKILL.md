---
name: enterprise-project
description: "Tier 3: Lead-Worker + Handoff for enterprise software development. Keywords: enterprise, large scale, production, architecture, scalability, 企业级, 大规模, 生产环境"
layer: workflow
role: lead-coordinator
tier: 3
version: 5.0.0
architecture: lead-worker-handoff
invokes:
  - decomposition-planner
  - orchestrator
  - coding-workflow
  - refactoring-workflow
  - aggregation-processor
  - security-auditor
  - performance-optimizer
invoked_by:
  - meta-layer-orchestrator
  - lead-agent
capabilities:
  - lead_worker_coordination
  - multiple_worker_teams
  - enterprise_quality_standards
  - security_compliance
  - scalability_planning
triggers:
  keywords:
    - enterprise
    - production
    - large scale
    - scalable
    - architecture
    - security compliance
    - 企业级
    - 生产环境
    - 大规模
    - 架构设计
  conditions:
    - "project needs enterprise-grade quality"
    - "requires security & compliance"
    - "needs scalability planning"
metrics:
  avg_execution_time: 90m
  success_rate: 0.80
  worker_teams: 5
  quality_gates: 7
---

# Enterprise Project - Tier 3

> **Tier 3 Complex Skill**: Lead-Worker + Handoff for enterprise software projects.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  LEAD AGENT (This Skill)                         │
│  • Enterprise architecture planning                                │
│  • 5 Worker Teams assembly & coordination                          │
│  • Multi-phase quality gates & compliance                          │
└────────────────────────┬─────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬───────────────┐
         │               │               │               │
┌────────▼────────┐ ┌───▼────────┐ ┌──▼──────────┐ ┌──▼────────────┐
│ WORKER TEAM 1   │ │ WORKER TEAM 2│ │ WORKER TEAM 3│ │ WORKER TEAM 4 │
│  Architecture    │ │  Development  │ │  Security    │ │  Performance  │
│  • Design      ━━┓│  • Backend  ━━┓│  • Audit     ━━┓│  • Optimize  ━━┓│
│  • Review      ◀━┛│  • Frontend ◀━┛│  • Compliance◀━┛│  • Scale     ◀━┛│
│    (Handoff)     │ │    (Handoff)   │ │    (Handoff)   │ │    (Handoff)    │
└────────┬─────────┘ └──────┬───────┘ └──────┬───────┘ └──────┬─────────┘
         │                    │                 │                 │
         └────────────────────┼─────────────────┼─────────────────┘
                              │                 │
                    ┌─────────▼─────────┐ ┌───▼──────────┐
                    │   WORKER TEAM 5    │ │  AGGREGATOR  │
                    │   DevOps & QA       │ └──────┬───────┘
                    │   • CI/CD     ━━┓  │        │
                    │   • E2E Test  ◀━┛  │        │
                    │   • Deploy       │  │        │
                    └────────┬─────────┘  │        │
                             │              │        │
                             └──────────────┴────────┘
                                            │
                                    ┌───────▼───────┐
                                    │  LEAD REVIEW   │
                                    │  & Final QC    │
                                    └───────────────┘
```

## Worker Teams (5 Teams Total)

### Team 1: Architecture (Handoff Chain)

| Expert | Responsibility |
|--------|----------------|
| **Enterprise Architect** | High-level system design |
| **Tech Lead Reviewer** | Architecture validation & feedback |

### Team 2: Development (Parallel Sub-Teams)

- **Backend Sub-Team**: API Designer → Backend Coder → Backend Tester
- **Frontend Sub-Team**: UI Designer → Frontend Coder → Frontend Tester

### Team 3: Security (Handoff Chain)

| Expert | Responsibility |
|--------|----------------|
| **Security Auditor** | Vulnerability assessment |
| **Compliance Officer** | GDPR/SOC2/ISO compliance |

### Team 4: Performance (Handoff Chain)

| Expert | Responsibility |
|--------|----------------|
| **Performance Engineer** | Optimization & load testing |
| **Scalability Planner** | Horizontal/vertical scaling design |

### Team 5: DevOps & QA (Handoff Chain)

| Expert | Responsibility |
|--------|----------------|
| **CI/CD Engineer** | Pipeline setup |
| **QA Engineer** | E2E & regression testing |
| **SRE** | Production deployment & monitoring |

## Enterprise Quality Gates (7 Gates)

| Gate # | Name | Phase |
|--------|------|-------|
| 1 | Architecture Sign-off | After Team 1 |
| 2 | Development Complete | After Team 2 |
| 3 | Security Pass | After Team 3 |
| 4 | Performance Pass | After Team 4 |
| 5 | CI/CD & QA Pass | After Team 5 |
| 6 | Integration Test Pass | Aggregation |
| 7 | Final Lead Sign-off | Review |

---

## Related Skills

- **decomposition-planner** - Enterprise task decomposition
- **security-auditor** - Security assessment
- **performance-optimizer** - Performance optimization
