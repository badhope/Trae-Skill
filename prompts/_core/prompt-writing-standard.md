# Prompt 编写规范

本文档定义如何编写高质量的 Prompt 文件，确保仓库中所有 Prompts 风格统一、结构清晰、AI 友好。

---

## 高质量 Prompt 的标准

### 1. 目标明确

- Prompt 应有清晰的任务目标
- 一句话能说明这个 Prompt 做什么
- 不存在歧义或模糊表述

### 2. 输入清晰

- 明确说明需要什么输入
- 变量定义清晰，有默认值
- 告知输入的格式要求

### 3. 输出明确

- 明确说明预期的输出格式
- 给出输出示例
- 定义成功/失败的标准

### 4. 结构完整

- 包含所有标准字段
- 有明确的 Context、Prompt Body、Variables、Usage、Example
- 包含自我检查机制

### 5. 可执行性强

- 不只是给方向，而是给具体指令
- 可以直接使用，不需额外解释
- 适合 AI 直接执行

### 6. 可扩展性好

- 预留字段扩展（如 applicable_models）
- 便于后续添加 examples 和 evals
- 不绑定特定模型

---

## Prompt 结构

每个 Prompt 文件应包含以下部分：

### Frontmatter（YAML 元信息）

```yaml
---
id: prompt-[category]-[name]-v[version]
name: [prompt-name]
summary: [一句话描述]
type: [routing|system|role|task|workflow|tool-use|output|meta|domain]
status: [draft|active|deprecated]
version: [x.y.z]
owner: [github-username]
category: [main-category]
sub_category: [sub-category]
tags: [tag1, tag2, tag3]
keywords: [keyword1, keyword2, keyword3]
intent: [使用意图]
applicable_models: [model1, model2, *]
input_requirements: [输入要求]
output_requirements: [输出要求]
tool_requirements: [工具要求]
preconditions: [前置条件]
anti_patterns: [应避免的模式]
failure_modes: [失败模式]
self_check: [自检清单]
related_skills: [skill-id1, skill-id2]
related_workflows: [workflow-id1, workflow-id2]
related_prompts: [prompt-id1, prompt-id2]
---
```

### Context（上下文）

说明 Prompt 的使用背景和目的。

```markdown
## Context

[这段描述为什么需要这个 Prompt，在什么场景下使用，解决什么问题]
```

### Prompt Body（核心指令）

这是 Prompt 的核心部分，包含 AI 执行的指令。

```markdown
## Prompt Body

[详细、清晰、可执行的指令]
```

### Variables（变量）

定义 Prompt 中可替换的变量。

```markdown
## Variables

| 变量名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| ${variable_name} | [说明] | [类型] | [默认值] | [是/否] |
```

### Usage（使用方式）

说明如何使用这个 Prompt。

```markdown
## Usage

[如何使用，包括：
1. 前置条件
2. 调用方式
3. 注意事项]
```

### Example Input（示例输入）

提供示例输入。

```markdown
## Example Input

```
[示例输入内容]
```
```

### Example Output（示例输出）

提供示例输出。

```markdown
## Example Output

```
[示例输出内容]
```
```

---

## Prompt Body 写作指南

### 1. 开篇明确任务

开头直接说明任务：

```markdown
# 正确示例
你是一个专业的代码审查员。请审查以下代码，并提供结构化的审查报告。

# 错误示例
我想让你帮我看看这个代码，不知道行不行...
```

### 2. 分点描述复杂任务

对于复杂任务，使用分点：

```markdown
请按以下步骤操作：
1. 分析代码结构和逻辑
2. 检查错误处理
3. 评估代码性能
4. 提供改进建议
```

### 3. 给出输出格式

明确输出格式：

```markdown
请按以下 JSON 格式输出：
```json
{
  "summary": "一句话总结",
  "issues": [
    {
      "severity": "high|medium|low",
      "description": "问题描述",
      "location": "文件:行号",
      "suggestion": "建议"
    }
  ]
}
```
```

### 4. 包含边界条件

说明边界情况：

```markdown
注意：
- 如果输入为空，返回 {"error": "empty input"}
- 如果代码超过 1000 行，只分析前 1000 行
- 如果是二进制文件，返回 {"error": "binary file"}
```

### 5. 使用占位变量

使用 ${variable} 表示需要替换的内容：

```markdown
请审查以下 ${language} 代码：
${code}

代码位于：${file_path}
```

---

## 字段写作指南

### summary（一句话描述）

**要求**：清晰、简洁，一句话说清楚 Prompt 做什么。

**示例**：
- ✅ "分析错误信息，定位 Bug 根因"
- ❌ "帮我看看代码有什么问题"

### intent（使用意图）

**要求**：说明为什么需要这个 Prompt，解决什么问题。

**示例**：
```
用于帮助 AI 在面对陌生代码仓库时，快速理解项目结构、
关键入口、主要模块分布，为后续调试或功能开发提供上下文基础。
```

### input_requirements（输入要求）

**要求**：明确需要什么输入，格式是什么。

**示例**：
```
需要以下输入：
1. error_message：错误信息或异常堆栈（字符串）
2. code_snippet：相关代码片段（字符串，可选）
3. file_path：文件路径（字符串，可选）
4. language：编程语言（字符串，默认 auto）
```

### output_requirements（输出要求）

**要求**：明确输出格式，提供示例。

**示例**：
```
输出一个结构化报告，包含：
1. root_cause（字符串）：根因分析
2. confidence（字符串：high/medium/low）：置信度
3. evidence（数组）：支持证据列表
4. hypothesis（数组）：其他可能原因（如有）

JSON 格式：
{
  "root_cause": "...",
  "confidence": "high",
  "evidence": ["...", "..."],
  "alternative_hypothesis": []
}
```

### anti_patterns（应避免的模式）

**要求**：列出常见错误使用方式。

**示例**：
```
1. 不要在未分析错误信息的情况下直接修改代码
2. 不要忽略边界条件和特殊情况
3. 不要只修复表面症状而不处理根本原因
4. 不要在没有验证的情况下宣布 Bug 已修复
```

### failure_modes（失败模式）

**要求**：列出可能失败的情况和处理方式。

**示例**：
```
1. 输入不完整 → 请求补充必要信息
2. 无法定位根因 → 返回最高可能性的假设和验证方法
3. 修复后验证失败 → 回滚修改并重新分析
```

### self_check（自检清单）

**要求**：AI 执行前应检查的项目。

**示例**：
```
执行前自检：
- [ ] 已收集完整的错误信息和上下文
- [ ] 已验证错误可复现
- [ ] 已确认代码修改不会引入新问题
- [ ] 已准备回滚方案
```

### related_skills（相关 Skills）

**要求**：列出相关的 Skills 路径。

**格式**：`[skill-id]`（如 `coding-bug-fixing`）

### related_workflows（相关 Workflows）

**要求**：列出相关的 Workflows。

**格式**：`[workflow-id]`

### related_prompts（相关 Prompts）

**要求**：列出相关的其他 Prompts。

**格式**：`[prompt-id]`

---

## 应该避免的写法

### 1. 模糊不清

```markdown
# 错误
帮我看看这个代码有什么问题

# 正确
你是一个专业的代码审查员。请审查以下代码，关注以下方面：
1. 代码正确性
2. 错误处理
3. 性能问题
4. 安全漏洞
```

### 2. 缺少边界条件

```markdown
# 错误
生成一个排序算法

# 正确
请实现一个排序算法，满足以下要求：
- 输入：整数数组，长度 1-10000
- 输出：升序排列的整数数组
- 时间复杂度：O(n log n)
- 如果输入为空，返回空数组
- 如果包含非整数，返回错误
```

### 3. 缺少输出格式

```markdown
# 错误
分析这段代码的性能

# 正确
请分析以下代码的性能，输出 JSON 格式：
{
  "time_complexity": "时间复杂度",
  "space_complexity": "空间复杂度",
  "bottlenecks": ["瓶颈1", "瓶颈2"],
  "suggestions": ["优化建议1", "优化建议2"]
}
```

### 4. 缺少自检机制

```markdown
# 错误
直接执行，不检查

# 正确
执行前自检：
- [ ] 输入参数是否完整
- [ ] 是否有足够的上下文
- [ ] 是否符合使用条件
```

---

## 粒度控制

### 单一职责原则

每个 Prompt 应只做一件事：

- ✅ `identify-root-cause` - 只做根因识别
- ✅ `generate-debug-plan` - 只做计划生成
- ❌ `fix-bug` - 包含太多职责

### 组合使用

复杂的任务通过组合多个 Prompts 实现：

```markdown
Bug 修复工作流：
1. identify-root-cause（识别根因）
2. generate-debug-plan（生成计划）
3. fix-bug-safely（安全修复）
4. verify-fix-after-change（验证修复）
```

---

## 版本控制

- 每个 Prompt 都有版本号
- 使用语义化版本：`主版本.次版本.修订号`
- 修改时遵循 `prompt-lifecycle.md` 的规范

---

## 相关文档

- [prompt-field-spec.md](prompt-field-spec.md) - 字段详细定义
- [prompt-style-guide.md](prompt-style-guide.md) - 写作风格指南
- [prompt-quality-checklist.md](prompt-quality-checklist.md) - 质量检查清单
- [prompt-lifecycle.md](prompt-lifecycle.md) - 生命周期管理
