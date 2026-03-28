---
name: test-generator
description: "Generates comprehensive test cases and suites for existing code with multiple framework support. Keywords: test, unit, integration, jest, pytest, coverage"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - testing-workflow
capabilities:
  - unit_test_generation
  - integration_test_generation
  - test_coverage_analysis
  - mock_creation
---

# Test Generator

为现有代码生成全面的测试用例和测试套件。

## 适用场景

- 为现有代码创建测试
- 提高测试覆盖率
- 为新功能编写测试
- 生成测试数据
- 创建回归测试

## 支持的测试框架

### JavaScript/TypeScript

| 框架 | 用途 | 文件模式 |
|------|------|----------|
| Jest | 单元、集成 | *.test.ts |
| Vitest | 单元、Vite项目 | *.test.ts |
| Cypress | E2E | *.cy.ts |
| Playwright | E2E | *.spec.ts |

### Python

| 框架 | 用途 | 文件模式 |
|------|------|----------|
| pytest | 单元、集成 | test_*.py |
| unittest | 单元、标准 | test_*.py |

### 其他语言

| 语言 | 框架 | 文件模式 |
|------|------|----------|
| Go | testing | *_test.go |
| Rust | built-in | tests/*.rs |
| Java | JUnit 5 | *Test.java |

## 测试用例生成

### 正常路径测试

```typescript
describe('getUser', () => {
  it('should return user for valid id', async () => {
    const user = await getUser('user-123');
    expect(user).toBeDefined();
    expect(user.id).toBe('user-123');
  });
});
```

### 边缘情况测试

```typescript
describe('validateEmail', () => {
  it('should return false for empty string', () => {
    expect(validateEmail('')).toBe(false);
  });

  it('should handle unicode in email', () => {
    expect(validateEmail('用户@例え.com')).toBe(true);
  });
});
```

### 错误处理测试

```typescript
describe('fetchUser', () => {
  it('should throw NotFoundError for non-existent user', async () => {
    await expect(fetchUser('non-existent'))
      .rejects
      .toThrow(NotFoundError);
  });
});
```

## 测试结构模板

### Jest/TypeScript

```typescript
import { functionToTest } from '../module';

describe('functionToTest', () => {
  describe('happy path', () => {
    it('should return expected result', () => {
      expect(functionToTest('input')).toBe('expected');
    });
  });

  describe('edge cases', () => {
    it('should handle empty input', () => {
      expect(functionToTest('')).toBe('');
    });
  });

  describe('error handling', () => {
    it('should throw for invalid input', () => {
      expect(() => functionToTest(null)).toThrow();
    });
  });
});
```

### pytest/Python

```python
import pytest
from module import function_to_test

class TestFunctionToTest:
    def test_happy_path(self):
        assert function_to_test('input') == 'expected'

    def test_empty_input(self):
        assert function_to_test('') == ''

    def test_invalid_input_raises(self):
        with pytest.raises(ValueError):
            function_to_test(None)
```

## 测试数据生成

### Fixtures

```typescript
export const mockUser = {
  id: 'user-123',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date('2024-01-01'),
};

export const mockUsers = Array.from({ length: 10 }, (_, i) => ({
  id: `user-${i}`,
  email: `user${i}@example.com`,
  name: `User ${i}`,
}));
```

### Mocks

```typescript
export const mockUserService = {
  getById: jest.fn().mockResolvedValue(mockUser),
  create: jest.fn().mockResolvedValue(mockUser),
  delete: jest.fn().mockResolvedValue(true),
};
```

## 覆盖率分析

| 类型 | 描述 | 目标 |
|------|------|------|
| Line | 执行的行 | 80%+ |
| Branch | 覆盖的分支 | 70%+ |
| Function | 调用的函数 | 90%+ |

```bash
# 生成覆盖率报告
npm test -- --coverage
```

## 相关技能

- [code-generator](../code/code-generator) - 代码生成
- [code-reviewer](../code/code-reviewer) - 代码审查
- [debugging-workflow](../../workflows/debugging-workflow) - 调试工作流
