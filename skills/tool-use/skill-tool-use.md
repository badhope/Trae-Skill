---
id: skill-tool-use-v1
name: Tool Use
summary: 指导 AI 安全、高效地使用各种工具（文件读取、命令执行等）
type: skill
category: tool-use
tags: [tool-use, file-reading, command-execution, safety]
keywords: [工具使用, 文件读取, 命令执行, 安全]
intent: 确保 AI 在使用工具时准确、安全、有效
typical_use_cases:
  - 需要读取多个文件获取信息时
  - 需要执行命令验证结果时
  - 需要组合多个工具的结果时
  - 配置文件检查后再行动
required_inputs:
  - 任务目标
  - 可用的工具列表
  - 上下文信息
expected_outputs:
  - 工具执行结果
  - 整合后的分析结论
  - 验证结果
paired_prompts:
  - prompt-tool-use-read-files
  - prompt-tool-use-analyze-folder
  - prompt-tool-use-search-before-concluding
  - prompt-tool-use-use-command
  - prompt-tool-use-combine-results
  - prompt-tool-use-inspect-config
  - prompt-tool-use-tools-step-by-step
  - prompt-tool-use-structured-summary
paired_workflows:
  - workflow-tool-assisted-debug
  - workflow-new-repo-onboarding
notes: |
  Tool Use 是跨领域的基础 Skill，多个工作流都依赖它
