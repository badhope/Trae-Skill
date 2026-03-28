---
name: concurrency-manager
description: "Manages concurrent task execution with rate limiting, queuing, and resource allocation. Keywords: concurrency, rate limit, queue, parallel, 并发管理"
layer: dispatcher
role: manager
version: 2.0.0
invokes: []
invoked_by:
  - model-router
  - task-planner
capabilities:
  - rate_limiting
  - request_queuing
  - parallel_execution
  - resource_allocation
triggers:
  keywords:
    - concurrent
    - parallel
    - queue
    - rate limit
    - throttle
metrics:
  max_concurrent: 100
  avg_queue_time: 200ms
  throughput: 1000 req/min
---

# Concurrency Manager

并发任务管理器，实现速率限制、请求队列和资源分配。

## 目的

管理并发任务执行：
- 速率限制：控制API调用频率
- 请求队列：有序处理请求
- 并行执行：最大化吞吐量
- 资源分配：合理分配计算资源

## 核心组件

### 1. 速率限制器

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
import asyncio

@dataclass
class RateLimit:
    requests_per_minute: int
    tokens_per_minute: int
    
class RateLimiter:
    def __init__(self, limits: Dict[str, RateLimit]):
        self.limits = limits
        self.request_history = defaultdict(deque)
        self.token_history = defaultdict(deque)
        self.lock = asyncio.Lock()
        
    async def acquire(self, model: str, tokens: int) -> bool:
        async with self.lock:
            now = datetime.now()
            limit = self.limits.get(model)
            
            if not limit:
                return True
                
            # 清理过期记录
            self._cleanup(model, now)
            
            # 检查请求限制
            if len(self.request_history[model]) >= limit.requests_per_minute:
                return False
                
            # 检查Token限制
            total_tokens = sum(self.token_history[model]) + tokens
            if total_tokens > limit.tokens_per_minute:
                return False
                
            # 记录本次请求
            self.request_history[model].append(now)
            self.token_history[model].append(tokens)
            return True
            
    def _cleanup(self, model: str, now: datetime):
        cutoff = now - timedelta(minutes=1)
        
        while self.request_history[model] and \
              self.request_history[model][0] < cutoff:
            self.request_history[model].popleft()
            
        while self.token_history[model] and \
              self.token_history[model][0] < cutoff:
            self.token_history[model].popleft()
```

### 2. 优先级队列

```python
from enum import IntEnum
import heapq

class Priority(IntEnum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3

@dataclass(order=True)
class QueuedTask:
    priority: int
    timestamp: float
    task: Task = field(compare=False)
    
class TaskQueue:
    def __init__(self, max_size: int = 1000):
        self.queue = []
        self.max_size = max_size
        self.not_empty = asyncio.Condition()
        
    async def enqueue(self, task: Task, priority: Priority) -> bool:
        if len(self.queue) >= self.max_size:
            return False
            
        queued = QueuedTask(
            priority=priority,
            timestamp=time.time(),
            task=task
        )
        
        heapq.heappush(self.queue, queued)
        
        async with self.not_empty:
            self.not_empty.notify()
            
        return True
        
    async def dequeue(self, timeout: float = 30.0) -> Optional[Task]:
        async with self.not_empty:
            start = time.time()
            
            while not self.queue:
                remaining = timeout - (time.time() - start)
                if remaining <= 0:
                    return None
                await asyncio.wait_for(
                    self.not_empty.wait(),
                    timeout=remaining
                )
                
        return heapq.heappop(self.queue).task
```

### 3. 并行执行器

```python
class ParallelExecutor:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.semaphore = asyncio.Semaphore(max_workers)
        self.active_tasks = {}
        
    async def execute_batch(
        self,
        tasks: List[Task],
        executor: Callable
    ) -> List[Result]:
        async def run_with_semaphore(task: Task) -> Result:
            async with self.semaphore:
                task_id = str(uuid.uuid4())
                self.active_tasks[task_id] = task
                
                try:
                    result = await executor(task)
                    return Result(success=True, data=result)
                except Exception as e:
                    return Result(success=False, error=str(e))
                finally:
                    del self.active_tasks[task_id]
                    
        return await asyncio.gather(
            *[run_with_semaphore(t) for t in tasks]
        )
        
    async def execute_dag(
        self,
        dag: TaskDAG,
        executor: Callable
    ) -> Dict[str, Result]:
        results = {}
        
        # 拓扑排序执行
        for level in dag.topological_levels():
            level_results = await self.execute_batch(
                [dag.nodes[n] for n in level],
                executor
            )
            results.update(dict(zip(level, level_results)))
            
        return results
```

### 4. 资源分配器

```python
@dataclass
class ResourcePool:
    total_memory: int
    total_compute: int
    used_memory: int = 0
    used_compute: int = 0
    
class ResourceAllocator:
    def __init__(self, pool: ResourcePool):
        self.pool = pool
        self.allocations = {}
        self.lock = asyncio.Lock()
        
    async def allocate(
        self,
        task_id: str,
        memory: int,
        compute: int
    ) -> bool:
        async with self.lock:
            if (self.pool.used_memory + memory > self.pool.total_memory or
                self.pool.used_compute + compute > self.pool.total_compute):
                return False
                
            self.pool.used_memory += memory
            self.pool.used_compute += compute
            self.allocations[task_id] = (memory, compute)
            return True
            
    async def release(self, task_id: str):
        async with self.lock:
            if task_id in self.allocations:
                memory, compute = self.allocations[task_id]
                self.pool.used_memory -= memory
                self.pool.used_compute -= compute
                del self.allocations[task_id]
```

## 完整管理器

```python
class ConcurrencyManager:
    def __init__(self, config: ConcurrencyConfig):
        self.rate_limiter = RateLimiter(config.rate_limits)
        self.queue = TaskQueue(config.max_queue_size)
        self.executor = ParallelExecutor(config.max_workers)
        self.allocator = ResourceAllocator(config.resource_pool)
        self.metrics = ConcurrencyMetrics()
        
    async def submit(
        self,
        task: Task,
        priority: Priority = Priority.MEDIUM
    ) -> Future[Result]:
        # 加入队列
        await self.queue.enqueue(task, priority)
        
        # 创建Future
        future = asyncio.Future()
        
        # 启动处理
        asyncio.create_task(self._process(task, future))
        
        return future
        
    async def _process(self, task: Task, future: asyncio.Future):
        try:
            # 等待速率限制
            while not await self.rate_limiter.acquire(
                task.model, task.estimated_tokens
            ):
                await asyncio.sleep(0.1)
                
            # 分配资源
            if not await self.allocator.allocate(
                task.id, task.memory_needed, task.compute_needed
            ):
                future.set_exception(ResourceExhaustedError())
                return
                
            # 执行任务
            result = await self.executor.execute(task)
            
            # 释放资源
            await self.allocator.release(task.id)
            
            # 设置结果
            future.set_result(result)
            
            # 记录指标
            self.metrics.record(task, result)
            
        except Exception as e:
            future.set_exception(e)
```

## 配置示例

```yaml
concurrency:
  max_workers: 20
  max_queue_size: 1000
  
  rate_limits:
    gpt-4o:
      requests_per_minute: 500
      tokens_per_minute: 30000
    claude-3-opus:
      requests_per_minute: 100
      tokens_per_minute: 20000
      
  resource_pool:
    total_memory: 16384  # MB
    total_compute: 100   # units
    
  priorities:
    - name: CRITICAL
      weight: 0
      examples: ["生产事故", "紧急修复"]
    - name: HIGH
      weight: 1
      examples: ["功能开发", "性能优化"]
    - name: MEDIUM
      weight: 2
      examples: ["代码审查", "文档更新"]
    - name: LOW
      weight: 3
      examples: ["日志清理", "归档任务"]
```

## 最佳实践

1. **优先级设置**: 合理设置任务优先级
2. **队列监控**: 监控队列深度和等待时间
3. **资源预留**: 为关键任务预留资源
4. **优雅降级**: 资源不足时的降级策略
5. **指标追踪**: 持续监控并发指标

## 相关技能

- [model-router](./model-router) - 模型路由
- [load-balancer](./load-balancer) - 负载均衡
- [task-registry](../meta/task-registry) - 任务注册
