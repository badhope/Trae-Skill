---
id: skill-coding-code-review-v1
name: Code Review
summary: 对代码进行全面的质量审查和建议
type: skill
category: coding
tags: [coding, review, code, quality]
keywords: [代码审查, 代码质量, code review]
intent: 提高代码质量，发现潜在问题
use_cases:
  - 提交代码前审查
  - Code review 同事的代码
  - 学习他人代码
inputs:
  - name: code
    type: string
    required: true
    description: 要审查的代码
  - name: language
    type: string
    required: false
    description: 编程语言
  - name: focus_area
    type: string
    required: false
    description: 重点审查领域 (quality/security/performance)
outputs:
  - name: review_report
    type: markdown
    description: 结构化的审查报告
  - name: quality_score
    type: number
    description: 质量评分 (1-10)
  - name: suggestions
    type: array
    description: 改进建议列表
prerequisites:
  - 代码片段
steps:
  - step: 1
    action: 理解代码功能和结构
  - step: 2
    action: 检查代码质量和可读性
  - step: 3
    action: 检查潜在 bug 和安全问题
  - step: 4
    action: 检查性能问题
  - step: 5
    action: 输出结构化报告
examples:
  - input: "code: function add(a,b){return a+b}, language: javascript"
    output: "Quality: 7/10, Issues: 缺少参数验证"
    notes: 简单函数示例
related_skills:
  - skill-coding-bug-fixing
  - skill-coding-test-generation
  - skill-coding-refactoring
related_prompts:
  - prompt-task-coding-code-review
notes: |
  - 适用于任何编程语言
  - 可以指定重点审查领域
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Code Review Skill

## 概述

对代码进行全面审查，提供质量评分和改进建议。

## 使用方法

1. 提供要审查的代码
2. (可选) 指定编程语言
3. (可选) 指定重点审查领域
4. AI 将返回结构化的审查报告

## 审查维度

1. **代码质量**: 可读性、可维护性、命名规范
2. **Bug 风险**: 潜在错误、边界条件、异常处理
3. **安全问题**: 注入攻击、敏感信息、权限控制
4. **性能**: 时间复杂度、不必要的循环、内存使用
5. **最佳实践**: 设计模式、语言特性、编码规范
