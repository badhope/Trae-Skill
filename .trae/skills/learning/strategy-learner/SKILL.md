---
name: strategy-learner
description: "Learning system for strategy optimization based on execution feedback and historical data. Keywords: learning, optimization, strategy, feedback, 策略学习"
layer: learning
role: learner
version: 2.0.0
invokes: []
invoked_by:
  - reflector
  - self-enhancer
capabilities:
  - strategy_optimization
  - pattern_recognition
  - feedback_learning
  - knowledge_accumulation
triggers:
  keywords:
    - learn
    - optimize
    - improve
    - feedback
    - 学习
    - 优化
metrics:
  learning_cycles: 1000
  improvement_rate: 0.15
  knowledge_items: 5000
---

# Strategy Learner

策略学习系统，基于执行反馈和历史数据进行策略优化。

## 目的

实现持续学习与优化：
- 策略优化：优化任务执行策略
- 模式识别：识别成功/失败模式
- 反馈学习：从反馈中学习
- 知识积累：积累执行知识

## 核心组件

### 1. 学习数据模型

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

class FeedbackType(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    USER_RATING = "user_rating"
    SELF_EVALUATION = "self_evaluation"

@dataclass
class ExecutionFeedback:
    task_id: str
    feedback_type: FeedbackType
    score: float  # 0.0 - 1.0
    details: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    
@dataclass
class StrategyPattern:
    pattern_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    success_rate: float
    sample_count: int
    last_updated: datetime
    
@dataclass
class LearningRecord:
    record_id: str
    task_type: str
    strategy_used: str
    execution_time: float
    token_usage: int
    result_quality: float
    feedback: Optional[ExecutionFeedback]
    lessons_learned: List[str]
    timestamp: datetime
```

### 2. 反馈收集器

```python
class FeedbackCollector:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.pending_feedback = []
        
    async def collect(
        self,
        task_id: str,
        feedback_type: FeedbackType,
        score: float,
        details: Optional[dict] = None
    ):
        feedback = ExecutionFeedback(
            task_id=task_id,
            feedback_type=feedback_type,
            score=score,
            details=details or {}
        )
        
        await self.storage.save("feedbacks", feedback)
        
        # 触发学习
        await self._trigger_learning(feedback)
        
    async def collect_user_rating(
        self,
        task_id: str,
        rating: int,  # 1-5
        comment: Optional[str] = None
    ):
        score = (rating - 1) / 4  # 转换为0-1
        await self.collect(
            task_id,
            FeedbackType.USER_RATING,
            score,
            {"rating": rating, "comment": comment}
        )
        
    async def collect_self_evaluation(
        self,
        task_id: str,
        criteria: Dict[str, float]
    ):
        score = sum(criteria.values()) / len(criteria)
        await self.collect(
            task_id,
            FeedbackType.SELF_EVALUATION,
            score,
            {"criteria": criteria}
        )
```

### 3. 模式识别器

```python
class PatternRecognizer:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.min_samples = 10
        
    async def identify_patterns(
        self,
        task_type: str,
        time_window: timedelta = timedelta(days=30)
    ) -> List[StrategyPattern]:
        # 获取历史执行记录
        records = await self.storage.query(
            "learning_records",
            {
                "task_type": task_type,
                "timestamp": {"$gte": datetime.now() - time_window}
            }
        )
        
        if len(records) < self.min_samples:
            return []
            
        # 特征提取
        features = self._extract_features(records)
        
        # 聚类分析
        clusters = self._cluster_executions(features)
        
        # 识别成功模式
        patterns = []
        for cluster in clusters:
            if cluster["success_rate"] > 0.7:
                pattern = StrategyPattern(
                    pattern_id=str(uuid.uuid4()),
                    name=self._generate_pattern_name(cluster),
                    description=self._describe_pattern(cluster),
                    conditions=cluster["common_conditions"],
                    actions=cluster["common_actions"],
                    success_rate=cluster["success_rate"],
                    sample_count=cluster["size"],
                    last_updated=datetime.now()
                )
                patterns.append(pattern)
                
        return patterns
        
    def _extract_features(
        self, 
        records: List[LearningRecord]
    ) -> List[Dict]:
        features = []
        for record in records:
            feature = {
                "complexity": record.task_complexity,
                "strategy": record.strategy_used,
                "execution_time": record.execution_time,
                "token_usage": record.token_usage,
                "result_quality": record.result_quality,
                "time_of_day": record.timestamp.hour,
                "day_of_week": record.timestamp.weekday()
            }
            features.append(feature)
        return features
        
    def _cluster_executions(
        self, 
        features: List[Dict]
    ) -> List[Dict]:
        # 简化的聚类实现
        # 实际应使用K-means或DBSCAN
        clusters = defaultdict(list)
        
        for f in features:
            key = (f["strategy"], f["complexity"] // 3)
            clusters[key].append(f)
            
        results = []
        for (strategy, complexity_group), items in clusters.items():
            success_rate = sum(
                1 for i in items if i["result_quality"] > 0.7
            ) / len(items)
            
            results.append({
                "strategy": strategy,
                "complexity_range": f"{complexity_group * 3}-{(complexity_group + 1) * 3}",
                "success_rate": success_rate,
                "size": len(items),
                "common_conditions": self._get_common_conditions(items),
                "common_actions": self._get_common_actions(items)
            })
            
        return results
```

### 4. 策略优化器

```python
class StrategyOptimizer:
    def __init__(
        self,
        storage: PersistentStorage,
        pattern_recognizer: PatternRecognizer
    ):
        self.storage = storage
        self.pattern_recognizer = pattern_recognizer
        self.strategies = {}
        
    async def optimize(
        self,
        task_type: str
    ) -> Dict[str, Any]:
        # 识别模式
        patterns = await self.pattern_recognizer.identify_patterns(task_type)
        
        # 获取当前策略
        current = await self._get_current_strategy(task_type)
        
        # 生成优化建议
        optimizations = []
        
        for pattern in patterns:
            if pattern.success_rate > current.get("success_rate", 0):
                optimization = {
                    "type": "strategy_update",
                    "task_type": task_type,
                    "current_strategy": current.get("name"),
                    "recommended_strategy": pattern.name,
                    "expected_improvement": pattern.success_rate - current.get("success_rate", 0),
                    "confidence": min(pattern.sample_count / 100, 1.0),
                    "reasoning": pattern.description
                }
                optimizations.append(optimization)
                
        # 保存优化建议
        for opt in optimizations:
            await self.storage.save("optimizations", opt)
            
        return {
            "task_type": task_type,
            "optimizations": optimizations,
            "patterns_found": len(patterns)
        }
        
    async def apply_optimization(
        self,
        optimization: Dict[str, Any]
    ) -> bool:
        task_type = optimization["task_type"]
        new_strategy = optimization["recommended_strategy"]
        
        # 更新策略
        self.strategies[task_type] = {
            "name": new_strategy,
            "updated_at": datetime.now(),
            "source": "learning"
        }
        
        await self.storage.save("strategies", {
            "task_type": task_type,
            "strategy": self.strategies[task_type]
        })
        
        return True
```

### 5. 知识库

```python
@dataclass
class KnowledgeItem:
    item_id: str
    category: str
    title: str
    content: str
    source: str  # "learning", "manual", "imported"
    confidence: float
    usage_count: int
    last_used: datetime
    created_at: datetime
    tags: List[str]

class KnowledgeBase:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        
    async def add(
        self,
        category: str,
        title: str,
        content: str,
        tags: List[str],
        source: str = "learning"
    ) -> str:
        item = KnowledgeItem(
            item_id=str(uuid.uuid4()),
            category=category,
            title=title,
            content=content,
            source=source,
            confidence=0.5,
            usage_count=0,
            last_used=datetime.now(),
            created_at=datetime.now(),
            tags=tags
        )
        
        await self.storage.save("knowledge", item)
        return item.item_id
        
    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 10
    ) -> List[KnowledgeItem]:
        filter_query = {"$text": {"$search": query}}
        
        if category:
            filter_query["category"] = category
            
        items = await self.storage.query(
            "knowledge",
            filter_query,
            sort=[("confidence", -1), ("usage_count", -1)],
            limit=limit
        )
        
        # 更新使用计数
        for item in items:
            await self.storage.update(
                "knowledge",
                {"item_id": item.item_id},
                {
                    "$inc": {"usage_count": 1},
                    "$set": {"last_used": datetime.now()}
                }
            )
            
        return items
        
    async def update_confidence(
        self,
        item_id: str,
        delta: float
    ):
        await self.storage.update(
            "knowledge",
            {"item_id": item_id},
            {"$inc": {"confidence": delta}}
        )
```

### 6. 完整学习系统

```python
class StrategyLearner:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.feedback_collector = FeedbackCollector(storage)
        self.pattern_recognizer = PatternRecognizer(storage)
        self.optimizer = StrategyOptimizer(storage, self.pattern_recognizer)
        self.knowledge_base = KnowledgeBase(storage)
        
    async def learn_from_execution(
        self,
        task: Task,
        result: Result,
        feedback: Optional[ExecutionFeedback] = None
    ):
        # 记录执行
        record = LearningRecord(
            record_id=str(uuid.uuid4()),
            task_type=task.type,
            strategy_used=task.strategy,
            execution_time=result.execution_time,
            token_usage=result.token_usage,
            result_quality=result.quality_score,
            feedback=feedback,
            lessons_learned=[],
            timestamp=datetime.now()
        )
        
        await self.storage.save("learning_records", record)
        
        # 如果有反馈，触发学习
        if feedback and feedback.score < 0.5:
            await self._analyze_failure(record)
        elif feedback and feedback.score > 0.8:
            await self._analyze_success(record)
            
    async def _analyze_failure(self, record: LearningRecord):
        # 分析失败原因
        analysis = await self._generate_failure_analysis(record)
        
        # 添加到知识库
        await self.knowledge_base.add(
            category="failure_patterns",
            title=f"Failure: {record.task_type}",
            content=analysis,
            tags=["failure", record.task_type, record.strategy_used]
        )
        
    async def _analyze_success(self, record: LearningRecord):
        # 分析成功因素
        analysis = await self._generate_success_analysis(record)
        
        # 添加到知识库
        await self.knowledge_base.add(
            category="success_patterns",
            title=f"Success: {record.task_type}",
            content=analysis,
            tags=["success", record.task_type, record.strategy_used]
        )
        
    async def run_learning_cycle(self):
        """定期学习循环"""
        for task_type in await self._get_active_task_types():
            # 优化策略
            optimization = await self.optimizer.optimize(task_type)
            
            # 自动应用高置信度优化
            for opt in optimization.get("optimizations", []):
                if opt["confidence"] > 0.8:
                    await self.optimizer.apply_optimization(opt)
```

## 学习循环

```yaml
learning_cycle:
  schedule: "0 */6 * * *"  # 每6小时
  
  steps:
    - name: "收集反馈"
      action: "collect_pending_feedback"
      
    - name: "识别模式"
      action: "identify_patterns"
      params:
        min_samples: 10
        time_window: "30d"
        
    - name: "优化策略"
      action: "optimize_strategies"
      
    - name: "更新知识库"
      action: "update_knowledge"
      
    - name: "生成报告"
      action: "generate_report"
```

## 最佳实践

1. **及时反馈**: 任务完成后及时收集反馈
2. **多样本学习**: 确保有足够样本再优化
3. **渐进优化**: 小步迭代，持续改进
4. **知识沉淀**: 将学习成果沉淀为知识
5. **效果验证**: 验证优化效果

## 相关技能

- [reflector](./reflector) - 反思系统
- [self-enhancer](./self-enhancer) - 自我增强
- [task-registry](../meta/task-registry) - 任务注册
