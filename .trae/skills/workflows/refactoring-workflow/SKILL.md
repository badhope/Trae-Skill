---
name: refactoring-workflow
description: "Systematic code refactoring workflow for improving code quality while preserving behavior. Keywords: refactor, restructure, improve, clean, 重构, 优化, 重构工作流"
layer: workflow
role: coordinator
version: 2.0.0
invokes:
  - code-search
  - cross-file-refactor
  - test-generator
  - code-coverage
  - aggregation-processor
invoked_by:
  - task-planner
  - orchestrator
  - decomposition-planner
capabilities:
  - smell_detection
  - refactoring_planning
  - safe_transformation
  - behavior_preservation
triggers:
  keywords:
    - refactor
    - restructure
    - improve code
    - clean code
    - technical debt
    - 重构
    - 优化代码
    - 技术债务
state_machine:
  states:
    - analysis
    - planning
    - transformation
    - verification
    - completion
  transitions:
    analysis -> planning: smells_identified
    planning -> transformation: plan_approved
    transformation -> verification: changes_made
    verification -> completion: tests_passing
metrics:
  avg_execution_time: 12m
  success_rate: 0.94
  token_efficiency: 0.85
  behavior_preservation_rate: 0.99
---

# Refactoring Workflow

系统性代码重构工作流，在保持行为的同时改善代码质量。

## 目的

为代码重构提供安全、系统化的流程：
- 识别代码异味和技术债务
- 制定安全的重构计划
- 执行重构并验证行为保持
- 确保测试覆盖率

## 能力

- **异味检测**: 识别代码异味和改进点
- **重构规划**: 制定安全的重构步骤
- **安全转换**: 执行重构变更
- **行为保持**: 确保功能不变

## 工作流程

### 阶段1: 分析 (Analysis)

```
输入: 目标代码
输出: 代码异味报告

步骤:
1. 扫描代码结构
2. 识别代码异味
3. 评估技术债务
4. 确定重构范围
5. 评估风险等级
```

### 阶段2: 规划 (Planning)

```
输入: 代码异味报告
输出: 重构计划

步骤:
1. 优先级排序
2. 分解重构步骤
3. 识别依赖关系
4. 规划测试策略
5. 评估影响范围
```

### 阶段3: 转换 (Transformation)

```
输入: 重构计划
输出: 重构后代码

步骤:
1. 确保测试覆盖
2. 小步重构
3. 每步验证
4. 更新相关代码
5. 保持提交原子性
```

### 阶段4: 验证 (Verification)

```
输入: 重构后代码
输出: 验证结果

步骤:
1. 运行所有测试
2. 检查行为一致性
3. 性能对比
4. 代码质量检查
5. 代码审查
```

### 阶段5: 完成 (Completion)

```
输入: 验证结果
输出: 重构报告

步骤:
1. 整理变更
2. 更新文档
3. 提交变更
4. 记录经验教训
5. 清理临时代码
```

## 重构技术

### 代码异味识别

| 异味类型 | 描述 | 重构方法 |
|----------|------|----------|
| 长方法 | 方法过长 | 提取方法 |
| 大类 | 类过大 | 提取类 |
| 重复代码 | 代码重复 | 提取方法/类 |
| 长参数列表 | 参数过多 | 引入参数对象 |
| 发散式变化 | 一个类多种变化 | 提取类 |
| 霰弹式修改 | 一个变化多个类 | 移动方法/字段 |
| 依恋情结 | 过度使用其他类数据 | 移动方法 |

### 重构模式

```markdown
## 提取方法 (Extract Method)

**何时使用**: 代码片段可以组合在一起并命名

**步骤**:
1. 创建新方法
2. 复制代码到新方法
3. 替换原代码为方法调用
4. 编译测试

## 移动方法 (Move Method)

**何时使用**: 方法更适合在另一个类中

**步骤**:
1. 在目标类创建方法
2. 复制方法体
3. 调整引用
4. 删除原方法
5. 编译测试
```

## 安全重构原则

1. **小步前进**: 每次只做一个小改动
2. **频繁测试**: 每步后运行测试
3. **版本控制**: 每个逻辑变更单独提交
4. **回滚准备**: 保持可回滚状态
5. **行为保持**: 不改变外部行为

## 使用示例

### 示例: 提取方法重构

```
用户: "重构这个长方法"

执行流程:
1. Analysis: 识别方法中的逻辑块
2. Planning: 确定提取顺序
3. Transformation: 逐步提取方法
4. Verification: 运行测试验证
5. Completion: 提交变更
```

## 重构检查清单

```markdown
## 重构前
- [ ] 有足够的测试覆盖
- [ ] 理解代码当前行为
- [ ] 识别重构范围
- [ ] 评估风险

## 重构中
- [ ] 小步变更
- [ ] 每步测试
- [ ] 保持代码可编译
- [ ] 频繁提交

## 重构后
- [ ] 所有测试通过
- [ ] 代码质量提升
- [ ] 行为保持不变
- [ ] 文档已更新
```

## 相关技能

- [cross-file-refactor](../../actions/code/cross-file-refactor) - 跨文件重构
- [test-generator](../../actions/test/test-generator) - 测试生成
- [code-coverage](../../actions/test/code-coverage) - 覆盖率分析
- [code-search](../../actions/search) - 代码搜索
