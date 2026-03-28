---
name: model-router
description: "Intelligent model routing based on task complexity and resource optimization. Routes tasks to appropriate models for cost-efficiency and performance. Keywords: model routing, load balancing, cost optimization, 模型路由"
layer: dispatcher
role: router
version: 2.0.0
invokes:
  - coding-workflow
  - debugging-workflow
invoked_by:
  - task-planner
  - decomposition-planner
capabilities:
  - complexity_assessment
  - model_selection
  - cost_optimization
  - latency_optimization
triggers:
  keywords:
    - route
    - model
    - complexity
    - cost
    - latency
metrics:
  avg_routing_time: 50ms
  cost_savings: 40%
  accuracy: 0.92
---

# Model Router

智能模型路由器，基于任务复杂度和资源优化进行模型选择。

## 目的

实现多模型环境下的智能路由：
- 复杂度评估：分析任务复杂度
- 模型选择：选择最优模型
- 成本优化：降低Token消耗
- 延迟优化：提升响应速度

## 核心能力

### 1. 复杂度评估算法

```python
class ComplexityAssessor:
    def assess(self, task: Task) -> ComplexityScore:
        score = 0
        
        # 关键词复杂度
        complex_keywords = ["架构", "设计", "优化", "重构", "多线程"]
        score += sum(2 for kw in complex_keywords if kw in task.content)
        
        # 文件数量
        score += min(task.file_count * 2, 10)
        
        # 依赖深度
        score += min(task.dependency_depth, 8)
        
        # 领域专业性
        if task.domain in ["ai", "security", "performance"]:
            score += 5
            
        return ComplexityScore(
            raw=score,
            level=self._categorize(score)
        )
    
    def _categorize(self, score: int) -> ComplexityLevel:
        if score <= 3:
            return ComplexityLevel.LOW
        elif score <= 7:
            return ComplexityLevel.MEDIUM
        elif score <= 12:
            return ComplexityLevel.HIGH
        else:
            return ComplexityLevel.CRITICAL
```

### 2. 模型路由策略

```yaml
routing_matrix:
  LOW:
    primary: "gpt-3.5-turbo"
    fallback: "gpt-4o-mini"
    max_tokens: 4000
    estimated_cost: "$0.001/1K tokens"
    
  MEDIUM:
    primary: "gpt-4o-mini"
    fallback: "gpt-4o"
    max_tokens: 8000
    estimated_cost: "$0.01/1K tokens"
    
  HIGH:
    primary: "gpt-4o"
    fallback: "claude-3-opus"
    max_tokens: 16000
    estimated_cost: "$0.03/1K tokens"
    
  CRITICAL:
    primary: "claude-3-opus"
    fallback: "gpt-4-turbo"
    max_tokens: 32000
    estimated_cost: "$0.05/1K tokens"
```

### 3. 路由决策引擎

```python
class ModelRouter:
    def __init__(self):
        self.assessor = ComplexityAssessor()
        self.registry = ModelRegistry()
        self.metrics = RoutingMetrics()
        
    async def route(self, task: Task) -> RoutingDecision:
        # 评估复杂度
        complexity = self.assessor.assess(task)
        
        # 获取路由配置
        config = self.routing_matrix[complexity.level]
        
        # 检查模型可用性
        primary = self.registry.get(config["primary"])
        if not primary.is_available():
            primary = self.registry.get(config["fallback"])
            
        # 记录路由决策
        decision = RoutingDecision(
            task_id=task.id,
            model=primary.name,
            complexity=complexity,
            estimated_tokens=config["max_tokens"],
            estimated_cost=config["estimated_cost"]
        )
        
        self.metrics.record(decision)
        return decision
```

## 模型能力矩阵

| 模型 | 推理能力 | 代码生成 | 速度 | 成本 | 最佳场景 |
|------|----------|----------|------|------|----------|
| gpt-3.5-turbo | ★★☆ | ★★☆ | ★★★ | ★★★ | 简单问答、格式转换 |
| gpt-4o-mini | ★★★ | ★★★ | ★★★ | ★★☆ | 中等任务、API调用 |
| gpt-4o | ★★★★ | ★★★★ | ★★☆ | ★★☆ | 复杂推理、架构设计 |
| claude-3-opus | ★★★★★ | ★★★★ | ★☆☆ | ★☆☆ | 专家级任务、深度分析 |
| claude-3-sonnet | ★★★★ | ★★★★ | ★★★ | ★★☆ | 平衡型任务 |

## 负载均衡策略

```python
class LoadBalancer:
    def __init__(self):
        self.model_loads = {}
        self.rate_limits = {
            "gpt-4o": {"rpm": 500, "tpm": 30000},
            "claude-3-opus": {"rpm": 100, "tpm": 20000}
        }
        
    def select_model(self, candidates: List[Model]) -> Model:
        # 按负载排序
        sorted_models = sorted(
            candidates,
            key=lambda m: self.model_loads.get(m.name, 0)
        )
        
        # 检查速率限制
        for model in sorted_models:
            if self._check_rate_limit(model):
                return model
                
        raise NoModelAvailableError()
        
    def _check_rate_limit(self, model: Model) -> bool:
        limits = self.rate_limits.get(model.name, {})
        current = self.model_loads.get(model.name, {})
        
        return (
            current.get("rpm", 0) < limits.get("rpm", float('inf')) and
            current.get("tpm", 0) < limits.get("tpm", float('inf'))
        )
```

## 熔断机制

```python
class CircuitBreaker:
    def __init__(self, threshold: int = 5, timeout: int = 60):
        self.failure_counts = {}
        self.threshold = threshold
        self.timeout = timeout
        self.states = {}  # CLOSED, OPEN, HALF_OPEN
        
    async def execute(self, model: Model, task: Task) -> Result:
        state = self.states.get(model.name, "CLOSED")
        
        if state == "OPEN":
            if self._should_retry(model):
                self.states[model.name] = "HALF_OPEN"
            else:
                raise CircuitOpenError(f"Model {model.name} is circuit open")
                
        try:
            result = await model.execute(task)
            self._on_success(model)
            return result
        except Exception as e:
            self._on_failure(model)
            raise
            
    def _on_failure(self, model: Model):
        self.failure_counts[model.name] = \
            self.failure_counts.get(model.name, 0) + 1
            
        if self.failure_counts[model.name] >= self.threshold:
            self.states[model.name] = "OPEN"
            
    def _on_success(self, model: Model):
        self.failure_counts[model.name] = 0
        self.states[model.name] = "CLOSED"
```

## 成本追踪

```python
class CostTracker:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        
    async def record(self, decision: RoutingDecision, actual: ActualUsage):
        record = CostRecord(
            task_id=decision.task_id,
            model=decision.model,
            estimated_tokens=decision.estimated_tokens,
            actual_tokens=actual.tokens,
            estimated_cost=decision.estimated_cost,
            actual_cost=actual.cost,
            timestamp=datetime.now()
        )
        
        await self.storage.save("costs", record)
        
    async def get_report(self, period: TimePeriod) -> CostReport:
        records = await self.storage.query(
            "costs",
            {"timestamp": {"$gte": period.start, "$lte": period.end}}
        )
        
        return CostReport(
            total_cost=sum(r.actual_cost for r in records),
            by_model=self._group_by_model(records),
            savings=self._calculate_savings(records)
        )
```

## 最佳实践

1. **复杂度优先**: 先评估复杂度再路由
2. **成本意识**: 持续监控Token消耗
3. **熔断保护**: 防止级联故障
4. **负载均衡**: 分散请求压力
5. **指标追踪**: 记录路由决策用于优化

## 相关技能

- [task-planner](../meta/task-planner) - 任务规划
- [decomposition-planner](../meta/decomposition-planner) - 任务分解
- [concurrency-manager](./concurrency-manager) - 并发管理
- [load-balancer](./load-balancer) - 负载均衡
