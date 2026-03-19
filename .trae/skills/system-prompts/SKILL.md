---
name: "system-prompts"
description: "System-level prompts for AI behavior configuration. Invoke when configuring AI system behavior or need base system prompts."
---

# System Prompts Skill

Base system prompts that define AI behavior for different contexts.

## When to Use

- When you need to configure AI system behavior
- As a foundation for other prompts
- When starting a new AI-assisted project
- For specialized AI tasks (coding, debugging, etc.)

## Available System Prompts

### 1. General AI Workbench

**Purpose:** Base system prompt for general AI assistance

**When to use:**
- General purpose AI assistance
- As foundation for other system prompts
- Multi-purpose work

**Key principles:**
- Follow user's intent
- Think step by step
- Maintain context
- Ask for clarification when needed

**File:** `prompts/system/prompt-system-general-ai-workbench.md`

### 2. Coding Agent System

**Purpose:** System prompt for programming tasks

**When to use:**
- Code generation tasks
- Software development
- Technical implementation

**Key principles:**
- Write complete, production-ready code
- Follow best practices
- Include tests and documentation
- Consider edge cases and error handling

**File:** `prompts/system/prompt-system-coding-agent.md`

### 3. Debugging Agent System

**Purpose:** System prompt for debugging tasks

**When to use:**
- Bug investigation
- Error analysis
- Problem solving

**Key principles:**
- Systematic analysis
- Evidence-based conclusions
- Minimal changes
- Complete verification

**File:** `prompts/system/prompt-system-debugging-agent.md`

## System Prompt Composition

System prompts can be layered:

```markdown
[Base System Prompt]
    ↓
[Domain System Prompt] (optional)
    ↓
[Task Prompt]
```

### Example: Code Generation

1. Start with `general-ai-workbench` as base
2. Add `coding-agent` for coding context
3. Use `generate-code-from-requirement` for the task

### Example: Bug Fixing

1. Start with `general-ai-workbench` as base
2. Add `debugging-agent` for debugging context
3. Use `identify-root-cause` for the task

## Using System Prompts

### In AI Chat Interface

Copy the system prompt content into the system prompt field.

### In AI Agent Context

Reference the system prompt by its path:
```
prompts/system/prompt-system-general-ai-workbench.md
```

### Combining Prompts

System prompts provide context, then task prompts provide specific instructions:

1. Set system prompt for overall behavior
2. Use task prompt for specific work
3. Use routing prompts to select appropriate prompts

## Best Practices

1. **Start with base**: Always use general-ai-workbench as foundation
2. **Layer as needed**: Add domain-specific system prompts
3. **Match to task**: Use the most relevant system prompt
4. **Keep updated**: Update system prompts as needs evolve

## Related Prompts

### System
- `prompt-system-general-ai-workbench`
- `prompt-system-coding-agent`
- `prompt-system-debugging-agent`

### Routing
- `prompt-routing-compose-multiple-prompts-for-one-task` - for combining prompts
