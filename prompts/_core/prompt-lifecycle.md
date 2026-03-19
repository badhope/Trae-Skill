# Prompt 生命周期管理

本文档定义 Prompt 从草稿到稳定版的完整生命周期，用于长期维护和版本控制。

---

## 生命周期状态

### 状态定义

| 状态 | 说明 | 使用场景 | 迁移条件 |
|------|------|----------|----------|
| `draft` | 草稿 | 新编写，未验证 | 验证通过 → active |
| `active` | 活跃 | 稳定可用 | 发现严重问题 → deprecated；需破坏性修改 → draft |
| `deprecated` | 已废弃 | 不推荐使用 | 永久状态 |

### 状态迁移图

```
draft → active → deprecated
         ↑
         └──────（破坏性变更）──→ draft → active
```

---

## 版本管理

### 语义化版本

```
主版本.次版本.修订号
X.Y.Z
```

| 版本类型 | 何时升级 | 示例 |
|----------|----------|------|
| **修订号** | Bug 修复，向后兼容 | 1.0.0 → 1.0.1 |
| **次版本** | 新增功能，向后兼容 | 1.0.0 → 1.1.0 |
| **主版本** | 破坏性变更 | 1.0.0 → 2.0.0 |

### 破坏性变更

以下情况需要升级主版本：

1. **输入格式变化**
   ```yaml
   # 变更前
   input: code (string)

   # 变更后
   input: { code: string, language: string }
   ```

2. **输出格式变化**
   ```yaml
   # 变更前
   output: { result: string }

   # 变更后
   output: { result: string, metadata: object }
   ```

3. **字段删除**
   - 删除必填字段
   - 改变字段含义

4. **功能范围变化**
   ```yaml
   # 变更前
   # 只分析 JavaScript

   # 变更后
   # 分析多种语言
   ```

### 非破坏性变更（升级次版本）

1. **新增可选字段**
2. **新增 Prompt（不是修改现有）**
3. **完善文档**
4. **新增示例**

### Bug 修复（升级修订号）

1. **修复歧义**
2. **补充遗漏的边界情况**
3. **修正错误描述**
4. **完善 anti_patterns / failure_modes**

---

## 状态管理规则

### Draft 状态

**进入条件**：
- 新编写的 Prompt
- 破坏性修改后的 Prompt
- 从 deprecated 重新启用的 Prompt

**要求**：
- 标注 `status: draft`
- 说明仍在验证中
- 不保证稳定性

**退出条件**：
- 通过质量检查清单
- 经过实际使用验证
- Owner 批准发布

### Active 状态

**进入条件**：
- Draft 状态验证通过
- 质量检查完整
- Owner 发布

**要求**：
- 保持稳定性
- 版本升级遵循规范
- 及时修复发现的问题

**退出条件**：
- 发现严重问题 → deprecated
- 需要破坏性修改 → draft
- 被更好的 Prompt 取代 → deprecated

### Deprecated 状态

**进入条件**：
- 被新版本取代
- 发现严重设计缺陷
- 不再维护

**要求**：
- 标注 `status: deprecated`
- 说明替代方案
- 保留历史版本供回溯

**不应做**：
- 不应删除 deprecated 的 Prompt
- 不应修改 deprecated 的内容（除非是更正明显错误）

---

## Prompt 拆分规则

### 何时拆分

当一个 Prompt 出现以下情况时，应拆分：

1. **功能混杂**
   ```yaml
   # 错误：一个 Prompt 做太多事
   "分析代码、修复 Bug、生成测试"

   # 正确：拆分为多个
   - analyze-code
   - fix-bug
   - generate-test
   ```

2. **组合场景过多**
   ```yaml
   # 如果一个 Prompt 被用于 >5 个完全不同场景
   # 考虑拆分或创建专门的 Workflow
   ```

3. **可选参数过多**
   ```yaml
   # 当必填参数 < 总参数 30% 时，考虑拆分
   # 例如：10 个参数，3 个必填
   ```

### 拆分流程

1. **识别核心功能和可选功能**
2. **创建新的独立 Prompt**
3. **更新原 Prompt，移除拆分内容**
4. **建立关联（related_prompts）**
5. **更新版本号**

### 拆分示例

**拆分前**：
```yaml
id: prompt-task-coding-full-cycle
name: Full Coding Cycle
summary: 完整编码周期，包括生成、审查、测试
```

**拆分后**：
```yaml
id: prompt-task-coding-generate-code-v1
name: Generate Code
summary: 根据需求生成代码

id: prompt-task-coding-review-code-v1
name: Review Code
summary: 审查代码质量

id: prompt-task-coding-generate-test-v1
name: Generate Test
summary: 生成测试用例

# Workflow 组合
id: prompt-workflow-coding-cycle
name: Coding Cycle
steps:
  - generate-code
  - review-code
  - generate-test
```

---

## Prompt 废弃规则

### 何时废弃

1. **功能重复**
   - 存在功能完全相同但质量更好的 Prompt
   - 用户无法区分两个 Prompt 的区别

2. **设计缺陷**
   - 发现根本性设计问题
   - 修复成本高于重新编写

3. **需求消失**
   - 对应的使用场景不再存在
   - 技术栈过时

### 废弃流程

1. **创建替代 Prompt（如需要）**
2. **更新被废弃 Prompt**：
   - 状态改为 `deprecated`
   - 添加 `替代方案` 说明
   - 更新文档
3. **更新索引和引用**
4. **通知相关用户**

### 废弃示例

```yaml
---
id: prompt-task-coding-old-generator
name: Old Code Generator
status: deprecated
version: "1.0.0"
替代方案: prompt-task-coding-generate-code-v2
deprecated_reason: |
  此 Prompt 的输出格式已被新版取代，
  新版提供更稳定的结构和更好的错误处理。
---
```

---

## 重复处理规则

### 识别重复

重复的Prompt有以下特征：
- 功能完全相同
- 输入输出格式相同
- 无法说出明显区别

### 处理方式

1. **保留最优版本**
   - 质量更好的保留
   - 如果质量相同，保留更新时间更近的

2. **建立别名（可选）**
   ```yaml
   # 在保留的 Prompt 中
   also_known_as:
     - prompt-task-coding-code-generator
     - prompt-task-coding-generate
   ```

3. **更新引用**
   - 更新所有引用重复 Prompt 的地方
   - 将引用指向保留版本

4. **废弃其他**
   - 其他版本标记为 deprecated

---

## 扩展规则

### 添加 Examples

**何时添加**：
- Prompt 稳定后
- 有实际使用案例时
- 需要帮助用户理解使用时

**要求**：
- 提供真实、有代表性的示例
- 包含 input 和 expected output
- 覆盖主要场景和边界情况

**格式**：
```yaml
## Examples

### Example 1: [场景描述]

**Input:**
\`\`\`
{输入内容}
\`\`\`

**Expected Output:**
\`\`\`json
{期望输出}
\`\`\`

### Example 2: [边界情况]

**Input:**
...
```

### 添加 Model Variants

**何时添加**：
- 通用版本稳定后
- 特定模型需要优化时

**命名规范**：
```yaml
# 通用版本
id: prompt-task-coding-generate-code-v1

# 模型变体
id: prompt-task-coding-generate-code-for-claude-v1
id: prompt-task-coding-generate-code-for-gpt4-v1
id: prompt-task-coding-generate-code-for-minimax-v1
```

**变体文件位置**：
```
prompts/task/coding/
├── prompt-task-coding-generate-code.md      # 通用版
├── variants/
│   ├── prompt-task-coding-generate-code-for-claude.md
│   ├── prompt-task-coding-generate-code-for-gpt4.md
│   └── prompt-task-coding-generate-code-for-minimax.md
```

### 添加 Evals

**何时添加**：
- Prompt 成熟后
- 需要量化评估时

**Eval 指标**：
- 任务完成率
- 输出格式正确率
- 用户满意度
- 边界情况处理率

---

## 维护流程

### 定期审查

| 频率 | 内容 |
|------|------|
| 每月 | 检查 draft 状态 Prompt |
| 每季度 | 审查所有 active Prompt |
| 每年 | 全面审查，更新过时内容 |

### Issue 处理

收到 Issue 后：

1. **Bug Report**
   - 确认是否可复现
   - 确定影响范围
   - 决定：修复 / 拆分 / 废弃

2. **功能请求**
   - 评估是否需要新 Prompt
   - 评估是否可扩展现有 Prompt
   - 决定：新增 / 扩展 / 拒绝

3. **改进建议**
   - 评估改进价值
   - 决定是否实施

### Commit 规范

```bash
# 新增 Prompt
git commit -m "feat(prompts): add prompt-task-debugging-fix-bug-safely"

# Bug 修复
git commit -m "fix(prompts): correct output format in generate-code"

# 功能增强
git commit -m "feat(prompts): add examples to identify-root-cause"

# 版本升级
git commit -m "v1.1.0: upgrade prompt-task-coding-review-code"

# 废弃
git commit -m "deprecate(prompts): mark old-generator as deprecated"
```

---

## 目录结构规范

### 单一 Prompt 文件

```
prompts/task/debugging/
├── prompt-task-debugging-identify-root-cause.md
├── prompt-task-debugging-generate-debug-plan.md
└── prompt-task-debugging-fix-bug-safely.md
```

### 带变体的 Prompt

```
prompts/task/coding/
├── prompt-task-coding-generate-code.md
└── variants/
    ├── prompt-task-coding-generate-code-for-claude.md
    ├── prompt-task-coding-generate-code-for-gpt4.md
    └── prompt-task-coding-generate-code-for-minimax.md
```

---

## 相关文档

- [prompt-writing-standard.md](prompt-writing-standard.md) - 编写规范
- [prompt-field-spec.md](prompt-field-spec.md) - 字段定义
- [prompt-quality-checklist.md](prompt-quality-checklist.md) - 质量检查
