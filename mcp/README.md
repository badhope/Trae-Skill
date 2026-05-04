# MCP - Model Context Protocol

> DevFlow Agent 基于 **MCP 标准协议** 构建开发工作流智能体
>
> 一次定义，多平台运行 ✅

---

## 🎯 核心概念

| 概念 | 说明 | 示例 |
|------|------|------|
| 🔧 **Tools** | AI 可调用的函数 | `fs_read_file()`, `terminal_exec()` |
| 📄 **Resources** | 上下文资源 | `agent://config`, `agent://workflow` |
| ⚡ **Prompts** | 预设命令 | `/new-project`, `/bug-fix` |

---

## 🚀 快速开始

### 创建 DevFlow Agent

```yaml
# agent.yaml
name: my-agent
version: 1.0.0
description: 我的开发工作流智能体

capabilities:
  - new-project
  - bug-fixing
  - code-review

workflows:
  - intent: new-project
    stages:
      - name: Plan
        skill: task-planner
      - name: Implement
        skill: fullstack-engine
```

---

## 📁 Agent 文件结构

```
my-agent/
├── agent.yaml           # 智能体配置
├── system-prompt.md    # 角色定义
├── workflow/           # 工作流定义
│   ├── intent.yaml     # 意图识别
│   ├── stages.yaml     # 阶段定义
│   └── tools.yaml      # 工具列表
├── knowledge/          # 知识库
└── tests/             # 测试用例
```

---

## 🔧 工具设计原则

1. **单一职责**：一个工具只做一件事
2. **语义命名**：`run_npm_test` 优于 `execute`
3. **完整描述**：让 AI 准确理解适用场景
4. **强类型参数**：提供清晰的参数定义
5. **结构化返回**：返回 JSON 格式

---

## ⚡ 意图识别

| 意图 | 关键词 | 工作流 |
|------|--------|--------|
| `new-project` | 创建, 新项目, initialize | full-project-workflow |
| `feature-implementation` | 实现, 功能, feature | feature-workflow |
| `bug-fixing` | 修复, bug, 错误 | bug-fix-workflow |
| `code-review` | 审查, review | code-review-workflow |
| `deployment` | 部署, deploy | deployment-workflow |

---

## 🔌 平台兼容性

| 平台 | 状态 |
|------|------|
| ✅ 豆包 | 直接上传文件夹 |
| ✅ Claude Desktop | MCP 标准兼容 |
| ✅ Cursor | 深度集成 |
| ✅ Windsurf | Cascade 支持 |
| ✅ Trae | 原生支持 |

---

## 📚 更多资源

- [DevFlow Agent 官方文档](../README.md)
- [MCP 官方规范](https://modelcontextprotocol.io/)
- [示例智能体](../example-agents/full-stack-assistant/)
