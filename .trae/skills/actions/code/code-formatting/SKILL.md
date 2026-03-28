---
name: code-formatting
description: "Code formatting expert for Prettier, Black, ESLint, and multi-language style enforcement. Keywords: prettier, black, format, style, eslint, lint"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
capabilities:
  - formatter_setup
  - style_configuration
  - pre_commit_hooks
  - ci_integration
---

# Code Formatting

代码格式化配置专家。

## 适用场景

- 设置代码格式化工具
- 配置Lint规则
- 创建风格指南
- 强制代码规范
- CI/CD集成

## Prettier配置

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

## ESLint配置

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    'prettier'
  ],
  rules: {
    'no-console': 'warn',
    '@typescript-eslint/no-unused-vars': 'error'
  }
};
```

## Python (Black + Ruff)

```toml
[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "W"]
```

## Pre-commit Hooks

```json
{
  "lint-staged": {
    "*.{js,ts}": ["eslint --fix", "prettier --write"],
    "*.py": ["black", "ruff check --fix"]
  }
}
```

## 相关技能

- [linting-config](../code/linting-config) - Lint配置
- [ci-cd-pipeline](../../domains/devops/ci-cd-pipeline) - CI/CD
