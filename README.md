# 📁 Folder as Agent - 懒人智能体工具

**English** | [简体中文](#简体中文)

---

## 🌟 简介

一个简单实用的工具，让您可以用文件夹和Markdown定义智能体工作流程，直接丢给豆包、Claude、Cursor等AI平台使用。

**懒人专属，开箱即用！** ✨

### 核心优势
- 📁 **文件夹即智能体**: 用简单的文件夹结构定义完整智能体
- 📝 **Markdown配置**: 无需编程，用Markdown/YAML配置工作流
- 🚀 **拖放即用**: 直接把文件夹拖给AI平台就能用
- 🔧 **预设工作流**: 内置16个常用工作流，覆盖开发全流程
- 🌍 **多平台兼容**: 支持豆包、Claude、Cursor、Windsurf等

---

## 🚀 快速开始（3步搞定！）

### 第一步：下载模板
```bash
git clone https://github.com/badhope/skills.git
cd skills/example-agents/full-stack-assistant
```

### 第二步：直接使用
- **方式1**: 把 `full-stack-assistant/` 文件夹拖到您的AI平台
- **方式2**: 复制整个文件夹到您的项目中

### 第三步：开始工作
用自然语言描述需求即可：
```
"创建一个React Todo应用"
"修复登录页面的Bug"
"审查我的代码质量"
```

---

## 📂 智能体结构

一个智能体就是一个文件夹：

```
full-stack-assistant/
├── agent.yaml          # 智能体配置（能力、工具、执行参数）
├── system-prompt.md    # 智能体角色定义
├── workflow/           # 工作流定义
│   ├── intent.yaml     # 意图识别规则
│   ├── stages.yaml     # 工作流程阶段
│   └── tools.yaml      # 可用工具列表
├── knowledge/          # 领域知识库
└── tests/              # 测试用例
```

---

## 📋 内置工作流

| 工作流 | 描述 | 适用场景 |
|--------|------|----------|
| `new-project` | 新项目创建 | 从头创建应用 |
| `feature-implementation` | 功能实现 | 开发新功能 |
| `bug-fixing` | Bug修复 | 定位并修复问题 |
| `code-review` | 代码审查 | 代码质量检查 |
| `technical-design` | 技术设计 | 架构设计文档 |
| `deployment` | 部署流程 | 应用部署 |
| `security-audit` | 安全审计 | 安全漏洞扫描 |

---

## 🎯 使用示例

### 示例1：创建项目
```
输入: "创建一个React Todo应用，使用TypeScript"

智能体自动:
1. 识别意图 → new-project
2. 执行工作流 → full-project-workflow
3. 输出: 完整项目结构
```

### 示例2：修复Bug
```
输入: "修复提交空表单时的错误"

智能体自动:
1. 识别意图 → bug-fixing
2. 执行工作流 → bug-fix-workflow
3. 输出: 根因分析 + 修复方案
```

---

## 🔌 平台支持

| 平台 | 使用方式 |
|------|----------|
| 🫘 **豆包** | 直接上传文件夹 |
| 🤖 **Claude Desktop** | 添加文件夹路径 |
| ✨ **Cursor** | `@load ./folder` |
| 🌊 **Windsurf** | 添加工作区目录 |
| 🚀 **Trae** | 添加项目目录 |

---

## 🛠️ 自定义智能体

不需要编程，只需修改配置文件：

1. **修改能力**: 编辑 `agent.yaml`
2. **定义流程**: 编辑 `workflow/stages.yaml`
3. **添加知识**: 在 `knowledge/` 放入文档
4. **测试验证**: 在 `tests/` 添加测试用例

---

## 📊 项目统计

| 项目 | 数量 |
|------|------|
| 内置工作流 | 16个 |
| 核心技能 | 7个 |
| 预设工具 | 50+ |
| 示例智能体 | 1个 |

---

## 📄 许可证
MIT License

---

---

# 简体中文

## 🌟 简介

一个简单实用的工具，让您可以用文件夹和Markdown定义智能体工作流程，直接丢给豆包、Claude、Cursor等AI平台使用。

**懒人专属，开箱即用！** ✨

### 核心优势
- 📁 **文件夹即智能体**: 用简单的文件夹结构定义完整智能体
- 📝 **Markdown配置**: 无需编程，用Markdown/YAML配置工作流
- 🚀 **拖放即用**: 直接把文件夹拖给AI平台就能用
- 🔧 **预设工作流**: 内置16个常用工作流，覆盖开发全流程
- 🌍 **多平台兼容**: 支持豆包、Claude、Cursor、Windsurf等

---

## 🚀 快速开始（3步搞定！）

### 第一步：下载模板
```bash
git clone https://github.com/badhope/skills.git
cd skills/example-agents/full-stack-assistant
```

### 第二步：直接使用
- **方式1**: 把 `full-stack-assistant/` 文件夹拖到您的AI平台
- **方式2**: 复制整个文件夹到您的项目中

### 第三步：开始工作
用自然语言描述需求即可：
```
"创建一个React Todo应用"
"修复登录页面的Bug"
"审查我的代码质量"
```

---

## 📂 智能体结构

一个智能体就是一个文件夹：

```
full-stack-assistant/
├── agent.yaml          # 智能体配置（能力、工具、执行参数）
├── system-prompt.md    # 智能体角色定义
├── workflow/           # 工作流定义
│   ├── intent.yaml     # 意图识别规则
│   ├── stages.yaml     # 工作流程阶段
│   └── tools.yaml      # 可用工具列表
├── knowledge/          # 领域知识库
└── tests/              # 测试用例
```

---

## 📋 内置工作流

| 工作流 | 描述 | 适用场景 |
|--------|------|----------|
| `new-project` | 新项目创建 | 从头创建应用 |
| `feature-implementation` | 功能实现 | 开发新功能 |
| `bug-fixing` | Bug修复 | 定位并修复问题 |
| `code-review` | 代码审查 | 代码质量检查 |
| `technical-design` | 技术设计 | 架构设计文档 |
| `deployment` | 部署流程 | 应用部署 |
| `security-audit` | 安全审计 | 安全漏洞扫描 |

---

## 🎯 使用示例

### 示例1：创建项目
```
输入: "创建一个React Todo应用，使用TypeScript"

智能体自动:
1. 识别意图 → new-project
2. 执行工作流 → full-project-workflow
3. 输出: 完整项目结构
```

### 示例2：修复Bug
```
输入: "修复提交空表单时的错误"

智能体自动:
1. 识别意图 → bug-fixing
2. 执行工作流 → bug-fix-workflow
3. 输出: 根因分析 + 修复方案
```

---

## 🔌 平台支持

| 平台 | 使用方式 |
|------|----------|
| 🫘 **豆包** | 直接上传文件夹 |
| 🤖 **Claude Desktop** | 添加文件夹路径 |
| ✨ **Cursor** | `@load ./folder` |
| 🌊 **Windsurf** | 添加工作区目录 |
| 🚀 **Trae** | 添加项目目录 |

---

## 🛠️ 自定义智能体

不需要编程，只需修改配置文件：

1. **修改能力**: 编辑 `agent.yaml`
2. **定义流程**: 编辑 `workflow/stages.yaml`
3. **添加知识**: 在 `knowledge/` 放入文档
4. **测试验证**: 在 `tests/` 添加测试用例

---

## 📊 项目统计

| 项目 | 数量 |
|------|------|
| 内置工作流 | 16个 |
| 核心技能 | 7个 |
| 预设工具 | 50+ |
| 示例智能体 | 1个 |

---

## 📄 许可证
MIT License

---

**懒人专属，轻松使用！** 🚀
