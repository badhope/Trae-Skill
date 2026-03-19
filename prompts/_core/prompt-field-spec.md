# Prompt 字段规范

本文档详细定义每个字段的含义、写法、示例和常见错误。

---

## 字段概览

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | ✅ | 唯一标识符 |
| `name` | ✅ | 名称 |
| `summary` | ✅ | 一句话描述 |
| `type` | ✅ | 类型 |
| `status` | ✅ | 状态 |
| `version` | ✅ | 版本号 |
| `owner` | ✅ | 维护者 |
| `category` | ✅ | 主分类 |
| `sub_category` |  | 子分类 |
| `tags` | ✅ | 标签 |
| `keywords` | ✅ | 关键词 |
| `intent` | ✅ | 使用意图 |
| `applicable_models` |  | 适用模型 |
| `input_requirements` | ✅ | 输入要求 |
| `output_requirements` | ✅ | 输出要求 |
| `tool_requirements` |  | 工具要求 |
| `preconditions` |  | 前置条件 |
| `anti_patterns` | ✅ | 应避免的模式 |
| `failure_modes` | ✅ | 失败模式 |
| `self_check` | ✅ | 自检清单 |
| `related_skills` |  | 相关 Skills |
| `related_workflows` |  | 相关 Workflows |
| `related_prompts` |  | 相关 Prompts |

---

## 必填字段

### id

**含义**：Prompt 的唯一标识符。

**写法**：
- 格式：`prompt-[category]-[specific-name]-v[version]`
- 使用小写字母和连字符
- 版本号用 `v` 前缀

**示例**：
```
✅ prompt-task-debugging-identify-root-cause-v1
✅ prompt-system-coding-agent-v1
❌ Prompt-Task-Debugging-Identify-Root-Cause (大写)
❌ prompt_task_debugging_identify_root_cause (下划线)
```

**常见错误**：
- 使用大写字母
- 使用下划线
- 版本号格式错误
- ID 不唯一

---

### name

**含义**：人类可读的名称。

**写法**：
- 使用标题式大小写
- 简洁明了
- 体现功能

**示例**：
```
✅ "Identify Root Cause"
✅ "Generate Debug Plan"
❌ "Root cause identification" (不够清晰)
❌ "The prompt for identifying root cause" (太长)
```

---

### summary

**含义**：一句话描述 Prompt 的功能。

**写法**：
- 一句话，不超过 50 字
- 说明做什么，不说明怎么做
- 使用动词开头

**示例**：
```
✅ "分析错误信息，定位 Bug 根因"
✅ "基于需求生成可执行的代码"
❌ "这个 Prompt 可以用来分析代码" (太模糊)
❌ "当用户报告了一个 Bug，我们需要先用这个 Prompt 来分析问题，
    看看是什么原因导致的，然后..." (太长)
```

---

### type

**含义**：Prompt 的类型。

**可选值**：

| 值 | 说明 |
|----|------|
| `routing` | 自主路由类 |
| `system` | 系统级提示词 |
| `role` | 角色型提示词 |
| `task` | 任务型提示词 |
| `workflow` | 工作流提示词 |
| `tool-use` | 工具调用提示词 |
| `output` | 输出格式提示词 |
| `meta` | Prompt 优化提示词 |
| `domain` | 领域型提示词 |

**示例**：
```
type: task
type: system
```

**常见错误**：
- 使用未定义的值
- 混用 type 和 category

---

### status

**含义**：Prompt 的当前状态。

**可选值**：

| 值 | 说明 | 使用场景 |
|----|------|----------|
| `draft` | 草稿 | 新编写，未经验证 |
| `active` | 活跃 | 稳定可用 |
| `deprecated` | 已废弃 | 不推荐使用 |

**示例**：
```
status: active
```

**常见错误**：
- 将草稿状态的内容标记为 active
- 不更新废弃状态的 Prompt

---

### version

**含义**：语义化版本号。

**写法**：
- 格式：`主版本.次版本.修订号`
- `主版本`：破坏性变更
- `次版本`：新增功能（向后兼容）
- `修订号`：Bug 修复（向后兼容）

**示例**：
```
✅ version: "1.0.0"  (首次发布)
✅ version: "1.1.0"  (新增功能)
✅ version: "1.1.1"  (Bug 修复)
✅ version: "2.0.0"  (破坏性变更)
❌ version: "1.0"    (不完整)
❌ version: "v1.0.0" (不应有 v 前缀，id 中才有)
```

---

### owner

**含义**：Prompt 的维护者 GitHub 用户名。

**写法**：
- GitHub 用户名
- 多个维护者用逗号分隔

**示例**：
```
owner: username
owner: username1, username2
```

---

### category

**含义**：主分类。

**写法**：
- 使用小写
- 与目录结构对应

**示例**：
```
category: task
category: system
category: routing
```

**常见错误**：
- 与 sub_category 混淆
- 使用大写字母

---

### sub_category

**含义**：子分类。

**写法**：
- 使用小写
- 位于 category 之下

**示例**：
```
category: task
sub_category: debugging

category: task
sub_category: coding
```

---

### tags

**含义**：标签，用于检索和分类。

**写法**：
- 数组格式
- 使用小写
- 包含同义词和相关概念
- 数量建议 5-10 个

**示例**：
```yaml
tags:
  - debugging
  - bug-fixing
  - error-analysis
  - root-cause
  - troubleshooting
```

**常见错误**：
- 标签太少（<3 个）
- 标签太多（>15 个）
- 使用大写字母
- 与 keywords 混淆

---

### keywords

**含义**：关键词，用于 AI 检索。

**写法**：
- 数组格式
- 包含可能的搜索词
- 与 tags 类似但更广泛

**示例**：
```yaml
keywords:
  - error
  - bug
  - crash
  - exception
  - stack trace
  - debug
  - fix
```

**常见错误**：
- 与 tags 完全相同
- 太少或太多

---

### intent

**含义**：使用意图，说明为什么需要这个 Prompt。

**写法**：
- 2-3 句话
- 说明解决的问题
- 说明使用场景

**示例**：
```
intent: |
  用于帮助 AI 在面对错误信息时，系统性地分析问题、
  定位根因。在用户报告 Bug 或遇到错误时作为第一步使用，
  为后续调试计划生成和实际修复提供分析基础。
```

**常见错误**：
- 写得太短（<1 句话）
- 写得太长（>5 句话）
- 只说明做什么，不说明为什么

---

### input_requirements

**含义**：明确的输入要求。

**写法**：
- 说明需要什么输入
- 说明输入格式
- 说明哪些是必填/可选

**示例**：
```yaml
input_requirements: |
  1. error_message（字符串，必填）：完整的错误信息或异常堆栈
  2. code_snippet（字符串，可选）：相关代码片段
  3. file_path（字符串，可选）：相关文件路径
  4. language（字符串，默认 auto）：编程语言
  5. context（字符串，可选）：额外上下文信息

  格式要求：
  - error_message 应包含完整的堆栈信息
  - code_snippet 不超过 500 行
```

**常见错误**：
- 模糊描述（如"需要代码"）
- 不说明必填/可选
- 不说明格式要求

---

### output_requirements

**含义**：明确的输出要求。

**写法**：
- 说明预期的输出格式
- 提供输出示例
- 说明成功/失败标准

**示例**：
```yaml
output_requirements: |
  输出一个结构化报告，包含以下字段：

  1. root_cause（字符串）：根因分析，简明扼要
  2. confidence（字符串）：置信度，取值 high/medium/low
  3. evidence（数组）：支持此根因的证据列表
  4. alternative_hypothesis（数组）：其他可能原因

  JSON 格式：
  {
    "root_cause": "...",
    "confidence": "high",
    "evidence": ["...", "..."],
    "alternative_hypothesis": []
  }

  成功标准：root_cause 清晰，confidence 有依据
```

**常见错误**：
- 不给出输出格式
- 不提供示例
- 不说明成功标准

---

### tool_requirements

**含义**：工具要求，说明需要什么外部工具或资源。

**写法**：
- 列出需要的工具
- 说明版本要求
- 说明如何使用

**示例**：
```yaml
tool_requirements: |
  1. Git：用于代码管理
  2. 语言运行时：如 Node.js 18+，Python 3.10+
  3. Linter：如 ESLint，Pylint（可选）
```

**常见错误**：
- 不说明版本要求
- 列出不存在的工具

---

### preconditions

**含义**：前置条件，使用 Prompt 前必须满足的条件。

**写法**：
- 列出使用前的必要条件
- 包括环境、权限、输入等

**示例**：
```yaml
preconditions: |
  1. 用户已提供错误信息或异常堆栈
  2. 代码环境可复现该错误
  3. 有代码的读写权限（如果是修复任务）
```

---

### anti_patterns

**含义**：应避免的使用模式。

**写法**：
- 列出常见错误
- 说明为什么是错的
- 给出正确做法

**示例**：
```yaml
anti_patterns: |
  1. **不要在未分析错误信息的情况下直接修改代码**
     正确做法：先使用 identify-root-cause 分析

  2. **不要忽略边界条件和特殊情况**
     正确做法：分析时考虑所有可能的输入情况

  3. **不要只修复表面症状而不处理根本原因**
     正确做法：确保根因被正确识别和处理
```

**常见错误**：
- 写得像是使用指南而非避免指南
- 不给出正确做法

---

### failure_modes

**含义**：可能的失败模式和应对方式。

**写法**：
- 列出可能失败的情况
- 说明如何处理
- 说明何时放弃

**示例**：
```yaml
failure_modes: |
  1. **输入不完整**
     处理：请求补充必要信息（error_message 必填）

  2. **无法定位根因**
     处理：返回最高可能性的假设 + 验证方法 + confidence: low

  3. **错误无法复现**
     处理：说明情况，建议用户尝试提供更多信息

  4. **修复后验证失败**
     处理：回滚修改，重新分析
```

**常见错误**：
- 不列出真实的失败情况
- 不给出处理方式

---

### self_check

**含义**：AI 执行前的自检清单。

**写法**：
- 使用 `[ ]` 格式的 checklist
- 列出执行前必须检查的项目
- 确保输入质量和上下文完整性

**示例**：
```yaml
self_check: |
  执行前自检清单：
  - [ ] error_message 是否完整（包含堆栈信息）
  - [ ] code_snippet 是否与错误相关
  - [ ] 是否需要用户补充信息
  - [ ] 是否有足够的上下文进行分析
```

**常见错误**：
- 写成执行步骤而非检查项
- 检查项太少

---

### related_skills

**含义**：相关的 Skills。

**写法**：
- 数组格式
- 使用 skill ID

**示例**：
```yaml
related_skills:
  - debugging
  - coding
  - repo-analysis
```

**常见错误**：
- 写 Skill 名称而非 ID
- 列出不相关的内容

---

### related_workflows

**含义**：相关的 Workflows。

**写法**：
- 数组格式
- 使用 workflow ID

**示例**：
```yaml
related_workflows:
  - bug-fix-workflow
  - code-review-workflow
```

---

### related_prompts

**含义**：相关的其他 Prompts。

**写法**：
- 数组格式
- 使用 prompt ID

**示例**：
```yaml
related_prompts:
  - prompt-task-debugging-generate-debug-plan
  - prompt-task-debugging-fix-bug-safely
  - prompt-task-debugging-verify-fix-after-change
```

---

## 字段关系

```
id (唯一标识)
  ├── type (类型)
  │     └── category (主分类)
  │           └── sub_category (子分类)
  ├── tags (标签) ← keywords (关键词)
  ├── intent (意图)
  ├── input_requirements (输入)
  │     └── preconditions (前置条件)
  ├── output_requirements (输出)
  ├── anti_patterns (避免)
  ├── failure_modes (失败)
  ├── self_check (自检)
  └── related_* (关联)
```

---

## 完整示例

```yaml
---
id: prompt-task-debugging-identify-root-cause-v1
name: Identify Root Cause
summary: 分析错误信息，定位 Bug 根因
type: task
status: active
version: "1.0.0"
owner: username
category: task
sub_category: debugging
tags:
  - debugging
  - bug-fixing
  - error-analysis
  - root-cause
  - troubleshooting
keywords:
  - error
  - bug
  - crash
  - exception
  - stack trace
  - debug
intent: |
  用于帮助 AI 在面对错误信息时，系统性地分析问题、
  定位根因。在用户报告 Bug 或遇到错误时作为第一步使用，
  为后续调试计划生成和实际修复提供分析基础。
applicable_models:
  - "*"
input_requirements: |
  1. error_message（字符串，必填）：完整的错误信息或异常堆栈
  2. code_snippet（字符串，可选）：相关代码片段
  3. file_path（字符串，可选）：相关文件路径
  4. language（字符串，默认 auto）：编程语言
output_requirements: |
  输出一个结构化报告，包含：
  - root_cause（字符串）：根因分析
  - confidence（字符串）：high/medium/low
  - evidence（数组）：支持证据
  - alternative_hypothesis（数组）：其他可能原因
anti_patterns: |
  1. 不要在未分析错误信息的情况下直接修改代码
  2. 不要忽略边界条件和特殊情况
  3. 不要只修复表面症状而不处理根本原因
failure_modes: |
  1. 输入不完整 → 请求补充必要信息
  2. 无法定位根因 → 返回最高可能性的假设
  3. 错误无法复现 → 说明情况并建议
self_check: |
  - [ ] error_message 是否完整
  - [ ] 是否有足够的上下文
  - [ ] 是否需要用户补充信息
related_skills:
  - debugging
related_workflows:
  - bug-fix-workflow
related_prompts:
  - prompt-task-debugging-generate-debug-plan
  - prompt-task-debugging-fix-bug-safely
---
```
