# Prompt 模板

## 什么是 Prompt

Prompt 是发送给 AI 模型的文本指令，可以是：
- 系统级指令 (system)
- 角色扮演指令 (role)
- 任务指令 (task)
- 工作流指令 (workflow)

## Prompt 类型

| 类型 | 用途 | 特点 |
|------|------|------|
| system | 设置 AI 行为规则 | 最高优先级，长期生效 |
| role | 定义 AI 扮演的角色 | 塑造 AI 性格和专业性 |
| task | 执行具体任务 | 一次性指令 |
| workflow | 组合多步骤 | 包含逻辑和流程控制 |

## 模板

```markdown
---
id: prompt-{type}-{category}-{name}-v1
name: Prompt Name
summary: 一句话描述这个 Prompt 的用途
type: prompt
prompt_type: {system|role|task|workflow}
applicable_models:
  - gpt-4
  - gpt-4-turbo
  - claude-3-opus
tags: [{tags}]
variables:
  - name: variable_name
    type: string
    required: true
    description: 变量描述
prompt_body: |
  完整的 prompt 文本
  可以使用 {{variable_name}} 占位符
output_requirements: |
  - 要求1
  - 要求2
examples:
  - variables:
      variable_name: 示例值
    input: 示例输入
    output: 示例输出
    notes: 示例说明
related_skills:
  - skill-category-related-skill-v1
notes: |
  注意事项
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Prompt Name

## 使用说明

这里是 Prompt 的详细使用说明。

## 变量说明

| 变量 | 类型 | 必填 | 描述 |
|------|------|------|------|
| variable_name | string | 是 | 变量描述 |

## 使用示例

### 示例1

**输入变量**:
- variable_name: xxx

**输出**:
xxx
```

## 示例：Code Review Prompt

```markdown
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
  1. 代码质量和可读性
  2. 潜在的 bug 和安全问题
  3. 性能优化建议
  4. 最佳实践建议

  代码：
  ```{{language}}
  {{code}}
  ```

  请以结构化的方式输出你的审查结果。
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

      **问题**:
      - 缺少类型检查
      - 没有参数验证

      **建议**:
      - 添加类型标注
      - 增加参数校验
    notes: 简单函数示例
related_skills:
  - skill-coding-code-review-v1
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
```

## System Prompt vs Role Prompt

### System Prompt 示例

```markdown
---
id: prompt-system-ai-assistant-v1
name: AI Assistant System Prompt
summary: 通用 AI 助手系统提示
type: prompt
prompt_type: system
applicable_models:
  - gpt-4
  - gpt-4-turbo
  - claude-3-opus
tags: [system, assistant, general]
prompt_body: |
  你是一位有帮助的 AI 助手。你的目标是：
  1. 准确理解用户需求
  2. 提供清晰、直接的回答
  3. 在适当时候询问澄清问题
  4. 承认自己的局限性

  回答原则：
  - 简洁明了
  - 结构化输出
  - 适度使用列表和代码块
output_requirements: []
related_skills: []
notes: 这是默认的系统提示，可以根据需要修改
created: 2026-03-19
version: 1.0.0
deprecated: false
---
```

### Role Prompt 示例

```markdown
---
id: prompt-role-senior-developer-v1
name: Senior Developer Role
summary: 资深开发者角色扮演
type: prompt
prompt_type: role
applicable_models:
  - gpt-4
  - claude-3-opus
tags: [role, developer, technical]
prompt_body: |
  你是一位具有 10 年经验的高级软件工程师，专精于：
  - 系统架构设计
  - 代码审查和重构
  - 性能优化
  - 技术难题攻关

  你的特点：
  - 注重代码质量和可维护性
  - 喜欢用简洁的方案解决问题
  - 习惯写详细的文档和注释
  - 乐于指导和分享经验

  当你回答技术问题时，你会：
  1. 先理解问题的本质
  2. 提供多种解决方案并比较
  3. 推荐最佳实践
  4. 给出具体代码示例
output_requirements: []
related_skills:
  - skill-coding-code-review
  - skill-coding-architecture-design
notes: 用于需要深厚技术背景的场景
created: 2026-03-19
version: 1.0.0
deprecated: false
---
```
