---
name: graphql
description: "GraphQL API development for flexible and efficient data querying. Keywords: graphql, apollo, schema, resolver, mutation, query, graphql api"
layer: domain
role: specialist
version: 2.0.0
domain: backend
languages:
  - typescript
  - python
frameworks:
  - apollo-server
  - graphql-python
  - hasura
invoked_by:
  - coding-workflow
  - api-design
capabilities:
  - schema_design
  - resolver_implementation
  - query_optimization
  - subscription_handling
triggers:
  keywords:
    - graphql
    - apollo
    - schema
    - resolver
    - mutation
    - query
    - subscription
metrics:
  avg_execution_time: 4s
  success_rate: 0.94
  api_quality: 0.90
---

# GraphQL

GraphQL API开发，用于灵活高效的数据查询。

## 目的

提供GraphQL开发的最佳实践：
- Schema设计
- Resolver实现
- 查询优化
- 订阅处理

## 能力

- **Schema设计**: 设计GraphQL Schema
- **Resolver实现**: 实现数据解析器
- **查询优化**: 优化查询性能
- **订阅处理**: 实现实时订阅

## GraphQL vs REST

| 特性 | GraphQL | REST |
|------|---------|------|
| 数据获取 | 按需获取 | 固定结构 |
| 接口数量 | 单一端点 | 多端点 |
| 版本管理 | 无需版本 | 需要版本 |
| 学习曲线 | 较陡 | 平缓 |

## Schema定义

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: DateTime!
}

type Query {
  users: [User!]!
  user(id: ID!): User
  posts: [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  onUserCreated: User!
}

input CreateUserInput {
  name: String!
  email: String!
}

input UpdateUserInput {
  name: String
  email: String
}
```

## Apollo Server (Node.js)

```typescript
import { ApolloServer, gql } from 'apollo-server';

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
  }

  type Mutation {
    createUser(name: String!, email: String!): User!
  }
`;

const resolvers = {
  Query: {
    users: () => users,
    user: (_, { id }) => users.find(u => u.id === id),
  },
  Mutation: {
    createUser: (_, { name, email }) => {
      const user = { id: Date.now().toString(), name, email };
      users.push(user);
      return user;
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });
server.listen().then(({ url }) => console.log(`Server at ${url}`));
```

## Ariadne (Python)

```python
from ariadne import QueryType, make_executable_schema, graphql_sync

type_defs = """
    type User {
        id: ID!
        name: String!
        email: String!
    }
    
    type Query {
        users: [User!]!
        user(id: ID!): User
    }
"""

query = QueryType()

@query.field("users")
def resolve_users(_, info):
    return get_users()

@query.field("user")
def resolve_user(_, info, id):
    return get_user_by_id(id)

schema = make_executable_schema(type_defs, query)
```

## DataLoader批处理

```typescript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids) => {
  const users = await User.find({ _id: { $in: ids } });
  return ids.map(id => users.find(u => u.id === id));
});

const resolvers = {
  Post: {
    author: (post) => userLoader.load(post.authorId),
  },
};
```

## 最佳实践

1. **Schema优先**: 先设计Schema再实现
2. **分页**: 使用Relay游标分页
3. **批处理**: 使用DataLoader避免N+1
4. **错误处理**: 规范化错误响应
5. **安全**: 实现查询深度和复杂度限制

## 相关技能

- [nodejs](../backend/nodejs) - Node.js开发
- [python](../backend/python) - Python开发
- [api-design](../../actions/code/api-design) - API设计
- [typescript](../backend/typescript) - TypeScript
