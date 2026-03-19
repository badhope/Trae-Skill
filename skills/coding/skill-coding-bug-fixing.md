---
id: skill-coding-bug-fixing-v1
name: Bug Fixing
summary: 快速定位 bug 原因并提供修复方案
type: skill
category: coding
tags: [coding, debug, bug, fix]
keywords: [bug修复, 调试, debug]
intent: 帮助开发者快速解决代码中的 bug
use_cases:
  - 代码出现错误时
  - 测试失败时
  - 收到 bug 报告时
inputs:
  - name: bug_description
    type: string
    required: true
    description: Bug 描述
  - name: code_snippet
    type: string
    required: true
    description: 相关代码
  - name: error_message
    type: string
    required: false
    description: 错误信息
  - name: environment
    type: string
    required: false
    description: 环境信息
outputs:
  - name: root_cause
    type: string
    description: 根本原因分析
  - name: fix_solution
    type: string
    description: 修复方案
  - name: test_plan
    type: string
    description: 测试计划
prerequisites:
  - 相关代码片段
steps:
  - step: 1
    action: 理解 bug 的表现和预期行为
  - step: 2
    action: 分析错误信息和代码逻辑
  - step: 3
    action: 定位根本原因
  - step: 4
    action: 设计修复方案
  - step: 5
    action: 提供修复代码和测试计划
examples:
  - input: "bug: 函数返回NaN, code: function divide(a,b){return a/b}"
    output: "Root cause: 除以0, Fix: 添加参数检查"
    notes: 简单除法函数示例
related_skills:
  - skill-coding-code-review
  - skill-coding-test-generation
related_prompts:
  - prompt-task-coding-debug
notes: |
  - 优先提供最小复现步骤
  - 包含完整的错误信息有助于更快定位
created: 2026-03-19
updated: 2026-03-19
version: 1.0.0
deprecated: false
---

# Bug Fixing Skill

## 概述

帮助开发者快速定位和修复代码中的 bug。

## 使用方法

1. 提供 bug 描述
2. 提供相关代码片段
3. (可选) 提供错误信息
4. AI 将分析原因并提供修复方案

## 修复流程

1. **复现问题** → 理解 bug 表现
2. **分析原因** → 找到根本原因
3. **设计方案** → 制定修复策略
4. **实施修复** → 提供修复代码
5. **验证测试** → 制定测试计划
