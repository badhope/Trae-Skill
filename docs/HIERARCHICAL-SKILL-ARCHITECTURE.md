# Hierarchical Collaborative Skill Architecture (HCSA)

## 分层协作式技能架构规范 v1.0

> **创新点**: 将传统单一Skill升级为三层协作架构，实现任务自动分解、智能调度、自我反思

---

## 1. 架构概述

### 1.1 核心理念

传统Skill是扁平的指令集，HCSA将其升级为**分层协作系统**：

```
┌─────────────────────────────────────────────────────────────┐
│                    META-SKILL LAYER                         │
│         (战略层 - 任务理解、分解、规划、反思)                   │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ TaskPlanner │  │ Orchestrator│  │ Reflector   │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
└─────────┼────────────────┼────────────────┼──────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                  WORKFLOW-SKILL LAYER                       │
│         (战术层 - 流程编排、状态管理、结果聚合)                 │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │ Coordinator │  │ StateManager│  │ Aggregator  │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
└─────────┼────────────────┼────────────────┼──────────────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                   ACTION-SKILL LAYER                        │
│         (执行层 - 具体操作、工具调用、数据处理)                 │
│                                                              │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
│  │ Coder  │ │Tester  │ │Analyst │ │Writer  │ │Reviewer│     │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 三层职责

| 层级 | 角色 | 职责 | 触发条件 |
|------|------|------|----------|
| **Meta-Skill** | 战略指挥官 | 理解意图、分解任务、规划路径、反思优化 | 复杂任务、多步骤任务 |
| **Workflow-Skill** | 战术协调官 | 编排流程、管理状态、聚合结果、处理异常 | 需要协调多个Action |
| **Action-Skill** | 执行专家 | 执行具体操作、调用工具、返回结果 | 单一明确任务 |

---

## 2. Skill元数据规范

### 2.1 扩展的Frontmatter

```yaml
---
# 基础信息
name: skill-name
description: "简短描述，包含触发关键词"
version: 1.0.0
author: Your Name
license: MIT

# HCSA核心字段
layer: meta | workflow | action    # 必需：所属层级
role: planner | orchestrator | coordinator | executor | reflector  # 必需：角色类型

# 协作关系
invokes: [skill-a, skill-b]        # 可选：调用的下层skill
invoked_by: [parent-skill]         # 可选：被哪个上层skill调用
depends_on: [dependency-skill]     # 可选：依赖的其他skill

# 触发配置
triggers:
  keywords: [keyword1, keyword2]   # 触发关键词
  patterns: ["regex pattern"]      # 触发模式
  conditions:                      # 触发条件
    - "user asks about X"
    - "task complexity > 3"

# 能力声明
capabilities:
  - task_decomposition             # 任务分解
  - result_aggregation             # 结果聚合
  - error_recovery                 # 错误恢复
  - self_reflection                # 自我反思

# 性能指标
metrics:
  avg_execution_time: 5s           # 平均执行时间
  success_rate: 0.95               # 成功率
  token_efficiency: 0.8            # Token效率
---
```

### 2.2 层级标识

```yaml
# Meta-Skill示例
layer: meta
role: planner
invokes: [coding-workflow, debugging-workflow]

# Workflow-Skill示例  
layer: workflow
role: coordinator
invokes: [code-generator, test-generator, reviewer]
invoked_by: [feature-planner]

# Action-Skill示例
layer: action
role: executor
invoked_by: [coding-coordinator]
```

---

## 3. 目录结构规范

### 3.1 标准结构

```
skill-repository/
├── meta/                          # Meta-Skill层
│   ├── task-planner/
│   │   ├── SKILL.md               # 主文件
│   │   ├── prompts/               # 内部提示词
│   │   │   ├── decompose.md
│   │   │   └── plan.md
│   │   ├── schemas/               # 数据结构
│   │   │   └── task-tree.json
│   │   └── examples/              # 示例
│   │       └── complex-task.md
│   ├── orchestrator/
│   │   └── SKILL.md
│   └── reflector/
│       └── SKILL.md
│
├── workflows/                     # Workflow-Skill层
│   ├── coding-workflow/
│   │   ├── SKILL.md
│   │   ├── states/                # 状态定义
│   │   │   └── state-machine.json
│   │   ├── transitions/           # 状态转换
│   │   │   └── transitions.yaml
│   │   └── templates/             # 输出模板
│   │       └── report.md
│   ├── debugging-workflow/
│   │   └── SKILL.md
│   └── research-workflow/
│       └── SKILL.md
│
├── actions/                       # Action-Skill层
│   ├── code-generator/
│   │   ├── SKILL.md
│   │   └── scripts/               # 执行脚本
│   │       └── generate.py
│   ├── test-generator/
│   │   └── SKILL.md
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── doc-writer/
│       └── SKILL.md
│
├── shared/                        # 共享资源
│   ├── schemas/                   # 通用数据结构
│   │   ├── task.json
│   │   ├── result.json
│   │   └── error.json
│   ├── prompts/                   # 通用提示词
│   │   ├── reflection.md
│   │   └── error-handling.md
│   └── utils/                     # 工具函数
│       └── helpers.py
│
└── config/                        # 配置文件
    ├── routing.yaml               # 路由配置
    ├── capabilities.yaml          # 能力映射
    └── thresholds.yaml            # 阈值配置
```

---

## 4. 执行流程规范

### 4.1 任务处理流程

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 1. INTENT ANALYSIS (Meta-Skill: TaskPlanner)            │
│    - 理解用户意图                                        │
│    - 评估任务复杂度                                      │
│    - 决定是否需要分层处理                                │
└─────────────────────────────────────────────────────────┘
    │
    ▼ (复杂任务)
┌─────────────────────────────────────────────────────────┐
│ 2. TASK DECOMPOSITION (Meta-Skill: TaskPlanner)         │
│    - 分解为子任务                                        │
│    - 识别依赖关系                                        │
│    - 生成执行计划                                        │
│    输出: TaskTree { tasks[], dependencies[], order[] }   │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 3. ORCHESTRATION (Meta-Skill: Orchestrator)             │
│    - 选择合适的Workflow-Skill                            │
│    - 分配任务给Workflow                                  │
│    - 监控执行进度                                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 4. COORDINATION (Workflow-Skill: Coordinator)           │
│    - 管理执行状态                                        │
│    - 调度Action-Skill                                    │
│    - 处理中间结果                                        │
│    - 处理异常情况                                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 5. EXECUTION (Action-Skill: Executor)                   │
│    - 执行具体操作                                        │
│    - 调用工具/API                                        │
│    - 返回执行结果                                        │
│    输出: ActionResult { status, data, metrics }          │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 6. AGGREGATION (Workflow-Skill: Aggregator)             │
│    - 收集所有Action结果                                  │
│    - 合并、去重、验证                                    │
│    - 生成中间输出                                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│ 7. REFLECTION (Meta-Skill: Reflector)                   │
│    - 评估执行质量                                        │
│    - 识别改进点                                          │
│    - 决定是否需要重试/调整                               │
│    - 记录学习经验                                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
最终输出
```

### 4.2 状态机设计

```yaml
# states/state-machine.yaml
states:
  initialized:
    description: "任务已初始化"
    transitions: [planning, direct_execution]
    
  planning:
    description: "正在规划任务"
    transitions: [decomposed, failed]
    
  decomposed:
    description: "任务已分解"
    transitions: [scheduling, failed]
    
  scheduling:
    description: "正在调度执行"
    transitions: [executing, failed]
    
  executing:
    description: "正在执行子任务"
    transitions: [aggregating, partial_failure, failed]
    
  aggregating:
    description: "正在聚合结果"
    transitions: [reflecting, failed]
    
  reflecting:
    description: "正在反思优化"
    transitions: [completed, retry, failed]
    
  completed:
    description: "任务完成"
    transitions: []
    
  retry:
    description: "需要重试"
    transitions: [planning, executing]
    
  partial_failure:
    description: "部分失败"
    transitions: [retry, degraded_completion]
    
  degraded_completion:
    description: "降级完成"
    transitions: [completed]
    
  failed:
    description: "任务失败"
    transitions: []
```

---

## 5. 通信协议

### 5.1 任务结构

```json
{
  "$schema": "./shared/schemas/task.json",
  "taskId": "task-uuid",
  "parentId": "parent-task-uuid",
  "type": "coding | debugging | analysis | writing",
  "layer": "meta | workflow | action",
  "complexity": {
    "score": 7,
    "factors": ["multi-step", "cross-file", "external-api"]
  },
  "input": {
    "query": "用户原始请求",
    "context": {},
    "constraints": []
  },
  "decomposition": {
    "strategy": "sequential | parallel | hybrid",
    "subtasks": [
      {
        "id": "subtask-1",
        "skill": "code-generator",
        "dependencies": [],
        "priority": "high"
      }
    ]
  },
  "state": "executing",
  "results": [],
  "metrics": {
    "startTime": "2025-01-01T00:00:00Z",
    "tokensUsed": 0,
    "actionsCount": 0
  }
}
```

### 5.2 结果结构

```json
{
  "$schema": "./shared/schemas/result.json",
  "resultId": "result-uuid",
  "taskId": "task-uuid",
  "status": "success | failure | partial",
  "layer": "action",
  "output": {
    "type": "code | text | data",
    "content": "实际输出内容",
    "artifacts": []
  },
  "confidence": 0.95,
  "issues": [],
  "suggestions": [],
  "metrics": {
    "executionTime": "2.5s",
    "tokensUsed": 1500,
    "toolCalls": 3
  }
}
```

---

## 6. 智能路由

### 6.1 路由配置

```yaml
# config/routing.yaml
routing_rules:
  - name: "complex_coding_task"
    condition:
      keywords: ["实现", "implement", "开发", "develop"]
      complexity_threshold: 5
      has_multiple_files: true
    route:
      meta_skill: "task-planner"
      workflow: "coding-workflow"
      
  - name: "simple_code_fix"
    condition:
      keywords: ["修复", "fix", "bug"]
      complexity_threshold: 3
    route:
      action_skill: "code-fixer"
      bypass_meta: true
      
  - name: "research_task"
    condition:
      keywords: ["研究", "research", "分析", "analyze"]
    route:
      meta_skill: "task-planner"
      workflow: "research-workflow"

fallback:
  default_meta: "task-planner"
  default_workflow: "general-workflow"
  default_action: "general-assistant"
```

### 6.2 复杂度评估

```python
# shared/utils/complexity.py
def evaluate_complexity(task: Task) -> ComplexityScore:
    """
    评估任务复杂度 (1-10)
    """
    score = 1
    factors = []
    
    # 多步骤检测
    if has_multiple_steps(task.query):
        score += 2
        factors.append("multi-step")
    
    # 跨文件检测
    if involves_multiple_files(task.context):
        score += 2
        factors.append("cross-file")
    
    # 外部依赖检测
    if requires_external_resources(task.query):
        score += 1
        factors.append("external-api")
    
    # 知识深度检测
    if requires_domain_expertise(task.query):
        score += 2
        factors.append("domain-expertise")
    
    # 时间跨度检测
    if is_long_running(task.query):
        score += 1
        factors.append("long-running")
    
    return ComplexityScore(
        score=min(score, 10),
        factors=factors
    )
```

---

## 7. 自我反思机制

### 7.1 反思流程

```markdown
## Reflection Protocol

### 1. Quality Assessment
- 结果是否符合预期？
- 是否满足所有约束条件？
- 是否有遗漏或错误？

### 2. Efficiency Analysis
- Token使用是否合理？
- 执行路径是否最优？
- 是否有不必要的步骤？

### 3. Learning Extraction
- 什么做法有效？
- 什么需要改进？
- 如何避免类似问题？

### 4. Decision Making
- [ ] 结果满意 → 完成
- [ ] 需要微调 → 返回执行层
- [ ] 策略错误 → 返回规划层
- [ ] 无法完成 → 报告失败原因
```

### 7.2 反思模板

```markdown
# shared/prompts/reflection.md

## 执行反思报告

### 任务概览
- 任务ID: {taskId}
- 执行路径: {executionPath}
- 总耗时: {totalTime}

### 质量评估
| 维度 | 得分 | 说明 |
|------|------|------|
| 正确性 | {score}/10 | {explanation} |
| 完整性 | {score}/10 | {explanation} |
| 效率性 | {score}/10 | {explanation} |

### 问题识别
{identifiedIssues}

### 改进建议
{improvementSuggestions}

### 决策
- [ ] 接受结果
- [ ] 需要重试: {retryReason}
- [ ] 需要调整策略: {adjustmentReason}
```

---

## 8. 最佳实践

### 8.1 Skill设计原则

1. **单一职责**: 每个Skill只做一件事
2. **渐进式加载**: 元数据 → 核心指令 → 参考文档
3. **明确边界**: 清晰定义输入输出
4. **可组合性**: 通过组合实现复杂功能
5. **可观测性**: 记录执行过程和指标

### 8.2 层级交互原则

1. **向下委托**: 上层只委托，不执行
2. **向上汇报**: 下层只汇报，不决策
3. **同级协作**: Workflow层可横向协作
4. **错误隔离**: 单层失败不影响其他层

### 8.3 性能优化

1. **并行执行**: 独立子任务并行处理
2. **缓存复用**: 相似任务结果缓存
3. **提前终止**: 满足条件提前结束
4. **资源限制**: Token和时间预算控制

---

## 9. 示例：完整Skill定义

### 9.1 Meta-Skill示例

```yaml
# meta/task-planner/SKILL.md
---
name: task-planner
description: "Intelligent task decomposition and planning. Use when task complexity > 5 or involves multiple steps."
layer: meta
role: planner
invokes: [coding-workflow, debugging-workflow, research-workflow]
capabilities:
  - task_decomposition
  - complexity_assessment
  - dependency_analysis
  - execution_planning
triggers:
  keywords: [implement, develop, build, create, 实现, 开发, 构建]
  conditions:
    - "task involves multiple files"
    - "task requires multiple steps"
    - "user asks for complex feature"
---

# Task Planner

> Strategic layer for understanding, decomposing, and planning complex tasks.

## When to Use

- Task complexity score > 5
- Involves multiple files or modules
- Requires coordination of multiple skills
- User requests complex feature implementation

## Core Capabilities

### 1. Intent Analysis
Understand what the user really wants:
- Extract core requirements
- Identify implicit constraints
- Detect ambiguity and ask clarifying questions

### 2. Complexity Assessment
Evaluate task difficulty:
```
Complexity = base_score
           + multi_step_factor (0-2)
           + cross_file_factor (0-2)
           + external_api_factor (0-1)
           + domain_expertise_factor (0-2)
           + long_running_factor (0-1)
```

### 3. Task Decomposition
Break down into manageable subtasks:
- Identify atomic operations
- Determine dependencies
- Establish execution order
- Assign to appropriate workflows

### 4. Execution Planning
Create actionable plan:
- Select appropriate workflow
- Define success criteria
- Set checkpoints
- Plan error recovery

## Output Format

```json
{
  "planId": "plan-uuid",
  "assessment": {
    "complexity": 7,
    "factors": ["multi-step", "cross-file"],
    "estimatedTime": "10-15 minutes"
  },
  "decomposition": {
    "strategy": "sequential",
    "subtasks": [
      {
        "id": "subtask-1",
        "description": "Analyze existing code structure",
        "skill": "code-analyzer",
        "dependencies": [],
        "priority": "high"
      }
    ]
  },
  "workflow": "coding-workflow",
  "checkpoints": [
    "After code analysis",
    "After implementation",
    "After testing"
  ]
}
```

## Examples

### Example 1: Feature Implementation

**Input:**
"Implement user authentication with JWT tokens"

**Analysis:**
- Complexity: 7 (multi-step, cross-file, security-critical)
- Strategy: Sequential with validation checkpoints

**Decomposition:**
1. Analyze existing auth patterns (code-analyzer)
2. Design auth flow (architecture-designer)
3. Implement JWT middleware (code-generator)
4. Add auth routes (code-generator)
5. Write tests (test-generator)
6. Security review (security-reviewer)

**Workflow:** coding-workflow

### Example 2: Bug Investigation

**Input:**
"Debug why the API is returning 500 errors intermittently"

**Analysis:**
- Complexity: 6 (multi-step, requires investigation)
- Strategy: Parallel investigation then synthesis

**Decomposition:**
1. Check recent changes (git-analyzer)
2. Analyze error logs (log-analyzer) [parallel]
3. Review API code (code-reviewer) [parallel]
4. Identify root cause (debugger)
5. Propose fix (code-fixer)

**Workflow:** debugging-workflow
```

### 9.2 Workflow-Skill示例

```yaml
# workflows/coding-workflow/SKILL.md
---
name: coding-workflow
description: "Orchestrates code generation, testing, and review workflow. Use for feature implementation tasks."
layer: workflow
role: coordinator
invokes: [code-generator, test-generator, code-reviewer, doc-writer]
invoked_by: [task-planner]
capabilities:
  - state_management
  - result_aggregation
  - error_recovery
---

# Coding Workflow

> Tactical layer for coordinating code generation tasks.

## State Machine

```
initialized → analyzing → generating → testing → reviewing → documenting → completed
                  ↓            ↓           ↓           ↓
                failed       failed      failed      failed
                  ↓            ↓           ↓           ↓
               recovery → retry → fallback
```

## Coordination Protocol

### Phase 1: Analysis
- Invoke: code-analyzer
- Collect: existing patterns, dependencies
- Decision: Proceed if analysis successful

### Phase 2: Generation
- Invoke: code-generator
- Collect: generated code
- Validation: Syntax check, type check
- Decision: Proceed if valid, retry if errors

### Phase 3: Testing
- Invoke: test-generator
- Collect: test cases
- Execution: Run tests
- Decision: Proceed if passing, fix if failing

### Phase 4: Review
- Invoke: code-reviewer
- Collect: review feedback
- Decision: Accept or request changes

### Phase 5: Documentation
- Invoke: doc-writer
- Collect: documentation
- Finalize: Complete workflow

## Error Handling

| Error Type | Action |
|------------|--------|
| Syntax Error | Retry with corrected prompt |
| Type Error | Invoke type-fixer |
| Test Failure | Invoke debug-workflow |
| Review Rejection | Return to generation phase |

## Output Aggregation

```json
{
  "workflowId": "workflow-uuid",
  "artifacts": {
    "code": "generated code",
    "tests": "test cases",
    "review": "review report",
    "docs": "documentation"
  },
  "metrics": {
    "totalTime": "8 minutes",
    "tokensUsed": 5000,
    "iterations": 2
  }
}
```
```

### 9.3 Action-Skill示例

```yaml
# actions/code-generator/SKILL.md
---
name: code-generator
description: "Generates code from specifications. Use when code implementation is needed."
layer: action
role: executor
invoked_by: [coding-workflow, debugging-workflow]
capabilities:
  - code_generation
  - template_application
  - syntax_validation
---

# Code Generator

> Execution layer for generating code.

## When to Use

- Need to generate new code
- Need to implement a function or module
- Need to create boilerplate code

## Input Requirements

```json
{
  "specification": "What to generate",
  "language": "python | javascript | go | ...",
  "style": "project style guide reference",
  "constraints": ["no external dependencies", "must be thread-safe"]
}
```

## Execution Steps

1. Parse specification
2. Identify code patterns
3. Generate code structure
4. Implement logic
5. Add error handling
6. Validate syntax
7. Return result

## Output Format

```json
{
  "status": "success",
  "output": {
    "files": [
      {
        "path": "src/module.py",
        "content": "generated code",
        "language": "python"
      }
    ]
  },
  "metrics": {
    "linesOfCode": 50,
    "executionTime": "2s"
  }
}
```
```

---

## 10. 迁移指南

### 10.1 从传统Skill迁移

```
传统Skill结构:
skill-name/
└── SKILL.md (所有内容在一起)

HCSA结构:
skill-name/
├── meta/
│   └── SKILL.md (规划、分解逻辑)
├── workflow/
│   └── SKILL.md (协调、状态管理)
└── actions/
    ├── action-1/SKILL.md
    └── action-2/SKILL.md
```

### 10.2 迁移步骤

1. **分析现有Skill**: 识别规划、协调、执行部分
2. **拆分职责**: 按三层架构分离
3. **定义接口**: 明确输入输出
4. **添加元数据**: 补充layer、role、invokes等字段
5. **测试验证**: 确保功能正确

---

## 附录

### A. 术语表

| 术语 | 定义 |
|------|------|
| Meta-Skill | 战略层技能，负责规划和反思 |
| Workflow-Skill | 战术层技能，负责协调和聚合 |
| Action-Skill | 执行层技能，负责具体操作 |
| Task Tree | 任务分解后的树形结构 |
| State Machine | 状态转换机制 |
| Reflection | 执行后的自我评估 |

### B. 参考资源

- [LangGraph Supervisor Architecture](https://github.com/langchain-ai/langgraph)
- [Hierarchical Task Network Planning](https://en.wikipedia.org/wiki/Hierarchical_task_network)
- [Orchestrator-Worker Pattern](https://docs.anthropic.com/claude/docs)
- [Agent Skills Specification](https://agentskills.io)

---

**版本历史**

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-01 | 初始版本 |
