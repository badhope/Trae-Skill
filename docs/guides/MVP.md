# MVP 搭建清单

## 第一批必须创建的目录

1. `skills/` - Skills 主目录
2. `prompts/` - Prompts 主目录
3. `workflows/` - Workflows 主目录
4. `registry/` - 注册表目录
5. `docs/guides/` - 规范文档目录

## 第一批必须写的文件

1. `README.md` - 仓库入口
2. `INDEX.md` - 全局索引
3. `docs/guides/SPEC.md` - 规范文档
4. `registry/skills-registry.md` - Skills 注册表
5. `registry/prompts-registry.md` - Prompts 注册表
6. `registry/workflows-registry.md` - Workflows 注册表
7. `docs/guides/skill-template.md` - Skill 模板
8. `docs/guides/prompt-template.md` - Prompt 模板
9. `docs/guides/workflow-template.md` - Workflow 模板

## 第一批最值得沉淀的 20 个核心 Skills

### Writing (写作类) - 4个
1. `skill-writing-article-draft` - 文章起草
2. `skill-writing-article-outline` - 文章大纲
3. `skill-writing-headline-generation` - 标题生成
4. `skill-writing-seo-optimize` - SEO 优化

### Coding (编程类) - 5个
5. `skill-coding-code-review` - 代码审查
6. `skill-coding-bug-fixing` - Bug 修复
7. `skill-coding-code-generation` - 代码生成
8. `skill-coding-refactoring` - 重构
9. `skill-coding-test-generation` - 测试生成

### Research (研究类) - 3个
10. `skill-research-topic-analysis` - 主题分析
11. `skill-research-deep-dive` - 深度研究
12. `skill-research-summarize` - 总结摘要

### Analysis (分析类) - 3个
13. `skill-analysis-data` - 数据分析
14. `skill-analysis-competitor` - 竞品分析
15. `skill-analysis-trend` - 趋势分析

### Productivity (效率类) - 3个
16. `skill-productivity-task-breakdown` - 任务拆解
17. `skill-productivity-time-management` - 时间管理
18. `skill-productivity-goal-setting` - 目标设定

### 其他 - 2个
19. `skill-design-ui-spec` - UI 设计规范
20. `skill-business-prd` - PRD 撰写

## 第一批最值得沉淀的 20 个核心 Prompts

### System Prompts - 3个
1. `prompt-system-ai-assistant` - AI 助手系统提示
2. `prompt-system-code-expert` - 代码专家系统提示
3. `prompt-system-writing-assistant` - 写作助手系统提示

### Role Prompts - 3个
4. `prompt-role-senior-developer` - 资深开发者角色
5. `prompt-role-technical-writer` - 技术写作角色
6. `prompt-role-business-analyst` - 商业分析角色

### Task Prompts - 10个
7. `prompt-task-coding-code-review` - 代码审查
8. `prompt-task-coding-debug` - 代码调试
9. `prompt-task-coding-generate-function` - 函数生成
10. `prompt-task-writing-article` - 文章写作
11. `prompt-task-writing-outline` - 大纲生成
12. `prompt-task-writing-summary` - 总结摘要
13. `prompt-task-research-deep-dive` - 深度研究
14. `prompt-task-analysis-data` - 数据分析
15. `prompt-task-analysis-competitor` - 竞品分析
16. `prompt-task-design-ui` - UI 设计

### Workflow Prompts - 2个
17. `prompt-workflow-bug-fix` - Bug 修复工作流
18. `prompt-workflow-feature-dev` - 功能开发工作流

### Meta Prompts - 2个
19. `prompt-meta-prompt优化` - Prompt 优化
20. `prompt-meta-skill-select` - Skill 选择

## 第一批最值得沉淀的 10 个 Workflows

1. `workflow-sequential-bug-fix` - Bug 修复工作流
2. `workflow-sequential-code-review` - 代码审查工作流
3. `workflow-multi-step-article-writing` - 文章写作工作流
4. `workflow-multi-step-feature-dev` - 功能开发工作流
5. `workflow-sequential-research-report` - 研究报告工作流
6. `workflow-conditional-content-review` - 内容审核工作流
7. `workflow-multi-step-prd-creation` - PRD 创建工作流
8. `workflow-sequential-test-automation` - 自动化测试工作流
9. `workflow-multi-step-data-analysis` - 数据分析工作流
10. `workflow-conditional-seo-optimization` - SEO 优化工作流

## 第一批建议完成的索引文件

1. `INDEX.md` - 全局索引（必须）
2. `registry/skills-registry.md` - Skills 注册表（必须）
3. `registry/prompts-registry.md` - Prompts 注册表（必须）
4. `registry/workflows-registry.md` - Workflows 注册表（必须）
5. `registry/tags-registry.md` - 标签注册表（建议）
6. `registry/relations-registry.md` - 关系注册表（建议）

## 实施优先级排序

### 第 1 周 - 基础设施
- [ ] 创建目录结构
- [ ] 完成 README.md 和 INDEX.md
- [ ] 完成 SPEC.md 规范文档
- [ ] 完成所有模板文件

### 第 2 周 - 核心 Skills (10个)
- [ ] 5 个 Coding Skills
- [ ] 3 个 Writing Skills
- [ ] 2 个 Research/Analysis Skills

### 第 3 周 - 核心 Prompts (10个)
- [ ] 3 个 System/Role Prompts
- [ ] 5 个 Task Prompts
- [ ] 2 个 Workflow Prompts

### 第 4 周 - Workflows 和 Registry
- [ ] 5 个核心 Workflows
- [ ] 完善所有 Registry 文件
- [ ] 建立索引和关联

### 后续 - 扩展完善
- [ ] 继续补充 Skills (达到 20 个)
- [ ] 继续补充 Prompts (达到 20 个)
- [ ] 继续补充 Workflows (达到 10 个)
- [ ] 添加 Templates
- [ ] 添加 Tools 说明
- [ ] 添加 Personal 内容
