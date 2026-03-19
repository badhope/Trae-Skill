# Skill 模板

## 什么是 Skill

Skill 是一个可复用的 AI 能力单元，包含：
- 明确的目标
- 输入输出定义
- 实施步骤
- 适用场景

## Skill vs Prompt vs Workflow

| 特性 | Skill | Prompt | Workflow |
|------|-------|--------|----------|
| 粒度 | 中等 | 细小 | 粗粒度 |
| 结构 | 定义 + 步骤 | 纯文本 | 步骤组合 |
| 复用 | 高 | 中 | 高 |
| 依赖 | 可组合 | 可嵌入 | 调用 Skill/Prompt |

## 模板

```markdown
---
id: skill-{category}-{name}-v1
name: Skill Name
summary: 一句话描述这个 Skill 解决什么问题
type: skill
category: {category}
tags: [{tags}]
keywords: [{keywords}]
intent: 解决什么问题
use_cases:
  - 场景1
  - 场景2
inputs:
  - name: input_name
    type: string
    required: true
    description: 输入描述
outputs:
  - name: output_name
    type: string
    description: 输出描述
prerequisites:
  - 前置条件1
steps:
  - step: 1
    action: 步骤1描述
  - step: 2
    action: 步骤2描述
examples:
  - input: 示例输入
    output: 示例输出
    notes: 示例说明
related_skills:
  - skill-category-related-skill-v1
related_prompts:
  - prompt-type-related-prompt-v1
notes: |
  注意事项：
  - 要点1
  - 要点2
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Skill Name

## 详细说明

这里是 Skill 的详细说明文档。

## 使用示例

```示例1
输入：xxx
输出：xxx
```

## 最佳实践

- 最佳实践1
- 最佳实践2
```

## 示例：Article Draft Skill

```markdown
---
id: skill-writing-article-draft-v1
name: Article Draft
summary: 根据主题快速生成文章大纲和初稿
type: skill
category: writing
tags: [writing, article, draft, content]
keywords: [文章起草, 写作, 内容创作]
intent: 帮助用户快速从零开始写出一篇文章
use_cases:
  - 需要快速写文章时
  - 头脑风暴后整理思路时
  - 写作卡壳时续写
inputs:
  - name: topic
    type: string
    required: true
    description: 文章主题
  - name: audience
    type: string
    required: false
    description: 目标读者
  - name: tone
    type: string
    required: false
    description: 写作风格 (formal/casual/technical)
outputs:
  - name: outline
    type: markdown
    description: 文章大纲
  - name: draft
    type: markdown
    description: 文章初稿
prerequisites:
  - 了解文章主题
steps:
  - step: 1
    action: 分析主题，确定文章类型和核心观点
  - step: 2
    action: 构建文章大纲（引言-主体-结论）
  - step: 3
    action: 根据大纲撰写初稿
examples:
  - input: "topic: AI未来发展, audience: 科技从业者, tone: technical"
    output: "# AI未来发展\n\n## 引言\n...\n## 主体\n...\n## 结论"
    notes: 示例说明
related_skills:
  - skill-writing-article-outline
  - skill-writing-seo-optimize
related_prompts:
  - prompt-task-writing-article-expansion
notes: |
  注意事项：
  - 确保主题明确
  - 保持逻辑连贯
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Article Draft Skill

## 概述

根据给定的主题、目标读者和写作风格，快速生成结构化的文章大纲和初稿。

## 使用方法

1. 提供文章主题
2. (可选) 指定目标读者
3. (可选) 选择写作风格
4. AI 将生成完整的大纲和初稿

## 与其他 Skill 配合

- `skill-writing-article-outline`: 生成更详细的大纲
- `skill-writing-seo-optimize`: 优化 SEO 效果
```
