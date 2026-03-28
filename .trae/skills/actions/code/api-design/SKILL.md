---
name: api-design
description: "RESTful and GraphQL API design expert for endpoints, authentication, versioning, and documentation. Keywords: api, rest, graphql, endpoint, authentication, openapi"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - backend-skills
capabilities:
  - rest_api_design
  - graphql_schema
  - authentication_design
  - api_versioning
  - documentation
---

# API Design

RESTful和GraphQL API设计专家。

## 适用场景

- 设计新的API端点
- 实现RESTful规范
- GraphQL Schema设计
- API版本控制
- 认证授权设计
- API文档生成

## RESTful API设计

### 资源命名

```
使用名词，不用动词: /users 而非 /getUsers
集合用复数: /users, /orders
使用kebab-case: /user-profiles
嵌套关系: /users/{id}/orders
```

### HTTP方法

```
GET    /users           # 列表
GET    /users/{id}      # 单个
POST   /users           # 创建
PUT    /users/{id}      # 替换
PATCH  /users/{id}      # 部分更新
DELETE /users/{id}      # 删除
```

### 状态码

```
200 OK              # 成功GET, PUT, PATCH
201 Created         # 成功POST
204 No Content      # 成功DELETE
400 Bad Request     # 无效输入
401 Unauthorized    # 需要认证
403 Forbidden       # 权限拒绝
404 Not Found       # 资源不存在
429 Too Many Requests # 限流
500 Internal Error  # 服务器错误
```

## 分页、过滤、排序

```
GET /users?page=1&limit=20
GET /users?status=active&role=admin
GET /users?sort=-created_at
GET /users?fields=id,name,email
```

## 认证设计

### JWT认证

```json
POST /auth/login
{ "email": "user@example.com", "password": "secret" }

Response:
{ "access_token": "eyJ...", "refresh_token": "eyJ...", "expires_in": 3600 }

API请求:
GET /users
Authorization: Bearer eyJ...
```

### 限流

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1648214400
```

## GraphQL Schema

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, page: Int, limit: Int): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
}

type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}
```

## 相关技能

- [backend-python](../../domains/backend/python) - Python后端
- [backend-nodejs](../../domains/backend/nodejs) - Node.js后端
- [security-auditor](../analysis/security-auditor) - 安全审计
