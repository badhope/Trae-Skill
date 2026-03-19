---
id: skill-routing-v1
name: Routing
summary: 路由和任务类型识别，引导 AI 选择合适的 prompts 和 workflows
type: skill
category: routing
tags: [routing, task-identification, selection, ai-understanding]
keywords: [路由, 任务识别, 选择, 导航]
intent: 帮助 AI 理解用户需求并路由到合适的资源
typical_use_cases:
  - 用户需求不明确时判断任务类型
  - 从多个候选中选择合适的 prompts
  - 组合多个 prompts 处理复杂任务
required_inputs:
  - 用户需求描述
  - 可选的上下文信息
expected_outputs:
  - 任务类型判断
  - 推荐的 prompts 列表
  - 路由理由
paired_prompts:
  - prompt-routing-scan-repository
  - prompt-routing-identify-task-type
  - prompt-routing-select-relevant
  - prompt-routing-compose
paired_workflows:
  - workflow-vague-request-to-action
  - workflow-prompt-selection-composition
notes: |
  该 Skill 与 .trae/skills/ai-routing 配合使用，ai-routing 提供底层路由能力
