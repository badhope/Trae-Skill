---
name: coding-workflow
description: "Orchestrates code generation, testing, and review workflow. Use for feature implementation and code development tasks. Keywords: implement, code, develop, write, 实现, 编码, 开发, 编写"
layer: workflow
role: coordinator
version: 2.0.0
invokes:
  - code-analyzer
  - code-generator
  - test-generator
  - code-reviewer
  - doc-writer
  - type-checker
  - linter
  - aggregation-processor
invoked_by:
  - task-planner
  - orchestrator
  - decomposition-planner
capabilities:
  - state_management
  - phase_coordination
  - result_aggregation
  - error_recovery
  - quality_gates
triggers:
  keywords:
    - implement
    - code
    - develop
    - write
    - create
    - 实现
    - 编码
    - 开发
    - 编写
  conditions:
    - "task involves code generation"
    - "feature implementation needed"
    - "module development required"
metrics:
  avg_execution_time: 8m
  success_rate: 0.90
  token_efficiency: 0.82
  quality_score_avg: 8.5
---

# Coding Workflow

> **Workflow-Skill**: Tactical coordinator for code generation and development tasks.

## Role Definition

You are the **Development Coordinator** at the workflow layer. Your responsibilities:

1. **Coordinate** multiple Action-Skills for code development
2. **Manage** execution state across phases
3. **Enforce** quality gates between phases
4. **Aggregate** results from multiple actions
5. **Handle** errors and trigger recovery
6. **Report** progress to Orchestrator

## State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CODING WORKFLOW STATES                        │
│                                                                      │
│  initialized ──► analyzing ──► designing ──► implementing           │
│       │              │              │              │                │
│       │              ▼              ▼              ▼                │
│       │           failed         failed         failed              │
│       │              │              │              │                │
│       │              └──────────────┴──────────────┘                │
│       │                            │                                 │
│       │                            ▼                                 │
│       │                        recovery                              │
│       │                            │                                 │
│       ▼                            ▼                                 │
│  implementing ──► testing ──► reviewing ──► documenting ──► completed│
│       │              │              │                                 │
│       ▼              ▼              ▼                                 │
│    failed         failed         failed                              │
│       │              │              │                                 │
│       └──────────────┴──────────────┘                                 │
│                      │                                                │
│                      ▼                                                │
│                  recovery ──► retry                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase Definitions

### Phase 1: Analysis

```yaml
purpose: "Understand existing codebase and requirements"
state: "analyzing"
actions:
  - skill: code-analyzer
    task: "Analyze project structure"
    output: "ProjectStructure"
    
  - skill: code-analyzer
    task: "Identify existing patterns"
    output: "PatternLibrary"
    
  - skill: code-analyzer
    task: "Check dependencies"
    output: "DependencyGraph"

quality_gate:
  checks:
    - "Project structure understood"
    - "Relevant patterns identified"
    - "Dependencies resolved"
  on_failure: "request_clarification"
  
estimated_time: "2-3 minutes"
```

### Phase 2: Design

```yaml
purpose: "Plan implementation approach"
state: "designing"
actions:
  - skill: code-generator
    task: "Generate implementation plan"
    input: "requirements + patterns"
    output: "ImplementationPlan"
    
  - skill: code-generator
    task: "Design data structures"
    output: "DataStructureDesign"

quality_gate:
  checks:
    - "Implementation plan is clear"
    - "Data structures are defined"
    - "Approach is validated"
  on_failure: "return_to_analysis"
  
checkpoint:
  trigger: "design_complete"
  action: "request_user_confirmation"
  message: "Implementation approach ready for review"
  
estimated_time: "2-3 minutes"
```

### Phase 3: Implementation

```yaml
purpose: "Generate the actual code"
state: "implementing"
actions:
  - skill: code-generator
    task: "Generate main implementation"
    output: "MainCode"
    
  - skill: code-generator
    task: "Generate helper functions"
    output: "HelperCode"
    
  - skill: type-checker
    task: "Validate types"
    output: "TypeValidation"
    
  - skill: linter
    task: "Check code style"
    output: "LintResults"

quality_gate:
  checks:
    - "No syntax errors"
    - "Type check passes"
    - "Lint check passes"
  on_failure: "fix_and_retry"
  
error_recovery:
  syntax_error:
    action: "fix_syntax"
    max_retries: 3
  type_error:
    action: "fix_types"
    max_retries: 2
  lint_error:
    action: "fix_style"
    max_retries: 2
    
estimated_time: "4-6 minutes"
```

### Phase 4: Testing

```yaml
purpose: "Generate and run tests"
state: "testing"
actions:
  - skill: test-generator
    task: "Generate unit tests"
    output: "UnitTests"
    
  - skill: test-generator
    task: "Generate integration tests"
    output: "IntegrationTests"
    
  - skill: test-runner
    task: "Execute tests"
    output: "TestResults"

quality_gate:
  checks:
    - "All tests pass"
    - "Coverage >= 80%"
    - "No critical test failures"
  on_failure: "debug_and_fix"
  
error_recovery:
  test_failure:
    action: "analyze_and_fix"
    max_retries: 3
  low_coverage:
    action: "generate_more_tests"
    threshold: 80
    
estimated_time: "3-4 minutes"
```

### Phase 5: Review

```yaml
purpose: "Quality and security review"
state: "reviewing"
actions:
  - skill: code-reviewer
    task: "Review code quality"
    output: "QualityReport"
    
  - skill: security-reviewer
    task: "Security analysis"
    output: "SecurityReport"
    
  - skill: performance-reviewer
    task: "Performance check"
    output: "PerformanceReport"

quality_gate:
  checks:
    - "Quality score >= 7/10"
    - "No security vulnerabilities"
    - "No performance issues"
  on_failure: "address_feedback"
  
error_recovery:
  quality_issue:
    action: "improve_code"
    max_retries: 2
  security_issue:
    action: "fix_security"
    priority: "critical"
  performance_issue:
    action: "optimize"
    priority: "high"
    
estimated_time: "2-3 minutes"
```

### Phase 6: Documentation

```yaml
purpose: "Generate documentation"
state: "documenting"
actions:
  - skill: doc-writer
    task: "Generate API documentation"
    output: "APIDocs"
    
  - skill: doc-writer
    task: "Generate usage examples"
    output: "Examples"
    
  - skill: doc-writer
    task: "Update README if needed"
    output: "ReadmeUpdate"

quality_gate:
  checks:
    - "API documented"
    - "Examples provided"
  on_failure: "complete_documentation"
  
estimated_time: "1-2 minutes"
```

## Coordination Protocol

### Sequential Phase Execution

```python
async def execute_workflow(task):
    """
    Execute coding workflow with sequential phases
    """
    state = WorkflowState(task)
    
    # Phase 1: Analysis
    state.transition("analyzing")
    analysis_result = await execute_phase("analysis", task)
    if not quality_gate_pass(analysis_result):
        return handle_failure(state, "analysis_failed")
    
    # Phase 2: Design
    state.transition("designing")
    design_result = await execute_phase("design", analysis_result)
    if not quality_gate_pass(design_result):
        return handle_failure(state, "design_failed")
    
    # Checkpoint: User confirmation
    if design_result.needs_confirmation:
        await request_user_confirmation(design_result)
    
    # Phase 3: Implementation
    state.transition("implementing")
    impl_result = await execute_phase("implementation", design_result)
    if not quality_gate_pass(impl_result):
        impl_result = await error_recovery(impl_result)
    
    # Phase 4: Testing
    state.transition("testing")
    test_result = await execute_phase("testing", impl_result)
    if not quality_gate_pass(test_result):
        test_result = await error_recovery(test_result)
    
    # Phase 5: Review
    state.transition("reviewing")
    review_result = await execute_phase("review", test_result)
    if not quality_gate_pass(review_result):
        review_result = await address_feedback(review_result)
    
    # Phase 6: Documentation
    state.transition("documenting")
    doc_result = await execute_phase("documentation", review_result)
    
    # Finalize
    state.transition("completed")
    return aggregate_results([
        analysis_result,
        design_result,
        impl_result,
        test_result,
        review_result,
        doc_result
    ])
```

### Parallel Task Execution (Within Phase)

```python
async def execute_phase(phase_name, input_data):
    """
    Execute phase with parallel task support
    """
    phase = PHASES[phase_name]
    results = {}
    
    # Group tasks by dependencies
    task_groups = group_by_dependencies(phase.actions)
    
    for group in task_groups:
        # Execute independent tasks in parallel
        if all_tasks_independent(group):
            parallel_results = await asyncio.gather(*[
                invoke_action(task) for task in group
            ])
            results.update(parallel_results)
        else:
            # Execute dependent tasks sequentially
            for task in sort_by_dependencies(group):
                result = await invoke_action(task)
                results[task.id] = result
    
    return PhaseResult(phase_name, results)
```

## Result Aggregation

### Aggregation Strategy

```python
def aggregate_results(phase_results):
    """
    Aggregate results from all phases into final output
    """
    return WorkflowResult(
        # Collect all artifacts
        artifacts=collect_artifacts(phase_results),
        
        # Calculate metrics
        metrics=calculate_metrics(phase_results),
        
        # Summarize execution
        summary=generate_summary(phase_results),
        
        # Extract issues
        issues=extract_issues(phase_results),
        
        # Generate recommendations
        recommendations=generate_recommendations(phase_results)
    )
```

### Output Format

```json
{
  "workflowId": "workflow-uuid",
  "status": "completed",
  "phases": {
    "analysis": {
      "status": "completed",
      "duration": "2m 15s",
      "outputs": {
        "projectStructure": "...",
        "patternLibrary": "..."
      }
    },
    "design": {
      "status": "completed",
      "duration": "2m 30s",
      "outputs": {
        "implementationPlan": "...",
        "dataStructures": "..."
      }
    },
    "implementation": {
      "status": "completed",
      "duration": "5m 10s",
      "outputs": {
        "files": [
          {
            "path": "src/auth/jwt.js",
            "lines": 150,
            "language": "javascript"
          },
          {
            "path": "src/auth/middleware.js",
            "lines": 80,
            "language": "javascript"
          }
        ]
      },
      "metrics": {
        "totalLines": 230,
        "complexity": "medium"
      }
    },
    "testing": {
      "status": "completed",
      "duration": "3m 45s",
      "outputs": {
        "testFiles": [
          {
            "path": "tests/auth.test.js",
            "tests": 15,
            "coverage": 92
          }
        ],
        "results": {
          "passed": 15,
          "failed": 0,
          "skipped": 0
        }
      }
    },
    "review": {
      "status": "completed",
      "duration": "2m 00s",
      "outputs": {
        "qualityScore": 8.5,
        "securityScore": "A",
        "performanceScore": "good"
      }
    },
    "documentation": {
      "status": "completed",
      "duration": "1m 30s",
      "outputs": {
        "apiDocs": "docs/api/auth.md",
        "examples": "docs/examples/auth-usage.md"
      }
    }
  },
  "artifacts": {
    "code": ["src/auth/jwt.js", "src/auth/middleware.js"],
    "tests": ["tests/auth.test.js"],
    "docs": ["docs/api/auth.md", "docs/examples/auth-usage.md"]
  },
  "metrics": {
    "totalTime": "17m 10s",
    "estimatedTime": "14-21m",
    "efficiency": 0.95,
    "tokensUsed": 6500,
    "qualityScore": 8.5,
    "testCoverage": 92
  },
  "issues": [],
  "recommendations": [
    "Consider adding rate limiting for production use",
    "Add logging for audit trail"
  ]
}
```

## Error Handling

### Error Categories

| Category | Examples | Recovery Strategy |
|----------|----------|-------------------|
| **Syntax** | Parse errors, missing brackets | Auto-fix with code-generator |
| **Type** | Type mismatches, missing types | Fix with type annotations |
| **Lint** | Style violations, formatting | Auto-format with linter |
| **Test** | Assertion failures, timeouts | Debug and fix implementation |
| **Security** | Vulnerabilities, exposures | Fix with security patterns |
| **Performance** | Slow operations, memory leaks | Optimize with patterns |

### Recovery Flow

```
ERROR DETECTED
    │
    ├─► CLASSIFY error type
    │
    ├─► DETERMINE recovery strategy
    │
    ├─► EXECUTE recovery
    │       │
    │       ├─► SUCCESS ──► Continue workflow
    │       │
    │       └─► FAILURE ──► Check retry count
    │                       │
    │                       ├─► Retries left ──► Retry
    │                       │
    │                       └─► Max retries ──► Escalate
    │
    └─► LOG recovery attempt
```

## Quality Gates

### Gate Implementation

```python
class QualityGate:
    """
    Quality gate between phases
    """
    
    def __init__(self, checks, on_failure):
        self.checks = checks
        self.on_failure = on_failure
    
    def evaluate(self, result):
        """
        Evaluate all checks and return pass/fail
        """
        failures = []
        
        for check in self.checks:
            if not self.run_check(check, result):
                failures.append(check)
        
        if failures:
            return GateResult(
                passed=False,
                failures=failures,
                action=self.on_failure
            )
        
        return GateResult(passed=True)
    
    def run_check(self, check, result):
        """
        Run individual quality check
        """
        # Implementation depends on check type
        if check == "no_syntax_errors":
            return result.syntax_valid
        elif check == "type_check_passes":
            return result.type_check_passed
        elif check == "all_tests_pass":
            return result.test_pass_rate == 1.0
        elif check == "coverage >= 80%":
            return result.coverage >= 80
        # ... more checks
```

### Gate Configuration

```yaml
# config/quality-gates.yaml

implementation_gate:
  checks:
    - no_syntax_errors
    - type_check_passes
    - lint_check_passes
  on_failure: fix_and_retry
  max_retries: 3

testing_gate:
  checks:
    - all_tests_pass
    - coverage >= 80%
    - no_critical_failures
  on_failure: debug_and_fix
  max_retries: 3

review_gate:
  checks:
    - quality_score >= 7
    - no_security_vulnerabilities
    - no_performance_issues
  on_failure: address_feedback
  max_retries: 2
```

## Examples

### Example 1: Feature Implementation

```
TASK: Implement user authentication with JWT

PHASE 1 - Analysis (2m):
  ✓ Analyzed project structure (Express.js, PostgreSQL)
  ✓ Identified existing patterns (middleware pattern used)
  ✓ Checked dependencies (jsonwebtoken available)

PHASE 2 - Design (2m):
  ✓ Generated implementation plan
  ✓ Designed data structures (User, Token)
  ⏸ CHECKPOINT: User confirmed approach

PHASE 3 - Implementation (5m):
  ✓ Generated JWT middleware (150 lines)
  ✓ Generated auth routes (80 lines)
  ✓ Type check passed
  ✓ Lint check passed

PHASE 4 - Testing (3m):
  ✓ Generated 15 unit tests
  ✓ All tests pass
  ✓ Coverage: 92%

PHASE 5 - Review (2m):
  ✓ Quality score: 8.5/10
  ✓ Security: No vulnerabilities
  ✓ Performance: Good

PHASE 6 - Documentation (1m):
  ✓ API documentation generated
  ✓ Usage examples created

RESULT: Completed successfully
ARTIFACTS: 2 code files, 1 test file, 2 doc files
METRICS: 17m total, 92% coverage, 8.5 quality score
```

### Example 2: Error Recovery Scenario

```
TASK: Implement file upload feature

PHASE 3 - Implementation:
  ✓ Generated upload handler
  ✗ Type check failed: Missing type for file parameter
  
  RECOVERY:
    → Attempt 1: Add type annotation
    → Type check passed ✓

PHASE 4 - Testing:
  ✓ Generated tests
  ✗ 2 tests failed: File size validation
  
  RECOVERY:
    → Attempt 1: Fix validation logic
    → Tests still failing
    → Attempt 2: Rewrite validation with proper bounds
    → All tests pass ✓

RESULT: Completed with 2 recovery cycles
```

## Related Skills

### Meta-Skills
- **task-planner** - Creates plans for this workflow
- **orchestrator** - Coordinates this workflow
- **reflector** - Analyzes execution results

### Action-Skills (Invoked)
- **code-analyzer** - Analyzes codebase
- **code-generator** - Generates code
- **test-generator** - Generates tests
- **code-reviewer** - Reviews code quality
- **doc-writer** - Creates documentation
- **type-checker** - Validates types
- **linter** - Checks style

### Related Workflows
- **debugging-workflow** - For bug fixes
- **refactoring-workflow** - For code improvement
- **testing-workflow** - For test-focused tasks
