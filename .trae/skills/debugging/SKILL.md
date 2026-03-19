---
name: "debugging"
description: "Systematic debugging process for finding and fixing bugs. Invoke when user encounters bugs, errors, or unexpected behavior in code."
---

# Debugging Skill

A systematic approach to debugging: identify root cause, plan fix, implement safely, verify solution.

## When to Use

- User reports a bug or error
- Code is not working as expected
- Need to find why something is failing
- Need to fix a bug and verify the fix

## Debugging Workflow

### Phase 1: Identify Root Cause

Use `identify-root-cause` to analyze the problem:

**Information Collection:**
- Error message and stack trace
- Environment information
- Reproduction steps
- Related logs

**Hypothesis Generation:**
- List all possible causes
- Categorize (code, data, environment)
- Assign likelihood (high/medium/low)

**Verification:**
- Design verification tests for each hypothesis
- Execute and collect evidence
- Eliminate false hypotheses
- Confirm root cause with confidence level

### Phase 2: Generate Debug Plan

Use `generate-debug-plan` to plan the fix:

**Strategy Selection:**
- Minimal change (emergency fix)
- Refactor (fundamental issue)
- Wrapper layer (temporary solution)

**Detailed Planning:**
- Specific fix steps
- Time estimation
- Resource requirements
- Risk identification

**Mitigation Planning:**
- Risk mitigation strategies
- Rollback plan
- Verification criteria

### Phase 3: Fix Bug Safely

Use `fix-bug-safely` to implement the fix:

**Principles:**
- Minimal change principle
- Test coverage requirement
- Regression prevention
- Rollback readiness

**Implementation:**
1. Backup current code
2. Make minimal necessary changes
3. Add/update test cases
4. Verify syntax and run tests

### Phase 4: Verify Fix

Use `verify-fix-after-change` to validate:

**Correctness Verification:**
- Core functionality works
- Boundary conditions handled
- Error handling proper

**Completeness Check:**
- Root cause eliminated
- Related scenarios covered
- Test coverage adequate

**Regression Testing:**
- Related functionality still works
- No performance degradation
- Integration tests pass

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Fix introduces new bugs | High | Comprehensive testing |
| Fix incomplete | Medium | Verify all scenarios |
| Regression | High | Full regression suite |
| Performance impact | Medium | Performance testing |

## Debugging Principles

1. **Don't guess, verify**: Always use evidence
2. **Start broad, narrow down**: Eliminate possibilities
3. **Check simplest first**: Common causes first
4. **Understand the system**: Know how it should work
5. **Document findings**: Record what you learned

## Related Prompts

- `prompt-task-debugging-identify-root-cause`
- `prompt-task-debugging-generate-debug-plan`
- `prompt-task-debugging-fix-bug-safely`
- `prompt-task-debugging-verify-fix-after-change`

## Related Skills

- `repo-analysis` - understand codebase when debugging
- `coding` - understand code implementation
