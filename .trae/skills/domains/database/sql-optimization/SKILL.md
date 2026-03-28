---
name: sql-optimization
description: "SQL optimization expert for query optimization, index design, and execution plan analysis. Keywords: sql, optimization, index, query, performance, explain"
layer: domain
role: specialist
version: 2.0.0
domain: database
invoked_by:
  - coding-workflow
  - performance-optimizer
capabilities:
  - query_optimization
  - index_design
  - execution_analysis
  - performance_tuning
---

# SQL Optimization

SQL优化专家。

## 适用场景

- 优化慢查询
- 设计索引
- 分析执行计划
- 数据库性能调优

## 查询分析

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 123;
```

## 索引设计

```sql
-- 单列索引
CREATE INDEX idx_users_email ON users(email);

-- 复合索引（顺序重要！）
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 覆盖索引
CREATE INDEX idx_orders_user_status_date 
ON orders(user_id, status) 
INCLUDE (created_at, total);

-- 部分索引
CREATE INDEX idx_orders_pending ON orders(created_at)
WHERE status = 'pending';
```

## 查询优化

### 避免SELECT *

```sql
-- 差
SELECT * FROM users WHERE id = 1;

-- 好
SELECT id, name, email FROM users WHERE id = 1;
```

### 使用EXISTS代替IN

```sql
-- 差
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders);

-- 好
SELECT * FROM users u WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.user_id = u.id
);
```

### 分页优化

```sql
-- Keyset分页（高效）
SELECT * FROM orders WHERE id > 12345 ORDER BY id LIMIT 20;
```

## 监控查询

```sql
-- 查找慢查询
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 10;

-- 查找未使用的索引
SELECT schemaname, tablename, indexname
FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

## 相关技能

- [database-migration](../database-migration) - 数据库迁移
- [redis-caching](../redis-caching) - Redis缓存
