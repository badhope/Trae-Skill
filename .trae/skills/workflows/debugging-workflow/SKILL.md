---
name: debugging-workflow
description: "Systematic debugging workflow for finding and fixing bugs. Use for bug investigation, error analysis, and issue resolution. Keywords: debug, fix, bug, error, issue, 调试, 修复, 错误, 问题"
layer: workflow
role: coordinator
version: 2.0.0
invokes:
  - log-analyzer
  - code-analyzer
  - error-analyzer
  - root-cause-finder
  - code-fixer
  - test-runner
  - aggregation-processor
invoked_by:
  - task-planner
  - orchestrator
  - decomposition-planner
capabilities:
  - investigation_coordination
  - hypothesis_management
  - fix_validation
  - regression_prevention
triggers:
  keywords:
    - debug
    - fix
    - bug
    - error
    - issue
    - problem
    - 调试
    - 修复
    - 错误
    - 问题
    - bug
  conditions:
    - "error or exception reported"
    - "unexpected behavior observed"
    - "test failure needs investigation"
metrics:
  avg_execution_time: 10m
  success_rate: 0.88
  token_efficiency: 0.78
  root_cause_accuracy: 0.92
---

# Debugging Workflow

> **Workflow-Skill**: Tactical coordinator for systematic debugging and bug fixing.

## Role Definition

You are the **Debugging Coordinator** at the workflow layer. Your responsibilities:

1. **Coordinate** investigation across multiple analysis tools
2. **Manage** hypothesis generation and validation
3. **Guide** systematic root cause identification
4. **Coordinate** fix implementation and validation
5. **Ensure** regression prevention
6. **Document** debugging process and lessons

## State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DEBUGGING WORKFLOW STATES                       │
│                                                                      │
│  initialized ──► gathering ──► analyzing ──► hypothesizing          │
│       │              │              │              │                │
│       │              ▼              ▼              ▼                │
│       │           failed         failed         failed              │
│       │              │              │              │                │
│       │              └──────────────┴──────────────┘                │
│       │                            │                                 │
│       │                            ▼                                 │
│       │                        escalation                            │
│       │                            │                                 │
│       ▼                            ▼                                 │
│  hypothesizing ──► validating ──► fixing ──► verifying ──► completed│
│       │               │              │            │                  │
│       ▼               ▼              ▼            ▼                  │
│    failed          failed         failed       failed               │
│       │               │              │            │                  │
│       └───────────────┴──────────────┴────────────┘                  │
│                            │                                         │
│                            ▼                                         │
│                        retry ──► (back to hypothesizing)             │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase Definitions

### Phase 1: Information Gathering

```yaml
purpose: "Collect all relevant information about the issue"
state: "gathering"
actions:
  - skill: log-analyzer
    task: "Extract error logs and stack traces"
    output: "ErrorLogs"
    
  - skill: code-analyzer
    task: "Identify affected code regions"
    output: "AffectedCode"
    
  - skill: git-analyzer
    task: "Check recent changes"
    output: "RecentChanges"
    
  - skill: environment-checker
    task: "Verify environment state"
    output: "EnvironmentState"

outputs_needed:
  - Error message and stack trace
  - Affected code files
  - Recent git changes
  - Environment configuration
  - User actions that triggered the issue
  
estimated_time: "2-3 minutes"
```

### Phase 2: Analysis

```yaml
purpose: "Analyze collected information to understand the problem"
state: "analyzing"
actions:
  - skill: error-analyzer
    task: "Parse and categorize error"
    output: "ErrorClassification"
    
  - skill: code-analyzer
    task: "Analyze code flow"
    output: "CodeFlowAnalysis"
    
  - skill: dependency-analyzer
    task: "Check dependency issues"
    output: "DependencyStatus"

analysis_checklist:
  - "Error type identified"
  - "Error location pinpointed"
  - "Code execution path traced"
  - "Dependencies verified"
  - "Environment factors considered"
  
estimated_time: "3-4 minutes"
```

### Phase 3: Hypothesis Generation

```yaml
purpose: "Generate and prioritize hypotheses about root cause"
state: "hypothesizing"
actions:
  - skill: root-cause-finder
    task: "Generate possible causes"
    output: "Hypotheses"
    
  - skill: evidence-matcher
    task: "Match evidence to hypotheses"
    output: "EvidenceMapping"

hypothesis_format:
  id: "H-{number}"
  description: "Clear description of possible cause"
  likelihood: "high | medium | low"
  evidence_for: ["evidence 1", "evidence 2"]
  evidence_against: ["contradicting evidence"]
  test_method: "How to validate this hypothesis"
  
prioritization:
  - Sort by likelihood (high first)
  - Consider ease of verification
  - Account for impact if true
  
estimated_time: "2-3 minutes"
```

### Phase 4: Hypothesis Validation

```yaml
purpose: "Systematically validate hypotheses to find root cause"
state: "validating"
actions:
  - skill: test-executor
    task: "Run verification tests"
    output: "TestResults"
    
  - skill: code-inspector
    task: "Inspect specific code paths"
    output: "InspectionResults"

validation_protocol:
  FOR each hypothesis (in priority order):
    1. Design verification test
    2. Execute test
    3. Analyze results
    4. Update hypothesis status
    
    IF hypothesis confirmed:
      RETURN root_cause
    ELSE:
      CONTINUE to next hypothesis
      
  IF no hypothesis confirmed:
    ESCALATE or generate new hypotheses

max_iterations: 5
estimated_time: "3-5 minutes"
```

### Phase 5: Fix Implementation

```yaml
purpose: "Implement the fix for identified root cause"
state: "fixing"
actions:
  - skill: code-fixer
    task: "Implement fix"
    output: "FixedCode"
    
  - skill: test-generator
    task: "Add regression tests"
    output: "RegressionTests"

fix_principles:
  - "Minimal change principle"
  - "Address root cause, not symptoms"
  - "Add defensive checks"
  - "Update documentation if needed"
  - "Add regression tests"

fix_checklist:
  - [ ] Fix addresses root cause
  - [ ] No new issues introduced
  - [ ] Code follows project style
  - [ ] Tests added for the fix
  - [ ] Documentation updated
  
estimated_time: "3-5 minutes"
```

### Phase 6: Verification

```yaml
purpose: "Verify the fix resolves the issue without side effects"
state: "verifying"
actions:
  - skill: test-runner
    task: "Run all tests"
    output: "TestResults"
    
  - skill: integration-tester
    task: "Run integration tests"
    output: "IntegrationResults"
    
  - skill: regression-checker
    task: "Check for regressions"
    output: "RegressionReport"

verification_checklist:
  - [ ] Original issue is fixed
  - [ ] All existing tests pass
  - [ ] New tests pass
  - [ ] No performance regression
  - [ ] No security regression
  - [ ] Edge cases handled
  
estimated_time: "2-3 minutes"
```

## Debugging Strategies

### Strategy 1: Binary Search Debugging

```python
def binary_search_debug(issue, code_range):
    """
    Narrow down issue location using binary search
    """
    while code_range.size > threshold:
        midpoint = code_range.midpoint
        
        # Test if issue is before or after midpoint
        if issue_occurs_in(code_range[:midpoint]):
            code_range = code_range[:midpoint]
        else:
            code_range = code_range[midpoint:]
    
    return code_range  # Narrowed down location
```

### Strategy 2: Differential Analysis

```python
def differential_analysis(current_state, known_good_state):
    """
    Compare current state with last known good state
    """
    differences = []
    
    # Code differences
    code_diff = compare_code(current_state, known_good_state)
    differences.extend(code_diff)
    
    # Configuration differences
    config_diff = compare_config(current_state, known_good_state)
    differences.extend(config_diff)
    
    # Environment differences
    env_diff = compare_environment(current_state, known_good_state)
    differences.extend(env_diff)
    
    return prioritize_differences(differences)
```

### Strategy 3: Trace Analysis

```python
def trace_analysis(error_trace):
    """
    Analyze execution trace to find issue origin
    """
    trace_chain = []
    
    for frame in error_trace:
        frame_info = {
            'file': frame.filename,
            'line': frame.lineno,
            'function': frame.function,
            'variables': extract_relevant_variables(frame)
        }
        trace_chain.append(frame_info)
    
    # Find the first frame in user code
    origin = find_user_code_origin(trace_chain)
    
    return {
        'origin': origin,
        'chain': trace_chain,
        'suspects': identify_suspects(trace_chain)
    }
```

## Hypothesis Management

### Hypothesis Template

```json
{
  "id": "H-1",
  "description": "Database connection pool exhausted due to unclosed connections",
  "likelihood": "high",
  "category": "resource_leak",
  "evidence": {
    "for": [
      "Error shows 'connection timeout'",
      "Recent commit added new DB queries",
      "Memory profile shows growing connections"
    ],
    "against": [
      "Connection pool has max limit",
      "No similar errors in other environments"
    ]
  },
  "testMethod": {
    "type": "code_inspection",
    "steps": [
      "Search for DB connection creation",
      "Check for corresponding close() calls",
      "Run connection leak detector"
    ]
  },
  "status": "pending",
  "validationAttempts": 0
}
```

### Hypothesis Tracking

```yaml
# Track all hypotheses during debugging session

hypotheses:
  H-1:
    status: confirmed
    validated_at: "2025-01-15T10:25:00Z"
    evidence: "Found 3 unclosed connections in auth module"
    
  H-2:
    status: rejected
    rejected_at: "2025-01-15T10:20:00Z"
    reason: "Connection pool settings are correct"
    
  H-3:
    status: pending
    priority: 2
    
current_focus: H-1
root_cause: "Unclosed database connections in auth module"
```

## Error Classification

### Error Taxonomy

```yaml
error_types:
  syntax_errors:
    examples: ["SyntaxError", "ParseError", "IndentationError"]
    typical_causes: ["typo", "missing bracket", "wrong indentation"]
    fix_difficulty: easy
    
  type_errors:
    examples: ["TypeError", "AttributeError", "KeyError"]
    typical_causes: ["wrong type", "missing attribute", "None value"]
    fix_difficulty: medium
    
  runtime_errors:
    examples: ["RuntimeError", "ValueError", "IndexError"]
    typical_causes: ["invalid input", "out of bounds", "invalid state"]
    fix_difficulty: medium
    
  resource_errors:
    examples: ["MemoryError", "TimeoutError", "ConnectionError"]
    typical_causes: ["resource leak", "slow operation", "network issue"]
    fix_difficulty: hard
    
  logic_errors:
    examples: ["Wrong output", "Infinite loop", "Race condition"]
    typical_causes: ["incorrect logic", "missing condition", "concurrency issue"]
    fix_difficulty: hard
```

### Error Analysis Template

```markdown
## Error Analysis

### Error Classification
- **Type**: {error_type}
- **Category**: {category}
- **Severity**: {critical|high|medium|low}

### Error Context
- **Location**: {file}:{line}
- **Function**: {function_name}
- **Stack Trace**: 
  ```
  {stack_trace}
  ```

### Triggering Conditions
- **User Action**: {what_user_did}
- **System State**: {system_state_at_error}
- **Input Data**: {input_that_caused_error}

### Impact Analysis
- **Affected Users**: {user_count_or_percentage}
- **Affected Features**: {list_of_features}
- **Business Impact**: {description}
```

## Output Format

### Debugging Report

```json
{
  "debuggingId": "debug-uuid",
  "status": "resolved",
  
  "issue": {
    "description": "API returning 500 errors intermittently",
    "errorType": "ConnectionError",
    "severity": "high",
    "firstObserved": "2025-01-15T09:00:00Z"
  },
  
  "investigation": {
    "phases": {
      "gathering": {
        "duration": "2m",
        "findings": [
          "Error occurs in auth module",
          "Recent deployment 2 hours ago",
          "Affects 5% of requests"
        ]
      },
      "analyzing": {
        "duration": "3m",
        "findings": [
          "Connection timeout errors",
          "Pool size at maximum",
          "Memory growing over time"
        ]
      },
      "hypothesizing": {
        "duration": "2m",
        "hypotheses": [
          {
            "id": "H-1",
            "description": "Connection leak in auth module",
            "likelihood": "high"
          },
          {
            "id": "H-2",
            "description": "Pool configuration too small",
            "likelihood": "medium"
          }
        ]
      },
      "validating": {
        "duration": "4m",
        "validatedHypothesis": "H-1",
        "evidence": "Found 3 unclosed connections in auth middleware"
      }
    }
  },
  
  "rootCause": {
    "description": "Database connections not properly closed in auth middleware",
    "location": "src/auth/middleware.js:45-60",
    "category": "resource_leak",
    "introducedIn": "commit abc123"
  },
  
  "fix": {
    "description": "Added connection cleanup in finally block",
    "files": ["src/auth/middleware.js"],
    "linesChanged": 5,
    "principle": "Ensure connections are always closed"
  },
  
  "verification": {
    "testsRun": 25,
    "testsPassed": 25,
    "regressionTestsAdded": 2,
    "performanceImpact": "none"
  },
  
  "metrics": {
    "totalTime": "15m",
    "hypothesesGenerated": 2,
    "hypothesesTested": 2,
    "fixAttempts": 1
  },
  
  "lessons": [
    {
      "category": "best_practice",
      "lesson": "Always use try-finally for resource cleanup",
      "action": "Add to coding standards checklist"
    },
    {
      "category": "testing",
      "lesson": "Add connection leak detection to CI",
      "action": "Create new test case"
    }
  ],
  
  "recommendations": [
    "Add connection pool monitoring",
    "Implement connection leak detection in tests",
    "Review other modules for similar patterns"
  ]
}
```

## Examples

### Example 1: Connection Error Debugging

```
ISSUE: API returning 500 errors intermittently

PHASE 1 - Gathering (2m):
  ✓ Collected error logs
  ✓ Identified affected endpoint: /api/auth/login
  ✓ Found recent deployment 2 hours ago
  ✓ Environment: production, PostgreSQL

PHASE 2 - Analyzing (3m):
  ✓ Error type: ConnectionError
  ✓ Pattern: Occurs under load
  ✓ Pool metrics: At maximum capacity

PHASE 3 - Hypothesizing (2m):
  H-1: Connection leak (likelihood: high)
  H-2: Pool too small (likelihood: medium)
  H-3: Network issue (likelihood: low)

PHASE 4 - Validating (4m):
  Testing H-1: Connection leak
    → Code inspection found unclosed connections
    → H-1 CONFIRMED ✓

PHASE 5 - Fixing (3m):
  ✓ Added connection cleanup in finally block
  ✓ Added regression test

PHASE 6 - Verifying (2m):
  ✓ All tests pass
  ✓ No regressions detected
  ✓ Load test shows stable connections

ROOT CAUSE: Unclosed database connections
FIX: Proper cleanup with try-finally
RESULT: Resolved
```

### Example 2: Logic Error Debugging

```
ISSUE: Cart total calculation incorrect

PHASE 1 - Gathering (2m):
  ✓ User report: Total shows $0 after adding items
  ✓ Affected: Checkout flow
  ✓ Reproducible: Yes, with specific items

PHASE 2 - Analyzing (3m):
  ✓ Traced calculation flow
  ✓ Found discount application logic
  ✓ Issue: Discount overwrites total instead of reducing

PHASE 3 - Hypothesizing (2m):
  H-1: Discount calculation wrong (likelihood: high)
  H-2: Currency conversion issue (likelihood: low)

PHASE 4 - Validating (3m):
  Testing H-1:
    → Inspected discount function
    → Found: total = discount (should be total -= discount)
    → H-1 CONFIRMED ✓

PHASE 5 - Fixing (2m):
  ✓ Fixed calculation operator
  ✓ Added unit tests for edge cases

PHASE 6 - Verifying (2m):
  ✓ Manual test passes
  ✓ All unit tests pass
  ✓ Edge cases covered

ROOT CAUSE: Wrong operator in discount calculation
FIX: Changed = to -=
RESULT: Resolved
```

## Related Skills

### Meta-Skills
- **task-planner** - Creates debugging plans
- **orchestrator** - Coordinates debugging workflow
- **reflector** - Analyzes debugging process

### Action-Skills (Invoked)
- **log-analyzer** - Analyzes error logs
- **code-analyzer** - Analyzes code structure
- **error-analyzer** - Classifies errors
- **root-cause-finder** - Identifies root causes
- **code-fixer** - Implements fixes
- **test-runner** - Validates fixes

### Related Workflows
- **coding-workflow** - For implementing features
- **testing-workflow** - For test-focused debugging
- **performance-workflow** - For performance issues
