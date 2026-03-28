---
name: self-enhancer
description: "Self-improvement system for autonomous capability enhancement and skill evolution. Keywords: self-improvement, enhancement, evolution, capability, 自我增强"
layer: learning
role: enhancer
version: 2.0.0
invokes:
  - strategy-learner
  - knowledge-base
invoked_by:
  - reflector
capabilities:
  - capability_enhancement
  - skill_evolution
  - prompt_optimization
  - workflow_improvement
triggers:
  keywords:
    - enhance
    - improve
    - evolve
    - upgrade
    - 增强
    - 进化
metrics:
  enhancements_applied: 150
  capability_growth: 0.25
  prompt_improvements: 80
---

# Self Enhancer

自我增强系统，实现自主能力提升和技能进化。

## 目的

实现持续自我改进：
- 能力增强：增强核心能力
- 技能进化：进化技能体系
- Prompt优化：优化提示词
- 工作流改进：改进工作流程

## 核心组件

### 1. 增强目标定义

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class EnhancementType(Enum):
    CAPABILITY = "capability"      # 能力增强
    SKILL = "skill"               # 技能进化
    PROMPT = "prompt"             # Prompt优化
    WORKFLOW = "workflow"         # 工作流改进
    PERFORMANCE = "performance"   # 性能优化

@dataclass
class EnhancementGoal:
    goal_id: str
    type: EnhancementType
    target: str
    current_state: Dict[str, Any]
    desired_state: Dict[str, Any]
    priority: int
    status: str
    created_at: datetime
    progress: float = 0.0
    
@dataclass
class EnhancementPlan:
    plan_id: str
    goal: EnhancementGoal
    steps: List[Dict[str, Any]]
    estimated_effort: float
    expected_improvement: float
    risks: List[str]
    created_at: datetime
```

### 2. 能力评估器

```python
class CapabilityAssessor:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.capability_metrics = {}
        
    async def assess(self, capability: str) -> Dict[str, float]:
        """评估特定能力"""
        # 获取历史执行数据
        executions = await self.storage.query(
            "learning_records",
            {"capability": capability}
        )
        
        if not executions:
            return {"score": 0.5, "confidence": 0.0}
            
        # 计算各项指标
        success_rate = sum(
            1 for e in executions if e["result_quality"] > 0.7
        ) / len(executions)
        
        avg_quality = sum(e["result_quality"] for e in executions) / len(executions)
        
        improvement_trend = self._calculate_trend(executions)
        
        return {
            "score": avg_quality,
            "success_rate": success_rate,
            "trend": improvement_trend,
            "sample_count": len(executions),
            "confidence": min(len(executions) / 50, 1.0)
        }
        
    async def identify_gaps(self) -> List[Dict]:
        """识别能力差距"""
        gaps = []
        
        # 获取所有能力定义
        capabilities = await self._get_capability_definitions()
        
        for cap in capabilities:
            current = await self.assess(cap["name"])
            
            if current["score"] < cap["target_score"]:
                gaps.append({
                    "capability": cap["name"],
                    "current_score": current["score"],
                    "target_score": cap["target_score"],
                    "gap": cap["target_score"] - current["score"],
                    "priority": self._calculate_priority(current, cap)
                })
                
        return sorted(gaps, key=lambda x: x["priority"], reverse=True)
        
    def _calculate_trend(self, executions: List) -> float:
        if len(executions) < 5:
            return 0.0
            
        recent = executions[-5:]
        older = executions[:-5]
        
        recent_avg = sum(e["result_quality"] for e in recent) / len(recent)
        older_avg = sum(e["result_quality"] for e in older) / len(older)
        
        return recent_avg - older_avg
```

### 3. 增强规划器

```python
class EnhancementPlanner:
    def __init__(
        self,
        storage: PersistentStorage,
        assessor: CapabilityAssessor
    ):
        self.storage = storage
        self.assessor = assessor
        
    async def create_enhancement_plan(
        self,
        gap: Dict
    ) -> EnhancementPlan:
        goal = EnhancementGoal(
            goal_id=str(uuid.uuid4()),
            type=EnhancementType.CAPABILITY,
            target=gap["capability"],
            current_state={"score": gap["current_score"]},
            desired_state={"score": gap["target_score"]},
            priority=gap["priority"],
            status="planned",
            created_at=datetime.now()
        )
        
        steps = await self._generate_steps(goal)
        
        return EnhancementPlan(
            plan_id=str(uuid.uuid4()),
            goal=goal,
            steps=steps,
            estimated_effort=sum(s.get("effort", 1) for s in steps),
            expected_improvement=gap["gap"],
            risks=await self._identify_risks(goal),
            created_at=datetime.now()
        )
        
    async def _generate_steps(
        self,
        goal: EnhancementGoal
    ) -> List[Dict]:
        steps = []
        
        if goal.type == EnhancementType.PROMPT:
            steps = await self._generate_prompt_steps(goal)
        elif goal.type == EnhancementType.WORKFLOW:
            steps = await self._generate_workflow_steps(goal)
        elif goal.type == EnhancementType.SKILL:
            steps = await self._generate_skill_steps(goal)
        else:
            steps = await self._generate_capability_steps(goal)
            
        return steps
        
    async def _generate_prompt_steps(
        self,
        goal: EnhancementGoal
    ) -> List[Dict]:
        return [
            {
                "step": 1,
                "action": "analyze_current_prompt",
                "description": "分析当前Prompt效果",
                "effort": 1
            },
            {
                "step": 2,
                "action": "identify_improvement_areas",
                "description": "识别改进点",
                "effort": 2
            },
            {
                "step": 3,
                "action": "generate_variations",
                "description": "生成Prompt变体",
                "effort": 2
            },
            {
                "step": 4,
                "action": "test_variations",
                "description": "测试变体效果",
                "effort": 3
            },
            {
                "step": 5,
                "action": "select_best",
                "description": "选择最优变体",
                "effort": 1
            },
            {
                "step": 6,
                "action": "deploy_improvement",
                "description": "部署改进",
                "effort": 1
            }
        ]
```

### 4. Prompt优化器

```python
class PromptOptimizer:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.variation_strategies = [
            "add_examples",
            "add_constraints",
            "restructure",
            "simplify",
            "add_context",
            "change_tone"
        ]
        
    async def optimize(
        self,
        prompt_id: str,
        performance_data: Dict
    ) -> Dict:
        # 获取当前Prompt
        current = await self._get_prompt(prompt_id)
        
        # 分析问题
        issues = self._analyze_issues(current, performance_data)
        
        # 生成变体
        variations = await self._generate_variations(current, issues)
        
        # 测试变体
        results = await self._test_variations(variations)
        
        # 选择最优
        best = self._select_best(results)
        
        return {
            "original": current,
            "best_variation": best["prompt"],
            "improvement": best["improvement"],
            "all_results": results
        }
        
    async def _generate_variations(
        self,
        prompt: str,
        issues: List[str]
    ) -> List[Dict]:
        variations = []
        
        for strategy in self.variation_strategies:
            if self._is_applicable(strategy, issues):
                variation = await self._apply_strategy(prompt, strategy)
                variations.append({
                    "strategy": strategy,
                    "prompt": variation
                })
                
        return variations
        
    async def _apply_strategy(
        self,
        prompt: str,
        strategy: str
    ) -> str:
        strategies = {
            "add_examples": self._add_examples,
            "add_constraints": self._add_constraints,
            "restructure": self._restructure,
            "simplify": self._simplify,
            "add_context": self._add_context,
            "change_tone": self._change_tone
        }
        
        return await strategies[strategy](prompt)
        
    async def _add_examples(self, prompt: str) -> str:
        example_prompt = f"""
{prompt}

## 示例

### 示例1
输入: [示例输入]
输出: [示例输出]

### 示例2
输入: [示例输入]
输出: [示例输出]
"""
        return example_prompt
        
    async def _add_constraints(self, prompt: str) -> str:
        constraint_prompt = f"""
{prompt}

## 约束条件
1. 输出必须符合指定格式
2. 避免冗余信息
3. 确保逻辑一致性
4. 保持专业术语准确
"""
        return constraint_prompt
```

### 5. 工作流改进器

```python
class WorkflowImprover:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        
    async def analyze_workflow(
        self,
        workflow_id: str
    ) -> Dict:
        # 获取工作流执行历史
        history = await self.storage.query(
            "workflow_executions",
            {"workflow_id": workflow_id}
        )
        
        # 分析瓶颈
        bottlenecks = self._find_bottlenecks(history)
        
        # 分析失败点
        failure_points = self._find_failure_points(history)
        
        # 分析资源使用
        resource_usage = self._analyze_resources(history)
        
        return {
            "bottlenecks": bottlenecks,
            "failure_points": failure_points,
            "resource_usage": resource_usage,
            "improvement_suggestions": self._generate_suggestions(
                bottlenecks, failure_points, resource_usage
            )
        }
        
    async def suggest_improvements(
        self,
        analysis: Dict
    ) -> List[Dict]:
        suggestions = []
        
        # 针对瓶颈的建议
        for bottleneck in analysis["bottlenecks"]:
            suggestions.append({
                "type": "bottleneck",
                "target": bottleneck["step"],
                "suggestion": "考虑并行化或优化算法",
                "expected_improvement": bottleneck["time_saved"],
                "effort": 3
            })
            
        # 针对失败点的建议
        for failure in analysis["failure_points"]:
            suggestions.append({
                "type": "reliability",
                "target": failure["step"],
                "suggestion": "添加重试机制或错误处理",
                "expected_improvement": failure["failure_rate"] * 0.5,
                "effort": 2
            })
            
        return suggestions
```

### 6. 自我增强执行器

```python
class SelfEnhancer:
    def __init__(self, storage: PersistentStorage):
        self.storage = storage
        self.assessor = CapabilityAssessor(storage)
        self.planner = EnhancementPlanner(storage, self.assessor)
        self.prompt_optimizer = PromptOptimizer(storage)
        self.workflow_improver = WorkflowImprover(storage)
        
    async def run_enhancement_cycle(self):
        """执行增强循环"""
        # 识别差距
        gaps = await self.assessor.identify_gaps()
        
        # 创建增强计划
        plans = []
        for gap in gaps[:5]:  # 优先处理前5个
            plan = await self.planner.create_enhancement_plan(gap)
            plans.append(plan)
            
        # 执行计划
        results = []
        for plan in plans:
            result = await self._execute_plan(plan)
            results.append(result)
            
        return {
            "gaps_identified": len(gaps),
            "plans_created": len(plans),
            "executions": results
        }
        
    async def _execute_plan(
        self,
        plan: EnhancementPlan
    ) -> Dict:
        execution_log = []
        
        for step in plan.steps:
            try:
                result = await self._execute_step(step)
                execution_log.append({
                    "step": step["step"],
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                execution_log.append({
                    "step": step["step"],
                    "status": "failed",
                    "error": str(e)
                })
                break
                
        return {
            "plan_id": plan.plan_id,
            "goal": plan.goal.target,
            "execution_log": execution_log,
            "completed": len([l for l in execution_log if l["status"] == "success"]),
            "total_steps": len(plan.steps)
        }
        
    async def _execute_step(self, step: Dict) -> Dict:
        actions = {
            "analyze_current_prompt": self._analyze_prompt,
            "generate_variations": self._generate_variations,
            "test_variations": self._test_variations,
            "deploy_improvement": self._deploy_improvement
        }
        
        action = step.get("action")
        if action in actions:
            return await actions[action](step)
            
        return {"status": "unknown_action"}
```

## 增强循环配置

```yaml
enhancement_cycle:
  schedule: "0 0 * * 0"  # 每周日执行
  
  phases:
    - name: "评估阶段"
      duration: "1h"
      actions:
        - assess_capabilities
        - identify_gaps
        - prioritize_improvements
        
    - name: "规划阶段"
      duration: "2h"
      actions:
        - create_enhancement_plans
        - estimate_effort
        - identify_risks
        
    - name: "执行阶段"
      duration: "4h"
      actions:
        - execute_plans
        - monitor_progress
        - handle_failures
        
    - name: "验证阶段"
      duration: "1h"
      actions:
        - verify_improvements
        - collect_metrics
        - update_knowledge
```

## 最佳实践

1. **渐进增强**: 小步迭代，持续改进
2. **数据驱动**: 基于数据做决策
3. **风险控制**: 评估并控制风险
4. **效果验证**: 验证增强效果
5. **知识沉淀**: 记录增强经验

## 相关技能

- [reflector](./reflector) - 反思系统
- [strategy-learner](./strategy-learner) - 策略学习
- [knowledge-base](./knowledge-base) - 知识库
