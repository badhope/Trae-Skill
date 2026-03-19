# Prompts 仓库索引

本文件是 Prompts 仓库的总索引，帮助 AI 和人类快速定位所需 Prompt。

---

## AI 使用指南

### 首次使用

当你获得这个仓库后，请按以下顺序操作：

#### 第一步：读取本索引

```markdown
1. 读取 prompts/README.md - 了解仓库定位
2. 读取本 INDEX.md - 了解 Prompt 分类
3. 如需自主路由，阅读 _routing/ 类提示词
```

#### 第二步：理解仓库结构

```
prompts/
├── _routing/           # 自主路由（AI 首先阅读）
├── _core/              # 核心规范（维护者阅读）
├── system/             # 系统级提示词
├── role/               # 角色型提示词
├── task/               # 任务型提示词
├── workflow/           # 工作流提示词
├── tool-use/           # 工具调用提示词
├── output/             # 输出格式提示词
├── meta/               # Prompt 优化提示词
└── domains/            # 领域型提示词
```

#### 第三步：确定任务类型

根据用户需求，判断任务类型：

| 任务类型 | 对应目录 | 说明 |
|----------|----------|------|
| 不知道用什么 Prompt | `_routing/` | 自主路由 |
| 定义 AI 行为方式 | `system/` | 系统级 |
| 扮演某个角色 | `role/` | 角色型 |
| 完成具体任务 | `task/` | 任务型 |
| 多步骤工作流 | `workflow/` | 工作流型 |
| 调用特定工具 | `tool-use/` | 工具型 |
| 格式化输出 | `output/` | 输出型 |
| 优化 Prompt | `meta/` | Meta 型 |
| 特定领域任务 | `domains/` | 领域型 |

---

## Prompt 分类详解

### `_routing/` - 自主路由类

**用途**：帮助 AI 自主理解仓库、选择和组合 Prompts。

**何时使用**：
- 面对新项目或陌生代码库
- 不确定该用哪个 Prompt
- 需要组合多个 Prompts
- 需要构建自定义工作流

**包含的 Prompts**：

| ID | 名称 | 用途 |
|----|------|------|
| `scan-repository-and-build-task-map` | 扫描仓库构建任务地图 | 扫描仓库结构，建立任务上下文 |
| `identify-task-type-and-route` | 识别任务类型并路由 | 判断任务类型，确定使用顺序 |
| `select-relevant-prompts-from-index` | 从索引选择相关 Prompts | 基于关键词和标签匹配 |
| `compose-multiple-prompts-for-one-task` | 组合多个 Prompts | 处理依赖、参数传递、结果汇总 |

**AI 路由流程**：

```markdown
1. scan-repository-and-build-task-map
   ↓
2. identify-task-type-and-route
   ↓
3. select-relevant-prompts-from-index
   ↓
4. compose-multiple-prompts-for-one-task
```

---

### `system/` - 系统级提示词

**用途**：定义 AI 的基础行为方式和长期准则。

**何时使用**：
- 作为所有其他 Prompt 的基础
- 需要定义 AI 的角色和行为
- 长期任务需要一致的行为规范

**包含的 Prompts**：

| ID | 名称 | 用途 |
|----|------|------|
| `general-ai-workbench` | 通用 AI 工作台 | 多功能助手基础行为 |
| `coding-agent` | 编程 Agent | 专业程序员行为准则 |
| `debugging-agent` | 调试 Agent | 专业调试助手行为准则 |

**使用建议**：
- 每次对话先加载一个 System Prompt
- 根据任务类型选择对应的 System Prompt
- 可叠加使用（如 `general-ai-workbench` + `coding-agent`）

---

### `task/` - 任务型提示词

**用途**：针对具体任务的提示词，可直接执行特定工作。

#### `task/coding/` - 编程类

| ID | 名称 | 用途 |
|----|------|------|
| `generate-code-from-requirement` | 从需求生成代码 | 自然语言需求 → 可执行代码 |
| `implement-feature-from-spec` | 从规格实现功能 | 技术规格 → 完整模块 |
| `review-code-for-quality` | 代码质量审查 | 代码 → 结构化审查报告 |

#### `task/debugging/` - 调试类

| ID | 名称 | 用途 |
|----|------|------|
| `identify-root-cause` | 识别根因 | 错误分析 → 根因确定 |
| `generate-debug-plan` | 生成调试计划 | 根因 → 修复计划 |
| `fix-bug-safely` | 安全修复 | 计划 → 实施修复 |
| `verify-fix-after-change` | 验证修复 | 修复 → 验证结果 |

#### `task/repo-analysis/` - 仓库分析类

| ID | 名称 | 用途 |
|----|------|------|
| `analyze-repository-structure` | 分析仓库结构 | 陌生仓库 → 项目地图 |
| `locate-bug-related-files` | 定位 Bug 相关文件 | Bug 描述 → 文件位置 |
| `summarize-project-architecture` | 总结项目架构 | 仓库 → 架构概要 |

#### `task/planning/` - 规划类

| ID | 名称 | 用途 |
|----|------|------|
| `create-execution-plan` | 创建执行计划 | 复杂任务 → 分阶段计划 |
| `break-down-task-into-subtasks` | 拆解任务 | 大任务 → 可执行子任务 |

#### `task/research/` - 研究类

| ID | 名称 | 用途 |
|----|------|------|
| `prepare-research-brief` | 准备研究简报 | 研究主题 → 结构化简报 |

---

### `workflow/` - 工作流提示词

**用途**：定义多步骤的完整工作流程。

**何时使用**：
- 需要按顺序执行多个步骤
- 复杂任务需要明确流程
- 需要确保步骤完整不遗漏

---

### `tool-use/` - 工具调用提示词

**用途**：定义如何调用特定工具或 API。

**何时使用**：
- 需要使用特定工具（如 Git、Docker）
- 需要调用外部 API
- 需要执行系统命令

---

### `output/` - 输出格式提示词

**用途**：定义标准化的输出格式。

**何时使用**：
- 需要特定格式的报告
- 需要结构化输出
- 需要符合特定规范

---

### `meta/` - Prompt 优化提示词

**用途**：用于优化、调试和重写其他 Prompts。

**何时使用**：
- 需要优化现有 Prompt
- 需要调试 Prompt 效果
- 需要将通用 Prompt 改写为特定场景

---

### `domains/` - 领域型提示词

**用途**：针对特定领域的专用提示词。

**何时使用**：
- 特定领域任务（如金融、医疗、教育）
- 行业专用场景
- 专业领域知识

---

## AI 自主选择流程

### 流程图

```
用户请求
    ↓
┌─────────────────────────────┐
│ 读取 _routing/ 提示词       │
│ scan-repository-and-restore │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│ identify-task-type-and-route│
│ 识别任务类型                │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│ select-relevant-prompts     │
│ 选择相关 Prompts            │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│ compose-multiple-prompts    │
│ 组合多个 Prompts            │
└─────────────────────────────┘
    ↓
执行任务
```

### 任务类型 → Prompt 映射

| 任务 | System Prompt | Task Prompts | Workflow |
|------|---------------|---------------|----------|
| 代码生成 | coding-agent | generate-code-from-requirement | - |
| Bug 修复 | debugging-agent | identify-root-cause → generate-debug-plan → fix-bug-safely → verify-fix | bug-fix-workflow |
| 仓库分析 | general-ai-workbench | analyze-repository-structure | repo-onboarding |
| 项目规划 | general-ai-workbench | create-execution-plan, break-down-task | planning-workflow |
| 技术研究 | general-ai-workbench | prepare-research-brief | research-workflow |
| 代码审查 | coding-agent | review-code-for-quality | code-review-workflow |

---

## 快速参考表

### 常用组合

| 场景 | 推荐组合 |
|------|----------|
| 写代码 | system/coding-agent + task/coding/generate-code |
| 修 Bug | system/debugging-agent + task/debugging/* (4个) |
| 分析代码库 | system/general-ai-workbench + task/repo-analysis/* (3个) |
| 做规划 | system/general-ai-workbench + task/planning/* (2个) |
| 做研究 | system/general-ai-workbench + task/research/prepare-research |

### 按用途查找

| 需要 | 去哪里找 |
|------|----------|
| 不知道用什么 | `_routing/` |
| 定义 AI 角色 | `system/` |
| 生成代码 | `task/coding/` |
| 调试修复 | `task/debugging/` |
| 理解代码库 | `task/repo-analysis/` |
| 做计划 | `task/planning/` |
| 做调研 | `task/research/` |
| 格式化输出 | `output/` |
| 调用工具 | `tool-use/` |

---

## 字段索引

所有 Prompts 包含以下标准字段：

| 字段 | 说明 |
|------|------|
| `id` | 唯一标识符 |
| `name` | 名称 |
| `summary` | 一句话描述 |
| `type` | 类型 |
| `status` | 状态 |
| `version` | 版本 |
| `category` | 主分类 |
| `sub_category` | 子分类 |
| `tags` | 标签 |
| `keywords` | 关键词 |
| `intent` | 使用意图 |
| `applicable_models` | 适用模型 |
| `input_requirements` | 输入要求 |
| `output_requirements` | 输出要求 |
| `preconditions` | 前置条件 |
| `anti_patterns` | 应避免的模式 |
| `failure_modes` | 失败模式 |
| `self_check` | 自检清单 |
| `related_skills` | 相关 Skills |
| `related_workflows` | 相关 Workflows |
| `related_prompts` | 相关 Prompts |

详见：[`_core/prompt-field-spec.md`](_core/prompt-field-spec.md)

---

## 维护指南

### 添加新 Prompt

1. 遵循 `prompt-writing-standard.md` 的规范
2. 使用 `prompt-quality-checklist.md` 检查
3. 更新本 INDEX.md
4. 提交 PR

### 版本升级

- 遵循 `prompt-lifecycle.md` 的规范
- 保持向后兼容时：`次版本号 +1`
- 破坏性变更：`主版本号 +1`

---

**最后更新**：2026-03-19
