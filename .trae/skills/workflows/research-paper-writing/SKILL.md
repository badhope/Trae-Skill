---
name: research-paper-writing
description: "Tier 3: Lead-Worker + Handoff for academic research paper writing. Keywords: research paper, academic, literature review, methodology, experiments, 学术论文, 研究, 文献综述"
layer: workflow
role: lead-coordinator
tier: 3
version: 5.0.0
architecture: lead-worker-handoff
invokes:
  - research-workflow
  - decomposition-planner
  - aggregation-processor
  - documentation
invoked_by:
  - meta-layer-orchestrator
  - lead-agent
capabilities:
  - lead_worker_coordination
  - research_literature_review
  - experimental_design
  - academic_writing
  - peer_review_simulation
triggers:
  keywords:
    - research paper
    - academic writing
    - literature review
    - methodology
    - experiments
    - 学术论文
    - 研究
    - 文献综述
    - 实验
  conditions:
    - "task requires academic research"
    - "needs literature review"
    - "involves experiments & analysis"
metrics:
  avg_execution_time: 120m
  success_rate: 0.75
  worker_teams: 4
  sections: 8
---

# Research Paper Writing - Tier 3

> **Tier 3 Complex Skill**: Lead-Worker + Handoff for academic research paper writing.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│              LEAD AGENT (Principal Investigator)             │
│  • Research topic definition & scope                          │
│  • 4 Research Teams coordination                              │
│  • Paper integration & final review                           │
└──────────────────────┬────────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────▼────────┐ ┌──▼──────────┐ ┌──▼──────────────┐
│ WORKER TEAM 1   │ │ WORKER TEAM 2│ │ WORKER TEAM 3   │
│  Literature     │ │  Methodology  │ │  Experiments    │
│  • Search      ━━┓│  • Design    ━━┓│  • Run       ━━┓│
│  • Review      ◀━┛│  • Validate  ◀━┛│  • Analyze   ◀━┛│
│    (Handoff)     │ │    (Handoff)   │ │    (Handoff)     │
└────────┬─────────┘ └──────┬─────────┘ └──────┬───────────┘
         │                    │                   │
         └────────────────────┼───────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   WORKER TEAM 4    │
                    │   Writing & Review  │
                    │   • Draft     ━━┓  │
                    │   • Revise    ◀━┛  │
                    │   • Format      │  │
                    └────────┬─────────┘  │
                             │              │
                             └──────────────┘
                                            │
                                    ┌───────▼───────┐
                                    │  LEAD REVIEW   │
                                    │  & Final Edit  │
                                    └───────────────┘
```

## Worker Teams (4 Teams)

### Team 1: Literature Review (Handoff Chain)

| Expert | Responsibility | Output |
|--------|----------------|--------|
| **Literature Searcher** | Find relevant papers (arXiv, Google Scholar, etc.) | Bibliography |
| **Literature Reviewer** | Synthesize & summarize research | Literature Review section |

### Team 2: Methodology (Handoff Chain)

| Expert | Responsibility | Output |
|--------|----------------|--------|
| **Methodology Designer** | Research design & approach | Methodology draft |
| **Methodology Validator** | Validate approach soundness | Final Methodology |

### Team 3: Experiments (Handoff Chain)

| Expert | Responsibility | Output |
|--------|----------------|--------|
| **Experiment Runner** | Design & run experiments | Raw data |
| **Data Analyst** | Analyze & visualize results | Results section, figures, tables |

### Team 4: Writing & Review (Handoff Chain)

| Expert | Responsibility | Output |
|--------|----------------|--------|
| **Paper Writer** | Draft all sections (Abstract, Intro, etc.) | Full draft |
| **Peer Reviewer** | Simulate peer review & feedback | Review comments |
| **Paper Reviser** | Address feedback & polish | Revised paper |
| **Formatter** | Format for target venue (ACM, IEEE, etc.) | Camera-ready |

## Paper Sections (8 Sections)

1. Abstract
2. Introduction
3. Related Work (from Team 1)
4. Methodology (from Team 2)
5. Experiments (from Team 3)
6. Results (from Team 3)
7. Discussion
8. Conclusion & Future Work

---

## Related Skills

- **research-workflow** - Core research workflow
- **documentation** - Academic writing
