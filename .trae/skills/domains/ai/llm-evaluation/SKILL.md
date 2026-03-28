---
name: llm-evaluation
description: "LLM evaluation and benchmarking for model performance, quality, and safety. Keywords: evaluation, benchmark, llm, metrics, ragas, deepeval, 评估, 基准测试"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
frameworks:
  - ragas
  - deepeval
  - trulens
invoked_by:
  - rag-system
  - langchain
capabilities:
  - quality_assessment
  - benchmark_execution
  - metric_calculation
  - safety_evaluation
triggers:
  keywords:
    - evaluate
    - evaluation
    - benchmark
    - metrics
    - ragas
    - deepeval
    - 评估
    - 基准测试
metrics:
  avg_execution_time: 10s
  success_rate: 0.93
  evaluation_accuracy: 0.90
---

# LLM Evaluation

LLM评估和基准测试，用于模型性能、质量和安全性评估。

## 目的

提供LLM应用的系统性评估：
- 质量评估指标
- 基准测试执行
- RAG系统评估
- 安全性评估

## 能力

- **质量评估**: 评估LLM输出质量
- **基准执行**: 执行标准基准测试
- **指标计算**: 计算评估指标
- **安全评估**: 评估安全性和合规性

## 评估框架

### 1. Ragas (RAG评估)

```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ]
)
```

### 2. DeepEval

```python
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
)

metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.7),
    HallucinationMetric(threshold=0.3),
]

evaluate(test_cases, metrics)
```

## 评估指标

### RAG指标

| 指标 | 描述 | 计算方式 |
|------|------|----------|
| Faithfulness | 答案是否基于上下文 | 答案声明 vs 上下文支持 |
| Answer Relevancy | 答案与问题的相关性 | 问题-答案相似度 |
| Context Precision | 检索上下文的精确度 | 相关上下文比例 |
| Context Recall | 检索上下文的召回率 | 需要信息覆盖率 |

### 生成质量指标

| 指标 | 描述 | 用途 |
|------|------|------|
| BLEU | 机器翻译质量 | 翻译评估 |
| ROUGE | 文本摘要质量 | 摘要评估 |
| Perplexity | 语言模型困惑度 | 模型质量 |
| BERTScore | 语义相似度 | 文本相似性 |

### 安全指标

| 指标 | 描述 | 评估内容 |
|------|------|----------|
| Toxicity | 有害内容检测 | 辱骂、仇恨言论 |
| Bias | 偏见检测 | 性别、种族偏见 |
| Hallucination | 幻觉检测 | 事实准确性 |
| PII Leakage | 隐私泄露 | 敏感信息暴露 |

## 基准测试

### 通用基准

| 基准 | 描述 | 评估能力 |
|------|------|----------|
| MMLU | 多任务语言理解 | 知识广度 |
| HellaSwag | 常识推理 | 推理能力 |
| GSM8K | 数学问题 | 数学推理 |
| HumanEval | 代码生成 | 编程能力 |
| TruthfulQA | 事实准确性 | 真实性 |

### RAG基准

| 基准 | 描述 | 评估内容 |
|------|------|----------|
| RAGAS | RAG质量评估 | 检索+生成质量 |
| RGB | RAG基准 | 端到端RAG |
| RECALL | 检索评估 | 检索系统质量 |

## 评估流程

```
输入: 测试数据集
输出: 评估报告

步骤:
1. 准备测试数据
2. 配置评估指标
3. 执行评估
4. 分析结果
5. 生成报告
```

## 评估模板

```python
from dataclasses import dataclass
from typing import List

@dataclass
class EvaluationResult:
    metric_name: str
    score: float
    threshold: float
    passed: bool
    details: dict

@dataclass
class EvaluationReport:
    overall_score: float
    results: List[EvaluationResult]
    recommendations: List[str]

def generate_report(report: EvaluationReport) -> str:
    return f"""
# LLM Evaluation Report

## Overall Score: {report.overall_score:.2f}

## Metric Results

| Metric | Score | Threshold | Status |
|--------|-------|-----------|--------|
{chr(10).join(f"| {r.metric_name} | {r.score:.2f} | {r.threshold:.2f} | {'✅' if r.passed else '❌'} |" for r in report.results)}

## Recommendations

{chr(10).join(f"- {rec}" for rec in report.recommendations)}
"""
```

## 使用示例

### 示例: RAG系统评估

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# 准备测试数据
test_data = {
    "question": ["What is Python?"],
    "answer": ["Python is a programming language..."],
    "contexts": [["Python is a high-level programming language..."]],
    "ground_truth": ["Python is a programming language"]
}

# 执行评估
result = evaluate(
    test_data,
    metrics=[faithfulness, answer_relevancy]
)

print(f"Faithfulness: {result['faithfulness']}")
print(f"Answer Relevancy: {result['answer_relevancy']}")
```

### 示例: 幻觉检测

```python
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

test_case = LLMTestCase(
    input="What is the capital of France?",
    actual_output="The capital of France is London.",
    context=["Paris is the capital of France."]
)

metric = HallucinationMetric(threshold=0.5)
metric.measure(test_case)

print(f"Hallucination Score: {metric.score}")
print(f"Reason: {metric.reason}")
```

## 最佳实践

1. **多指标评估**: 使用多个指标综合评估
2. **阈值设置**: 根据应用场景设置合理阈值
3. **持续监控**: 定期评估模型表现
4. **A/B测试**: 对比不同配置效果
5. **人工审核**: 结合人工评估验证

## 评估工具

| 工具 | 描述 | 链接 |
|------|------|------|
| Ragas | RAG评估框架 | GitHub |
| DeepEval | LLM评估框架 | GitHub |
| LangSmith | LangChain评估平台 | Website |
| TruLens | LLM可解释性 | GitHub |
| Arize Phoenix | LLM监控 | GitHub |

## 相关技能

- [rag-system](../rag-system) - RAG系统
- [langchain](../langchain) - LangChain框架
- [openai](../openai) - OpenAI API
- [claude-api](../claude-api) - Claude API
