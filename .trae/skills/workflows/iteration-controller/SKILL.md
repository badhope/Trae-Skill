---
name: iteration-controller
description: "Tier 2: Control iterations, prevent infinite loops, enforce quality gates and stopping conditions. Keywords: iteration control, loop prevention, quality gate, 迭代控制, 防止死循环"
layer: workflow
role: controller
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - reflector
  - task-registry
invoked_by:
  - lead-agent
  - full-stack-development
  - enterprise-project
capabilities:
  - iteration_limiting
  - quality_gate_enforcement
  - early_termination
  - infinite_loop_prevention
triggers:
  keywords:
    - iteration control
    - loop prevention
    - quality gate
    - stop condition
    - 迭代控制
    - 防止死循环
  conditions:
    - "task involves multiple iterations"
    - "risk of infinite loop"
    - "need quality checkpoints"
metrics:
  avg_iterations: 3-5
  loop_prevention_rate: 1.0
  early_termination_rate: 0.25
---

# Iteration Controller - Tier 2

> **Tier 2 Skill**: Control iterations, prevent infinite loops, enforce quality gates

## What is Iteration Control?

Prevent infinite loops, enforce maximum iterations, and set quality gates for early termination.

```
PROBLEM: Infinite Loop!
  Generate → Test → Bad → Regenerate → Test → Bad → Regenerate...
  (Repeats forever!)

SOLUTION: Iteration Controller
  ┌───────────────────────────────────────────────┐
  │  ITERATION CONTROLLER                         │
  │                                               │
  │  • Max Iterations: 5                          │
  │  • Quality Gate: Score ≥ 80%                  │
  │  • Early Termination: If 2x same result      │
  │  • Fallback: Return best attempt              │
  └───────────────────────────────────────────────┘
                    │
                    ▼
  Iteration 1: Generate → Score: 65% → Continue
  Iteration 2: Generate → Score: 72% → Continue
  Iteration 3: Generate → Score: 85% → ✓ PASS! Stop early!
                    │
                    ▼
              No infinite loop!
              Only 3 iterations instead of infinite!
```

## Default Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| **max_iterations** | 5 | Maximum attempts before stopping |
| **quality_threshold** | 0.8 | Minimum score to pass (0.0-1.0) |
| **early_stop_same** | 2 | Stop if N consecutive same results |
| **early_stop_no_progress** | 3 | Stop if no improvement in N iterations |
| **fallback_strategy** | "best_attempt" | What to return if fails: best_attempt or last_attempt |

## Handoff Chain

```
Iteration Setup ━━(handoff)━━► Iteration Loop ━━(handoff)━━► Quality Check ━━(handoff)━━► Termination Decision
     │                       │                      │                      │
  ├─ Set limits        ├─ Run iteration      ├─ Score result      ├─ Decide: continue/stop
  └─ Quality gates     └─ Track progress     └─ Compare to threshold  └─ Return best if stopping
```

## Phase 1: Setup

```yaml
purpose: "Configure iteration limits"
state: setting_up
config:
  max_iterations: 5
  quality_threshold: 0.8
  early_stop_same: 2
  early_stop_no_progress: 3
  fallback_strategy: "best_attempt"

output: IterationConfig
```

## Phase 2: Iteration Loop

```yaml
purpose: "Run iterations with tracking"
state: iterating
current_iteration: 1
history: []

loop:
  - Run the task
  - Score the result
  - Add to history
  - Check for termination
  
  if pass_quality_gate:
    handoff_to: "Early Termination (Success)"
  elif hit_max_iterations:
    handoff_to: "Termination (Max Iterations)"
  elif early_stop_condition:
    handoff_to: "Early Termination (Stop Condition)"
  else:
    continue to next iteration
```

## Phase 3: Quality Check

```yaml
purpose: "Evaluate result quality"
state: quality_checking
scoring_criteria:
  - correctness: 0.4
  - completeness: 0.3
  - quality: 0.2
  - safety: 0.1

output: QualityScore (0.0-1.0)
```

## Phase 4: Termination Decision

```yaml
purpose: "Decide whether to continue or stop"
state: deciding
termination_conditions:
  - "quality_score >= quality_threshold" → SUCCESS
  - "current_iteration >= max_iterations" → MAX_ITERATIONS
  - "N consecutive same results" → NO_PROGRESS
  - "no improvement in N iterations" → STAGNANT

if stopping:
  if success:
    return result
  else:
    return fallback (best_attempt or last_attempt)
else:
  continue to next iteration
```

## Example: Prompt Generation (Preventing Infinite Loop)

```
TASK: Generate a good prompt for blog writing

BEFORE (No Control):
  Iteration 1: Prompt v1 → Score 55% → Regenerate
  Iteration 2: Prompt v2 → Score 60% → Regenerate
  Iteration 3: Prompt v3 → Score 58% → Regenerate
  Iteration 4: Prompt v4 → Score 62% → Regenerate
  Iteration 5: Prompt v5 → Score 59% → Regenerate
  ... (infinite loop!)

AFTER (With Iteration Controller):
  Config:
    max_iterations: 5
    quality_threshold: 0.8
    fallback: best_attempt
  
  Iteration 1: Prompt v1 → Score 55% → Continue
  Iteration 2: Prompt v2 → Score 60% → Continue
  Iteration 3: Prompt v3 → Score 78% → Continue
  Iteration 4: Prompt v4 → Score 75% → Continue
  Iteration 5: Prompt v5 → Score 72% → MAX ITERATIONS
  
  FALLBACK: Return best_attempt → Prompt v3 (78%)
  
RESULT: No infinite loop! Got best attempt in 5 iterations!
```

## Related Skills

- **reflector** - Reflection and analysis
- **task-registry** - Task history
- **fallback-manager** - Fallback strategies
