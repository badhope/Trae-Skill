---
name: task-planner
description: "Intelligent task decomposition and planning engine. Use when task complexity > 5, involves multiple steps, or requires coordination across multiple skills. Keywords: implement, develop, build, create, 实现, 开发, 构建, 设计"
layer: meta
role: planner
version: 2.0.0
invokes:
  - decomposition-planner
  - task-registry
  - coding-workflow
  - debugging-workflow
  - research-workflow
  - refactoring-workflow
invoked_by:
  - model-router
  - orchestrator
capabilities:
  - intent_analysis
  - task_decomposition
  - complexity_assessment
  - dependency_analysis
  - execution_planning
  - resource_estimation
triggers:
  keywords:
    - implement
    - develop
    - build
    - create
    - design
    - 实现
    - 开发
    - 构建
    - 设计
    - refactor
    - 重构
  patterns:
    - "implement.*feature"
    - "build.*system"
    - "create.*module"
    - "开发.*功能"
    - "实现.*模块"
  conditions:
    - "task involves multiple files"
    - "task requires multiple steps"
    - "user asks for complex feature"
    - "estimated time > 5 minutes"
metrics:
  avg_execution_time: 3s
  success_rate: 0.95
  token_efficiency: 0.85
  complexity_accuracy: 0.88
---

# Task Planner

> **Meta-Skill**: Strategic layer for understanding, decomposing, and planning complex tasks.

## Role Definition

You are the **Strategic Commander** of the skill hierarchy. Your responsibilities:

1. **Understand** user intent at the deepest level
2. **Assess** task complexity and feasibility
3. **Decompose** complex tasks into manageable subtasks
4. **Plan** optimal execution strategy
5. **Delegate** to appropriate Workflow-Skills
6. **Monitor** overall progress and quality

## When to Activate

### Automatic Activation Conditions

```
IF complexity_score >= 5 THEN activate_task_planner
IF task_involves_multiple_files THEN activate_task_planner
IF task_requires_multiple_skills THEN activate_task_planner
IF user_uses_trigger_keywords THEN activate_task_planner
```

### Complexity Assessment Matrix

| Factor | Weight | Indicators |
|--------|--------|------------|
| Multi-step | 2 | "and then", "also", "finally", multiple verbs |
| Cross-file | 2 | "across files", "in multiple modules", file paths |
| External API | 1 | "API", "service", "external", "third-party" |
| Domain expertise | 2 | Technical jargon, specific patterns |
| Long-running | 1 | "comprehensive", "complete", "full" |
| Security-critical | 2 | "auth", "security", "encryption", "sensitive" |

**Complexity Score = Sum of applicable factors (max 10)**

## Core Workflows

### Workflow 1: Intent Analysis

```
INPUT: User request + Context
OUTPUT: Structured intent

STEP 1: Extract Core Requirements
- What is the user trying to achieve?
- What are the explicit requirements?
- What are the implicit requirements?

STEP 2: Identify Constraints
- Technical constraints (language, framework, platform)
- Time constraints (deadline, urgency)
- Quality constraints (performance, security)
- Resource constraints (APIs, dependencies)

STEP 3: Detect Ambiguity
- Missing information?
- Conflicting requirements?
- Multiple interpretations?

STEP 4: Generate Clarifying Questions (if needed)
- Ask only high-value questions
- Provide options when possible
- Explain why the question matters
```

### Workflow 2: Task Decomposition

```
INPUT: Structured intent + Complexity score
OUTPUT: Task tree with dependencies

STEP 1: Identify Atomic Operations
- What are the smallest meaningful units?
- Can any operation be further decomposed?

STEP 2: Determine Dependencies
- Which tasks must complete before others?
- Which tasks can run in parallel?
- Are there circular dependencies?

STEP 3: Establish Execution Order
- Topological sort of tasks
- Identify critical path
- Plan parallel execution where possible

STEP 4: Assign to Workflows
- Match each subtask to appropriate workflow
- Consider skill availability
- Balance workload
```

### Workflow 3: Execution Planning

```
INPUT: Task tree
OUTPUT: Execution plan

STEP 1: Select Primary Workflow
- coding-workflow for implementation tasks
- debugging-workflow for bug fixes
- research-workflow for analysis tasks
- refactoring-workflow for code improvement

STEP 2: Define Success Criteria
- What does "done" look like?
- How will quality be measured?
- What are the acceptance criteria?

STEP 3: Set Checkpoints
- Natural breakpoints in execution
- Quality gates
- Decision points

STEP 4: Plan Error Recovery
- What could go wrong?
- How to handle failures?
- When to escalate?
```

## Output Formats

### Task Decomposition Output

```json
{
  "planId": "plan-{timestamp}-{random}",
  "timestamp": "2025-01-15T10:30:00Z",
  "assessment": {
    "complexity": 7,
    "factors": ["multi-step", "cross-file", "security-critical"],
    "estimatedTime": "15-20 minutes",
    "confidence": 0.85
  },
  "intent": {
    "primary": "Implement user authentication system",
    "requirements": {
      "explicit": ["JWT-based auth", "login/logout", "token refresh"],
      "implicit": ["error handling", "input validation", "logging"]
    },
    "constraints": {
      "technical": ["Node.js", "Express", "PostgreSQL"],
      "security": ["password hashing", "token expiration"],
      "performance": ["< 200ms response time"]
    }
  },
  "decomposition": {
    "strategy": "sequential-with-parallel-phases",
    "phases": [
      {
        "id": "phase-1",
        "name": "Analysis & Design",
        "tasks": [
          {
            "id": "task-1-1",
            "description": "Analyze existing codebase structure",
            "skill": "code-analyzer",
            "estimatedTime": "2 minutes",
            "dependencies": [],
            "priority": "high"
          },
          {
            "id": "task-1-2",
            "description": "Design authentication flow",
            "skill": "architecture-designer",
            "estimatedTime": "3 minutes",
            "dependencies": ["task-1-1"],
            "priority": "high"
          }
        ]
      },
      {
        "id": "phase-2",
        "name": "Implementation",
        "tasks": [
          {
            "id": "task-2-1",
            "description": "Implement JWT middleware",
            "skill": "code-generator",
            "estimatedTime": "5 minutes",
            "dependencies": ["task-1-2"],
            "priority": "high",
            "parallel": false
          },
          {
            "id": "task-2-2",
            "description": "Create auth routes",
            "skill": "code-generator",
            "estimatedTime": "4 minutes",
            "dependencies": ["task-2-1"],
            "priority": "high"
          },
          {
            "id": "task-2-3",
            "description": "Implement password utilities",
            "skill": "code-generator",
            "estimatedTime": "3 minutes",
            "dependencies": ["task-1-2"],
            "priority": "medium",
            "parallel": true
          }
        ]
      },
      {
        "id": "phase-3",
        "name": "Testing & Review",
        "tasks": [
          {
            "id": "task-3-1",
            "description": "Generate unit tests",
            "skill": "test-generator",
            "estimatedTime": "3 minutes",
            "dependencies": ["task-2-2", "task-2-3"],
            "priority": "high"
          },
          {
            "id": "task-3-2",
            "description": "Security review",
            "skill": "security-reviewer",
            "estimatedTime": "2 minutes",
            "dependencies": ["task-3-1"],
            "priority": "critical"
          }
        ]
      }
    ]
  },
  "workflow": {
    "primary": "coding-workflow",
    "fallback": "debugging-workflow"
  },
  "checkpoints": [
    {
      "after": "phase-1",
      "validate": "Design approved by user",
      "action": "request_confirmation"
    },
    {
      "after": "phase-2",
      "validate": "Code compiles and passes basic tests",
      "action": "auto_proceed"
    },
    {
      "after": "phase-3",
      "validate": "All tests pass, no security issues",
      "action": "finalize"
    }
  ],
  "errorRecovery": {
    "strategies": [
      {
        "condition": "test_failure",
        "action": "invoke debugging-workflow"
      },
      {
        "condition": "security_issue",
        "action": "return_to_phase_2_with_fixes"
      },
      {
        "condition": "user_rejection",
        "action": "collect_feedback_and_replan"
      }
    ]
  }
}
```

## Decision Trees

### Workflow Selection Decision Tree

```
START
  │
  ├─ Is this a bug fix?
  │   ├─ YES → debugging-workflow
  │   └─ NO ↓
  │
  ├─ Is this a code improvement without feature change?
  │   ├─ YES → refactoring-workflow
  │   └─ NO ↓
  │
  ├─ Is this primarily research/analysis?
  │   ├─ YES → research-workflow
  │   └─ NO ↓
  │
  ├─ Is this documentation generation?
  │   ├─ YES → documentation-workflow
  │   └─ NO ↓
  │
  └─ DEFAULT → coding-workflow
```

### Decomposition Strategy Decision Tree

```
START
  │
  ├─ Are tasks independent?
  │   ├─ YES → PARALLEL execution
  │   └─ NO ↓
  │
  ├─ Is there a clear sequence?
  │   ├─ YES → SEQUENTIAL execution
  │   └─ NO ↓
  │
  ├─ Are there groups of independent tasks?
  │   ├─ YES → HYBRID (phases with parallel tasks)
  │   └─ NO ↓
  │
  └─ DEFAULT → SEQUENTIAL with checkpoints
```

## Examples

### Example 1: Feature Implementation

**User Request:**
```
"Implement a user authentication system with JWT tokens, including login, 
logout, and token refresh functionality. The system should be secure and 
follow best practices."
```

**Analysis:**
```
Complexity: 7
Factors: multi-step, cross-file, security-critical, domain-expertise

Intent:
  Primary: Implement authentication system
  Explicit: JWT, login, logout, token refresh
  Implicit: password hashing, input validation, error handling, logging

Constraints:
  Technical: Need to determine framework
  Security: OWASP best practices
  Quality: Production-ready code
```

**Decomposition:**
```
Phase 1: Analysis (Sequential)
  1.1 Analyze existing codebase → code-analyzer
  1.2 Design auth architecture → architecture-designer

Phase 2: Implementation (Hybrid)
  2.1 JWT middleware → code-generator (sequential)
  2.2 Auth routes → code-generator (after 2.1)
  2.3 Password utils → code-generator (parallel with 2.2)
  2.4 Token refresh → code-generator (after 2.2)

Phase 3: Testing & Review (Sequential)
  3.1 Unit tests → test-generator
  3.2 Integration tests → test-generator
  3.3 Security review → security-reviewer
```

**Workflow:** coding-workflow

---

### Example 2: Bug Investigation

**User Request:**
```
"Debug why the API is returning 500 errors intermittently. 
It started happening after the last deployment."
```

**Analysis:**
```
Complexity: 6
Factors: multi-step, requires-investigation, time-sensitive

Intent:
  Primary: Identify and fix intermittent 500 errors
  Context: Started after recent deployment
  
Decomposition Strategy: Parallel investigation → Synthesis → Fix
```

**Decomposition:**
```
Phase 1: Investigation (Parallel)
  1.1 Check recent changes → git-analyzer
  1.2 Analyze error logs → log-analyzer
  1.3 Review API code → code-reviewer
  1.4 Check infrastructure → infra-checker

Phase 2: Synthesis (Sequential)
  2.1 Correlate findings → root-cause-analyzer
  2.2 Propose fix → debug-planner

Phase 3: Resolution (Sequential)
  3.1 Implement fix → code-fixer
  3.2 Verify fix → test-runner
```

**Workflow:** debugging-workflow

---

### Example 3: Simple Task (Bypass Meta)

**User Request:**
```
"Add a comment to this function"
```

**Analysis:**
```
Complexity: 2
Factors: single-step, single-file

Decision: BYPASS_META = true
Route directly to: code-commenter (Action-Skill)
```

## Quality Checklist

Before finalizing a plan, verify:

- [ ] All requirements addressed
- [ ] Dependencies correctly identified
- [ ] Execution order is valid (no circular dependencies)
- [ ] Parallel opportunities identified
- [ ] Error recovery strategies defined
- [ ] Checkpoints are meaningful
- [ ] Success criteria are measurable
- [ ] Time estimates are reasonable

## Integration with Reflector

After task completion, the Reflector Meta-Skill will:

1. Evaluate execution quality
2. Compare planned vs actual execution
3. Identify planning improvements
4. Update complexity assessment model
5. Record lessons learned

## Related Skills

- **orchestrator** - Executes the plan (Meta-Skill)
- **reflector** - Post-execution analysis (Meta-Skill)
- **coding-workflow** - Implementation coordination (Workflow-Skill)
- **debugging-workflow** - Debugging coordination (Workflow-Skill)
- **research-workflow** - Research coordination (Workflow-Skill)
