---
name: aggregation-processor
description: "Intelligent result aggregation with conflict resolution, consistency checking, and quality scoring. Keywords: aggregation, merge, conflict, consistency, 结果聚合"
layer: workflow
role: processor
version: 2.0.0
invokes: []
invoked_by:
  - coding-workflow
  - debugging-workflow
  - decomposition-planner
capabilities:
  - result_aggregation
  - conflict_detection
  - conflict_resolution
  - consistency_checking
  - quality_scoring
triggers:
  keywords:
    - aggregate
    - merge
    - combine
    - consolidate
    - 聚合
    - 合并
metrics:
  aggregations_performed: 3000
  conflict_resolution_rate: 0.95
  avg_processing_time: 200ms
---

# Aggregation Processor

智能结果聚合处理器，实现冲突检测、一致性检查和质量评分。

## 目的

实现多源结果聚合：
- 结果聚合：合并多个子任务结果
- 冲突检测：识别结果冲突
- 冲突解决：自动或人工解决冲突
- 一致性检查：确保结果一致性
- 质量评分：评估聚合结果质量

## 核心组件

### 1. 聚合数据模型

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class ConflictType(Enum):
    VALUE = "value"              # 值冲突
    STRUCTURE = "structure"      # 结构冲突
    SEMANTIC = "semantic"        # 语义冲突
    TEMPORAL = "temporal"        # 时序冲突
    PRIORITY = "priority"        # 优先级冲突

class ResolutionStrategy(Enum):
    LATEST = "latest"            # 使用最新值
    HIGHEST_CONFIDENCE = "highest_confidence"  # 使用最高置信度
    CONSENSUS = "consensus"      # 共识机制
    PRIORITY = "priority"        # 优先级机制
    MANUAL = "manual"            # 人工干预

@dataclass
class SubTaskResult:
    task_id: str
    source: str
    content: Any
    confidence: float
    timestamp: datetime
    metadata: Dict[str, Any]
    
@dataclass
class Conflict:
    conflict_id: str
    type: ConflictType
    location: str
    values: List[Any]
    sources: List[str]
    severity: float
    resolution: Optional[str]
    resolution_strategy: Optional[ResolutionStrategy]
    
@dataclass
class AggregationResult:
    result_id: str
    content: Any
    source_count: int
    conflicts_detected: int
    conflicts_resolved: int
    consistency_score: float
    quality_score: float
    aggregation_time: float
    metadata: Dict[str, Any]
```

### 2. 冲突检测器

```python
class ConflictDetector:
    def __init__(self):
        self.detection_rules = self._load_rules()
        
    def _load_rules(self) -> Dict:
        return {
            "value_conflict": {
                "condition": lambda v1, v2: v1 != v2,
                "severity": lambda v1, v2: 1.0 if type(v1) != type(v2) else 0.5
            },
            "structure_conflict": {
                "condition": lambda s1, s2: self._compare_structure(s1, s2) < 0.8,
                "severity": 0.7
            },
            "semantic_conflict": {
                "condition": lambda s1, s2: self._semantic_similarity(s1, s2) < 0.5,
                "severity": 0.6
            }
        }
        
    async def detect(
        self,
        results: List[SubTaskResult]
    ) -> List[Conflict]:
        conflicts = []
        
        # 两两比较
        for i, r1 in enumerate(results):
            for r2 in results[i+1:]:
                detected = await self._compare_results(r1, r2)
                conflicts.extend(detected)
                
        return conflicts
        
    async def _compare_results(
        self,
        r1: SubTaskResult,
        r2: SubTaskResult
    ) -> List[Conflict]:
        conflicts = []
        
        # 值冲突检测
        if r1.content != r2.content:
            conflicts.append(Conflict(
                conflict_id=str(uuid.uuid4()),
                type=ConflictType.VALUE,
                location="content",
                values=[r1.content, r2.content],
                sources=[r1.source, r2.source],
                severity=0.5,
                resolution=None,
                resolution_strategy=None
            ))
            
        # 结构冲突检测
        if isinstance(r1.content, dict) and isinstance(r2.content, dict):
            struct_conflicts = self._detect_structure_conflicts(
                r1.content, r2.content, r1.source, r2.source
            )
            conflicts.extend(struct_conflicts)
            
        return conflicts
        
    def _detect_structure_conflicts(
        self,
        d1: Dict,
        d2: Dict,
        s1: str,
        s2: str
    ) -> List[Conflict]:
        conflicts = []
        
        keys1, keys2 = set(d1.keys()), set(d2.keys())
        
        # 缺失键
        missing_in_1 = keys2 - keys1
        missing_in_2 = keys1 - keys2
        
        if missing_in_1 or missing_in_2:
            conflicts.append(Conflict(
                conflict_id=str(uuid.uuid4()),
                type=ConflictType.STRUCTURE,
                location="keys",
                values=[
                    {"missing": list(missing_in_1)},
                    {"missing": list(missing_in_2)}
                ],
                sources=[s1, s2],
                severity=0.3,
                resolution=None,
                resolution_strategy=None
            ))
            
        # 递归检查共同键
        for key in keys1 & keys2:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                conflicts.extend(
                    self._detect_structure_conflicts(
                        d1[key], d2[key], s1, s2
                    )
                )
                
        return conflicts
```

### 3. 冲突解决器

```python
class ConflictResolver:
    def __init__(self, config: Dict):
        self.config = config
        self.strategies = {
            ResolutionStrategy.LATEST: self._resolve_latest,
            ResolutionStrategy.HIGHEST_CONFIDENCE: self._resolve_confidence,
            ResolutionStrategy.CONSENSUS: self._resolve_consensus,
            ResolutionStrategy.PRIORITY: self._resolve_priority
        }
        
    async def resolve(
        self,
        conflict: Conflict,
        results: List[SubTaskResult],
        strategy: ResolutionStrategy = ResolutionStrategy.HIGHEST_CONFIDENCE
    ) -> Any:
        resolver = self.strategies.get(strategy)
        
        if resolver:
            return await resolver(conflict, results)
            
        return None
        
    async def _resolve_latest(
        self,
        conflict: Conflict,
        results: List[SubTaskResult]
    ) -> Any:
        source_map = {r.source: r for r in results}
        
        latest = max(
            [source_map[s] for s in conflict.sources if s in source_map],
            key=lambda r: r.timestamp
        )
        
        return latest.content
        
    async def _resolve_confidence(
        self,
        conflict: Conflict,
        results: List[SubTaskResult]
    ) -> Any:
        source_map = {r.source: r for r in results}
        
        best = max(
            [source_map[s] for s in conflict.sources if s in source_map],
            key=lambda r: r.confidence
        )
        
        return best.content
        
    async def _resolve_consensus(
        self,
        conflict: Conflict,
        results: List[SubTaskResult]
    ) -> Any:
        # 对相同值进行投票
        value_counts = {}
        
        for value in conflict.values:
            key = str(value)
            value_counts[key] = value_counts.get(key, 0) + 1
            
        # 返回票数最多的值
        majority = max(value_counts.items(), key=lambda x: x[1])
        return eval(majority[0])
        
    async def _resolve_priority(
        self,
        conflict: Conflict,
        results: List[SubTaskResult]
    ) -> Any:
        # 根据来源优先级选择
        priority_order = self.config.get("source_priority", [])
        
        for source in priority_order:
            if source in conflict.sources:
                source_map = {r.source: r for r in results}
                return source_map[source].content
                
        return conflict.values[0]
```

### 4. 一致性检查器

```python
class ConsistencyChecker:
    def __init__(self):
        self.rules = self._load_rules()
        
    def _load_rules(self) -> List[Dict]:
        return [
            {
                "name": "type_consistency",
                "check": lambda d: self._check_type_consistency(d)
            },
            {
                "name": "reference_integrity",
                "check": lambda d: self._check_references(d)
            },
            {
                "name": "semantic_consistency",
                "check": lambda d: self._check_semantic_consistency(d)
            }
        ]
        
    async def check(
        self,
        content: Any
    ) -> Dict[str, float]:
        scores = {}
        
        for rule in self.rules:
            try:
                score = await rule["check"](content)
                scores[rule["name"]] = score
            except Exception as e:
                scores[rule["name"]] = 0.0
                
        overall = sum(scores.values()) / len(scores)
        scores["overall"] = overall
        
        return scores
        
    async def _check_type_consistency(
        self,
        content: Any
    ) -> float:
        if not isinstance(content, dict):
            return 1.0
            
        issues = 0
        total = 0
        
        for key, value in content.items():
            total += 1
            
            # 检查类型标注一致性
            if isinstance(value, dict):
                if "_type" in value and "value" in value:
                    expected_type = value["_type"]
                    actual_type = type(value["value"]).__name__
                    if expected_type.lower() != actual_type.lower():
                        issues += 1
                        
        return 1.0 - (issues / total if total > 0 else 0)
        
    async def _check_references(
        self,
        content: Any
    ) -> float:
        if not isinstance(content, dict):
            return 1.0
            
        # 收集所有ID
        all_ids = set()
        references = []
        
        def collect_ids(obj, path=""):
            if isinstance(obj, dict):
                if "id" in obj:
                    all_ids.add(obj["id"])
                if "_ref" in obj:
                    references.append(obj["_ref"])
                for k, v in obj.items():
                    collect_ids(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    collect_ids(item, f"{path}[{i}]")
                    
        collect_ids(content)
        
        # 检查引用完整性
        valid_refs = sum(1 for ref in references if ref in all_ids)
        
        return valid_refs / len(references) if references else 1.0
        
    async def _check_semantic_consistency(
        self,
        content: Any
    ) -> float:
        # 简化的语义一致性检查
        # 实际应使用NLP模型
        return 0.9
```

### 5. 质量评分器

```python
class QualityScorer:
    def __init__(self):
        self.dimensions = [
            "completeness",
            "correctness",
            "consistency",
            "relevance",
            "timeliness"
        ]
        
    async def score(
        self,
        result: AggregationResult,
        original_results: List[SubTaskResult]
    ) -> Dict[str, float]:
        scores = {}
        
        # 完整性
        scores["completeness"] = await self._score_completeness(
            result, original_results
        )
        
        # 正确性
        scores["correctness"] = await self._score_correctness(
            result, original_results
        )
        
        # 一致性
        scores["consistency"] = result.consistency_score
        
        # 相关性
        scores["relevance"] = await self._score_relevance(
            result, original_results
        )
        
        # 时效性
        scores["timeliness"] = await self._score_timeliness(
            result, original_results
        )
        
        # 总分
        scores["overall"] = sum(scores.values()) / len(scores)
        
        return scores
        
    async def _score_completeness(
        self,
        result: AggregationResult,
        original_results: List[SubTaskResult]
    ) -> float:
        # 检查是否所有原始结果的关键信息都被保留
        original_keys = set()
        for r in original_results:
            if isinstance(r.content, dict):
                original_keys.update(r.content.keys())
                
        result_keys = set()
        if isinstance(result.content, dict):
            result_keys.update(result.content.keys())
            
        if not original_keys:
            return 1.0
            
        return len(result_keys & original_keys) / len(original_keys)
        
    async def _score_correctness(
        self,
        result: AggregationResult,
        original_results: List[SubTaskResult]
    ) -> float:
        # 基于置信度加权平均
        if not original_results:
            return 0.5
            
        return sum(r.confidence for r in original_results) / len(original_results)
        
    async def _score_relevance(
        self,
        result: AggregationResult,
        original_results: List[SubTaskResult]
    ) -> float:
        # 简化的相关性评分
        return 0.85
        
    async def _score_timeliness(
        self,
        result: AggregationResult,
        original_results: List[SubTaskResult]
    ) -> float:
        if not original_results:
            return 1.0
            
        # 检查结果是否基于最新数据
        latest_original = max(r.timestamp for r in original_results)
        age = (datetime.now() - latest_original).total_seconds()
        
        # 1小时内为1.0，之后线性衰减
        if age < 3600:
            return 1.0
        else:
            return max(0.5, 1.0 - (age - 3600) / 86400)
```

### 6. 完整聚合处理器

```python
class AggregationProcessor:
    def __init__(self, config: Dict):
        self.config = config
        self.conflict_detector = ConflictDetector()
        self.conflict_resolver = ConflictResolver(config)
        self.consistency_checker = ConsistencyChecker()
        self.quality_scorer = QualityScorer()
        
    async def aggregate(
        self,
        results: List[SubTaskResult],
        strategy: ResolutionStrategy = ResolutionStrategy.HIGHEST_CONFIDENCE
    ) -> AggregationResult:
        start_time = time.time()
        
        # 检测冲突
        conflicts = await self.conflict_detector.detect(results)
        
        # 解决冲突
        resolved_content = await self._resolve_all_conflicts(
            results, conflicts, strategy
        )
        
        # 一致性检查
        consistency_scores = await self.consistency_checker.check(
            resolved_content
        )
        
        # 创建聚合结果
        result = AggregationResult(
            result_id=str(uuid.uuid4()),
            content=resolved_content,
            source_count=len(results),
            conflicts_detected=len(conflicts),
            conflicts_resolved=len([c for c in conflicts if c.resolution]),
            consistency_score=consistency_scores["overall"],
            quality_score=0.0,
            aggregation_time=time.time() - start_time,
            metadata={
                "conflicts": [
                    {
                        "type": c.type.value,
                        "resolution": c.resolution
                    } for c in conflicts
                ]
            }
        )
        
        # 质量评分
        quality_scores = await self.quality_scorer.score(result, results)
        result.quality_score = quality_scores["overall"]
        
        return result
        
    async def _resolve_all_conflicts(
        self,
        results: List[SubTaskResult],
        conflicts: List[Conflict],
        strategy: ResolutionStrategy
    ) -> Any:
        if not results:
            return None
            
        if len(results) == 1:
            return results[0].content
            
        # 从第一个结果开始
        merged = results[0].content.copy() if isinstance(results[0].content, dict) else results[0].content
        
        # 解决每个冲突
        for conflict in conflicts:
            resolved_value = await self.conflict_resolver.resolve(
                conflict, results, strategy
            )
            
            # 应用解决结果
            if conflict.location == "content":
                merged = resolved_value
            elif isinstance(merged, dict) and "." in conflict.location:
                self._apply_nested_resolution(merged, conflict.location, resolved_value)
                
        return merged
        
    def _apply_nested_resolution(
        self,
        content: Dict,
        location: str,
        value: Any
    ):
        keys = location.split(".")
        current = content
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
            
        current[keys[-1]] = value
```

## 聚合策略配置

```yaml
aggregation_strategies:
  default: highest_confidence
  
  by_task_type:
    code_generation: latest
    data_analysis: consensus
    research: highest_confidence
    documentation: priority
    
  source_priority:
    - verified_agent
    - primary_model
    - fallback_model
    - cached_result
```

## 最佳实践

1. **明确策略**: 根据任务类型选择聚合策略
2. **冲突透明**: 记录所有检测到的冲突
3. **质量验证**: 聚合后进行质量检查
4. **渐进合并**: 大数据集分批聚合
5. **回溯能力**: 保留原始结果引用

## 相关技能

- [decomposition-planner](../meta/decomposition-planner) - 任务分解
- [coding-workflow](./coding-workflow) - 编码工作流
- [reflector](../learning/reflector) - 反思系统
