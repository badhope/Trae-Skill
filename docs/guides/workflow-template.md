# Workflow 模板

## 什么是 Workflow

Workflow 是一个多步骤的工作流程组合，用于完成复杂任务。

## Workflow vs Skill vs Prompt

| 特性 | Workflow | Skill | Prompt |
|------|----------|-------|--------|
| 粒度 | 粗粒度 | 中等粒度 | 细粒度 |
| 结构 | 步骤序列 | 定义 + 步骤 | 纯文本 |
| 依赖 | 调用多个 Skill/Prompt | 可组合 | 可嵌入 |
| 逻辑 | 包含条件分支 | 无 | 无 |
| 输出 | 复合输出 | 单一输出 | 单一输出 |

## 模板

```markdown
---
id: workflow-{type}-{name}-v1
name: Workflow Name
goal: 描述这个工作流的最终目标
scenario: 适用场景描述
type: workflow
workflow_type: {multi-step|sequential|conditional}
required_inputs:
  - name: input_name
    type: string
    required: true
    description: 输入描述
outputs:
  - name: output_name
    type: string
    description: 输出描述
steps:
  - step: 1
    name: 步骤名称
    action: 步骤动作描述
    used_skills:
      - skill-name
    used_prompts:
      - prompt-name
    decision_points:
      - if: 条件1
        then: 执行步骤1a
        else: 执行步骤1b
  - step: 2
    name: 步骤名称
    action: 步骤动作描述
    used_skills:
      - skill-name
used_skills:
  - skill-category-skill-name-v1
used_prompts:
  - prompt-type-prompt-name-v1
decision_points:
  - condition: 条件描述
    branches:
      - if: 条件A
        then: 步骤序列A
      - if: 条件B
        then: 步骤序列B
final_deliverables:
  - 最终输出1
  - 最终输出2
notes: |
  注意事项
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Workflow Name

## 概述

工作流的详细描述。

## 流程图

```
开始 → 步骤1 → 步骤2 → 结束
         ↓
      决策点
         ↓
    条件A  条件B
```

## 详细步骤

### 步骤1: 步骤名称

**动作**: 步骤动作描述

**使用 Skill**: skill-name
**使用 Prompt**: prompt-name

**决策点**:
- 如果 条件1 → 执行步骤1a
- 否则 → 执行步骤1b

### 步骤2: 步骤名称

...

## 使用示例

**输入**:
- input_name: xxx

**输出**:
- output_name: xxx

**执行路径**: 步骤1 → 条件A → 步骤2 → 步骤3 → 结束
```

## 示例：Bug Fix Workflow

```markdown
---
id: workflow-sequential-bug-fix-v1
name: Bug Fix Workflow
goal: 快速定位并修复 bug
scenario: 当代码出现 bug 时使用此工作流
type: workflow
workflow_type: sequential
required_inputs:
  - name: bug_description
    type: string
    required: true
    description: Bug 描述
  - name: code_snippet
    type: string
    required: true
    description: 相关代码片段
  - name: error_message
    type: string
    required: false
    description: 错误信息
outputs:
  - name: bug_analysis
    type: string
    description: Bug 原因分析
  - name: fixed_code
    type: string
    description: 修复后的代码
  - name: test_plan
    type: string
    description: 测试计划
steps:
  - step: 1
    name: Bug 分析
    action: 分析 bug 的可能原因
    used_skills:
      - skill-coding-bug-fixing
    used_prompts:
      - prompt-task-coding-debug
  - step: 2
    name: 根因定位
    action: 确定 bug 的根本原因
    used_skills:
      - skill-coding-code-analysis
  - step: 3
    name: 修复方案
    action: 设计并实施修复方案
    used_skills:
      - skill-coding-code-generation
  - step: 4
    name: 验证测试
    action: 验证修复并编写测试
    used_skills:
      - skill-coding-test-generation
used_skills:
  - skill-coding-bug-fixing-v1
  - skill-coding-code-analysis-v1
  - skill-coding-code-generation-v1
  - skill-coding-test-generation-v1
used_prompts:
  - prompt-task-coding-debug-v1
decision_points:
  - condition: Bug 复杂度
    branches:
      - if: 简单bug
        then: 步骤1 → 步骤3 → 步骤4
      - if: 复杂bug
        then: 步骤1 → 步骤2 → 步骤3 → 步骤4
final_deliverables:
  - Bug 分析报告
  - 修复后的代码
  - 测试用例
notes: |
  - 如果无法复现 bug，先收集更多环境信息
  - 修复后务必运行相关测试
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Bug Fix Workflow

## 概述

一个系统化的 Bug 修复工作流，从分析到修复到验证的完整流程。

## 流程图

```
开始 → Bug分析 → 根因定位 → 修复方案 → 验证测试 → 结束
                ↓
           简单bug? → 否 → 继续
                ↓ 是
              跳过
```

## 使用场景

1. 收到 bug 报告时
2. 代码出现异常行为时
3. 测试失败需要修复时

## 与其他 Workflow 的区别

- **Bug Fix Workflow**: 专注于修复已知的 bug
- **Code Review Workflow**: 侧重于代码质量审查
- **Feature Development Workflow**: 侧重于新功能开发
```
