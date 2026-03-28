---
name: decomposition-planner
description: "Advanced task decomposition with dependency analysis, complexity assessment, and execution planning. Keywords: decomposition, planning, dependency, subtask, 任务分解"
layer: meta
role: planner
version: 2.0.0
invokes:
  - model-router
  - task-registry
invoked_by:
  - task-planner
capabilities:
  - task_decomposition
  - dependency_analysis
  - complexity_assessment
  - execution_planning
triggers:
  keywords:
    - decompose
    - breakdown
    - subtask
    - plan
    - 分解
    - 拆解
metrics:
  avg_decomposition_time: 500ms
  accuracy: 0.88
  avg_subtasks: 4.2
---

# Decomposition Planner

高级任务分解规划器，实现依赖分析、复杂度评估和执行计划生成。

## 目的

将复杂任务分解为可执行的子任务：
- 依赖分析：识别任务间依赖关系
- 复杂度评估：评估子任务复杂度
- 执行计划：生成最优执行顺序
- 资源估算：预估所需资源

## 核心算法

### 1. 任务分解策略

```python
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from enum import Enum

class DecompositionStrategy(Enum):
    SEQUENTIAL = "sequential"      # 顺序执行
    PARALLEL = "parallel"          # 并行执行
    HYBRID = "hybrid"              # 混合模式
    CONDITIONAL = "conditional"    # 条件分支

@dataclass
class SubTask:
    id: str
    name: str
    description: str
    dependencies: Set[str] = field(default_factory=set)
    complexity: int = 0
    estimated_time: float = 0.0
    estimated_tokens: int = 0
    assigned_agent: Optional[str] = None
    status: str = "pending"
    
@dataclass
class DecompositionPlan:
    task_id: str
    subtasks: Dict[str, SubTask]
    execution_order: List[List[str]]  # 按层级组织
    strategy: DecompositionStrategy
    total_complexity: int
    estimated_duration: float
    critical_path: List[str]
```

### 2. 分解规则引擎

```python
class DecompositionRules:
    def __init__(self):
        self.rules = self._load_rules()
        
    def _load_rules(self) -> Dict:
        return {
            "software_development": {
                "pattern": r"(开发|实现|构建|创建).*(系统|功能|模块)",
                "subtasks": [
                    {"name": "需求分析", "complexity": 3},
                    {"name": "架构设计", "complexity": 4},
                    {"name": "编码实现", "complexity": 5},
                    {"name": "单元测试", "complexity": 3},
                    {"name": "集成测试", "complexity": 3},
                    {"name": "文档编写", "complexity": 2}
                ],
                "dependencies": {
                    "架构设计": ["需求分析"],
                    "编码实现": ["架构设计"],
                    "单元测试": ["编码实现"],
                    "集成测试": ["单元测试"],
                    "文档编写": ["需求分析"]
                }
            },
            "bug_fixing": {
                "pattern": r"(修复|解决|debug).*(bug|问题|错误)",
                "subtasks": [
                    {"name": "问题复现", "complexity": 3},
                    {"name": "根因分析", "complexity": 4},
                    {"name": "修复实现", "complexity": 4},
                    {"name": "验证测试", "complexity": 3}
                ],
                "dependencies": {
                    "根因分析": ["问题复现"],
                    "修复实现": ["根因分析"],
                    "验证测试": ["修复实现"]
                }
            },
            "research": {
                "pattern": r"(研究|调研|分析).*(技术|方案|问题)",
                "subtasks": [
                    {"name": "信息收集", "complexity": 2},
                    {"name": "数据分析", "complexity": 4},
                    {"name": "结论总结", "complexity": 3},
                    {"name": "报告撰写", "complexity": 3}
                ],
                "dependencies": {
                    "数据分析": ["信息收集"],
                    "结论总结": ["数据分析"],
                    "报告撰写": ["结论总结"]
                }
            }
        }
        
    def match(self, task: Task) -> Optional[Dict]:
        for rule_name, rule in self.rules.items():
            if re.search(rule["pattern"], task.content, re.IGNORECASE):
                return rule
        return None
```

### 3. 依赖图构建

```python
class DependencyGraph:
    def __init__(self):
        self.nodes: Dict[str, SubTask] = {}
        self.edges: Dict[str, Set[str]] = defaultdict(set)
        
    def add_subtask(self, subtask: SubTask):
        self.nodes[subtask.id] = subtask
        for dep_id in subtask.dependencies:
            self.edges[dep_id].add(subtask.id)
            
    def topological_sort(self) -> List[List[str]]:
        """返回按层级组织的执行顺序"""
        in_degree = {n: 0 for n in self.nodes}
        
        for node in self.nodes:
            for dep in self.nodes[node].dependencies:
                in_degree[node] += 1
                
        levels = []
        current_level = [n for n, d in in_degree.items() if d == 0]
        
        while current_level:
            levels.append(current_level)
            next_level = []
            
            for node in current_level:
                for dependent in self.edges[node]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_level.append(dependent)
                        
            current_level = next_level
            
        return levels
        
    def find_critical_path(self) -> List[str]:
        """找到关键路径（最长路径）"""
        dp = {}
        
        def get_earliest_finish(node_id: str) -> float:
            if node_id in dp:
                return dp[node_id]
                
            subtask = self.nodes[node_id]
            if not subtask.dependencies:
                dp[node_id] = subtask.estimated_time
            else:
                max_dep_time = max(
                    get_earliest_finish(dep) 
                    for dep in subtask.dependencies
                )
                dp[node_id] = max_dep_time + subtask.estimated_time
                
            return dp[node_id]
            
        # 计算所有节点的最早完成时间
        for node_id in self.nodes:
            get_earliest_finish(node_id)
            
        # 回溯找到关键路径
        critical_path = []
        current = max(dp, key=dp.get)
        
        while current:
            critical_path.append(current)
            deps = self.nodes[current].dependencies
            
            if not deps:
                break
                
            current = max(deps, key=lambda d: dp[d])
            
        return list(reversed(critical_path))
```

### 4. 完整规划器

```python
class DecompositionPlanner:
    def __init__(self, storage: PersistentStorage):
        self.rules = DecompositionRules()
        self.storage = storage
        self.complexity_assessor = ComplexityAssessor()
        
    async def decompose(self, task: Task) -> DecompositionPlan:
        # 匹配分解规则
        rule = self.rules.match(task)
        
        if rule:
            subtasks = self._create_from_rule(task, rule)
        else:
            subtasks = await self._ai_decompose(task)
            
        # 构建依赖图
        graph = DependencyGraph()
        for subtask in subtasks.values():
            graph.add_subtask(subtask)
            
        # 计算执行顺序
        execution_order = graph.topological_sort()
        
        # 找到关键路径
        critical_path = graph.find_critical_path()
        
        # 计算总复杂度
        total_complexity = sum(s.complexity for s in subtasks.values())
        
        # 估算总时长
        estimated_duration = sum(
            max(subtasks[n].estimated_time for n in level)
            for level in execution_order
        )
        
        plan = DecompositionPlan(
            task_id=task.id,
            subtasks=subtasks,
            execution_order=execution_order,
            strategy=self._determine_strategy(execution_order),
            total_complexity=total_complexity,
            estimated_duration=estimated_duration,
            critical_path=critical_path
        )
        
        # 持久化存储
        await self.storage.save("decomposition_plans", plan)
        
        return plan
        
    def _create_from_rule(
        self, 
        task: Task, 
        rule: Dict
    ) -> Dict[str, SubTask]:
        subtasks = {}
        
        for i, st_def in enumerate(rule["subtasks"]):
            subtask = SubTask(
                id=f"{task.id}_{i}",
                name=st_def["name"],
                description=f"{task.content} - {st_def['name']}",
                complexity=st_def["complexity"],
                estimated_time=st_def["complexity"] * 2,  # 分钟
                estimated_tokens=st_def["complexity"] * 500
            )
            subtasks[subtask.id] = subtask
            
        # 设置依赖
        for name, deps in rule.get("dependencies", {}).items():
            st_id = next(
                k for k, v in subtasks.items() 
                if v.name == name
            )
            for dep_name in deps:
                dep_id = next(
                    k for k, v in subtasks.items() 
                    if v.name == dep_name
                )
                subtasks[st_id].dependencies.add(dep_id)
                
        return subtasks
        
    async def _ai_decompose(self, task: Task) -> Dict[str, SubTask]:
        """使用AI进行智能分解"""
        prompt = f"""
        请将以下任务分解为具体的子任务：
        
        任务：{task.content}
        
        请按以下格式输出：
        1. 子任务名称 | 复杂度(1-5) | 依赖的子任务编号
        
        示例：
        1. 需求分析 | 3 | 无
        2. 架构设计 | 4 | 1
        3. 编码实现 | 5 | 2
        """
        
        response = await self.llm.generate(prompt)
        return self._parse_ai_response(response, task)
        
    def _determine_strategy(
        self, 
        execution_order: List[List[str]]
    ) -> DecompositionStrategy:
        if len(execution_order) == 1:
            return DecompositionStrategy.PARALLEL
        elif all(len(level) == 1 for level in execution_order):
            return DecompositionStrategy.SEQUENTIAL
        else:
            return DecompositionStrategy.HYBRID
```

## 分解模板库

```yaml
templates:
  feature_development:
    name: "功能开发"
    subtasks:
      - id: requirements
        name: "需求分析"
        complexity: 3
        time: 30
      - id: design
        name: "技术设计"
        complexity: 4
        time: 45
        dependencies: [requirements]
      - id: implement
        name: "编码实现"
        complexity: 5
        time: 120
        dependencies: [design]
      - id: test
        name: "测试验证"
        complexity: 3
        time: 30
        dependencies: [implement]
      - id: document
        name: "文档更新"
        complexity: 2
        time: 15
        dependencies: [requirements]
        
  performance_optimization:
    name: "性能优化"
    subtasks:
      - id: profile
        name: "性能分析"
        complexity: 4
        time: 60
      - id: identify
        name: "瓶颈识别"
        complexity: 4
        time: 30
        dependencies: [profile]
      - id: optimize
        name: "优化实现"
        complexity: 5
        time: 90
        dependencies: [identify]
      - id: benchmark
        name: "基准测试"
        complexity: 3
        time: 30
        dependencies: [optimize]
```

## 最佳实践

1. **MECE原则**: 子任务相互独立、完全穷尽
2. **合理粒度**: 子任务复杂度3-5为宜
3. **明确依赖**: 清晰标注依赖关系
4. **预留缓冲**: 为关键路径预留时间
5. **动态调整**: 根据执行反馈调整计划

## 相关技能

- [task-planner](./task-planner) - 任务规划
- [task-registry](./task-registry) - 任务注册
- [model-router](../dispatcher/model-router) - 模型路由
- [aggregation-processor](../workflows/aggregation-processor) - 结果聚合
