# AI Skill & Prompt 仓库

<!-- ==================== METADATA ==================== -->
<!--
  repository: badhope/skill
  version: v2.0.0
  description: 模块化 AI Skill/Prompt/Workflow 仓库，具备高级技术能力
  topics: [ai, prompts, skills, workflows, coding, debugging, mcp, rl-engine, academic, creative]
-->
<!-- ================================================= -->

<!-- Language Switcher -->
[English](README.md) · [中文](README.zh-CN.md)

---

[![Version](https://img.shields.io/badge/version-v2.0.0-blue.svg)](https://github.com/badhope/skill)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-yellowgreen.svg)](LICENSE-CODE)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-orange.svg)](LICENSE-CONTENT)
[![GitHub stars](https://img.shields.io/github/stars/badhope/skill?style=social)](https://github.com/badhope/skill)

---

## 🎯 一句话定位

模块化的 AI Skill/Prompt/Workflow 资产仓库，集成强化学习、上下文记忆系统、MCP 工具和学术/创意应用专业模块，同时面向**人类用户**（快速查找复制使用）和 **AI 系统**（自主理解、路由、筛选、组合资产）。

---

## 🚀 核心能力

### 🧠 上下文记忆系统
分层记忆架构，支持语义搜索：

| 记忆类型 | TTL | 容量 | 用途 |
|----------|-----|------|------|
| **短期记忆** | 1小时 | 100条 | 当前对话上下文 |
| **中期记忆** | 2小时 | 无限 | 会话级信息 |
| **长期记忆** | 永久 | 无限 | 跨会话知识 |

**核心特性：**
- 语义相似度检索（响应时间<100ms）
- 重要性评分与衰减机制
- 时间戳版本控制的冲突解决
- 基于标签和嵌入向量的搜索

### 🤖 强化学习引擎
基于 PPO 的 RL 框架，用于自适应工作流优化：

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

**功能：**
- 多维度奖励函数（代码质量、解决效率、用户满意度）
- 优先采样经验回放
- 动态 epsilon 衰减的探索-利用平衡
- 代码模拟与执行环境

### 🔧 MCP（模型控制程序）工具
可扩展的工具框架，包含专业模块：

| 工具 | 说明 |
|------|------|
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
| **上下文感知文献搜索** | 跨研究数据库的语义搜索 |
| **研究论文增强** | 结构优化、清晰度提升 |
| **查重检测** | 原创性验证与引用检查 |
| **学术诚信验证** | 学术工作诚信验证 |

### 🎓 学习支持模块

- 自适应学习路径推荐
- 知识缺口识别
- 间隔重复计划
- 进度跟踪与评估

---

## 🎨 创意内容生成套件

### ✍️ 小说与故事开发

| 特性 | 说明 |
|------|------|
| **叙事结构辅助** | 三幕式、英雄之旅、救命情节 |
| **角色发展** | 原型映射、动机分析 |
| **世界观构建** | 一致性检查、传说管理 |
| **对话生成** | 语调适配、角色声音保持 |

### 📝 专业文案工具

- 跨受众语调适配（正式、休闲、技术）
- 品牌声音一致性检查
- A/B 标题优化
- 行动号召有效性分析

### 🎬 多模态内容生成

| 模态 | 能力 |
|------|------|
| **文生图** | Stable Diffusion 集成就绪 |
| **文生视频** | 分镜生成、场景描述 |
| **视听整合** | 字幕同步、音频描述 |

### 🤖 智能体开发工具包

- 可定制行为模式
- 个性化配置
- 记忆与上下文管理
- 工具使用工作流集成

---

## 🏗️ 架构优化

### 📦 模块化架构

```
src/
├── context_memory/     # 分层语义记忆
│   ├── stores.py       # 短期/中期/长期存储
│   ├── semantic_search.py  # 向量运算、相似度
│   └── manager.py      # 记忆编排
├── rl_engine/          # 强化学习
│   ├── engine.py       # RL 核心实现
│   ├── ppo.py          # 策略/价值网络
│   └── reward.py       # 奖励计算
├── coding_engine/     # 代码分析与生成
│   ├── analyzer.py     # 语法分析
│   ├── quality.py      # 代码质量检查
│   ├── patterns.py     # 设计模式库
│   └── algorithms.py   # 算法实现
├── network/           # 分布式通信
│   └── communication.py  # 服务网格、负载均衡
├── mcp_tools/        # MCP 工具框架
│   ├── framework.py    # 工具编排
│   ├── tools.py       # 内置工具
│   └── mcu_tools.py   # MCU 代码生成
└── special/          # 专业模块
    └── modules.py     # 动画、游戏、模拟等
```

### ⚡ 性能优化

| 优化项 | 技术 |
|--------|------|
| **计算效率** | 向量化操作、async/await 模式 |
| **步骤简化** | 并行执行、缓存 |
| **文本压缩** | Token 优化、结构化输出 |
| **质量提升** | RL 反馈循环 |

---

## ✨ 仓库内容概览

| 类型 | 数量 | 说明 |
|------|------|------|
| **Prompts** | 132+ | 可直接使用的提示词，覆盖编程、调试、规划、研究等场景 |
| **Skills** | 14 | AI 能力定义，用于任务路由和执行 |
| **Workflows** | 10 | 多步骤执行流程，用于复杂任务 |
| **Tool-Use 指南** | 8 | 文件读取、命令执行等工具的系统化使用指南 |
| **Output 格式** | 6 | JSON、YAML、Markdown、表格、检查清单、报告 |
| **Meta Prompts** | 8 | Prompt 工程工具，用于优化和调试 |

---

## 🚀 快速开始

### 人类用户

```
1. 根据任务类型找到对应目录
2. 选择适合你需求的 prompt
3. 复制粘贴到你的 AI 工具中使用
```

**我想要 AI 帮我……**

| 任务 | 去哪里 |
|------|--------|
| 生成或修改代码 | [prompts/task/coding/](prompts/task/coding/) |
| 调试和修复 Bug | [prompts/task/debugging/](prompts/task/debugging/) |
| 理解代码仓库 | [prompts/task/repo-analysis/](prompts/task/repo-analysis/) |
| 制定执行计划 | [prompts/task/planning/](prompts/task/planning/) |
| 做研究调研 | [prompts/task/research/](prompts/task/research/) |
| 执行多步骤工作流 | [prompts/workflow/](prompts/workflow/) |
| 输出特定格式 | [prompts/output/](prompts/output/) |
| 优化 Prompt | [prompts/meta/](prompts/meta/) |

---

### AI 系统

AI 应按以下顺序读取文件：

```
1. START-HERE.md            → 入口点
2. ARCHITECTURE.md          → 了解设计理念
3. ASSET-MAP.md             → 查看完整资产清单
4. INDEX.md                 → 了解整体结构
5. registry/prompts-registry.yaml → 发现可用 prompts
6. registry/routes-registry.yaml  → 学习任务到资产的路由
7. AI-USAGE.md              → 了解使用模式
8. AI-ROUTING.md            → 了解路由逻辑
9. AI-BOOTSTRAP.md          → 首次使用引导
```

---

## 📁 目录结构

```
skill/
│
├── 🎯 入口文档
├── START-HERE.md              ← 起点（人类与AI）
├── ARCHITECTURE.md            ← 设计理念
├── ASSET-MAP.md               ← 完整资产清单
├── DECISION-LOG.md            ← 关键决策与理由
├── EXTENSION-GUIDE.md         ← 如何添加新资产
├── MAINTENANCE-RULES.md       ← 标准与约定
├── QUALITY-STANDARDS.md       ← 质量要求
│
├── 📖 核心入口
├── README.md                   ← 英文版
├── README.zh-CN.md            ← 中文版（你在这里）
├── INDEX.md                   ← 主索引
│
├── 💬 提示词
├── prompts/
│   ├── _routing/              ← AI 路由提示词
│   ├── _core/                 ← 标准与规范
│   ├── system/                ← 系统提示词
│   ├── task/                   │ ← 任务特定
│   │   ├── coding/            │    20+ prompts
│   │   ├── debugging/         │    20+ prompts
│   │   ├── repo-analysis/     │    10+ prompts
│   │   ├── planning/          │    2 prompts
│   │   ├── research/          │    1 prompt
│   │   ├── refactoring/       │    8 prompts
│   │   ├── testing/           │    8 prompts
│   │   ├── engineering-planning/│  8 prompts
│   │   ├── documentation-for-code/│ 6 prompts
│   │   └── code-review/       │    8 prompts
│   ├── general/                │ ← 通用能力
│   │   ├── clarification/     │    8 prompts
│   │   ├── context-memory/    │    8 prompts
│   │   ├── reasoning/         │    7 prompts
│   │   ├── search/            │    7 prompts
│   │   ├── user-style-adaptation/│ 8 prompts
│   │   ├── long-term-assistant/│  8 prompts
│   │   ├── creative-special/  │   10 prompts
│   │   ├── personal/          │    6 prompts
│   │   ├── reflection/        │    6 prompts
│   │   └── learning-support/  │    8 prompts
│   ├── workflow/               │ ← 10个工作流
│   ├── tool-use/               │ ← 8个工具指南
│   ├── output/                  │ ← 6个输出格式
│   └── meta/                   │ ← 8个元提示词
│
├── 🎯 技能
├── skills/                     ← 标准技能目录
│   ├── ai-routing/
│   ├── routing/
│   ├── coding/
│   ├── debugging/
│   ├── planning/
│   ├── repo-analysis/
│   ├── research/
│   ├── tool-use/
│   ├── prompt-composition/
│   ├── system-prompts/
│   ├── workflows/
│   ├── writing/
│   ├── data-visualization/
│   ├── devops/
│   ├── mcu/
│   ├── security/
│   ├── learning-support/
│   ├── reflection/
│   ├── personal/
│   └── creative-special/
│
├── 🔧 源代码（技术实现）
├── src/
│   ├── context_memory/        # 记忆系统
│   ├── rl_engine/             # RL框架
│   ├── coding_engine/         # 代码分析
│   ├── network/               # 通信模块
│   ├── mcp_tools/             # MCP框架
│   └── special/               # 专业模块
│
├── 📚 注册表（AI可读）
├── registry/
│   ├── prompts-registry.yaml   ← 所有提示词元数据
│   ├── skills-registry.yaml    ← 所有技能元数据
│   ├── routes-registry.yaml    ← 任务路由规则
│   ├── relations-registry.yaml ← 资产关系
│   └── tags-registry.yaml     ← 统一标签字典
│
├── 📎 示例与精选
├── examples/                   ← 实际使用示例
│   ├── coding/
│   ├── debugging/
│   ├── general/
│   └── creative-special/
│
├── author-picks/               ← 维护者推荐
│
├── 📚 文档
├── docs/guides/
│   ├── SPEC.md                ← 完整规范
│   └── templates/             ← 资产模板
│
├── 🤖 AI 指南
├── AI-USAGE.md                 ← 使用模式
├── AI-ROUTING.md               ← 路由逻辑
├── AI-BOOTSTRAP.md             ← 引导指南
│
└── 📄 项目文档
├── CHANGELOG.md               ← 版本历史
├── PROJECT-PLAN.md            ← 路线图
├── CONTRIBUTING.md            ← 贡献指南
├── CODE_OF_CONDUCT.md         ← 社区准则
├── SECURITY.md                ← 安全政策
└── LICENSE*                   ← 许可协议
```

---

## 🧪 测试与质量保证

### 测试覆盖

| 模块 | 测试数 | 状态 |
|------|--------|------|
| context_memory | 15+ | ✅ 通过 |
| rl_engine | 20+ | ✅ 通过 |
| coding_engine | 25+ | ✅ 通过 |
| network | 15+ | ✅ 通过 |
| mcp_tools | 20+ | ✅ 通过 |
| special | 26+ | ✅ 通过 |
| **总计** | **156** | **✅ 全部通过** |

### 运行测试

```bash
# 设置 PYTHONPATH 并运行所有测试
export PYTHONPATH=src
pytest tests/ -v

# 运行特定模块测试
pytest tests/test_context_memory.py -v
pytest tests/test_rl_engine.py -v
pytest tests/test_coding_engine.py -v
```

---

## 🔀 路由工作原理

```
1. AI 解析用户请求
       ↓
2. 与 routes-registry.yaml 中的 trigger_patterns 匹配
       ↓
3. 选择推荐的主 prompt + 支持性 prompts
       ↓
4. 检查 relations-registry.yaml 中的相关资产
       ↓
5. 按顺序执行选定的 prompts
```

---

## 🎯 核心任务覆盖

| 任务 | 主 Prompt | 支持 Prompt |
|------|-----------|-------------|
| **编程** | generate-code-from-requirement | read-files, output-markdown |
| **调试** | identify-root-cause | generate-plan, fix-bug, verify |
| **仓库分析** | analyze-repository-structure | read-files, summarize-arch |
| **规划** | break-down-task | create-execution-plan, output-checklist |
| **研究** | prepare-research-brief | output-markdown-report |
| **Prompt工程** | debug-failing-prompt | shorten, evaluate, adapt |

---

## 🔒 双许可证模式

| 许可证 | 适用于 |
|--------|--------|
| **Apache-2.0** | 代码、脚本、配置（`.trae/skills/`、配置） |
| **CC BY 4.0** | 内容资产（prompts、workflows、skills、文档） |

> ℹ️ 可自由使用 Apache-2.0 内容。使用 CC BY 4.0 内容请注明出处。

---

## 🤝 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

---

## 📌 版本信息

| 项目 | 值 |
|------|-----|
| **当前版本** | **v2.0.0** |
| **发布日期** | 2026-03-22 |

v2.0.0 主要更新：
- 支持语义搜索的上下文记忆系统
- 强化学习引擎集成
- 带 MCU 支持的 MCP 工具框架
- 专业模块（动画、游戏、模拟）
- 学术与创意工具套件

详见 [CHANGELOG.md](CHANGELOG.md)。

---

## 🔗 快速参考

| 需要 | 去哪里 |
|------|--------|
| 全局索引 | [INDEX.md](INDEX.md) |
| 提示词索引 | [prompts/INDEX.md](prompts/INDEX.md) |
| AI 使用 | [AI-USAGE.md](AI-USAGE.md) |
| AI 路由 | [AI-ROUTING.md](AI-ROUTING.md) |
| 技术文档 | [docs/ARCHITECTURE-DETAILED.md](docs/ARCHITECTURE-DETAILED.md) |
