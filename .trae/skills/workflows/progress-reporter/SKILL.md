---
name: progress-reporter
description: "Tier 1: Report progress to user, show what's happening, estimate time remaining. Keywords: progress report, status update, ETA, 进度报告, 状态更新"
layer: workflow
role: reporter
tier: 1
version: 5.0.0
architecture: single-agent
invokes:
  - task-registry
invoked_by:
  - lead-agent
  - full-stack-development
  - enterprise-project
capabilities:
  - progress_tracking
  - status_reporting
  - eta_estimation
  - user_communication
triggers:
  keywords:
    - progress report
    - status update
    - ETA
    - how much longer
    - 进度报告
    - 状态更新
    - 还要多久
  conditions:
    - "long-running task"
    - "user asks for status"
    - "every N minutes"
metrics:
  update_frequency: "every 2-5 minutes"
  user_satisfaction: 0.9
  eta_accuracy: 0.85
---

# Progress Reporter - Tier 1

> **Tier 1 Skill**: Report progress, show status, estimate time remaining

## What is Progress Reporting?

Keep the user informed about what's happening, how much is done, and how long is left.

```
NO PROGRESS REPORT:
  User: "How's it going?"
  AI: "Working on it..."
  (User waits 45min with no idea what's happening)
  → Frustrated!

WITH PROGRESS REPORTER:
  User: "How's it going?"
  
  [0:05] Progress: 10% (Researching...)
  [0:10] Progress: 25% (Designing API...)
  [0:15] Progress: 40% (Writing backend code...)
  [0:20] Progress: 60% (Writing frontend code...)
  [0:25] Progress: 75% (Setting up DevOps...)
  [0:30] Progress: 90% (Testing...)
  [0:35] Progress: 100% (Done!) ✓
  
  → User always knows what's happening!
  → No frustration!
```

## Progress Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Percent Complete** | 0-100% | 45% |
| **Current Phase** | What's happening now | "Writing frontend code" |
| **ETA** | Estimated time remaining | "~15 minutes left" |
| **Completed** | What's already done | ["Research", "API Design"] |
| **Upcoming** | What's next | ["Testing", "Deployment"] |

## Report Formats

### Format 1: Short Status

```
Progress: 45% | Current: Writing frontend | ETA: ~15min left
```

### Format 2: Detailed Update

```
╔═══════════════════════════════════════════════╗
║          PROGRESS UPDATE                       ║
╠═══════════════════════════════════════════════╣
║  Overall Progress:  45% █████░░░░░░░░░░░░░░  ║
║                                                   ║
║  Current Phase:    Writing frontend code         ║
║  Time Elapsed:     20 minutes                    ║
║  ETA:              ~15 minutes left              ║
║                                                   ║
║  Completed:                                        ║
║    ✓ Research (10%)                               ║
║    ✓ API Design (25%)                             ║
║    ✓ Backend Code (40%)                           ║
║                                                   ║
║  Up Next:                                          ║
║    ○ Frontend Code (in progress)                  ║
║    ○ DevOps Setup                                  ║
║    ○ Testing                                       ║
║    ○ Deployment                                    ║
╚═══════════════════════════════════════════════╝
```

## When to Report

| Trigger | Frequency |
|---------|-----------|
| **Phase change** | Every time phase changes |
| **Time-based** | Every 2-5 minutes |
| **User request** | Immediately when user asks |
| **Milestone** | At 25%, 50%, 75%, 100% |

## Handoff/Integration

```
Lead Agent ━━(periodic updates)━━► Progress Reporter ━━(output)━━► User
     │                                    │
  ├─ Current phase                  ├─ Format report
  ├─ Percent complete               └─ Send to user
  └─ History
```

## Example: Full Stack Project Progress

```
PROJECT: Full Stack Todo App

[0:00] Starting...
  Progress: 0% | Current: Initializing | ETA: ~45min

[0:05] Phase 1 Complete!
  Progress: 10% █░░░░░░░░░ | Current: Researching...
  Completed: ✓ Kickoff

[0:10] Phase 2 Complete!
  Progress: 25% ██░░░░░░░░ | Current: Designing API...
  Completed: ✓ Research, ✓ API Design

[0:20] Phase 3 Complete!
  Progress: 50% █████░░░░░ | Current: Writing backend...
  Completed: ✓ Research, ✓ API Design, ✓ Backend

[0:30] Phase 4 Complete!
  Progress: 75% ████████░░ | Current: Writing frontend...
  Completed: ✓ ..., ✓ Frontend

[0:40] Phase 5 Complete!
  Progress: 90% █████████░ | Current: Testing...
  Completed: ✓ ..., ✓ DevOps

[0:45] DONE!
  Progress: 100% ██████████ | Complete!
  ✓ All tasks done!
```

## Related Skills

- **task-registry** - Task history
- **lead-agent** - Overall coordination
