---
name: "planning"
description: "Creates execution plans and breaks down complex tasks into subtasks. Invoke when user needs help planning a project, feature, or complex task."
---

# Planning Skill

Systematic project and task planning methodologies.

## When to Use

- User needs to plan a new project or feature
- Complex task needs to be broken down
- Need to create a project roadmap
- Need to estimate time and resources
- Need to identify risks and dependencies

## Planning Workflows

### 1. Create Execution Plan

Use `create-execution-plan` for comprehensive project planning:

**Components:**
- Project overview and objectives
- Phase breakdown with milestones
- Detailed timeline
- Risk assessment
- Resource allocation
- Communication plan
- Success criteria

**Phase Structure:**
```
P0: Preparation (1 week)
    - Requirements confirmation
    - Architecture design
    - Environment setup

P1: Development (4 weeks)
    - Core feature development
    - Integration
    - Unit testing

P2: Testing (2 weeks)
    - Integration testing
    - Performance testing
    - UAT

P3: Deployment (1 week)
    - Deployment preparation
    - Staged rollout
    - Full release
```

### 2. Break Down Task into Subtasks

Use `break-down-task-into-subtasks` for task decomposition:

**Decomposition Principles:**
- MECE (Mutually Exclusive, Completely Exhaustive)
- Each subtask should be 0.5-2 days of work
- Clear dependencies between subtasks
- Each subtask has clear output

**Structure:**
```
L1: Phase/Module (e.g., Development)
L2: Functional Block (e.g., User Module)
L3: Executable Task (e.g., Implement Login)
```

## Task Breakdown Example

For a "User Registration Feature":

```
1. Preparation
   1.1 Set up environment
   1.2 Review existing auth system

2. Database Design
   2.1 Design user table schema
   2.2 Create database migration

3. Backend Development
   3.1 Implement registration API
   3.2 Add input validation
   3.3 Implement password hashing
   3.4 Add email uniqueness check

4. Frontend Development
   4.1 Create registration form
   4.2 Add form validation
   4.3 Connect to API

5. Testing
   5.1 Write unit tests
   5.2 Write integration tests

6. Deployment
   6.1 Deploy to staging
   6.2 Verify in production
```

## Risk Management

### Risk Matrix

| Impact | Low | Medium | High |
|--------|-----|--------|------|
| **Likelihood High** | 🟡 | 🔴 | 🔴 |
| **Likelihood Medium** | 🟢 | 🟡 | 🔴 |
| **Likelihood Low** | 🟢 | 🟢 | 🟡 |

### Mitigation Strategies

1. **Personnel shortage**: Buffer resources, cross-train
2. **Technical difficulty**: Tech spike, alternative solutions
3. **Requirement changes**: Agile approach, scope management
4. **Third-party dependencies**: Multi-vendor, fallback options

## Estimation Techniques

### Three-Point Estimation

```
Estimate = (Optimistic + 4×Most Likely + Pessimistic) / 6
```

### Time Buffers

| Task Complexity | Buffer |
|-----------------|--------|
| Simple | 10% |
| Medium | 20% |
| Complex | 30% |

## Deliverables

When planning, always define:

1. **Milestones**: Key checkpoints with dates
2. **Dependencies**: What must be completed first
3. **Success Criteria**: How to measure completion
4. **Risks**: What could go wrong
5. **Mitigation**: How to reduce risk impact

## Related Prompts

- `prompt-task-planning-create-execution-plan`
- `prompt-task-planning-break-down-task-into-subtasks`

## Related Skills

- `research` - for research tasks before planning
- `repo-analysis` - understand technical constraints
