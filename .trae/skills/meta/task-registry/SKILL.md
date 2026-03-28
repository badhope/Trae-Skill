---
name: task-registry
description: "Persistent task registry for tracking task status, dependencies, and execution history. Keywords: registry, tracking, status, history, 任务注册"
layer: meta
role: registry
version: 2.0.0
invokes: []
invoked_by:
  - task-planner
  - decomposition-planner
  - orchestrator
capabilities:
  - task_tracking
  - dependency_management
  - history_persistence
  - status_monitoring
triggers:
  keywords:
    - register
    - track
    - status
    - history
    - 注册
    - 追踪
metrics:
  storage_type: "persistent"
  max_tasks: 100000
  query_latency: 10ms
---

# Task Registry

持久化任务注册中心，追踪任务状态、依赖关系和执行历史。

## 目的

实现任务全生命周期管理：
- 状态追踪：实时追踪任务状态
- 依赖管理：管理任务间依赖
- 历史持久化：持久化存储执行历史
- 监控告警：异常状态告警

## 数据模型

### 1. 任务记录Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TaskRecord",
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "唯一任务标识"
    },
    "parent_id": {
      "type": ["string", "null"],
      "description": "父任务ID"
    },
    "name": {
      "type": "string",
      "description": "任务名称"
    },
    "description": {
      "type": "string",
      "description": "任务描述"
    },
    "status": {
      "type": "string",
      "enum": ["pending", "queued", "running", "completed", "failed", "cancelled", "retrying"],
      "description": "任务状态"
    },
    "priority": {
      "type": "integer",
      "minimum": 0,
      "maximum": 3,
      "description": "优先级 0=CRITICAL, 1=HIGH, 2=MEDIUM, 3=LOW"
    },
    "complexity": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "description": "复杂度评分"
    },
    "dependencies": {
      "type": "array",
      "items": {"type": "string"},
      "description": "依赖任务ID列表"
    },
    "dependents": {
      "type": "array",
      "items": {"type": "string"},
      "description": "被依赖任务ID列表"
    },
    "assigned_agent": {
      "type": ["string", "null"],
      "description": "分配的代理"
    },
    "assigned_model": {
      "type": ["string", "null"],
      "description": "分配的模型"
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "创建时间"
    },
    "started_at": {
      "type": ["string", "null"],
      "format": "date-time",
      "description": "开始时间"
    },
    "completed_at": {
      "type": ["string", "null"],
      "format": "date-time",
      "description": "完成时间"
    },
    "estimated_duration": {
      "type": "number",
      "description": "预估时长(分钟)"
    },
    "actual_duration": {
      "type": ["number", "null"],
      "description": "实际时长(分钟)"
    },
    "estimated_tokens": {
      "type": "integer",
      "description": "预估Token数"
    },
    "actual_tokens": {
      "type": ["integer", "null"],
      "description": "实际Token数"
    },
    "result": {
      "type": ["object", "null"],
      "description": "执行结果"
    },
    "error": {
      "type": ["string", "null"],
      "description": "错误信息"
    },
    "retry_count": {
      "type": "integer",
      "minimum": 0,
      "description": "重试次数"
    },
    "max_retries": {
      "type": "integer",
      "minimum": 0,
      "maximum": 5,
      "description": "最大重试次数"
    },
    "metadata": {
      "type": "object",
      "description": "扩展元数据"
    }
  },
  "required": ["task_id", "name", "status", "priority", "created_at"]
}
```

### 2. 任务状态机

```python
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "pending"        # 等待执行
    QUEUED = "queued"          # 已入队列
    RUNNING = "running"        # 执行中
    COMPLETED = "completed"    # 已完成
    FAILED = "failed"          # 失败
    CANCELLED = "cancelled"    # 已取消
    RETRYING = "retrying"      # 重试中

class TaskStateMachine:
    TRANSITIONS = {
        TaskStatus.PENDING: [TaskStatus.QUEUED, TaskStatus.CANCELLED],
        TaskStatus.QUEUED: [TaskStatus.RUNNING, TaskStatus.CANCELLED],
        TaskStatus.RUNNING: [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.RETRYING],
        TaskStatus.FAILED: [TaskStatus.RETRYING, TaskStatus.CANCELLED],
        TaskStatus.RETRYING: [TaskStatus.QUEUED, TaskStatus.CANCELLED],
        TaskStatus.COMPLETED: [],
        TaskStatus.CANCELLED: []
    }
    
    @classmethod
    def can_transition(
        cls, 
        from_status: TaskStatus, 
        to_status: TaskStatus
    ) -> bool:
        return to_status in cls.TRANSITIONS.get(from_status, [])
        
    @classmethod
    def get_valid_transitions(
        cls, 
        status: TaskStatus
    ) -> list:
        return cls.TRANSITIONS.get(status, [])
```

### 3. 持久化存储

```python
import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

class TaskRegistry:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self._init_db()
        
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
            
    def _init_db(self):
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    parent_id TEXT,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    complexity INTEGER,
                    dependencies TEXT,
                    dependents TEXT,
                    assigned_agent TEXT,
                    assigned_model TEXT,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    estimated_duration REAL,
                    actual_duration REAL,
                    estimated_tokens INTEGER,
                    actual_tokens INTEGER,
                    result TEXT,
                    error TEXT,
                    retry_count INTEGER DEFAULT 0,
                    max_retries INTEGER DEFAULT 3,
                    metadata TEXT,
                    FOREIGN KEY (parent_id) REFERENCES tasks(task_id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_status ON tasks(status);
                CREATE INDEX IF NOT EXISTS idx_parent ON tasks(parent_id);
                CREATE INDEX IF NOT EXISTS idx_created ON tasks(created_at);
                CREATE INDEX IF NOT EXISTS idx_agent ON tasks(assigned_agent);
                
                CREATE TABLE IF NOT EXISTS task_history (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    old_status TEXT,
                    new_status TEXT,
                    timestamp TEXT NOT NULL,
                    details TEXT,
                    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_history_task ON task_history(task_id);
            """)
            
    async def register(self, task: TaskRecord) -> str:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO tasks (
                    task_id, parent_id, name, description, status, priority,
                    complexity, dependencies, dependents, assigned_agent,
                    assigned_model, created_at, estimated_duration,
                    estimated_tokens, max_retries, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id, task.parent_id, task.name, task.description,
                task.status, task.priority, task.complexity,
                json.dumps(task.dependencies), json.dumps(task.dependents),
                task.assigned_agent, task.assigned_model,
                task.created_at.isoformat(), task.estimated_duration,
                task.estimated_tokens, task.max_retries,
                json.dumps(task.metadata)
            ))
            
            self._record_history(
                conn, task.task_id, None, task.status, "Task registered"
            )
            
        return task.task_id
        
    async def update_status(
        self, 
        task_id: str, 
        new_status: TaskStatus,
        details: Optional[dict] = None
    ) -> bool:
        with self._get_connection() as conn:
            # 获取当前状态
            row = conn.execute(
                "SELECT status FROM tasks WHERE task_id = ?",
                (task_id,)
            ).fetchone()
            
            if not row:
                return False
                
            old_status = TaskStatus(row["status"])
            
            # 验证状态转换
            if not TaskStateMachine.can_transition(old_status, new_status):
                return False
                
            # 更新状态
            update_fields = ["status = ?"]
            params = [new_status.value]
            
            if new_status == TaskStatus.RUNNING:
                update_fields.append("started_at = ?")
                params.append(datetime.now().isoformat())
            elif new_status == TaskStatus.COMPLETED:
                update_fields.append("completed_at = ?")
                params.append(datetime.now().isoformat())
                
            params.append(task_id)
            
            conn.execute(
                f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = ?",
                params
            )
            
            # 记录历史
            self._record_history(
                conn, task_id, old_status.value, new_status.value,
                json.dumps(details) if details else None
            )
            
        return True
        
    def _record_history(
        self, 
        conn, 
        task_id: str, 
        old_status: Optional[str],
        new_status: str,
        details: Optional[str]
    ):
        conn.execute("""
            INSERT INTO task_history (task_id, old_status, new_status, timestamp, details)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, old_status, new_status, datetime.now().isoformat(), details))
```

### 4. 查询接口

```python
class TaskQuery:
    def __init__(self, registry: TaskRegistry):
        self.registry = registry
        
    async def get_by_id(self, task_id: str) -> Optional[TaskRecord]:
        with self.registry._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM tasks WHERE task_id = ?",
                (task_id,)
            ).fetchone()
            
            return self._row_to_record(row) if row else None
            
    async def get_children(self, task_id: str) -> List[TaskRecord]:
        with self.registry._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE parent_id = ?",
                (task_id,)
            ).fetchall()
            
            return [self._row_to_record(row) for row in rows]
            
    async def get_by_status(
        self, 
        status: TaskStatus,
        limit: int = 100
    ) -> List[TaskRecord]:
        with self.registry._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY created_at LIMIT ?",
                (status.value, limit)
            ).fetchall()
            
            return [self._row_to_record(row) for row in rows]
            
    async def get_ready_tasks(self) -> List[TaskRecord]:
        """获取所有依赖已满足的待执行任务"""
        with self.registry._get_connection() as conn:
            rows = conn.execute("""
                SELECT t.* FROM tasks t
                WHERE t.status = 'pending'
                AND NOT EXISTS (
                    SELECT 1 FROM tasks dep
                    WHERE dep.task_id IN (
                        SELECT value FROM json_each(t.dependencies)
                    )
                    AND dep.status != 'completed'
                )
            """).fetchall()
            
            return [self._row_to_record(row) for row in rows]
            
    async def get_history(
        self, 
        task_id: str
    ) -> List[dict]:
        with self.registry._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM task_history WHERE task_id = ? ORDER BY timestamp",
                (task_id,)
            ).fetchall()
            
            return [dict(row) for row in rows]
            
    async def get_statistics(self) -> dict:
        with self.registry._get_connection() as conn:
            stats = {}
            
            # 按状态统计
            rows = conn.execute(
                "SELECT status, COUNT(*) as count FROM tasks GROUP BY status"
            ).fetchall()
            stats["by_status"] = {row["status"]: row["count"] for row in rows}
            
            # 按优先级统计
            rows = conn.execute(
                "SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority"
            ).fetchall()
            stats["by_priority"] = {row["priority"]: row["count"] for row in rows}
            
            # 平均执行时间
            row = conn.execute("""
                SELECT AVG(actual_duration) as avg_duration
                FROM tasks WHERE status = 'completed' AND actual_duration IS NOT NULL
            """).fetchone()
            stats["avg_duration"] = row["avg_duration"]
            
            # 成功率
            row = conn.execute("""
                SELECT 
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                    COUNT(*) as total
                FROM tasks
            """).fetchone()
            stats["success_rate"] = row["completed"] / row["total"] if row["total"] > 0 else 0
            
            return stats
```

### 5. 监控告警

```python
class TaskMonitor:
    def __init__(self, registry: TaskRegistry):
        self.registry = registry
        self.alerts = []
        
    async def check_health(self) -> dict:
        issues = []
        
        # 检查长时间运行的任务
        stuck_tasks = await self._find_stuck_tasks()
        if stuck_tasks:
            issues.append({
                "type": "stuck_tasks",
                "severity": "warning",
                "count": len(stuck_tasks),
                "tasks": stuck_tasks[:5]
            })
            
        # 检查失败率
        stats = await self.registry.query.get_statistics()
        if stats["success_rate"] < 0.8:
            issues.append({
                "type": "low_success_rate",
                "severity": "critical",
                "rate": stats["success_rate"]
            })
            
        # 检查队列积压
        pending = stats["by_status"].get("pending", 0)
        if pending > 100:
            issues.append({
                "type": "queue_backlog",
                "severity": "warning",
                "count": pending
            })
            
        return {
            "healthy": len([i for i in issues if i["severity"] == "critical"]) == 0,
            "issues": issues
        }
        
    async def _find_stuck_tasks(
        self, 
        threshold_minutes: int = 60
    ) -> List[str]:
        with self.registry._get_connection() as conn:
            rows = conn.execute("""
                SELECT task_id FROM tasks
                WHERE status = 'running'
                AND datetime(started_at) < datetime('now', ?)
            """, (f"-{threshold_minutes} minutes",)).fetchall()
            
            return [row["task_id"] for row in rows]
```

## 最佳实践

1. **及时更新**: 任务状态变化时立即更新
2. **历史追溯**: 保留完整执行历史
3. **定期清理**: 归档历史任务数据
4. **监控告警**: 实时监控异常状态
5. **数据备份**: 定期备份任务数据

## 相关技能

- [task-planner](./task-planner) - 任务规划
- [decomposition-planner](./decomposition-planner) - 任务分解
- [concurrency-manager](../dispatcher/concurrency-manager) - 并发管理
