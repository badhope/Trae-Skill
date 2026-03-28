---
name: git-operations
description: "Git operations expert for branch management, merge conflicts, commit conventions, and repository maintenance. Keywords: git, branch, merge, commit, rebase, cherry-pick"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - all-workflows
capabilities:
  - branch_management
  - conflict_resolution
  - commit_conventions
  - rebase_operations
  - repository_maintenance
---

# Git Operations

Git版本控制操作专家。

## 适用场景

- 管理Git分支和合并策略
- 解决复杂合并冲突
- 实现提交规范
- 执行cherry-pick、rebase操作
- 仓库清理和维护

## 分支命名规范

```
feature/<ticket-id>-<description>
fix/<ticket-id>-<description>
hotfix/<ticket-id>-<description>
release/<version>
```

## 提交规范

```
<type>(<scope>): <subject>

类型:
- feat: 新功能
- fix: Bug修复
- docs: 文档
- style: 代码风格
- refactor: 重构
- test: 测试
- chore: 维护
```

## 常用操作

### 交互式Rebase

```bash
git rebase -i HEAD~3
# pick, reword, squash, drop
```

### 解决冲突

```bash
git status
# 编辑冲突文件
git add <resolved-file>
git commit
```

### Cherry-Pick

```bash
git cherry-pick <commit-hash>
git cherry-pick <start>..<end>
```

## 仓库维护

```bash
git clean -fd           # 清理未跟踪文件
git branch -d <branch>  # 删除已合并分支
git fetch --prune       # 清理远程引用
git gc --aggressive     # 垃圾回收
```

## 相关技能

- [ci-cd-pipeline](../../domains/devops/ci-cd-pipeline) - CI/CD流水线
- [code-review](../code/code-review) - 代码审查
