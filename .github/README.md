# 🚀 DevFlow Agent

**Development Workflow Agent - 7 Core Skills + 16 Workflows for AI Platforms**

> ✅ 适用于所有 AI 平台: Claude Desktop • Cursor • Windsurf • Trae • 豆包

---

## ⚡ 快速开始

### 使用示例智能体

1. 下载 `example-agents/full-stack-assistant/` 文件夹
2. 上传到您的 AI 平台
3. 用自然语言描述任务

### 加载到编辑器

#### Claude Desktop

添加到 `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "devflow-agent": {
      "command": "npx",
      "args": ["-y", "@devflow-agent/core"]
    }
  }
}
```

#### Cursor / Windsurf / Trae

按照编辑器的 MCP 配置添加:

```bash
npx -y @devflow-agent/core
```

---

## 📦 核心功能

| 组件 | 数量 | 描述 |
|------|------|------|
| 🚀 **核心技能** | 7 | Task Planner, Fullstack Engine, Testing Master, etc. |
| 📋 **工作流** | 16 | 覆盖开发全周期 |
| 🛠️ **工具映射** | 50+ | 完整的工具-技能映射 |
| 🔌 **平台支持** | 5+ | 所有 MCP 兼容的 AI 平台 |

---

## 📁 项目结构

```
DevFlow Agent/
├── example-agents/           # 示例智能体
│   └── full-stack-assistant/ # 全栈开发助手
├── packages/core/skill/      # 核心技能实现
│   └── skills/              # 7个技能
├── .agent-skills/           # 技能配置
│   └── skills/config/       # 工具-技能映射
└── README.md                # 主文档
```

---

## 🔗 链接

- 📚 [完整文档](../README.md)
- 🛠️ [技能列表](../packages/core/skill/)
- 🐛 [问题反馈](https://github.com/badhope/devflow-agent/issues)
- 💬 [讨论区](https://github.com/badhope/devflow-agent/discussions)

---

## ⭐ 支持

如果这个项目对您有帮助，请给一个 ⭐！

---

**为 AI 开发者社区构建** ❤️
