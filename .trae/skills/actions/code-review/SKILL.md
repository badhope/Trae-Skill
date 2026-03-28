---
name: code-review
description: "Comprehensive code review for quality, security, and best practices. Keywords: review, code review, pull request, pr, 代码审查, 评审"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - debugging-workflow
  - aggregation-processor
capabilities:
  - quality_assessment
  - security_review
  - best_practice_check
  - suggestion_generation
triggers:
  keywords:
    - review
    - code review
    - pull request
    - pr review
    - check code
    - 代码审查
    - 评审
    - 检查代码
metrics:
  avg_execution_time: 3s
  success_rate: 0.92
  token_efficiency: 0.85
  issue_detection_rate: 0.88
---

# Code Review

全面的代码审查，评估代码质量、安全性和最佳实践遵循情况。

## 目的

为代码变更提供系统性审查：
- 识别代码质量问题
- 发现潜在安全漏洞
- 检查最佳实践遵循
- 提供改进建议

## 能力

- **质量评估**: 评估代码可读性、可维护性
- **安全审查**: 识别安全漏洞
- **最佳实践检查**: 检查编码规范遵循
- **建议生成**: 提供具体改进建议

## 审查维度

### 1. 代码质量

| 维度 | 检查项 |
|------|--------|
| 可读性 | 命名、注释、代码结构 |
| 可维护性 | 模块化、耦合度、复杂度 |
| 性能 | 算法效率、资源使用 |
| 测试 | 测试覆盖、测试质量 |

### 2. 安全审查

| 类别 | 检查项 |
|------|--------|
| 输入验证 | SQL注入、XSS、CSRF |
| 认证授权 | 密码处理、会话管理 |
| 敏感数据 | 加密、日志脱敏 |
| 依赖安全 | 已知漏洞、版本更新 |

### 3. 最佳实践

| 类别 | 检查项 |
|------|--------|
| 设计模式 | 模式使用是否恰当 |
| 错误处理 | 异常处理、错误传播 |
| 代码复用 | DRY原则、抽象层次 |
| 文档 | 注释、README、API文档 |

## 审查流程

```
输入: 代码变更 (diff)
输出: 审查报告

步骤:
1. 理解变更上下文
2. 检查代码质量
3. 执行安全审查
4. 验证最佳实践
5. 生成审查报告
```

## 审查模板

### 审查报告模板

```markdown
# 代码审查报告

## 概述
- 文件数: X
- 变更行数: +X/-Y
- 总体评分: A/B/C/D

## 发现的问题

### 严重 (Critical)
- [ ] 问题1: 描述
  - 位置: file:line
  - 建议: 具体修改建议

### 重要 (Major)
- [ ] 问题2: 描述

### 建议 (Minor)
- [ ] 建议1: 描述

## 优点
- 优点1
- 优点2

## 总结
[总体评价和建议]
```

## 审查检查清单

### 通用检查

```markdown
## 功能正确性
- [ ] 代码是否实现了预期功能
- [ ] 边界条件是否处理
- [ ] 错误情况是否处理

## 代码质量
- [ ] 命名是否清晰有意义
- [ ] 代码是否易于理解
- [ ] 是否有重复代码
- [ ] 函数/方法是否过长

## 安全性
- [ ] 输入是否验证
- [ ] 敏感数据是否保护
- [ ] 是否有潜在漏洞

## 性能
- [ ] 是否有不必要的循环
- [ ] 数据结构选择是否合理
- [ ] 是否有内存泄漏风险

## 测试
- [ ] 是否有足够的测试
- [ ] 测试是否覆盖边界情况
- [ ] 测试是否独立可重复
```

### 语言特定检查

```markdown
## Python
- [ ] 使用类型注解
- [ ] 遵循PEP 8
- [ ] 使用上下文管理器
- [ ] 避免可变默认参数

## JavaScript/TypeScript
- [ ] 使用const/let而非var
- [ ] 异步操作正确处理
- [ ] 类型定义完整
- [ ] 避免any类型

## Go
- [ ] 错误正确处理
- [ ] goroutine泄漏检查
- [ ] 使用context传递
- [ ] 接口定义合理
```

## 使用示例

### 示例: Pull Request审查

```
用户: "审查这个PR"

执行:
1. 获取PR diff
2. 分析变更范围
3. 执行质量检查
4. 执行安全检查
5. 生成审查报告

输出:
# 代码审查报告

## 发现的问题

### 严重
- [ ] SQL注入风险: user_input直接拼接到SQL
  - 位置: api.py:45
  - 建议: 使用参数化查询

### 重要
- [ ] 缺少错误处理
  - 位置: service.py:78
  - 建议: 添加try-except块

### 建议
- [ ] 函数过长(50行)
  - 位置: utils.py:100
  - 建议: 拆分为多个小函数
```

## 审查原则

1. **建设性**: 提供具体改进建议，而非单纯批评
2. **尊重**: 保持专业和礼貌的语气
3. **聚焦**: 关注重要问题，避免过度纠结细节
4. **上下文**: 考虑项目背景和约束

## 相关技能

- [linting-config](../code/linting-config) - Lint配置
- [security-auditor](../../domains/security/security-auditor) - 安全审计
- [test-generator](../test/test-generator) - 测试生成
