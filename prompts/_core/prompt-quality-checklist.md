# Prompt 质量检查清单

本文档是每个 Prompt 作者在交付前的检查表，确保 Prompt 可用、稳定、可扩展。

---

## 检查清单概览

| 类别 | 检查项数量 |
|------|-----------|
| 目标与定位 | 4 |
| 输入与输出 | 6 |
| 内容质量 | 6 |
| 关联与组合 | 4 |
| 可维护性 | 5 |
| 合规与安全 | 3 |

---

## 1. 目标与定位

### [ ] 1.1 目标明确

- [ ] Prompt 有清晰的一句话 summary
- [ ] summary 能准确描述 Prompt 实际功能
- [ ] 不会让用户误解 Prompt 的用途
- [ ] intent 字段说明了为什么需要这个 Prompt

**检查方法**：
```markdown
# 问自己：
- "一句话能说清楚这个 Prompt 做什么吗？"
- "用户看了 summary 会知道什么时候用它吗？"
- "它和其他 Prompt 有什么区别？"
```

### [ ] 1.2 类型正确

- [ ] `type` 字段值正确（routing/system/role/task/workflow/tool-use/output/meta/domain）
- [ ] `category` 和 `sub_category` 与目录结构一致
- [ ] 不存在 type 分类错误（如把 task 标为 system）

### [ ] 1.3 适用范围清晰

- [ ] `applicable_models` 字段已填写（即使是通用 `*`）
- [ ] 适用范围与 Prompt 内容一致
- [ ] 没有假设超出范围的模型能力

### [ ] 1.4 版本状态正确

- [ ] `status` 字段准确反映当前状态
- [ ] 新编写的是 `draft`
- [ ] 稳定可用的是 `active`
- [ ] 不再维护的是 `deprecated`

---

## 2. 输入与输出

### [ ] 2.1 输入要求完整

- [ ] `input_requirements` 列出所有输入
- [ ] 明确标注必填和可选
- [ ] 说明输入格式要求
- [ ] 有默认值说明（如果有）

**示例格式**：
```yaml
input_requirements: |
  1. error_message（字符串，**必填**）：完整错误堆栈
  2. code_snippet（字符串，可选）：相关代码，最多 500 行
  3. language（字符串，默认 auto）：编程语言
```

### [ ] 2.2 输入边界清晰

- [ ] 说明空输入的处理方式
- [ ] 说明非法输入的处理方式
- [ ] 说明超长输入的处理方式
- [ ] 说明格式错误输入的处理方式

### [ ] 2.3 输出要求明确

- [ ] `output_requirements` 完整描述输出格式
- [ ] 提供输出示例
- [ ] 说明成功输出的标准
- [ ] 说明失败输出的标准

**必须包含**：
```yaml
output_requirements: |
  输出格式：JSON
  必需字段：[字段列表]
  可选字段：[字段列表]
  示例：{...}
```

### [ ] 2.4 输出结构稳定

- [ ] JSON 结构在版本间保持稳定（除非破坏性变更）
- [ ] 字段命名一致
- [ ] 类型定义明确（string/number/array/object）

### [ ] 2.5 前置条件说明

- [ ] `preconditions` 列出使用前必须满足的条件
- [ ] 包括环境要求
- [ ] 包括权限要求
- [ ] 包括输入要求

### [ ] 2.6 工具要求说明（如有）

- [ ] `tool_requirements` 列出所需工具
- [ ] 说明版本要求
- [ ] 说明工具用途

---

## 3. 内容质量

### [ ] 3.1 Prompt Body 完整

- [ ] 核心指令清晰、完整、可执行
- [ ] 不存在歧义或模糊表述
- [ ] 没有假设用户知道背景信息
- [ ] 没有依赖"常识"但实际不常识的内容

**自检问题**：
```markdown
- [ ] 任何人拿到这个 Prompt 都能直接使用吗？
- [ ] AI 能否无需额外解释就执行？
- [ ] 指令是否具体而非抽象？
```

### [ ] 3.2 Variables 定义完整

- [ ] 所有变量都有定义
- [ ] 说明变量类型
- [ ] 说明默认值（如果有）
- [ ] 说明是否必填

**Variables 检查**：
```markdown
| 变量名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| ${var1} | ... | string | - | 是 |
| ${var2} | ... | array | [] | 否 |
```

### [ ] 3.3 Anti-patterns 完整

- [ ] `anti_patterns` 列出常见错误使用方式
- [ ] 说明为什么是错误的
- [ ] 给出正确做法
- [ ] 至少 3 条（复杂任务更多）

**格式示例**：
```markdown
anti_patterns: |
  1. **不要 [错误做法]**
     正确做法：[正确做法]

  2. **不要 [错误做法]**
     正确做法：[正确做法]
```

### [ ] 3.4 Failure Modes 完整

- [ ] `failure_modes` 列出可能失败的情况
- [ ] 给出每种情况的治疗方式
- [ ] 说明何时应该返回错误而非继续
- [ ] 至少 3 条

### [ ] 3.5 Self-check 完整

- [ ] `self_check` 包含执行前的自检清单
- [ ] 使用 `[ ]` checklist 格式
- [ ] 至少 4 条
- [ ] 检查项具体可操作

**检查标准**：
```markdown
- [ ] 输入是否完整
- [ ] 上下文是否充足
- [ ] 是否符合使用条件
- [ ] 是否有边界情况需要处理
```

### [ ] 3.6 示例完整

- [ ] 有 Example Input
- [ ] 有 Example Output
- [ ] 示例真实、可复制
- [ ] 示例覆盖主流程

---

## 4. 关联与组合

### [ ] 4.1 Related Skills 正确

- [ ] `related_skills` 列出相关的 Skills
- [ ] 使用 skill ID（非名称）
- [ ] 关联的 Skills 真实存在
- [ ] 关联是合理的、有意义的

### [ ] 4.2 Related Workflows 正确

- [ ] `related_workflows` 列出相关的 Workflows
- [ ] 使用 workflow ID
- [ ] 关联的 Workflows 真实存在

### [ ] 4.3 Related Prompts 正确

- [ ] `related_prompts` 列出相关的其他 Prompts
- [ ] 使用 prompt ID
- [ ] 关联是上下游关系或互补关系
- [ ] 不存在循环依赖

### [ ] 4.4 适合组合使用

- [ ] Prompt 可独立使用
- [ ] Prompt 也可组合使用
- [ ] 与其他 Prompts 组合时有明确的顺序
- [ ] 组合方式已在 Related 或 Usage 中说明

---

## 5. 可维护性

### [ ] 5.1 命名规范

- [ ] 文件名符合规范：`prompt-[category]-[name].md`
- [ ] `id` 字段符合规范：`prompt-[category]-[name]-v[x.y.z]`
- [ ] `name` 字段简洁明了
- [ ] 无重复 ID

### [ ] 5.2 标签完整

- [ ] `tags` 字段包含 5-10 个标签
- [ ] `keywords` 字段包含相关关键词
- [ ] 标签有助于检索
- [ ] 不存在标签滥用

### [ ] 5.3 可扩展性

- [ ] 预留了扩展字段
- [ ] 不绑定特定模型（除非必要）
- [ ] 结构支持后续添加 examples
- [ ] 支持后续添加 model variants

### [ ] 5.4 文档完整

- [ ] Context 部分说明了背景
- [ ] Usage 部分说明了使用方式
- [ ] 所有字段都有填写（必填字段）
- [ ] 文档与实际行为一致

### [ ] 5.5 Owner 正确

- [ ] `owner` 字段填写正确
- [ ] 维护者真实存在
- [ ] 多维护者时用逗号分隔

---

## 6. 合规与安全

### [ ] 6.1 内容安全

- [ ] 不包含恶意指令
- [ ] 不包含敏感信息
- [ ] 不违反模型使用政策
- [ ] 适合公开仓库

### [ ] 6.2 授权清晰

- [ ] 了解 MIT/Apache 等开源许可
- [ ] 内容可合规使用
- [ ] 引用他人内容有标注

### [ ] 6.3 无信息泄露

- [ ] 不在 Prompt 中暴露密钥或凭证
- [ ] 不在示例中暴露敏感信息
- [ ] 使用占位符代替真实数据

---

## 快速检查表

完成检查后，在此处打勾：

```
目标与定位
[ ] 1.1 目标明确
[ ] 1.2 类型正确
[ ] 1.3 适用范围清晰
[ ] 1.4 版本状态正确

输入与输出
[ ] 2.1 输入要求完整
[ ] 2.2 输入边界清晰
[ ] 2.3 输出要求明确
[ ] 2.4 输出结构稳定
[ ] 2.5 前置条件说明
[ ] 2.6 工具要求说明

内容质量
[ ] 3.1 Prompt Body 完整
[ ] 3.2 Variables 定义完整
[ ] 3.3 Anti-patterns 完整
[ ] 3.4 Failure Modes 完整
[ ] 3.5 Self-check 完整
[ ] 3.6 示例完整

关联与组合
[ ] 4.1 Related Skills 正确
[ ] 4.2 Related Workflows 正确
[ ] 4.3 Related Prompts 正确
[ ] 4.4 适合组合使用

可维护性
[ ] 5.1 命名规范
[ ] 5.2 标签完整
[ ] 5.3 可扩展性
[ ] 5.4 文档完整
[ ] 5.5 Owner 正确

合规与安全
[ ] 6.1 内容安全
[ ] 6.2 授权清晰
[ ] 6.3 无信息泄露
```

---

## 常见问题修复

### 问题 1：summary 太模糊

**错误**：
```yaml
summary: "代码分析"
```

**正确**：
```yaml
summary: "分析代码质量，识别正确性、健壮性、性能、安全性问题"
```

### 问题 2：anti_patterns 只说"不要..."

**错误**：
```yaml
anti_patterns: |
  1. 不要忽略错误
```

**正确**：
```yaml
anti_patterns: |
  1. **不要忽略错误处理**
     正确做法：始终检查返回值，确保错误被正确处理和传播
```

### 问题 3：output_requirements 太简略

**错误**：
```yaml
output_requirements: "输出分析报告"
```

**正确**：
```yaml
output_requirements: |
  输出 JSON 格式报告：
  {
    "summary": "string - 一句话总结",
    "issues": [
      {
        "severity": "high|medium|low",
        "type": "correctness|performance|security|...",
        "description": "问题描述",
        "location": "文件:行号",
        "suggestion": "修复建议"
      }
    ],
    "score": "number - 1-10 质量分数"
  }
```

### 问题 4：self_check 流于形式

**错误**：
```yaml
self_check: |
  - [ ] 已阅读文档
  - [ ] 理解任务
```

**正确**：
```yaml
self_check: |
  - [ ] error_message 是否包含完整堆栈
  - [ ] code_snippet 与错误是否相关
  - [ ] 是否需要用户补充信息
  - [ ] 是否有足够的上下文进行分析
```

---

## 相关文档

- [prompt-writing-standard.md](prompt-writing-standard.md) - 编写规范
- [prompt-field-spec.md](prompt-field-spec.md) - 字段定义
- [prompt-lifecycle.md](prompt-lifecycle.md) - 生命周期管理
