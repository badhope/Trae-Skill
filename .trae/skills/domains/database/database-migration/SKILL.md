---
name: database-migration
description: "Database migration expert for schema changes, data migrations, rollback strategies, and migration tools. Keywords: migration, database, schema, flyway, prisma, liquibase"
layer: domain
role: specialist
version: 2.0.0
domain: database
invoked_by:
  - coding-workflow
  - deployment-workflow
capabilities:
  - schema_migration
  - data_migration
  - rollback_strategy
  - tool_configuration
---

# Database Migration

数据库迁移专家。

## 适用场景

- 创建数据库Schema迁移
- 执行数据迁移
- 管理迁移版本控制
- 设置迁移工具
- 处理回滚场景

## 迁移原则

- 迁移应该是可逆的
- 每个迁移应该是原子的
- 永远不要修改已存在的迁移
- 先在staging测试
- 迁移前备份

## Prisma (Node.js)

```bash
npx prisma migrate dev --name add_user_table
npx prisma migrate deploy
```

## Flyway (Java)

```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);
```

```bash
flyway migrate
flyway info
```

## Django (Python)

```bash
python manage.py makemigrations
python manage.py migrate
```

## 安全迁移模式

### 非锁定迁移

```sql
-- PostgreSQL
ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active';
CREATE INDEX CONCURRENTLY idx_users_status ON users(status);
```

### 零停机迁移

```sql
-- 1. 添加新列
ALTER TABLE users ADD COLUMN new_email VARCHAR(255);

-- 2. 回填数据
UPDATE users SET new_email = email;

-- 3. 添加约束
ALTER TABLE users ALTER COLUMN new_email SET NOT NULL;

-- 4. 切换应用

-- 5. 删除旧列
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN new_email TO email;
```

## 相关技能

- [sql-optimization](../sql-optimization) - SQL优化
- [redis-caching](../redis-caching) - Redis缓存
- [backend-python](../backend/python) - Python后端
