# Thesis Specialist - 论文专家智能体

[![版本](https://img.shields.io/badge/version-2.2.0-blue.svg)](README_zh.md)
[![平台](https://img.shields.io/badge/platform-Folder--as--Agent-green.svg)](README_zh.md)
[![许可证](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![CI状态](https://img.shields.io/github/actions/workflow/status/badhope/Thesis-Specialist-Agent/ci.yml?branch=main)](https://github.com/badhope/Thesis-Specialist-Agent/actions)

---

**🌐 语言:** [English](README.md) | [中文](README_zh.md)

---

## 目录

- [关于项目](#关于项目)
- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [使用示例](#使用示例)
- [技术架构](#技术架构)
- [项目结构](#项目结构)
- [开发指南](#开发指南)
- [许可证](#许可证)

---

## 关于项目

**Thesis Specialist** 是一个创新的 **"文件夹即智能体"（Folder-as-Agent）** 平台，专为学术论文写作而设计。整个平台可以下载后直接提交给任何大语言模型（LLM），如豆包、Claude、GPT或Gemini，立即使用。

### 核心概念

"文件夹即智能体"概念将整个文件夹转变为一个智能体。只需下载文件夹并提交给任何兼容的LLM，智能体会自动按照预定义的流程执行完整的论文写作工作流。

### 平台定位

本平台定位为专业学术写作助手，具备以下特点：
- **开箱即用**：无需配置，下载即可使用
- **完整流程**：严格遵循8阶段工作流程
- **多智能体协作**：协调多个专家完成复杂任务
- **质量保障**：包含验证和评审机制

---

## 功能特性

| 功能 | 描述 |
|------|------|
| 8阶段执行流程 | 从意图识别到最终输出的严格8阶段流程 |
| 8个专家引擎 | 主题、文献、结构、写作等专业化引擎 |
| 4个元智能体 | 协调、规划、评审、进度追踪 |
| 4个工具 | 文献检索、语法检查、数据可视化、格式转换 |
| 记忆系统 | 用户偏好、会话历史、项目状态、知识库 |
| 零配置 | 下载即用 |

---

## 快速开始

### 方法一：直接提交给LLM（推荐）

```
1. 下载此文件夹
2. 将整个文件夹提交给豆包、Claude、GPT或Gemini
3. 用自然语言描述您的论文需求
4. 智能体自动执行完整工作流程
```

### 方法二：参考文件

```
1. 阅读 agent.yaml 了解平台配置
2. 阅读 system-prompt.md 了解系统指令
3. 选择适合您任务的 SKILL.md
4. 使用具体需求提交给LLM
```

---

## 使用示例

### 示例一：主题选择

**输入：**
```
帮我找一个计算机视觉方向的硕士论文研究方向。
```

**输出：** 主题专家提供：
- 3-5个候选主题及详细分析
- 评分（创新性、可行性、研究价值）
- 推荐排名及理由
- 建议的后续步骤

### 示例二：文献综述

**输入：**
```
我需要帮助写一篇关于机器学习在医疗领域应用的文献综述。
```

**输出：** 文献专家提供：
- 多数据库检索策略
- 组织好的文献结构
- 关键发现总结
- 引用建议

### 示例三：论文规划

**输入：**
```
帮我规划一下论文写作的整体流程，我需要在3个月内完成。
```

**输出：** 任务规划专家提供：
- 任务分解为可管理的阶段
- 里程碑时间线
- 各阶段专家分配
- 进度跟踪检查点

---

## 技术架构

### 系统架构

Thesis Specialist 采用精密的8阶段执行流程：
1. 意图识别 → 2. 专家匹配 → 3. 任务规划 → 4. 专家执行
5. 工具调用 → 6. 结果整合 → 7. 质量检查 → 8. 最终输出

---

## 项目结构

```
thesis-specialist/
├── .github/workflows/ci.yml     # CI/CD 流水线
├── .gitignore                    # Git 忽略规则
├── LICENSE                       # MIT 许可证
├── README.md                     # 英文文档
├── README_zh.md                  # 中文文档
├── CONTRIBUTING.md               # 贡献指南
├── CODE_OF_CONDUCT.md            # 行为准则
├── SUPPORT.md                    # 支持信息
├── SECURITY.md                   # 安全政策
├── agent.yaml                    # 平台配置
├── system-prompt.md             # 系统提示词
├── config-validator.py           # 配置验证器
├── logger.py                    # 日志系统
├── skills/
│   ├── engines/                 # 8个专家引擎
│   └── meta/                    # 元智能体
├── tools/                       # 工具
├── memory/                      # 记忆系统
├── utils/                       # 工具函数
└── tests/                       # 测试
```

---

## 开发指南

### 环境要求

- Python 3.10+
- PyYAML

### 安装依赖

```bash
pip install pyyaml
```

### 运行测试

```bash
python -m unittest tests.test_agent -v
```

### 配置验证

```bash
python config-validator.py
```

---

## 许可证

本项目采用 MIT 许可证。

---

**版本**: 2.2.0  
**最后更新**: 2026-05-04  
**仓库地址**: https://github.com/badhope/Thesis-Specialist-Agent
