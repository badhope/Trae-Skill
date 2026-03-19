# Prompts 仓库

一个高质量、结构化、开源维护的 Prompt 仓库，既适合人类复制使用，也适合 AI 下载后自动检索、路由和组合使用。

## 仓库定位

这是一个用于存放和组织 AI Prompts、Workflows 和相关资源的开源仓库。仓库设计遵循以下原则：

- **AI 友好**：结构化设计，支持 AI 自动解析、检索和路由
- **人类可读**：清晰的文档和注释，方便直接浏览和维护
- **模块化**：小颗粒度设计，支持灵活组合
- **可扩展**：预留扩展空间，支持模型变体和场景特化

## 目录结构

```
prompts/
├── _routing/           # AI 自主路由和选择
├── _core/             # 核心规范和指南
├── system/            # 系统级提示词
├── role/              # 角色型提示词
├── task/              # 任务型提示词
│   ├── coding/        # 编程相关
│   ├── debugging/      # 调试相关
│   ├── repo-analysis/ # 仓库分析
│   ├── planning/      # 规划相关
│   └── research/      # 研究相关
├── workflow/          # 工作流提示词
├── tool-use/          # 工具调用提示词
├── output/            # 输出格式提示词
├── meta/              # Prompt 优化提示词
└── domains/           # 领域型提示词
```

## 快速开始

### 人类使用

1. **查找合适的 Prompt**：浏览对应分类目录，或使用 `INDEX.md` 索引
2. **复制使用**：直接复制 `Prompt Body` 部分到你的 AI 对话中
3. **组合使用**：根据需要组合多个 Prompts、Workflows 和 Skills

### AI 使用

1. **读取 INDEX**：首先读取 `prompts/INDEX.md` 了解仓库结构
2. **判断任务类型**：根据用户需求判断任务类型
3. **选择合适的 Prompt**：使用 `_routing/` 类提示词辅助选择
4. **组合使用**：按需组合多个 Prompts 和 Workflows

## 分类说明

### `_routing/` - 自主路由

帮助 AI 在拿到整个仓库后，自主检索、选择和组合 Prompts。

| Prompt | 用途 |
|--------|------|
| `scan-repository-and-build-task-map` | 扫描仓库结构，构建任务地图 |
| `identify-task-type-and-route` | 识别任务类型并路由 |
| `select-relevant-prompts-from-index` | 从索引选择相关 Prompts |
| `compose-multiple-prompts-for-one-task` | 组合多个 Prompts |

### `system/` - 系统级提示词

定义 AI 的基础行为准则。

| Prompt | 用途 |
|--------|------|
| `general-ai-workbench` | 通用 AI 工作台 |
| `coding-agent` | 编程 Agent |
| `debugging-agent` | 调试 Agent |

### `task/` - 任务型提示词

针对具体任务的提示词。

#### `task/coding/` - 编程类

| Prompt | 用途 |
|--------|------|
| `generate-code-from-requirement` | 根据需求生成代码 |
| `implement-feature-from-spec` | 根据规格实现功能 |
| `review-code-for-quality` | 代码质量审查 |

#### `task/debugging/` - 调试类

| Prompt | 用途 |
|--------|------|
| `identify-root-cause` | 识别根因 |
| `generate-debug-plan` | 生成调试计划 |
| `fix-bug-safely` | 安全修复 Bug |
| `verify-fix-after-change` | 验证修复 |

#### `task/repo-analysis/` - 仓库分析类

| Prompt | 用途 |
|--------|------|
| `analyze-repository-structure` | 分析仓库结构 |
| `locate-bug-related-files` | 定位 Bug 相关文件 |
| `summarize-project-architecture` | 总结项目架构 |

#### `task/planning/` - 规划类

| Prompt | 用途 |
|--------|------|
| `create-execution-plan` | 创建执行计划 |
| `break-down-task-into-subtasks` | 拆解任务 |

#### `task/research/` - 研究类

| Prompt | 用途 |
|--------|------|
| `prepare-research-brief` | 准备研究简报 |

### `workflow/` - 工作流提示词

定义多步骤的工作流程。

### `tool-use/` - 工具调用提示词

定义如何使用特定工具或 API。

### `output/` - 输出格式提示词

定义标准化的输出格式。

### `meta/` - Prompt 优化提示词

用于优化、调试和重写其他 Prompts。

### `domains/` - 领域型提示词

针对特定领域的专用提示词。

## 如何查找合适的 Prompt

### 方法 1：浏览目录

根据任务类型浏览对应目录：
- 编程任务 → `task/coding/`
- 调试任务 → `task/debugging/`
- 分析任务 → `task/repo-analysis/`

### 方法 2：使用索引

查看 `INDEX.md` 获取完整的 Prompt 索引和推荐使用顺序。

### 方法 3：AI 辅助路由

下载仓库后，让 AI 读取 `_routing/` 类提示词，AI 将自动帮你选择合适的 Prompts。

## 如何复制使用

1. 打开对应的 Prompt 文件
2. 复制 `Prompt Body` 部分（不包括 frontmatter 和元信息）
3. 根据需要修改 `Variables` 中的变量
4. 粘贴到 AI 对话中使用

## 如何组合使用

### Prompt 组合原则

1. **系统 + 任务**：先加载系统提示词，再加载任务提示词
2. **路由优先**：复杂任务先用路由提示词确定流程
3. **按需组合**：不是越多越好，根据实际需要选择

### 示例组合

**代码生成任务**：
```
1. general-ai-workbench (系统)
2. coding-agent (系统)
3. generate-code-from-requirement (任务)
```

**Bug 修复任务**：
```
1. general-ai-workbench (系统)
2. debugging-agent (系统)
3. identify-root-cause (任务)
4. generate-debug-plan (任务)
5. fix-bug-safely (任务)
6. verify-fix-after-change (任务)
```

## 如何贡献新 Prompt

### 贡献流程

1. **Fork 仓库**
2. **创建分支**：`git checkout -b prompt/your-prompt-name`
3. **编写 Prompt**：遵循 `prompt-writing-standard.md` 中的规范
4. **自检**：使用 `prompt-quality-checklist.md` 检查
5. **提交 PR**：描述 Prompt 的用途和使用方式

### 命名规范

- 文件名：`prompt-[category]-[specific-name].md`
- ID：`prompt-[category]-[name]-v[version]`
- 示例：`prompt-task-coding-generate-code-from-requirement.md`

### 新增位置

| 类型 | 目录 |
|------|------|
| 路由提示词 | `_routing/` |
| 系统提示词 | `system/` |
| 任务提示词 | `task/[category]/` |
| 工作流提示词 | `workflow/` |
| 工具提示词 | `tool-use/` |

## 如何保持统一风格

1. **遵循写作规范**：阅读 `prompt-writing-standard.md`
2. **使用标准字段**：按照 `prompt-field-spec.md` 定义字段
3. **参考风格指南**：`prompt-style-guide.md` 定义了语言风格
4. **使用检查清单**：`prompt-quality-checklist.md` 用于交付前检查

## 维护建议

### 版本管理

- 使用语义化版本：`主版本.次版本.修订号`
- `v1.0.0`：全新 Prompt
- `v1.1.0`：新增功能（向后兼容）
- `v2.0.0`：破坏性变更

### 状态管理

- `draft`：草稿，不保证稳定性
- `active`：活跃版本，稳定可用
- `deprecated`：已废弃，不推荐使用

### 定期审查

- 审查频率：每季度一次
- 检查内容：准确性、相关性、完整性
- 更新维护：及时更新过时内容

## 相关资源

- **Skills 仓库**：[../skills/](../skills/) - 配套的 Skills
- **Workflows 仓库**：[../workflows/](../workflows/) - 工作流集合
- **Registry**：[../registry/](../registry/) - 全量索引

## License

本仓库采用 MIT License。

## 贡献

欢迎提交 Issue 和 Pull Request！
