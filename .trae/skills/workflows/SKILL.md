---
name: "workflows"
description: "Provides workflow templates and guidance for multi-step processes. Invoke when user wants to follow a structured workflow or needs a repeatable process template."
---

# Workflows Skill

Reusable workflow templates for common development processes.

## When to Use

- User needs a repeatable process template
- Complex multi-step task requires structure
- Want to ensure consistent outcomes
- Need guidance through a complex process

## Available Workflows

### 1. Sequential Bug Fix Workflow

**When to use:** User reports a bug that needs systematic fixing

```
Identify Root Cause
        ↓
Generate Debug Plan
        ↓
Fix Bug Safely
        ↓
Verify Fix
```

**Related Skills:** `debugging`, `repo-analysis`

### 2. Multi-Step Feature Development

**When to use:** Implementing a new feature from scratch

```
Create Execution Plan
        ↓
Break Down into Subtasks
        ↓
Implement Feature
        ↓
Code Review
        ↓
Test and Verify
```

**Related Skills:** `planning`, `coding`, `coding-code-review`

### 3. Repository Onboarding

**When to use:** Working with a new/unfamiliar codebase

```
Analyze Repository Structure
        ↓
Summarize Architecture
        ↓
Locate Key Files
        ↓
Understand Dependencies
```

**Related Skills:** `repo-analysis`

### 4. Research Workflow

**When to use:** Investigating a topic or technology

```
Prepare Research Brief
        ↓
Gather Information
        ↓
Analyze and Compare
        ↓
Document Findings
        ↓
Make Recommendations
```

**Related Skills:** `research`, `planning`

### 5. Code Review Workflow

**When to use:** Reviewing code for quality

```
Understand Code Context
        ↓
Review for Correctness
        ↓
Review for Quality
        ↓
Document Issues
        ↓
Provide Recommendations
```

**Related Skills:** `coding-code-review`, `coding`

## Workflow Structure

Each workflow follows a consistent structure:

```yaml
name: Workflow Name
description: When to use this workflow
phases:
  - name: Phase 1
    steps:
      - step: "Step description"
        prompts: [related prompts]
        skills: [related skills]
    output: What this phase produces
transition: How to move to next phase
```

## Creating Custom Workflows

To create a custom workflow:

1. **Define objective**: What is the workflow trying to achieve?
2. **Identify phases**: Break into logical phases
3. **Define steps**: Each step should be a coherent unit
4. **Map to skills**: Link each step to relevant skills/prompts
5. **Define transitions**: How do you move between phases?
6. **Set outputs**: What does each phase produce?

## Workflow Principles

1. **Clear phases**: Each phase has a clear purpose
2. **Defined outputs**: Each step produces something
3. **的回滚能力**: Can go back and revise
4. **Verification gates**: Each phase has acceptance criteria
5. **Documentation**: Progress is documented

## Related Prompts

- `prompt-routing-compose-multiple-prompts-for-one-task` - for combining prompts into workflows

## Related Skills

- All individual skills can be composed into workflows
