---
name: reflector
description: "Reflection system for analyzing execution results, identifying issues, and generating improvement insights. Keywords: reflection, analysis, feedback, improvement, 反思"
layer: learning
role: reflector
version: 2.0.0
invokes:
  - strategy-learner
  - self-enhancer
invoked_by:
  - coding-workflow
  - debugging-workflow
  - task-planner
capabilities:
  - execution_analysis
  - issue_identification
  - insight_generation
  - improvement_recommendation
triggers:
  keywords:
    - reflect
    - analyze
    - review
    - improve
    - 反思
    - 分析
metrics:
  reflections_performed: 5000
  insights_generated: 3000
  improvements_applied: 800
---

# Reflector

反思系统，分析执行结果、识别问题并生成改进洞察。

## 目的

实现执行后反思：
- 执行分析：分析执行过程和结果
- 问题识别：识别问题和改进点
- 洞察生成：生成改进洞察
- 建议推荐：推荐具体改进措施

## 核心组件

### 1. 反思框架

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class ReflectionType(Enum):
    POST_EXECUTION = "post_execution"      # 执行后反思
    PERIODIC = "periodic"                  # 定期反思
    TRIGGERED = "triggered"                # 触发式反思
    DEEP_DIVE = "deep_dive"               # 深度反思

class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class ReflectionContext:
    task_id: str
    task_type: str
    execution_log: List[Dict]
    result: Dict[str, Any]
    metrics: Dict[str, float]
    errors: List[Dict]
    warnings: List[Dict]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Issue:
    issue_id: str
    type: str
    severity: IssueSeverity
    description: str
    location: str
    impact: str
    suggested_fix: str
    related_patterns: List[str]

@dataclass
class Insight:
    insight_id: str
    category: str
    title: str
    description: str
    evidence: List[str]
    confidence: float
    actionable: bool
    recommendations: List[str]
    
@dataclass
class ReflectionReport:
    report_id: str
    context: ReflectionContext
    issues: List[Issue]
    insights: List[Insight]
    overall_score: float
    improvement_priority: List[str]
    created_at: datetime
```

### 2. 执行分析器

```python
class ExecutionAnalyzer:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        
    async def analyze(
        self,
        context: ReflectionContext
    ) -> Dict[str, Any]:
        analysis = {
            "performance": await self._analyze_performance(context),
            "quality": await self._analyze_quality(context),
            "efficiency": await self._analyze_efficiency(context),
            "errors": await self._analyze_errors(context),
            "patterns": await self._analyze_patterns(context)
        }
        
        return analysis
        
    async def _analyze_performance(
        self,
        context: ReflectionContext
    ) -> Dict:
        metrics = context.metrics
        
        return {
            "execution_time": metrics.get("execution_time", 0),
            "token_usage": metrics.get("token_usage", 0),
            "api_calls": metrics.get("api_calls", 0),
            "efficiency_score": self._calculate_efficiency(metrics)
        }
        
    async def _analyze_quality(
        self,
        context: ReflectionContext
    ) -> Dict:
        result = context.result
        
        return {
            "completeness": self._assess_completeness(result),
            "correctness": self._assess_correctness(result),
            "consistency": self._assess_consistency(result),
            "quality_score": self._calculate_quality(result)
        }
        
    async def _analyze_errors(
        self,
        context: ReflectionContext
    ) -> Dict:
        errors = context.errors
        
        error_patterns = self._identify_error_patterns(errors)
        
        return {
            "error_count": len(errors),
            "error_types": self._categorize_errors(errors),
            "patterns": error_patterns,
            "root_causes": self._analyze_root_causes(errors)
        }
        
    async def _analyze_patterns(
        self,
        context: ReflectionContext
    ) -> Dict:
        # 与历史执行对比
        historical = await self._get_historical_executions(
            context.task_type
        )
        
        return {
            "deviations": self._find_deviations(context, historical),
            "improvements": self._find_improvements(context, historical),
            "regressions": self._find_regressions(context, historical)
        }
```

### 3. 问题识别器

```python
class IssueIdentifier:
    def __init__(self):
        self.rules = self._load_rules()
        
    def _load_rules(self) -> Dict:
        return {
            "performance": {
                "slow_execution": {
                    "condition": lambda m: m.get("execution_time", 0) > 300,
                    "severity": IssueSeverity.HIGH,
                    "description": "执行时间过长",
                    "suggestion": "考虑优化算法或并行处理"
                },
                "high_token_usage": {
                    "condition": lambda m: m.get("token_usage", 0) > 10000,
                    "severity": IssueSeverity.MEDIUM,
                    "description": "Token使用量过高",
                    "suggestion": "优化Prompt或使用更高效的模型"
                }
            },
            "quality": {
                "incomplete_result": {
                    "condition": lambda r: r.get("completeness", 1) < 0.8,
                    "severity": IssueSeverity.HIGH,
                    "description": "结果不完整",
                    "suggestion": "检查任务分解是否合理"
                },
                "low_confidence": {
                    "condition": lambda r: r.get("confidence", 1) < 0.7,
                    "severity": IssueSeverity.MEDIUM,
                    "description": "结果置信度低",
                    "suggestion": "增加验证步骤或收集更多信息"
                }
            },
            "execution": {
                "retry_exceeded": {
                    "condition": lambda e: any(
                        err.get("type") == "retry_exceeded" 
                        for err in e
                    ),
                    "severity": IssueSeverity.CRITICAL,
                    "description": "重试次数超限",
                    "suggestion": "检查根本原因并修复"
                },
                "timeout": {
                    "condition": lambda e: any(
                        err.get("type") == "timeout" 
                        for err in e
                    ),
                    "severity": IssueSeverity.HIGH,
                    "description": "执行超时",
                    "suggestion": "优化执行流程或增加超时时间"
                }
            }
        }
        
    async def identify(
        self,
        context: ReflectionContext
    ) -> List[Issue]:
        issues = []
        
        # 检查性能问题
        for rule_name, rule in self.rules["performance"].items():
            if rule["condition"](context.metrics):
                issues.append(Issue(
                    issue_id=str(uuid.uuid4()),
                    type="performance",
                    severity=rule["severity"],
                    description=rule["description"],
                    location="execution",
                    impact=self._assess_impact(rule["severity"]),
                    suggested_fix=rule["suggestion"],
                    related_patterns=[]
                ))
                
        # 检查质量问题
        for rule_name, rule in self.rules["quality"].items():
            if rule["condition"](context.result):
                issues.append(Issue(
                    issue_id=str(uuid.uuid4()),
                    type="quality",
                    severity=rule["severity"],
                    description=rule["description"],
                    location="result",
                    impact=self._assess_impact(rule["severity"]),
                    suggested_fix=rule["suggestion"],
                    related_patterns=[]
                ))
                
        # 检查执行问题
        for rule_name, rule in self.rules["execution"].items():
            if rule["condition"](context.errors):
                issues.append(Issue(
                    issue_id=str(uuid.uuid4()),
                    type="execution",
                    severity=rule["severity"],
                    description=rule["description"],
                    location="execution",
                    impact=self._assess_impact(rule["severity"]),
                    suggested_fix=rule["suggestion"],
                    related_patterns=[]
                ))
                
        return issues
```

### 4. 洞察生成器

```python
class InsightGenerator:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.knowledge_base = KnowledgeBase(storage)
        
    async def generate(
        self,
        context: ReflectionContext,
        analysis: Dict,
        issues: List[Issue]
    ) -> List[Insight]:
        insights = []
        
        # 从问题生成洞察
        for issue in issues:
            insight = await self._issue_to_insight(issue, context)
            if insight:
                insights.append(insight)
                
        # 从模式生成洞察
        pattern_insights = await self._analyze_patterns(analysis)
        insights.extend(pattern_insights)
        
        # 从历史对比生成洞察
        historical_insights = await self._compare_with_history(context)
        insights.extend(historical_insights)
        
        # 去重和排序
        insights = self._deduplicate(insights)
        insights.sort(key=lambda i: i.confidence, reverse=True)
        
        return insights
        
    async def _issue_to_insight(
        self,
        issue: Issue,
        context: ReflectionContext
    ) -> Optional[Insight]:
        # 查找相关历史案例
        similar_cases = await self.knowledge_base.search(
            issue.description,
            category="issues"
        )
        
        if similar_cases:
            best_case = similar_cases[0]
            return Insight(
                insight_id=str(uuid.uuid4()),
                category="issue_resolution",
                title=f"解决{issue.type}问题的方法",
                description=f"基于历史案例，建议{issue.suggested_fix}",
                evidence=[
                    f"历史案例: {best_case.title}",
                    f"当前问题: {issue.description}"
                ],
                confidence=min(best_case.confidence, 0.9),
                actionable=True,
                recommendations=[
                    issue.suggested_fix,
                    f"参考案例: {best_case.content[:200]}"
                ]
            )
            
        return Insight(
            insight_id=str(uuid.uuid4()),
            category="issue_identification",
            title=f"发现{issue.type}问题",
            description=issue.description,
            evidence=[f"位置: {issue.location}"],
            confidence=0.7,
            actionable=True,
            recommendations=[issue.suggested_fix]
        )
        
    async def _analyze_patterns(
        self,
        analysis: Dict
    ) -> List[Insight]:
        insights = []
        
        # 性能模式
        if analysis["performance"]["efficiency_score"] < 0.7:
            insights.append(Insight(
                insight_id=str(uuid.uuid4()),
                category="performance",
                title="性能优化机会",
                description="执行效率低于预期，存在优化空间",
                evidence=[
                    f"效率分数: {analysis['performance']['efficiency_score']:.2f}",
                    f"执行时间: {analysis['performance']['execution_time']}s"
                ],
                confidence=0.8,
                actionable=True,
                recommendations=[
                    "分析执行日志找出耗时步骤",
                    "考虑并行化或缓存优化"
                ]
            ))
            
        return insights
```

### 5. 反思执行器

```python
class Reflector:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.analyzer = ExecutionAnalyzer(storage)
        self.issue_identifier = IssueIdentifier()
        self.insight_generator = InsightGenerator(storage)
        
    async def reflect(
        self,
        context: ReflectionContext,
        reflection_type: ReflectionType = ReflectionType.POST_EXECUTION
    ) -> ReflectionReport:
        # 执行分析
        analysis = await self.analyzer.analyze(context)
        
        # 识别问题
        issues = await self.issue_identifier.identify(context)
        
        # 生成洞察
        insights = await self.insight_generator.generate(
            context, analysis, issues
        )
        
        # 计算总体评分
        overall_score = self._calculate_overall_score(
            analysis, issues
        )
        
        # 确定改进优先级
        improvement_priority = self._prioritize_improvements(
            issues, insights
        )
        
        report = ReflectionReport(
            report_id=str(uuid.uuid4()),
            context=context,
            issues=issues,
            insights=insights,
            overall_score=overall_score,
            improvement_priority=improvement_priority,
            created_at=datetime.now()
        )
        
        # 持久化存储
        await self.storage.save("reflection_reports", report)
        
        # 触发学习
        await self._trigger_learning(report)
        
        return report
        
    def _calculate_overall_score(
        self,
        analysis: Dict,
        issues: List[Issue]
    ) -> float:
        base_score = 1.0
        
        # 根据问题扣分
        for issue in issues:
            if issue.severity == IssueSeverity.CRITICAL:
                base_score -= 0.3
            elif issue.severity == IssueSeverity.HIGH:
                base_score -= 0.2
            elif issue.severity == IssueSeverity.MEDIUM:
                base_score -= 0.1
            elif issue.severity == IssueSeverity.LOW:
                base_score -= 0.05
                
        # 考虑性能分数
        performance_score = analysis["performance"]["efficiency_score"]
        quality_score = analysis["quality"]["quality_score"]
        
        final_score = (
            base_score * 0.4 + 
            performance_score * 0.3 + 
            quality_score * 0.3
        )
        
        return max(0.0, min(1.0, final_score))
        
    def _prioritize_improvements(
        self,
        issues: List[Issue],
        insights: List[Insight]
    ) -> List[str]:
        priorities = []
        
        # 按严重性排序问题
        sorted_issues = sorted(
            issues,
            key=lambda i: [
                IssueSeverity.CRITICAL,
                IssueSeverity.HIGH,
                IssueSeverity.MEDIUM,
                IssueSeverity.LOW
            ].index(i.severity)
        )
        
        for issue in sorted_issues[:5]:
            priorities.append(f"[{issue.severity.value}] {issue.suggested_fix}")
            
        # 添加高置信度洞察
        for insight in insights:
            if insight.confidence > 0.8 and insight.actionable:
                priorities.extend(insight.recommendations[:2])
                
        return list(dict.fromkeys(priorities))[:10]
        
    async def _trigger_learning(self, report: ReflectionReport):
        # 触发策略学习
        for insight in report.insights:
            if insight.actionable:
                await self.storage.save("learning_queue", {
                    "type": "insight",
                    "insight": insight,
                    "source_report": report.report_id,
                    "timestamp": datetime.now()
                })
```

## 反思触发条件

```yaml
triggers:
  post_execution:
    - task_completed
    - task_failed
    - error_occurred
    
  periodic:
    - schedule: "0 0 * * *"  # 每日
      scope: "daily_summary"
    - schedule: "0 0 * * 0"  # 每周
      scope: "weekly_review"
      
  threshold_based:
    - metric: "success_rate"
      condition: "< 0.8"
      action: "deep_dive_reflection"
    - metric: "error_rate"
      condition: "> 0.2"
      action: "error_analysis"
```

## 最佳实践

1. **及时反思**: 任务完成后立即反思
2. **深度分析**: 不只看表面，深挖根因
3. **行动导向**: 反思结果要可执行
4. **知识沉淀**: 将洞察转化为知识
5. **持续改进**: 反思-改进-验证循环

## 相关技能

- [strategy-learner](./strategy-learner) - 策略学习
- [self-enhancer](./self-enhancer) - 自我增强
- [knowledge-base](./knowledge-base) - 知识库
