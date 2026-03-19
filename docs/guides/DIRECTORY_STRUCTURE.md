# 目录结构

## 简单版目录树 (MVP)

适合个人快速起步，核心结构最小化。

```
skill/
├── README.md              # 仓库入口 (必须)
├── INDEX.md               # 全局索引 (必须)
├── LICENSE                # 开源协议
│
├── skills/                # Skills 目录 (必须)
│   ├── writing/           # 写作类
│   ├── coding/            # 编程类
│   └── README.md
│
├── prompts/               # Prompts 目录 (必须)
│   ├── system/            # 系统提示
│   ├── task/              # 任务提示
│   └── README.md
│
├── workflows/             # Workflows 目录 (建议)
│   └── README.md
│
├── templates/             # 模板目录 (建议)
│   └── README.md
│
├── registry/              # 注册表 (必须)
│   ├── skills-registry.md
│   ├── prompts-registry.md
│   ├── workflows-registry.md
│   ├── tags-registry.md
│   └── relations-registry.md
│
└── docs/                  # 文档目录 (建议)
    └── guides/
        ├── SPEC.md
        ├── skill-template.md
        ├── prompt-template.md
        └── workflow-template.md
```

## 进阶版目录树

适合长期维护和开源协作。

```
skill/
├── README.md              # 仓库入口
├── INDEX.md               # 全局索引
├── LICENSE                # 开源协议
├── CONTRIBUTING.md        # 贡献指南
├── CHANGELOG.md           # 变更日志
│
├── skills/                # Skills 目录
│   ├── README.md
│   ├── writing/           # 写作类
│   │   ├── article-draft/
│   │   ├── article-outline/
│   │   ├── seo-optimize/
│   │   └── README.md
│   ├── coding/            # 编程类
│   │   ├── code-review/
│   │   ├── bug-fixing/
│   │   ├── code-generation/
│   │   ├── refactoring/
│   │   ├── test-generation/
│   │   └── README.md
│   ├── research/          # 研究类
│   ├── analysis/          # 分析类
│   ├── design/            # 设计类
│   ├── automation/        # 自动化类
│   ├── agent/             # Agent 类
│   ├── business/          # 商业类
│   ├── learning/          # 学习类
│   ├── productivity/      # 效率类
│   ├── media/             # 媒体类
│   └── personal/          # 个人类
│
├── prompts/               # Prompts 目录
│   ├── README.md
│   ├── system/            # 系统级提示
│   ├── role/              # 角色扮演提示
│   ├── task/              # 任务型提示
│   ├── workflow/          # 工作流提示
│   └── templates/         # Prompt 模板
│
├── workflows/             # Workflows 目录
│   ├── README.md
│   ├── multi-step/        # 多步骤工作流
│   ├── sequential/        # 顺序工作流
│   └── conditional/       # 条件工作流
│
├── templates/             # 模板目录
│   ├── README.md
│   ├── docs/              # 文档模板
│   │   ├── README-template.md
│   │   ├── PRD-template.md
│   │   └── ISSUE-template.md
│   ├── planning/          # 计划模板
│   │   ├── task-breakdown.md
│   │   └── project-plan.md
│   └── output/            # 输出格式模板
│
├── tools/                 # 工具说明
│   ├── README.md
│   ├── cli/               # CLI 工具
│   ├── api/               # API 工具
│   └── external/          # 外部工具集成
│
├── docs/                  # 文档
│   ├── README.md
│   ├── guides/            # 使用指南
│   │   ├── getting-started.md
│   │   ├── add-skill.md
│   │   ├── add-prompt.md
│   │   ├── add-workflow.md
│   │   └── SPEC.md
│   └── references/        # 参考资料
│
├── personal/             # 个人内容
│   ├── README.md
│   ├── knowledge/         # 知识库
│   ├── notes/             # 笔记
│   └── memory/            # 记忆
│
├── registry/              # 注册表
│   ├── skills-registry.md
│   ├── prompts-registry.md
│   ├── workflows-registry.md
│   ├── tags-registry.md
│   └── relations-registry.md
│
└── assets/                # 资源文件
    ├── images/
    └── data/
```

## 两者差异

| 特性 | 简单版 | 进阶版 |
|------|--------|--------|
| 目录深度 | 浅 | 深 |
| 子目录数 | 少 | 多 |
| 个人内容 | 无 | 完整 |
| 工具说明 | 无 | 完整 |
| 贡献指南 | 无 | 完整 |
| 维护成本 | 低 | 高 |
| 适合场景 | 个人 | 开源协作 |

## 建议

**个人维护者起步**：
- 先用简单版 MVP
- 按需逐步扩展
- 不要过度设计

**未来开源协作**：
- 提前规划好分类
- 预留扩展目录
- 完善 CONTRIBUTING.md
- 建立贡献流程
