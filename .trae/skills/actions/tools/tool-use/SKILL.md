---
name: tool-use
description: "Guides AI to use tools safely and effectively for file reading, command execution, and result combination. Keywords: tool, read, command, combine, safe"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - debugging-workflow
  - all-workflows
capabilities:
  - file_reading
  - command_execution
  - result_combination
  - safe_operations
---

# Tool Use

确保AI安全有效地使用工具。

## 适用场景

- 读取多个文件获取信息
- 执行命令验证结果
- 组合多个工具结果
- 操作前检查配置文件

## 工具使用原则

### 1. 先读后改

修改前总是读取相关文件：
- 理解当前代码结构
- 检查现有实现
- 验证项目约定

### 2. 安全执行命令

执行命令时：
- 优先只读操作
- 验证破坏性命令
- 检查命令白名单

### 3. 组合结果

使用多个工具时：
- 逻辑聚合信息
- 交叉验证一致性
- 综合得出结论

## 安全指南

1. **先读取**: 修改前理解上下文
2. **验证命令**: 检查破坏性操作
3. **检查路径**: 确保文件路径正确
4. **验证输出**: 确认工具结果合理

## 常用模式

### 批量读取

```
1. 确定需要读取的文件列表
2. 并行读取所有文件
3. 合并和分析结果
4. 得出结论
```

### 安全命令执行

```
1. 检查命令是否在白名单
2. 确认参数正确性
3. 执行命令
4. 验证输出
```

## 相关技能

- [tool-use-read-files-first](../tools/read-files-first) - 先读文件
- [tool-use-step-by-step](../tools/step-by-step) - 逐步执行
- [tool-use-combine-multiple-results](../tools/combine-results) - 组合结果
