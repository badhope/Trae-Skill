---
id: prompt-task-coding-code-review-v1
name: Code Review
summary: 对代码进行全面的审查和建议
type: prompt
prompt_type: task
applicable_models:
  - gpt-4
  - gpt-4-turbo
  - claude-3-opus
tags: [coding, review, code, quality]
variables:
  - name: code
    type: string
    required: true
    description: 要审查的代码
  - name: language
    type: string
    required: false
    description: 编程语言
prompt_body: |
  你是一位资深的代码审查员。请审查以下代码，关注：
  1. 代码质量和可读性（命名、注释、结构）
  2. 潜在的 bug 和安全问题
  3. 性能优化建议
  4. 最佳实践建议

  代码：
  ```{{language}}
  {{code}}
  ```

  请以结构化的 Markdown 格式输出审查结果。
output_requirements: |
  - 代码质量评分 (1-10)
  - 优点列表
  - 问题列表 (分严重/一般/建议)
  - 优化建议
  - 重构建议 (如有)
examples:
  - variables:
      code: "function add(a, b) { return a + b }"
      language: javascript
    output: |
      ## 代码审查结果

      **代码质量评分**: 7/10

      **优点**:
      - 简洁易读
      - 函数名直观

      **问题**:
      - [一般] 缺少类型检查
      - [建议] 没有参数验证

      **建议**:
      - 添加 TypeScript 类型标注
      - 增加参数校验
    notes: 简单函数示例
related_skills:
  - skill-coding-code-review
notes: |
  - 适用于任何编程语言
  - 输出格式可根据需要调整
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Code Review Prompt

## 概述

通用的代码审查 Prompt，适用于各种编程语言。

## 变量说明

| 变量 | 类型 | 必填 | 描述 |
|------|------|------|------|
| code | string | 是 | 要审查的代码 |
| language | string | 否 | 编程语言 |

## 使用方法

1. 设置 variables 中的 code 和 language
2. 将 prompt_body 发送给 AI
3. AI 将返回结构化的审查结果
