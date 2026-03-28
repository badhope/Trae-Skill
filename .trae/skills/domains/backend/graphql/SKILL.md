---
name: graphql
description: "GraphQL API development with schema design, resolvers, and federation. Keywords: graphql, apollo, schema, resolver, federation, API"
layer: domain
role: specialist
version: 2.0.0
domain: backend
languages:
  - javascript
  - typescript
  - python
frameworks:
  - apollo-server
  - graphql-js
  - strawberry
  - ariadne
invoked_by:
  - coding-workflow
  - api-design
capabilities:
  - schema_design
  - resolver_implementation
  - federation_setup
  - subscription_handling
  - query_optimization
---

# GraphQL

GraphQL API开发专家，专注于Schema设计、Resolver实现和Federation架构。

## 适用场景

- 灵活的数据查询API
- 微服务数据聚合
- 实时数据订阅
- 移动端API优化
- API网关

## 核心架构

### 1. Schema设计

```graphql
type User {
  id: ID!
  email: String!
  name: String!
  avatar: String
  status: UserStatus!
  posts: [Post!]!
  postsCount: Int!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  commentsCount: Int!
  tags: [String!]!
  published: Boolean!
  createdAt: DateTime!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
  createdAt: DateTime!
}

enum UserStatus {
  ACTIVE
  INACTIVE
  SUSPENDED
}

input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UpdateUserInput {
  email: String
  name: String
  avatar: String
}

input CreatePostInput {
  title: String!
  content: String!
  tags: [String!]
  published: Boolean = false
}

input PostFilterInput {
  authorId: ID
  published: Boolean
  tags: [String!]
}

input PaginationInput {
  page: Int = 1
  limit: Int = 20
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Query {
  me: User
  user(id: ID!): User
  users(pagination: PaginationInput): UserConnection!
  
  post(id: ID!): Post
  posts(filter: PostFilterInput, pagination: PaginationInput): [Post!]!
  
  search(query: String!, type: SearchType): [SearchResult!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  
  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: CreatePostInput!): Post!
  deletePost(id: ID!): Boolean!
  
  createComment(postId: ID!, content: String!): Comment!
  deleteComment(id: ID!): Boolean!
}

type Subscription {
  onPostCreated: Post!
  onCommentAdded(postId: ID!): Comment!
  onUserStatusChanged(userId: ID!): User!
}

scalar DateTime

union SearchResult = User | Post | Comment

enum SearchType {
  USER
  POST
  ALL
}
```

### 2. Apollo Server实现

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { GraphQLDateTime } from 'graphql-scalars';
import { PubSub } from 'graphql-subscriptions';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { applyMiddleware } from 'graphql-middleware';
import { shield, rule, inputRule } from 'graphql-shield';

const pubsub = new PubSub();

const POST_CREATED = 'POST_CREATED';
const COMMENT_ADDED = 'COMMENT_ADDED';

const typeDefs = `#graphql
  ${schemaAbove}
`;

const resolvers = {
  DateTime: GraphQLDateTime,
  
  User: {
    posts: async (parent, args, { dataSources }) => {
      return dataSources.postAPI.getPostsByAuthor(parent.id);
    },
    postsCount: async (parent, args, { dataSources }) => {
      return dataSources.postAPI.countPostsByAuthor(parent.id);
    }
  },
  
  Post: {
    author: async (parent, args, { dataSources }) => {
      return dataSources.userAPI.getUser(parent.authorId);
    },
    comments: async (parent, args, { dataSources }) => {
      return dataSources.commentAPI.getCommentsByPost(parent.id);
    },
    commentsCount: async (parent, args, { dataSources }) => {
      return dataSources.commentAPI.countCommentsByPost(parent.id);
    }
  },
  
  Query: {
    me: async (_, __, { user, dataSources }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      return dataSources.userAPI.getUser(user.id);
    },
    
    user: async (_, { id }, { dataSources }) => {
      const user = await dataSources.userAPI.getUser(id);
      if (!user) throw new UserInputError('User not found');
      return user;
    },
    
    users: async (_, { pagination }, { dataSources }) => {
      return dataSources.userAPI.getUsers(pagination);
    },
    
    post: async (_, { id }, { dataSources }) => {
      const post = await dataSources.postAPI.getPost(id);
      if (!post) throw new UserInputError('Post not found');
      return post;
    },
    
    posts: async (_, { filter, pagination }, { dataSources }) => {
      return dataSources.postAPI.getPosts(filter, pagination);
    },
    
    search: async (_, { query, type }, { dataSources }) => {
      return dataSources.searchAPI.search(query, type);
    }
  },
  
  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      const existingUser = await dataSources.userAPI.getUserByEmail(input.email);
      if (existingUser) {
        throw new UserInputError('Email already exists');
      }
      
      const hashedPassword = await hashPassword(input.password);
      const user = await dataSources.userAPI.createUser({
        ...input,
        password: hashedPassword
      });
      
      return user;
    },
    
    updateUser: async (_, { id, input }, { user, dataSources }) => {
      if (user.id !== id && !user.isAdmin) {
        throw new ForbiddenError('Not authorized');
      }
      
      return dataSources.userAPI.updateUser(id, input);
    },
    
    createPost: async (_, { input }, { user, dataSources }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      
      const post = await dataSources.postAPI.createPost({
        ...input,
        authorId: user.id
      });
      
      pubsub.publish(POST_CREATED, { onPostCreated: post });
      
      return post;
    },
    
    createComment: async (_, { postId, content }, { user, dataSources }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      
      const comment = await dataSources.commentAPI.createComment({
        postId,
        content,
        authorId: user.id
      });
      
      pubsub.publish(COMMENT_ADDED, { 
        onCommentAdded: comment 
      });
      
      return comment;
    }
  },
  
  Subscription: {
    onPostCreated: {
      subscribe: () => pubsub.asyncIterator([POST_CREATED])
    },
    
    onCommentAdded: {
      subscribe: (_, { postId }) => {
        return pubsub.asyncIterator([COMMENT_ADDED]);
      }
    }
  }
};

const isAuthenticated = rule({ cache: 'contextual' })(
  async (parent, args, ctx) => {
    return ctx.user !== null;
  }
);

const isAdmin = rule({ cache: 'contextual' })(
  async (parent, args, ctx) => {
    return ctx.user?.role === 'ADMIN';
  }
);

const permissions = shield({
  Query: {
    me: isAuthenticated
  },
  Mutation: {
    createPost: isAuthenticated,
    updatePost: isAuthenticated,
    deletePost: isAuthenticated,
    createComment: isAuthenticated
  }
});

const schema = applyMiddleware(
  makeExecutableSchema({ typeDefs, resolvers }),
  permissions
);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginLandingPageLocalDefault(),
    ApolloServerPluginCacheControl({
      defaultMaxAge: 60
    })
  ],
  formatError: (error) => {
    console.error(error);
    return {
      message: error.message,
      code: error.extensions?.code,
      path: error.path
    };
  }
});

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => {
    const token = req.headers.authorization?.replace('Bearer ', '');
    const user = token ? await verifyToken(token) : null;
    
    return {
      user,
      dataSources: {
        userAPI: new UserAPI(),
        postAPI: new PostAPI(),
        commentAPI: new CommentAPI(),
        searchAPI: new SearchAPI()
      }
    };
  }
});

console.log(`Server ready at ${url}`);
```

### 3. DataLoader优化

```typescript
import DataLoader from 'dataloader';

class UserLoader {
  private loader: DataLoader<string, User>;
  
  constructor(userService: UserService) {
    this.loader = new DataLoader(async (ids: readonly string[]) => {
      const users = await userService.getUsersByIds([...ids]);
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) || null);
    });
  }
  
  async load(id: string): Promise<User | null> {
    return this.loader.load(id);
  }
  
  async loadMany(ids: string[]): Promise<(User | null)[]> {
    return this.loader.loadMany(ids);
  }
}

function createDataLoaders(services: Services) {
  return {
    userLoader: new UserLoader(services.user),
    postLoader: new PostLoader(services.post),
    commentLoader: new CommentLoader(services.comment)
  };
}
```

### 4. Federation

```typescript
import { buildSubgraphSchema } from '@apollo/subgraph';

const typeDefs = `#graphql
  extend type Query {
    users: [User]
  }
  
  type User @key(fields: "id") {
    id: ID!
    email: String!
    name: String!
  }
  
  extend type Post @key(fields: "id") {
    id: ID! @external
    author: User @requires(fields: "authorId")
    authorId: ID! @external
  }
`;

const resolvers = {
  Query: {
    users: (_, __, { dataSources }) => {
      return dataSources.userAPI.getUsers();
    }
  },
  
  User: {
    __resolveReference: async (reference, { dataSources }) => {
      return dataSources.userAPI.getUser(reference.id);
    }
  },
  
  Post: {
    author: async (post, _, { dataSources }) => {
      return dataSources.userAPI.getUser(post.authorId);
    }
  }
};

const schema = buildSubgraphSchema([{ typeDefs, resolvers }]);
```

## 最佳实践

1. **Schema优先**: 先设计Schema再实现
2. **批量加载**: 使用DataLoader避免N+1问题
3. **权限控制**: 使用Shield进行权限管理
4. **错误处理**: 统一错误格式
5. **性能监控**: 启用Apollo Studio
6. **版本控制**: Schema版本化管理

## 相关技能

- [api-design](../../actions/code/api-design) - API设计
- [backend-nodejs](../nodejs) - Node.js后端
- [backend-python](../python) - Python后端
- [unit-test](../../testing/unit-test) - 单元测试
