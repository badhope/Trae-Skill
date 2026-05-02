# MCP - Model Context Protocol

> Trae Skills 采用 **Anthropic MCP 标准协议** 构建技能生态
> 
> 一次编写，兼容所有 AI 客户端 ✅

---

## 🎯 三大核心原语

| 原语 | 控制者 | 用途 | 示例 |
|------|-------|------|------|
| 🔧 **Tools** | AI 模型 | 可执行函数 | `git_status()`, `run_tests()` |
| 📄 **Resources** | IDE 应用 | 上下文注入 | `trae://git/changes` |
| ⚡ **Prompts** | 用户 | 命令式触发 | `/review-changes` |

---

## 🚀 快速开始

### 5 分钟创建你的第一个 MCP Skill

```typescript
import { createMCPServer } from '@trae/skills'

export default createMCPServer({
  name: 'my-skill',
  version: '1.0.0',
  description: '我的第一个 MCP 技能',
  author: 'Your Name',
  icon: '✨'
})
  // 1. 添加工具 (AI 自主决定何时调用)
  .addTool({
    name: 'do_something',
    description: '工具功能说明，让 AI 理解何时使用',
    parameters: {
      input: {
        type: 'string',
        description: '参数说明',
        required: true
      }
    },
    execute: async (params) => {
      return { result: params.input }
    }
  })
  // 2. 添加提示词命令 (用户输入 / 触发)
  .addPrompt({
    name: 'do-task',
    description: '用户输入 /do-task 触发',
    generate: async (args) => {
      return `完整的 LLM 提示词...`
    }
  })
  // 3. 添加资源 (自动注入上下文)
  .addResource({
    uri: 'trae://my-skill/data',
    name: '数据摘要',
    description: '自动注入到上下文',
    get: async () => {
      return { data: '实时获取' }
    }
  })
  .build()
```

---

## 📦 官方 MCP 服务器

| 服务器 | 状态 | 工具数 | 提示词 | 资源 |
|--------|------|--------|--------|------|
| **git** | ✅ 稳定 | 4 | 1 | 1 |
| **terminal** | ✅ 稳定 | 4 | 1 | 1 |
| **code-review** | ✅ 稳定 | 2 | 2 | 1 |
| **testing** | 🚧 开发中 | - | - | - |
| **database** | 🚧 开发中 | - | - | - |

---

## 🔧 工具设计最佳实践

### ❌ 反面教材
```typescript
// ❌ 太宽泛，AI 不知道何时用
{
  name: 'execute',
  description: '执行代码',
  parameters: { code: { type: 'string' } }
}
```

### ✅ 正面教材
```typescript
// ✅ 具体、明确，边界清晰
{
  name: 'run_npm_test',
  description: '运行 Jest 单元测试，返回覆盖率报告',
  parameters: {
    file: {
      type: 'string',
      description: '指定测试文件路径，如 tests/utils.test.ts',
      required: false
    }
  },
  execute: async (params) => { ... }
}
```

### 设计原则
1. **单一职责**：一个工具只做一件事
2. **语义命名**：`run_unit_tests` 优于 `execute`
3. **完整描述**：让 AI 准确理解适用场景
4. **强类型参数**：尽可能提供枚举值
5. **结构化返回**：返回 JSON，不要返回纯文本

---

## ⚡ 提示词设计最佳实践

### 命名规范
- 使用短横线：`/review-file` 而不是 `reviewFile`
- 动词开头：`/generate`, `/fix`, `/explain`
- 领域清晰：`/docker-logs`, `/sql-explain`

### 结构规范
```typescript
.generate(async (args) => {
  return `
## 🎯 任务目标
明确告诉 AI 要做什么

### 约束条件
1. 输出格式要求
2. 必须遵守的规则
3. 禁止事项

### 可用工具
- 调用 \`tool_name\` 做什么
  `.trim()
})
```

---

## 📄 资源设计最佳实践

### URI 命名规范
```
trae://{server-name}/{resource-name}

示例:
trae://git/changes
trae://terminal/project-info
trae://database/schema
```

### 设计原则
1. **小而精**：资源内容不要超过 10KB
2. **结构化**：返回 JSON，不要返回大文本
3. **实时性**：每次访问都重新计算
4. **幂等性**：多次访问结果一致

---

## 🧪 验证和测试

在 Trae IDE 中快速验证：

```
> /mcp list                   # 列出所有服务器
> /mcp tools git             # 查看 git 服务器的工具
> /mcp call git git_status   # 手动调用工具
> /review-changes            # 触发提示词
```

---

## 🔌 兼容性

本实现 100% 兼容 MCP 标准，可无缝对接：

| 平台 | 兼容状态 |
|------|---------|
| ✅ Trae IDE | 原生支持 |
| ✅ Anthropic Claude | 标准兼容 |
| ✅ OpenAI ChatGPT | 标准兼容 |
| ✅ Cursor | 可接入 |
| ✅ Windsurf | 可接入 |

---

## 📚 更多资源

- [MCP 官方规范](https://modelcontextprotocol.io/)
- [Anthropic Agent Skills](https://www.anthropic.com/engineering/agent-skills)
- [开发模板](./template/index.ts)
