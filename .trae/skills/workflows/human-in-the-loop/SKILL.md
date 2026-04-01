---
name: human-in-the-loop
description: "Tier 1: Involve human in decision making - ask for feedback, approval, clarification. Keywords: human in the loop, ask user, get approval, 人在回路, 询问用户"
layer: workflow
role: human-facilitator
tier: 1
version: 5.0.0
architecture: single-agent
invokes:
  - task-registry
invoked_by:
  - lead-agent
  - fallback-manager
  - enterprise-project
capabilities:
  - user_feedback_collection
  - decision_clarification
  - approval_workflow
  - human_guidance
triggers:
  keywords:
    - human in the loop
    - ask user
    - get approval
    - need input
    - 人在回路
    - 询问用户
    - 确认
  conditions:
    - "ambiguous decision"
    - "needs approval"
    - "high stakes"
    - "multiple valid options"
metrics:
  user_engagement: 0.92
  decision_quality: 0.95
---

# Human-in-the-Loop - Tier 1

> **Tier 1 Skill**: Involve human in decision making

## What is Human-in-the-Loop?

When AI is unsure, ask the human for guidance, approval, or clarification.

```
NO HUMAN-IN-THE-LOOP:
  AI: "I'll choose Option A"
  User: "Wait, I wanted Option B!"
  → Frustration!

WITH HUMAN-IN-THE-LOOP:
  AI: "I have 2 options:
    A: Simple & fast (80% feature)
    B: Complete & slow (100% feature)
    
  Which do you prefer?"
  
  User: "Option A please"
  
  AI: "Got it! Building Option A."
  → Happy user! Got exactly what they wanted!
```

## When to Ask Human

| Scenario | Action |
|----------|--------|
| **Ambiguous decision** | Present options, ask to choose |
| **High stakes** | Ask for approval before proceeding |
| **Multiple valid options** | Present pros/cons, let user decide |
| **Unclear requirements** | Ask for clarification |
| **Ethical/safety concerns** | Must get human approval |

## Interaction Patterns

### Pattern 1: Multiple Choice

```yaml
purpose: "Present options"
state: presenting_options
options:
  - option_a:
      name: "Simple & Fast"
      description: "80% features, 2 days"
      pros: ["Fast", "Cheap"]
      cons: ["Missing some features"]
  - option_b:
      name: "Complete"
      description: "100% features, 5 days"
      pros: ["Full features"]
      cons: ["Slow", "Expensive"]

question: "Which option do you prefer?"

output: UserChoice
```

### Pattern 2: Approval Request

```yaml
purpose: "Ask for approval"
state: requesting_approval
context:
  what: "About to delete 10 files"
  why: "They're unused"
  risk: "Low (backups exist)"

question: "Proceed with deletion?"
options: ["Yes", "No", "Review first"]

output: ApprovalDecision
```

### Pattern 3: Clarification

```yaml
purpose: "Ask for clarification"
state: clarifying
ambiguity: "User said 'make it fast' - unclear what that means"

questions:
  - "What does 'fast' mean to you?"
  - "A: Response time < 100ms?"
  - "B: Development time < 1 day?"
  - "C: Both?"

output: Clarification
```

## Handoff/Integration

```
AI Task ━━(needs human)━━► Human-in-the-Loop ━━(user input)━━► Continue Task
     │                              │
  ├─ Uncertainty            ├─ Ask user
  └─ Options               └─ Get answer
```

## Example: Full Stack Project with Human Approval

```
TASK: Build a full stack app

PHASE 1: Research & Planning
  ✓ Done

PHASE 2: Architecture Decision (needs human!)
  AI: "I have 2 architecture options:
  
    Option A: Monolith
      • Pros: Simple, fast to build
      • Cons: Harder to scale later
      
    Option B: Microservices
      • Pros: Easy to scale
      • Cons: Complex, slower to build
      
  Which architecture do you want?"

User: "Option A (Monolith) please - let's keep it simple first"

AI: "Got it! Proceeding with monolith."

PHASE 3-6: Build, test, deploy...
  ✓ Done (with human-approved architecture!)

RESULT: Happy user! Got exactly what they wanted!
```

## Related Skills

- **lead-agent** - Overall coordination
- **task-registry** - Task history
- **fallback-manager** - Fallback if no human response
