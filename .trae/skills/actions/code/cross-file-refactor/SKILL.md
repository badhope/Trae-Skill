---
name: cross-file-refactor
description: "Safely refactors code across multiple files while maintaining consistency. Keywords: refactor, rename, move, restructure, import"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
capabilities:
  - symbol_renaming
  - code_moving
  - import_updating
  - module_extraction
---

# Cross-File Refactor

跨文件安全重构专家。

## 适用场景

- 重命名函数/类/变量
- 在文件间移动代码
- 提取模块
- 更新导入路径
- 修改类型定义

## 重构类型

| 操作 | 影响文件 | 风险 |
|------|----------|------|
| 局部变量重命名 | 1 | 低 |
| 函数重命名 | 多个 | 中 |
| 类重命名 | 多个 | 中 |
| 模块重命名 | 很多 | 高 |

## 工作流程

```
1. 分析范围 - 找到所有引用
2. 制定计划 - 确定变更顺序
3. 执行重构 - 更新定义和引用
4. 验证结果 - 运行测试和类型检查
```

## 安全检查

```
重构前:
- [ ] 所有测试通过
- [ ] 无类型错误
- [ ] Git状态干净
- [ ] 创建备份/分支

重构后:
- [ ] 所有测试通过
- [ ] 无类型错误
- [ ] 无Lint错误
- [ ] 构建成功
```

## 相关技能

- [code-generator](../code/code-generator) - 代码生成
- [code-search-navigator](../tools/code-search-navigator) - 代码搜索
