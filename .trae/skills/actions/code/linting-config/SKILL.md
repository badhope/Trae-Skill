---
name: linting-config
description: "Linting configuration expert for ESLint, Ruff, golangci-lint, and Clippy across languages. Keywords: lint, eslint, ruff, golangci-lint, clippy"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
capabilities:
  - linter_setup
  - rule_configuration
  - custom_rules
  - monorepo_config
---

# Linting Configuration

代码检查配置专家。

## 适用场景

- 设置Lint工具
- 配置自定义规则
- CI/CD集成
- 修复Lint错误
- 创建共享配置

## ESLint (TypeScript)

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
    '@typescript-eslint/no-unused-vars': 'error',
    'import/order': ['error', { alphabetize: { order: 'asc' } }]
  }
};
```

## Ruff (Python)

```toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "B", "W", "UP"]
ignore = ["E501"]
```

## golangci-lint

```yaml
linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
```

## 相关技能

- [code-formatting](../code/code-formatting) - 代码格式化
- [ci-cd-pipeline](../../domains/devops/ci-cd-pipeline) - CI/CD
