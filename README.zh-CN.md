# AI Skill & Prompt 仓库

[English](README.md) · [中文](README.zh-CN.md)

---

[![版本](https://img.shields.io/badge/version-v2.0.0-blue.svg)](https://github.com/badhope/skill)
[![许可证: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellowgreen.svg)](LICENSE-CODE)
[![许可证: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-orange.svg)](LICENSE-CONTENT)
[![GitHub stars](https://img.shields.io/github/stars/badhope/skill?style=social)](https://github.com/badhope/skill)
[![GitHub forks](https://img.shields.io/github/forks/badhope/skill?style=social)](https://github.com/badhope/skill)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![维护状态](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/badhope/skill/graphs/commit-activity)

---

## 🎯 项目概述

**AI Skill & Prompt Repository** 是一个模块化的 **AI 技能/提示词/工作流** 知识库，专为追求高效编程和智能化工作流的开发者设计。

| 适用对象 | 核心价值 |
|----------|----------|
| **开发者** | 快速查找、复制、使用高质量提示词 |
| **AI 系统** | 自主理解、路由、选择和组合技能 |
| **研究者** | 学术写作、研究辅助、文献检索 |
| **创作者** | 创意写作、内容生成、灵感激发 |

**核心技术栈:** GPT-4 · Claude · 强化学习 · 上下文记忆 · MCP 工具

---

## ⭐ 为什么选择本项目？

| 特性 | 说明 |
|------|------|
| 🏆 **132+ 精选提示词** | 覆盖编程、调试、学习、创意等场景 |
| 🎯 **78+ 标准化技能** | 模块化设计，即插即用 |
| 🔧 **10+ 预置工作流** | 开箱即用的多步骤任务流 |
| 🧠 **上下文记忆系统** | <100ms 语义检索响应 |
| 🤖 **强化学习引擎** | 自适应工作流优化 |
| 🔌 **MCP 工具框架** | 可扩展的代码质量检测、文档生成 |
| 📚 **学术写作套件** | 文献检索、论文优化、查重检测 |
| 🎨 **创意内容生成** | 小说创作、专业文案、多模态生成 |
| 🌐 **双语支持** | 完整的中英文文档 |

---

## 🚀 核心能力

### 🧠 上下文记忆系统

分层记忆架构，支持语义搜索：

| 记忆类型 | TTL | 容量 | 适用场景 |
|---------|-----|------|----------|
| **短期记忆** | 1小时 | 100条 | 当前对话上下文 |
| **中期记忆** | 2小时 | 无限 | 会话级信息 |
| **长期记忆** | 永久 | 无限 | 跨会话知识 |

**核心特性:**
- 语义相似度检索（响应时间 <100ms）
- 重要性评分与衰减机制
- 时间戳版本控制的冲突解决
- 基于标签和嵌入向量的搜索

### 🤖 强化学习引擎

基于 PPO 的 RL 框架，实现自适应工作流优化：

```python
from rl_engine import RLEngine, RLConfig

config = RLConfig(
    state_dim=128,
    action_dim=10,
    learning_rate=0.001,
    gamma=0.99
)
engine = RLEngine(config)
```

**能力矩阵:**
- 多维度奖励函数（代码质量、解决效率、用户满意度）
- 优先级采样经验回放
- 动态 ε 衰减的探索-利用平衡
- 代码模拟与执行环境

### 🔧 MCP 工具框架

可扩展的工具框架，包含专业模块：

| 工具 | 功能描述 |
|------|----------|
| **CodeQualityCheckerTool** | 静态代码分析、风格检查 |
| **UnitTestGeneratorTool** | 自动化测试生成 |
| **APIDocGeneratorTool** | OpenAPI/Swagger 文档生成 |
| **RefactoringAssistantTool** | 代码异味检测与重构建议 |
| **CodeGeneratorTool** | MCU 代码生成 |
| **PeripheralDriverTool** | GPIO、UART、SPI、I2C 驱动生成 |

---

## 📚 学术与专业工具

### 🔬 学术写作套件

| 模块 | 功能 |
|------|------|
| **上下文感知文献搜索** | 语义搜索研究数据库 |
| **研究论文增强** | 结构优化、清晰度提升 |
| **抄袭检测** | 原创性验证与引用检查 |
| **学术诚信验证** | 学术诚信验证 |

### 🎓 学习支持模块

- 自适应学习路径推荐
- 知识缺口识别
- 间隔重复调度
- 进度跟踪与评估

### ✍️ 专业写作工具

- 多受众语气适配（正式/休闲/技术）
- 品牌调性一致性检查
- A/B 标题优化
- 行动号召效果分析

---

## 🎨 创意内容生成

### 📖 小说与故事开发

| 特性 | 描述 |
|------|------|
| **叙事结构辅助** | 三幕式、英雄之旅、救命猫 |
| **角色发展** | 原型映射、动机分析 |
| **世界观构建** | 一致性检查、世界观管理 |
| **对话生成** | 语气适配、角色声音保持 |

### 🎬 多模态内容生成

| 模态 | 能力 |
|------|------|
| **文本转图像** | Stable Diffusion 集成就绪 |
| **文本转视频** | 故事板生成、场景描述 |
| **音视频** | 字幕同步、音频描述 |

### 🤖 智能体开发工具包

- 可定制行为模式
- 人格配置
- 记忆与上下文管理
- 工具使用工作流集成

---

## 🏗️ 架构设计

### 📦 模块化架构

```
src/
├── context_memory/     # 分层记忆 + 语义搜索
│   ├── stores.py       # 短期/中期/长期存储
│   ├── semantic_search.py  # 向量运算、相似度
│   └── manager.py      # 记忆编排
├── rl_engine/          # 强化学习
│   ├── engine.py       # RL核心实现
│   ├── ppo.py          # Policy/Value网络
│   └── reward.py       # 奖励计算
├── coding_engine/     # 代码分析与生成
│   ├── analyzer.py     # 语法分析
│   ├── quality.py      # 代码质量检查
│   ├── patterns.py     # 设计模式库
│   └── algorithms.py   # 算法实现
├── network/           # 分布式通信
│   └── communication.py  # 服务网格、负载均衡
├── mcp_tools/        # MCP工具框架
│   ├── framework.py    # 工具编排
│   ├── tools.py       # 内置工具
│   └── mcu_tools.py   # MCU代码生成
└── special/          # 特殊功能模块
    └── modules.py     # 动画、游戏、模拟等
```

---

## ✨ 资源一览

| 类别 | 数量 | 描述 |
|------|:----:|------|
| **Prompts** | 132+ | 编程、调试、规划、研究用提示词 |
| **Skills** | 78+ | AI任务路由能力定义 |
| **Workflows** | 10+ | 多步骤执行流程 |
| **Tool-Use Guides** | 8+ | 文件读取、命令执行系统方法 |
| **Output Formats** | 6+ | JSON、YAML、Markdown、表格、清单、报告 |
| **Meta Prompts** | 8+ | 提示词工程工具 |
| **Special Modules** | 6 | 动画、游戏、模拟等专业模块 |

---

## 🚀 快速导航

### 人类用户

> **"我想要AI帮我..."**

| 任务 | 链接 |
|------|------|
| 🔨 生成或修改代码 | [prompts/task/coding/](prompts/task/coding/) |
| 🐛 调试和修复Bug | [prompts/task/debugging/](prompts/task/debugging/) |
| 📊 理解代码仓库 | [prompts/task/repo-analysis/](prompts/task/repo-analysis/) |
| 📋 创建执行计划 | [prompts/task/planning/](prompts/task/planning/) |
| 🔬 进行研究 | [prompts/task/research/](prompts/task/research/) |
| 🔄 执行多步骤工作流 | [prompts/workflow/](prompts/workflow/) |
| 📤 输出特定格式 | [prompts/output/](prompts/output/) |
| 🛠️ 优化提示词 | [prompts/meta/](prompts/meta/) |
| 📧 日常邮件撰写 | [prompts/everyday/](prompts/everyday/) |
| ✅ 清单生成 | [prompts/everyday/prompt-everyday-checklist.md](prompts/everyday/) |

---

### AI 系统

**引导顺序** — 按此顺序读取文件：

```
1. START-HERE.md              → 入口点
2. ARCHITECTURE.md            → 设计理念
3. ASSET-MAP.md               → 完整清单
4. INDEX.md                   → 结构概览
5. registry/prompts-registry.yaml  → 发现提示词
6. registry/routes-registry.yaml   → 学习路由
7. AI-USAGE.md                → 使用模式
8. AI-ROUTING.md              → 路由逻辑
9. AI-BOOTSTRAP.md            → 首次设置
```

---

## 📈 统计数据

| 指标 | 数值 |
|------|------|
| 📝 Prompts | 132+ |
| 🎯 Skills | 78+ |
| 🔧 Workflows | 10+ |
| ⚙️ Source Modules | 6 |
| 📚 Documentation | 50+ |
| 🌍 Languages | 2 (EN/ZH) |

---

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

**贡献方式:**

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多详情。

---

## 📄 许可证

本项目采用双许可证：

- **代码部分**: [Apache-2.0 License](LICENSE-CODE)
- **内容部分**: [CC BY 4.0 License](LICENSE-CONTENT)

---

## 🔗 相关链接

| 链接 | 描述 |
|------|------|
| [📦 NPM Package](https://npmjs.com/) | 前端组件包 (即将上线) |
| [🐍 PyPI Package](https://pypi.org/) | Python SDK (即将上线) |
| [📖 Documentation](https://github.com/badhope/skill/wiki) | 完整文档 |
| [🐛 Issue Tracker](https://github.com/badhope/skill/issues) | 问题反馈 |
| [💬 Discussions](https://github.com/badhope/skill/discussions) | 讨论区 |

---

## 📬 联系方式

- **GitHub**: [badhope](https://github.com/badhope)
- **Project Link**: [https://github.com/badhope/skill](https://github.com/badhope/skill)

---

<div align="center">
  <strong>如果这个项目对你有帮助，请给它一个 ⭐</strong>
  <br>
  <em>使用 ❤️ 由 badhope 构建</em>
</div>
