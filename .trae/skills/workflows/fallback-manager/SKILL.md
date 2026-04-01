---
name: fallback-manager
description: "Tier 1: Handle failures gracefully - fallback strategies, best attempt, last resort. Keywords: fallback, best effort, graceful degradation, 回退策略, 最佳尝试"
layer: workflow
role: fallback-specialist
tier: 1
version: 5.0.0
architecture: single-agent
invokes:
  - reflector
  - task-registry
invoked_by:
  - iteration-controller
  - lead-agent
capabilities:
  - fallback_strategies
  - graceful_degradation
  - best_effort_delivery
  - failure_recovery
triggers:
  keywords:
    - fallback
    - best effort
    - graceful degradation
    - what if fails
    - 回退
    - 最佳尝试
  conditions:
    - "task failed"
    - "max iterations hit"
    - "need to deliver something"
metrics:
  fallback_success_rate: 0.95
  user_satisfaction: 0.88
---

# Fallback Manager - Tier 1

> **Tier 1 Skill**: Handle failures gracefully with fallback strategies

## What is Fallback Management?

When things fail, deliver the best possible result instead of nothing.

```
NO FALLBACK:
  Task: Generate a good prompt
  Iteration 1: Bad
  Iteration 2: Bad
  Iteration 3: Bad
  Iteration 4: Bad
  Iteration 5: Bad
  (Max iterations hit)
  → Result: "Sorry, I failed."
  → User: Frustrated!

WITH FALLBACK MANAGER:
  Task: Generate a good prompt
  Iteration 1: Score 55%
  Iteration 2: Score 60% (BEST)
  Iteration 3: Score 58%
  Iteration 4: Score 62%
  Iteration 5: Score 59%
  (Max iterations hit)
  
  FALLBACK: Return BEST attempt (Iteration 2, 60%)
  → Result: "Here's my best attempt (score: 60%)"
  → User: Happy! Got something usable!
```

## Fallback Strategies

| Strategy | When to Use | What Happens |
|----------|-------------|--------------|
| **best_attempt** | Always safe | Return highest-scoring attempt |
| **last_attempt** | If recent is better | Return the last attempt |
| **simplified_version** | If complex fails | Return a simpler version |
| **template_fallback** | If generation fails | Use a pre-built template |
| **human_in_the_loop** | If critical | Ask user for help |

## Handoff/Integration

```
Main Task ━━(failed)━━► Fallback Manager ━━(deliver)━━► User
     │                      │
  ├─ Tried & failed    ├─ Pick fallback strategy
  └─ History           └─ Deliver best possible
```

## Phase 1: Evaluate History

```yaml
purpose: "Look at what was tried"
state: evaluating_history
inputs:
  attempts: [...]
  scores: [...]
  timestamps: [...]

analysis:
  - Which attempt had highest score?
  - Which attempt was most recent?
  - Are any attempts usable?

output: HistoryAnalysis
```

## Phase 2: Select Fallback Strategy

```yaml
purpose: "Choose best fallback"
state: selecting_strategy
strategies_order:
  1. best_attempt (highest score)
  2. last_attempt (most recent)
  3. simplified_version (simpler)
  4. template_fallback (pre-built)
  5. human_in_the_loop (ask user)

selection:
  if best_attempt score > 0.5:
    use best_attempt
  else:
    try simplified_version

output: SelectedFallback
```

## Phase 3: Deliver with Explanation

```yaml
purpose: "Deliver fallback result"
state: delivering
communication:
  - Be transparent: "This is my best attempt"
  - Explain limitations: "Score: 60%"
  - Offer next steps: "Want me to iterate more?"

output: FallbackResultWithExplanation
```

## Example: Prompt Generation with Fallback

```
TASK: Generate a good prompt for blog writing

ATTEMPTS:
  Iteration 1: Prompt v1 → Score: 55%
  Iteration 2: Prompt v2 → Score: 60% ← BEST
  Iteration 3: Prompt v3 → Score: 58%
  Iteration 4: Prompt v4 → Score: 62%
  Iteration 5: Prompt v5 → Score: 59%

MAX ITERATIONS HIT!

FALLBACK MANAGER:
  ✓ Evaluate history: Best is Iteration 4 (62%)
  ✓ Select strategy: best_attempt
  ✓ Deliver with explanation

DELIVERED TO USER:
  "I wasn't able to reach the quality threshold, but here's my best attempt (score: 62%):
  
  [Prompt v4 here]
  
  Want me to keep trying to improve it?"

RESULT: User is happy! Got something usable instead of nothing!
```

## Related Skills

- **iteration-controller** - Iteration control (often paired)
- **reflector** - Reflection
- **task-registry** - Task history
