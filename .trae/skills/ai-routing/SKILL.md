---
name: "ai-routing"
description: "Enables AI to autonomously scan repository, identify task type, and select appropriate prompts/workflows. Invoke when AI needs to understand a new project or select the right approach."
---

# AI Routing Skill

Enables AI agents to autonomously navigate and utilize a skill/prompt repository.

## When to Use

- AI receives a new task and needs to understand available resources
- Need to determine which prompts or skills to use
- Working with an unfamiliar codebase
- Need to compose multiple prompts for complex tasks

## Routing Process

### 1. Scan Repository

Use `scan-repository-and-build-task-map`:

1. Read INDEX.md and registry files
2. Explore directory structure
3. Identify available skills, prompts, workflows
4. Build a task map of available resources

### 2. Identify Task Type

Use `identify-task-type-and-route`:

1. Analyze the user's request
2. Classify into categories:
   - Coding (generate, implement, review)
   - Debugging (identify, fix, verify)
   - Analysis (understand, locate, summarize)
   - Planning (plan, break down, estimate)
   - Research (investigate, evaluate, recommend)
3. Determine routing path

### 3. Select Relevant Prompts

Use `select-relevant-prompts-from-index`:

1. Match task type to prompt categories
2. Filter by keywords and tags
3. Rank by relevance
4. Select top candidates

### 4. Compose for Task

Use `compose-multiple-prompts-for-one-task`:

1. Identify prompt dependencies
2. Determine execution order
3. Handle parameter passing between prompts
4. Combine into coherent workflow

## Task Type Mapping

| Task Type | Primary Category | Secondary |
|-----------|------------------|-----------|
| Generate code | `task/coding/` | `system/` |
| Fix bug | `task/debugging/` | `task/repo-analysis/` |
| Understand codebase | `task/repo-analysis/` | `system/` |
| Plan feature | `task/planning/` | `task/research/` |
| Investigate topic | `task/research/` | - |

## Repository Structure

```
prompts/
├── _routing/      # Meta prompts for navigation
├── system/        # System-level prompts
├── task/
│   ├── coding/
│   ├── debugging/
│   ├── repo-analysis/
│   ├── planning/
│   └── research/
```

## Best Practices

1. **Always scan first**: Build context before selecting prompts
2. **Combine system + task**: Use appropriate system prompt as base
3. **Check related items**: Prompts reference related skills/workflows
4. **Maintain context**: Pass information between prompt stages

## Related Prompts

- `prompt-routing-scan-repository-and-build-task-map`
- `prompt-routing-identify-task-type-and-route`
- `prompt-routing-select-relevant-prompts-from-index`
- `prompt-routing-compose-multiple-prompts-for-one-task`
