# 规范文档

## 1. 文件命名规范

### 目录命名
- 使用小写字母和连字符
- 复数形式：skills, prompts, workflows
- 层级清晰：writing, writing/article, writing/article/seo

### 文件命名
```
{type}-{category}-{name}.md
```
示例：
- `skill-writing-article-draft.md`
- `prompt-task-coding-code-review.md`
- `workflow-sequential-bug-fix.md`

### ID 命名
```
{type}-{category}-{name}-{version}
```
示例：
- `skill-writing-article-draft-v1`
- `prompt-task-coding-code-review-v1`

## 2. 元信息规范

每个文件头部必须包含 YAML frontmatter：

```yaml
---
id: skill-writing-article-draft-v1
name: Article Draft
type: skill
category: writing
tags: [writing, article, draft, content]
keywords: [文章起草, 写作, 内容创作]
intent: 根据主题快速生成文章大纲和初稿
use_cases:
  - 需要快速写文章时
  - 头脑风暴后整理思路时
inputs:
  - topic: 文章主题
  - audience: 目标读者
  - tone: 写作风格
outputs:
  - outline: 文章大纲
  - draft: 文章初稿
related_skills:
  - skill-writing-article-outline
  - skill-writing-seo-optimize
related_prompts:
  - prompt-task-writing-article-expansion
notes: 这是什么, 不要做什么
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---
```

## 3. 标签规范

### 常用标签
- writing, coding, research, analysis, design, automation
- agent, business, learning, productivity, media, personal
- article, document, report, email, social
- code, debug, refactor, test, api, architecture
- seo, marketing, sales, customer
- beginner, intermediate, advanced
- fast, detailed, creative, analytical

### 标签层级
- 主标签：技能大类 (writing, coding)
- 辅标签：具体功能 (article, seo)
- 场景标签：使用场景 (fast, detailed)

## 4. 新增规则

1. 先检查是否已存在相似的 skill/prompt
2. 遵循命名规范
3. 必须包含完整的 frontmatter
4. 必须添加到对应的 registry
5. 示例可选但强烈推荐

## 5. 去重规则

- 相似内容先检查 tags 和 keywords 重叠度
- 超过 70% 重叠考虑合并
- 合并时保留所有 related_skills/prompts

## 6. 弃用规则

- 设置 `deprecated: true`
- 添加 `replaced_by` 字段指向新版本
- 在文件末尾添加弃用说明

```yaml
deprecated: true
replaced_by: skill-writing-article-draft-v2
deprecated_reason: |
  功能已被新版替代，请使用 v2 版本。
deprecated_date: 2026-06-01
```

## 7. 版本规则

- 首次创建：v1.0.0
- 小幅更新：v1.0.1 (bug 修复)
- 功能更新：v1.1.0 (新增功能)
- 重大更新：v2.0.0 (破坏性变更)

## 8. 文件头规范

### Skill 文件
```markdown
---
id: skill-{category}-{name}-v{major}
name: Name
summary: 一句话描述
type: skill
category: {category}
tags: [...]
keywords: [...]
intent: 解决什么问题
use_cases: [...]
inputs: [...]
outputs: [...]
prerequisites: [...]
steps: [...]
examples: [...]
related_skills: [...]
related_prompts: [...]
notes: 注意事项
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: x.x.x
deprecated: false
---

# Skill Name

详细说明...
```

### Prompt 文件
```markdown
---
id: prompt-{type}-{category}-{name}-v{major}
name: Name
summary: 一句话描述
type: prompt
prompt_type: {system|role|task|workflow}
applicable_models: [gpt-4, claude-3, ...]
tags: [...]
variables: [...]
prompt_body: |
  完整的 prompt 文本
output_requirements: [...]
examples: [...]
related_skills: [...]
notes: 注意事项
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: x.x.x
deprecated: false
---

# Prompt Name

使用说明...
```

### Workflow 文件
```markdown
---
id: workflow-{type}-{name}-v{major}
name: Name
goal: 目标描述
scenario: 适用场景
required_inputs: [...]
outputs: [...]
steps: [...]
used_skills: [...]
used_prompts: [...]
decision_points: [...]
final_deliverables: [...]
notes: 注意事项
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: x.x.x
deprecated: false
---

# Workflow Name

详细说明...
```
