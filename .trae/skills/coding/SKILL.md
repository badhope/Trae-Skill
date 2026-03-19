---
name: "coding"
description: "Generates, implements, and reviews code based on requirements or specifications. Invoke when user wants to generate code, implement features, or needs code reviewed."
---

# Coding Skill

A comprehensive coding skill for generating, implementing, and reviewing code.

## When to Use

- User wants to generate code from requirements
- User wants to implement a feature from spec
- User needs code reviewed for quality
- User wants help with coding tasks

## Coding Workflow

### 1. Generate Code from Requirement

Use `generate-code-from-requirement` when:
- User provides a natural language requirement
- Need to convert requirements to working code

Process:
1. Extract requirement elements
2. Identify constraints (language, framework, quality standards)
3. Design data structures and functions
4. Generate code with error handling
5. Create test cases
6. Document usage

### 2. Implement Feature from Spec

Use `implement-feature-from-spec` when:
- User provides a technical specification
- Need to implement a complete module

Process:
1. Parse and understand specification
2. Analyze integration points
3. Plan implementation sequence
4. Implement with types, core logic, integration
5. Create test specification
6. Provide integration guide

### 3. Review Code for Quality

Use `review-code-for-quality` when:
- User wants feedback on existing code
- Need to assess code quality

Process:
1. Understand code functionality and context
2. Evaluate multiple dimensions:
   - Correctness (30%)
   - Robustness (20%)
   - Readability (15%)
   - Performance (10%)
   - Security (15%)
   - Maintainability (10%)
3. Document strengths and issues
4. Provide actionable suggestions

## Code Quality Standards

### Must Have
- Input validation
- Error handling
- Appropriate comments
- Meaningful naming
- Unit tests

### Should Have
- Documentation
- Logging
- Performance optimization
- Security measures

## Output Requirements

When generating code, always provide:

1. **Code**: Complete, runnable code
2. **Tests**: Test cases covering main scenarios
3. **Documentation**: Usage instructions
4. **Trade-offs**: Technical decisions and reasoning

## Related Prompts

### Code Generation
- `prompt-task-coding-generate-code-from-requirement`
- `prompt-task-coding-implement-feature-from-spec`

### Code Review
- `prompt-task-coding-review-code-for-quality`

### Related Skills
- `coding-bug-fixing` - when bugs need to be fixed
- `coding-code-review` - comprehensive review workflow
