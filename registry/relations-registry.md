# Relations Registry

> 所有 Skills、Prompts、Workflows 之间的关联关系。

## 统计

- **总计**: 0 条关系
- **最后更新**: 2026-03-19

## 关系类型

### 1. Skill → Skill (技能组合)

| Source | Relation | Target | 说明 |
|--------|----------|--------|------|
| - | combines_with | - | - |
| - | requires | - | - |
| - | preceded_by | - | - |
| - | followed_by | - | - |

### 2. Skill → Prompt (技能驱动)

| Source | Relation | Target | 说明 |
|--------|----------|--------|------|
| - | uses_prompt | - | - |
| - | inspired_by | - | - |

### 3. Workflow → Skill/Prompt (工作流引用)

| Workflow | Used Skills | Used Prompts |
|----------|-------------|--------------|
| - | - | - |

## 常用组合路径

### 写作组合
```
writing/article-outline → writing/article-draft → writing/seo-optimize
```

### 编码组合
```
coding/code-generation → coding/code-review → coding/bug-fixing
```

### 研究组合
```
research/topic-analysis → research/deep-dive → research/report-write
```

## 添加新关系

1. 更新相关文件的 `related_skills` / `related_prompts` 字段
2. 在对应关系表中添加条目
3. 确保关系闭合（双向引用）
