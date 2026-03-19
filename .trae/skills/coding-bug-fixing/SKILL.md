---
name: "coding-bug-fixing"
description: "Analyzes and fixes code bugs using systematic debugging methodology. Invoke when user reports a bug, error, or unexpected behavior in code."
---

# Coding Bug Fixing Skill

A systematic debugging and bug-fixing methodology for professional developers.

## When to Use

- User reports a bug or error
- Code is not working as expected
- Need to find root cause of an issue
- Need to safely fix a bug without introducing regression

## Debugging Process

### 1. Identify Root Cause

Use the `identify-root-cause` approach:

1. Collect error information (error message, logs, stack trace)
2. Understand expected behavior
3. Generate hypotheses for possible causes
4. Verify each hypothesis with evidence
5. Determine the root cause with confidence level

### 2. Generate Debug Plan

Create a structured debug plan:

1. Define the fix strategy (minimal change vs refactor)
2. List specific steps to implement the fix
3. Identify risks and mitigation strategies
4. Define verification criteria
5. Prepare rollback plan

### 3. Fix Bug Safely

Follow minimal change principle:

1. Make the smallest necessary change
2. Update/add test cases to cover the bug
3. Verify syntax correctness
4. Run tests to ensure no regression

### 4. Verify Fix

After making changes:

1. Verify the bug is fixed
2. Ensure no regression in related functionality
3. Check performance impact
4. Confirm all tests pass

## Key Principles

- **Evidence over guesswork**: Always verify hypotheses with evidence
- **Minimal change**: Make only necessary changes to fix the bug
- **Test coverage**: Ensure new test cases cover the bug scenario
- **Regression prevention**: Verify related functionality still works
- **Rollback ready**: Always have a plan to revert changes

## Related Prompts

- `prompt-task-debugging-identify-root-cause`
- `prompt-task-debugging-generate-debug-plan`
- `prompt-task-debugging-fix-bug-safely`
- `prompt-task-debugging-verify-fix-after-change`
