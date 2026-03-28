---
name: code-coverage
description: "Test coverage analysis expert for coverage tools, reporting, and threshold configuration. Keywords: coverage, test, jest, pytest, lcov, threshold"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - testing-workflow
capabilities:
  - coverage_analysis
  - threshold_configuration
  - report_generation
  - ci_integration
---

# Code Coverage

测试覆盖率分析专家。

## 适用场景

- 设置覆盖率工具
- 分析覆盖率报告
- 提高测试覆盖率
- 配置覆盖率阈值
- CI/CD覆盖率集成

## 覆盖率类型

| 类型 | 描述 | 目标 |
|------|------|------|
| Line | 执行的代码行 | 80%+ |
| Branch | 覆盖的分支 | 70%+ |
| Function | 调用的函数 | 90%+ |
| Statement | 执行的语句 | 80%+ |

## Jest配置

```javascript
// jest.config.js
module.exports = {
  coverageProvider: 'v8',
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80 }
  }
};
```

## pytest-cov

```bash
pytest --cov=src --cov-report=html --cov-fail-under=80
```

## Go覆盖率

```bash
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## CI集成

```yaml
- run: npm test -- --coverage
- uses: codecov/codecov-action@v3
  with:
    files: ./coverage/lcov.info
```

## 相关技能

- [test-generator](../test/test-generator) - 测试生成
- [ci-cd-pipeline](../../domains/devops/ci-cd-pipeline) - CI/CD流水线
