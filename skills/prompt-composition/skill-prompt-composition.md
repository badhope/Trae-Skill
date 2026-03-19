---
id: skill-prompt-composition-v1
name: Prompt Composition
summary: 将多个 prompts 组合为连贯工作流的技术
type: skill
category: prompt-composition
tags: [prompt-composition, workflow, orchestration, multi-step]
keywords: [Prompt组合, 工作流, 编排, 多步骤]
intent: 指导 AI 如何将多个 prompts 有机组合，处理复杂任务
typical_use_cases:
  - 复杂任务需要多个步骤时
  - 需要确定 prompts 执行顺序时
  - 需要在 prompts 之间传递参数时
  - 需要建立 prompt 执行闭环时
required_inputs:
  - 任务目标
  - 可用的 prompts 列表
  - 上下文信息
expected_outputs:
  - 组合后的 prompt 序列
  - 每个 prompt 的输入输出定义
  - 执行顺序说明
paired_prompts:
  - prompt-routing-compose
  - prompt-routing-select-relevant
paired_workflows:
  - workflow-prompt-selection-composition
notes: |
  该 Skill 是复杂任务处理的核心，用于将简单 prompts 组装成复杂工作流
