---
name: redis-caching
description: "Redis caching expert for caching strategies, data structures, distributed locks, and rate limiting. Keywords: redis, cache, rate-limit, session, distributed-lock"
layer: domain
role: specialist
version: 2.0.0
domain: database
invoked_by:
  - coding-workflow
  - backend-python
  - backend-nodejs
capabilities:
  - caching_strategies
  - rate_limiting
  - session_management
  - distributed_locks
  - pub_sub
---

# Redis Caching

Redis缓存专家。

## 适用场景

- 实现缓存策略
- 使用Redis数据结构
- 会话管理
- 限流
- 分布式锁

## 连接设置

```typescript
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: 6379
});
```

## 缓存模式

### Cache-Aside

```typescript
async function getUser(id: string) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  
  const user = await db.query('SELECT * FROM users WHERE id = $1', [id]);
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  return user;
}
```

### 限流

```typescript
async function rateLimit(key: string, limit: number, windowSeconds: number) {
  const current = await redis.incr(key);
  if (current === 1) await redis.expire(key, windowSeconds);
  return { allowed: current <= limit, remaining: limit - current };
}
```

### 分布式锁

```typescript
async function acquireLock(key: string, ttlMs: number) {
  const token = crypto.randomUUID();
  const acquired = await redis.set(key, token, 'PX', ttlMs, 'NX');
  return acquired === 'OK' ? token : null;
}
```

## 数据结构

```typescript
// Strings
await redis.set('key', 'value');
await redis.setex('key', 3600, 'value');

// Hashes
await redis.hset('user:1', 'name', 'John');

// Lists
await redis.lpush('queue', 'item');

// Sorted Sets
await redis.zadd('leaderboard', 100, 'user1');
```

## 相关技能

- [database-migration](../database-migration) - 数据库迁移
- [sql-optimization](../sql-optimization) - SQL优化
