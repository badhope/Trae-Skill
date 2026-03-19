---
name: "coding-code-review"
description: "Performs comprehensive code quality review. Invoke when user asks for code review or needs feedback on code quality."
---

# Coding Code Review Skill

A systematic approach to reviewing code for quality, correctness, and improvements.

## When to Use

- User asks for code review
- Before merging changes
- After completing a feature
- When refactoring code

## Review Dimensions

### 1. Correctness (30%)
- Does the code correctly implement the requirements?
- Are edge cases handled?
- Is the logic sound?

### 2. Robustness (20%)
- Input validation
- Error handling
- Boundary conditions

### 3. Readability (15%)
- Clear naming
- Appropriate comments
- Logical structure

### 4. Performance (10%)
- Time complexity
- Space complexity
- Resource usage

### 5. Security (15%)
- Vulnerability check
- Authentication/authorization
- Data protection

### 6. Maintainability (10%)
- Coupling and cohesion
- Testability
- Code organization

## Review Process

1. **Understand Context**: What is the code supposed to do?
2. **Analyze Structure**: How is the code organized?
3. **Check Each Dimension**: Evaluate against criteria
4. **Document Issues**: List problems with severity
5. **Provide Suggestions**: Offer specific improvements

## Issue Severity

| Severity | Description |
|----------|-------------|
| 🔴 Critical | Must fix before release |
| 🟡 Moderate | Should fix before release |
| 🟢 Suggestion | Can fix in future iterations |

## Output Format

Provide a structured review report:

```
# Code Review Report

## Overall Score: X/10

## Strengths
- [List of positive aspects]

## Issues Found
### 🔴 Critical
- [Issue 1] - [Location] - [Suggestion]
### 🟡 Moderate
- [Issue 1] - [Location] - [Suggestion]

## Risk Assessment
- [Potential risks and mitigations]

## Recommendations
- [Actionable recommendations]
```

## Related Prompts

- `prompt-task-coding-review-code-for-quality`
