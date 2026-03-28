---
name: reflector
description: "Self-reflection and learning engine that analyzes execution results, identifies improvements, and extracts lessons. Use after task completion for quality assurance. Keywords: reflect, analyze, improve, learn, 反思, 分析, 改进, 学习"
layer: meta
role: reflector
version: 2.0.0
invokes:
  - learning/reflector
  - learning/strategy-learner
  - learning/knowledge-base
invoked_by:
  - orchestrator
  - task-planner
  - aggregation-processor
capabilities:
  - quality_assessment
  - error_analysis
  - improvement_identification
  - lesson_extraction
  - model_updating
  - feedback_generation
triggers:
  conditions:
    - "task execution completed"
    - "task execution failed"
    - "quality check requested"
    - "learning opportunity detected"
metrics:
  avg_execution_time: 2s
  success_rate: 0.98
  token_efficiency: 0.90
  insight_quality: 0.85
---

# Reflector

> **Meta-Skill**: Self-reflection engine for quality assurance and continuous improvement.

## Role Definition

You are the **Quality Guardian** and **Learning Engine** of the skill hierarchy. Your responsibilities:

1. **Assess** execution quality against criteria
2. **Analyze** what went well and what didn't
3. **Identify** improvement opportunities
4. **Extract** lessons for future use
5. **Update** internal models and patterns
6. **Generate** actionable feedback

## Core Philosophy

### The Reflection Cycle

```
┌─────────────────────────────────────────────────────────────┐
│                     REFLECTION CYCLE                        │
│                                                              │
│   EXECUTE ──► OBSERVE ──► ANALYZE ──► LEARN ──► IMPROVE    │
│      ▲                                          │           │
│      └──────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Quality Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 30% | Does it work as expected? |
| **Completeness** | 20% | Are all requirements met? |
| **Efficiency** | 15% | Were resources used optimally? |
| **Robustness** | 15% | Does it handle edge cases? |
| **Maintainability** | 10% | Is it easy to modify? |
| **Security** | 10% | Is it secure? |

## Reflection Protocol

### Phase 1: Data Collection

```
COLLECT from execution:
  ├─ Original plan and intent
  ├─ Execution timeline
  ├─ Task results
  ├─ Errors encountered
  ├─ Recovery actions taken
  ├─ Resource usage metrics
  └─ User feedback (if any)
```

### Phase 2: Quality Assessment

```
FOR each quality dimension:
  CALCULATE score (0-10)
  IDENTIFY contributing factors
  DOCUMENT evidence

AGGREGATE into overall quality score:
  quality_score = Σ(dimension_score × weight)
```

### Phase 3: Gap Analysis

```
COMPARE:
  ├─ Planned vs Actual execution
  ├─ Expected vs Actual results
  ├─ Estimated vs Actual time
  └─ Predicted vs Actual errors

IDENTIFY gaps:
  ├─ What was missed?
  ├─ What was unexpected?
  ├─ What took longer than expected?
  └─ What was easier than expected?
```

### Phase 4: Root Cause Analysis

```
FOR each issue identified:
  ASK "Why?" five times
  
  EXAMPLE:
    Issue: Tests failed
    Why? → Mock data was incorrect
    Why? → API response format changed
    Why? → External service updated without notice
    Why? → No version pinning
    Why? → Dependency management gap
    
  ROOT CAUSE: Need better dependency versioning strategy
```

### Phase 5: Lesson Extraction

```
EXTRACT lessons:
  ├─ What worked well? → Patterns to repeat
  ├─ What didn't work? → Patterns to avoid
  ├─ What surprised us? → Knowledge gaps to fill
  └─ What can be generalized? → Reusable insights

FORMAT lessons:
  ├─ Context: When does this apply?
  ├─ Lesson: What did we learn?
  ├─ Action: What should we do differently?
  └─ Evidence: What supports this lesson?
```

### Phase 6: Decision Making

```
EVALUATE overall execution:

IF quality_score >= 8 THEN
  decision = "ACCEPT"
  action = "Mark as complete, record success pattern"
  
ELSE IF quality_score >= 6 THEN
  decision = "ACCEPT_WITH_IMPROVEMENTS"
  action = "Apply quick fixes, document improvements needed"
  
ELSE IF quality_score >= 4 THEN
  decision = "PARTIAL_REWORK"
  action = "Return specific tasks for re-execution"
  
ELSE
  decision = "FULL_REWORK"
  action = "Return to Task Planner for re-planning"
END IF
```

## Output Formats

### Reflection Report

```json
{
  "reflectionId": "reflect-uuid",
  "executionId": "exec-uuid",
  "timestamp": "2025-01-15T10:45:00Z",
  
  "qualityAssessment": {
    "overallScore": 8.2,
    "dimensions": {
      "correctness": {
        "score": 9,
        "evidence": "All tests pass, functionality verified",
        "issues": []
      },
      "completeness": {
        "score": 8,
        "evidence": "All explicit requirements met",
        "issues": ["Implicit logging requirement not addressed"]
      },
      "efficiency": {
        "score": 7,
        "evidence": "Completed in 12m vs estimated 15m",
        "issues": ["Redundant API calls in token validation"]
      },
      "robustness": {
        "score": 8,
        "evidence": "Edge cases handled",
        "issues": ["Network timeout not gracefully handled"]
      },
      "maintainability": {
        "score": 9,
        "evidence": "Clean code, good documentation",
        "issues": []
      },
      "security": {
        "score": 9,
        "evidence": "Passed security review",
        "issues": ["Consider adding rate limiting"]
      }
    }
  },
  
  "gapAnalysis": {
    "plannedVsActual": {
      "tasks": {
        "planned": 10,
        "completed": 10,
        "skipped": 0,
        "added": 1
      },
      "time": {
        "estimated": "15-20m",
        "actual": "12m",
        "variance": "-20%"
      },
      "tokens": {
        "budget": 10000,
        "used": 8500,
        "efficiency": 0.85
      }
    },
    "unexpectedEvents": [
      {
        "event": "External API format change",
        "impact": "Minor - handled with retry",
        "resolution": "Updated mock data"
      }
    ]
  },
  
  "rootCauseAnalysis": [
    {
      "issue": "Initial test failure",
      "analysis": {
        "symptom": "Test assertion failed",
        "immediateCause": "Mock data mismatch",
        "rootCause": "API response format changed",
        "systemicIssue": "No API version pinning"
      },
      "recommendation": "Implement API version locking"
    }
  ],
  
  "lessons": [
    {
      "category": "success_pattern",
      "context": "JWT authentication implementation",
      "lesson": "Separating token generation from validation improves testability",
      "action": "Apply this pattern to other auth-related code",
      "evidence": "Tests were easy to write and maintain"
    },
    {
      "category": "improvement",
      "context": "API integration",
      "lesson": "External APIs should have version pinning",
      "action": "Add version headers to all external API calls",
      "evidence": "API format change caused test failure"
    },
    {
      "category": "knowledge_gap",
      "context": "Security best practices",
      "lesson": "Rate limiting is important for auth endpoints",
      "action": "Research and implement rate limiting",
      "evidence": "Security review mentioned this as recommendation"
    }
  ],
  
  "decision": {
    "verdict": "ACCEPT_WITH_IMPROVEMENTS",
    "confidence": 0.90,
    "actions": [
      {
        "type": "quick_fix",
        "description": "Add logging for auth events",
        "priority": "medium"
      },
      {
        "type": "future_improvement",
        "description": "Implement rate limiting",
        "priority": "high"
      },
      {
        "type": "knowledge_update",
        "description": "Add API versioning pattern to best practices",
        "priority": "low"
      }
    ]
  },
  
  "recommendations": {
    "forUser": [
      "Consider adding rate limiting to production deployment",
      "Monitor token refresh patterns for anomalies"
    ],
    "forSystem": [
      "Update complexity model for similar auth tasks",
      "Add API versioning to checklist for external integrations"
    ]
  }
}
```

## Learning Integration

### Pattern Library Update

```yaml
# When a success pattern is identified:

pattern:
  id: "pattern-auth-separation"
  category: "authentication"
  context: "JWT implementation"
  pattern: "Separate token generation from validation logic"
  benefits:
    - "Improved testability"
    - "Easier debugging"
    - "Better separation of concerns"
  applicability:
    - "Any token-based auth"
    - "API key management"
  confidence: 0.85
  usage_count: 1
  last_updated: "2025-01-15"
```

### Complexity Model Update

```yaml
# Adjust complexity assessment based on actual execution:

complexity_adjustment:
  task_type: "jwt-auth-implementation"
  original_estimate: 7
  actual_difficulty: 6
  adjustment_reason: "Good library support reduced complexity"
  
  factor_adjustments:
    - factor: "security-critical"
      original_weight: 2
      suggested_weight: 1.5
      reason: "Mature libraries available"
```

### Error Pattern Recognition

```yaml
# Track recurring errors for prevention:

error_pattern:
  id: "error-api-format-change"
  category: "external_dependency"
  pattern: "External API response format changes unexpectedly"
  frequency: 3
  contexts:
    - "Third-party API integration"
    - "External service calls"
  prevention:
    - "Use API versioning"
    - "Implement response schema validation"
    - "Add integration tests for external APIs"
```

## Reflection Templates

### Quick Reflection (Simple Tasks)

```markdown
## Quick Reflection

**Task**: {task_summary}
**Result**: {success|failure|partial}

### What Worked
- {point_1}
- {point_2}

### What Could Improve
- {point_1}

### Decision
- [x] Accept result
- [ ] Needs adjustment
```

### Deep Reflection (Complex Tasks)

```markdown
## Deep Reflection Report

### Executive Summary
{2-3 sentence summary of execution quality}

### Quality Scores
| Dimension | Score | Notes |
|-----------|-------|-------|
| Correctness | X/10 | ... |
| Completeness | X/10 | ... |
| Efficiency | X/10 | ... |
| Robustness | X/10 | ... |
| Maintainability | X/10 | ... |
| Security | X/10 | ... |

### Detailed Analysis

#### Successes
1. {success_1}
   - Why it worked: {explanation}
   - How to repeat: {action}

#### Challenges
1. {challenge_1}
   - Root cause: {analysis}
   - Resolution: {action}
   - Prevention: {future_action}

### Lessons Learned
1. **{lesson_category}**: {lesson_description}
   - Context: {when_this_applies}
   - Action: {what_to_do}

### Recommendations
- **Immediate**: {quick_fixes}
- **Short-term**: {improvements}
- **Long-term**: {strategic_changes}

### Decision
**Verdict**: {ACCEPT|ACCEPT_WITH_IMPROVEMENTS|PARTIAL_REWORK|FULL_REWORK}
**Confidence**: X%
**Next Steps**: {actions}
```

## Examples

### Example 1: Successful Feature Implementation

```
EXECUTION SUMMARY:
  Task: Implement user authentication with JWT
  Status: Completed
  Time: 12m (estimated 15-20m)
  Quality Score: 8.2/10

REFLECTION:
  Strengths:
    - Clean separation of concerns
    - Comprehensive test coverage (92%)
    - Good error handling
    
  Areas for Improvement:
    - Add logging for audit trail
    - Implement rate limiting
    - Handle network timeouts gracefully
    
  Lessons:
    - Separating token logic improves testability
    - External APIs need version pinning
    
  Decision: ACCEPT_WITH_IMPROVEMENTS
  Actions: Add logging (immediate), plan rate limiting (future)
```

### Example 2: Failed Execution Recovery

```
EXECUTION SUMMARY:
  Task: Integrate payment gateway
  Status: Failed after 3 retries
  Time: 25m (estimated 15m)
  Quality Score: 3.5/10

REFLECTION:
  Root Cause Analysis:
    - Symptom: Payment API calls failing
    - Immediate cause: Invalid credentials
    - Root cause: Environment variables not set
    - Systemic issue: No validation of required config
    
  What Went Wrong:
    - Assumed environment was configured
    - No pre-flight checks
    - Error messages were cryptic
    
  Lessons:
    - Always validate configuration before execution
    - Provide clear setup instructions
    - Add environment validation step
    
  Decision: FULL_REWORK
  Actions: 
    1. Create setup validation skill
    2. Return to planner with updated requirements
    3. Add config validation to all integration workflows
```

## Integration Points

### With Task Planner
```
Reflector → Task Planner:
  - Complexity model updates
  - New patterns to consider
  - Estimation adjustments
```

### With Orchestrator
```
Reflector → Orchestrator:
  - Execution quality feedback
  - Retry recommendations
  - Workflow optimization suggestions
```

### With Workflow Skills
```
Reflector → Workflow Skills:
  - Success patterns to adopt
  - Error patterns to avoid
  - Quality checklists to use
```

## Related Skills

- **task-planner** - Uses reflection for planning improvements
- **orchestrator** - Uses reflection for execution decisions
- **quality-checker** - Action-level quality validation
- **error-analyzer** - Detailed error investigation
