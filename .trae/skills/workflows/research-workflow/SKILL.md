---
name: research-workflow
description: "Systematic research workflow for investigating topics, evaluating options, and producing findings. Keywords: research, investigate, analyze, explore, 研究, 调研, 分析"
layer: workflow
role: coordinator
version: 2.0.0
invokes:
  - code-search
  - documentation
  - web-search
  - aggregation-processor
invoked_by:
  - task-planner
  - orchestrator
  - decomposition-planner
capabilities:
  - topic_investigation
  - source_evaluation
  - finding_synthesis
  - recommendation_generation
triggers:
  keywords:
    - research
    - investigate
    - analyze
    - explore
    - study
    - evaluate
    - 研究
    - 调研
    - 分析
    - 探索
state_machine:
  states:
    - planning
    - gathering
    - analyzing
    - synthesizing
    - reporting
  transitions:
    planning -> gathering: sources_identified
    gathering -> analyzing: data_collected
    analyzing -> synthesizing: patterns_found
    synthesizing -> reporting: conclusions_drawn
metrics:
  avg_execution_time: 5m
  success_rate: 0.95
  token_efficiency: 0.88
  recommendation_quality: 0.90
---

# Research Workflow

系统性研究工作流，用于主题调研、选项评估和发现总结。

## 目的

为复杂研究任务提供结构化流程，确保：
- 全面覆盖研究主题
- 系统性信息收集
- 客观分析和评估
- 清晰的结论和建议

## 能力

- **主题调查**: 深入研究特定主题
- **来源评估**: 评估信息来源可靠性
- **发现综合**: 整合多源信息
- **建议生成**: 基于研究提供建议

## 工作流程

### 阶段1: 规划 (Planning)

```
输入: 研究主题/问题
输出: 研究计划

步骤:
1. 明确研究目标
2. 确定研究范围
3. 识别关键问题
4. 制定搜索策略
5. 设定时间预算
```

### 阶段2: 收集 (Gathering)

```
输入: 研究计划
输出: 收集的信息

步骤:
1. 执行搜索查询
2. 收集相关文档
3. 记录关键发现
4. 标注来源
5. 组织收集的材料
```

### 阶段3: 分析 (Analyzing)

```
输入: 收集的信息
输出: 分析结果

步骤:
1. 分类信息
2. 识别模式
3. 比较选项
4. 评估证据强度
5. 记录洞察
```

### 阶段4: 综合 (Synthesizing)

```
输入: 分析结果
输出: 综合发现

步骤:
1. 整合发现
2. 识别共同主题
3. 解决矛盾信息
4. 形成结论
5. 准备建议
```

### 阶段5: 报告 (Reporting)

```
输入: 综合发现
输出: 研究报告

步骤:
1. 组织报告结构
2. 撰写发现摘要
3. 提供详细分析
4. 列出建议
5. 引用来源
```

## 使用示例

### 示例1: 技术选型研究

```
用户: "研究一下前端框架选型，React vs Vue vs Angular"

执行流程:
1. Planning: 确定评估维度（性能、生态、学习曲线等）
2. Gathering: 收集各框架文档、社区讨论、性能测试
3. Analyzing: 按维度对比分析
4. Synthesizing: 形成对比结论
5. Reporting: 输出选型建议报告
```

### 示例2: 最佳实践研究

```
用户: "研究微服务架构的最佳实践"

执行流程:
1. Planning: 确定研究范围（拆分策略、通信、部署等）
2. Gathering: 收集架构文章、案例研究
3. Analyzing: 提取共性模式和反模式
4. Synthesizing: 形成最佳实践清单
5. Reporting: 输出实践指南
```

## 研究模板

### 技术研究模板

```markdown
# 研究报告: [主题]

## 摘要
[简要总结]

## 研究问题
- 问题1
- 问题2

## 方法
[研究方法说明]

## 发现
### 发现1
[详细说明]

### 发现2
[详细说明]

## 对比分析
| 维度 | 选项A | 选项B |
|------|-------|-------|
| ... | ... | ... |

## 建议
1. [建议1]
2. [建议2]

## 参考
- [来源1]
- [来源2]
```

## 质量标准

- **全面性**: 覆盖研究主题的关键方面
- **客观性**: 平衡呈现不同观点
- **可操作性**: 提供具体建议
- **可追溯性**: 引用信息来源

## 相关技能

- [code-search](../actions/search) - 代码搜索
- [documentation](../actions/documentation) - 文档生成
- [task-planner](../meta/task-planner) - 任务规划
