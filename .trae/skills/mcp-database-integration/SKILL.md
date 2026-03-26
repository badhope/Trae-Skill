# MCP Database Integration

## Description
MCP 数据库集成专家。帮助实现 MCP 与各种数据库的集成，包括 PostgreSQL、MySQL、MongoDB、Redis 等。

## Details

### 功能特性
- 多数据库支持
- 安全查询执行
- 结果格式化
- 连接池管理
- 查询优化
- 事务支持

### PostgreSQL 集成

#### 配置
```typescript
import { Pool } from "pg";

const pool = new Pool({
  host: process.env.PG_HOST || "localhost",
  port: parseInt(process.env.PG_PORT || "5432"),
  database: process.env.PG_DATABASE,
  user: process.env.PG_USER,
  password: process.env.PG_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```

#### 工具实现
```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "pg_query",
      description: "Execute a PostgreSQL query",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "SQL query to execute"
          },
          params: {
            type: "array",
            items: { type: "string" },
            description: "Query parameters"
          }
        },
        required: ["query"]
      }
    },
    {
      name: "pg_list_tables",
      description: "List all tables in the database"
    },
    {
      name: "pg_describe_table",
      description: "Get table schema information",
      inputSchema: {
        type: "object",
        properties: {
          table: { type: "string" }
        },
        required: ["table"]
      }
    }
  ]
}));

// 安全查询执行
async function executeQuery(query: string, params: any[] = []) {
  // 验证查询类型
  const queryType = query.trim().toUpperCase().split(/\s+/)[0];
  const allowedTypes = ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN"];
  
  if (!allowedTypes.includes(queryType)) {
    throw new Error(`Query type "${queryType}" is not allowed. Only read queries are permitted.`);
  }
  
  // 检查危险操作
  const dangerousPatterns = [
    /;\s*DROP/i,
    /;\s*DELETE/i,
    /;\s*TRUNCATE/i,
    /;\s*ALTER/i,
    /;\s*CREATE/i,
    /;\s*INSERT/i,
    /;\s*UPDATE/i,
    /INTO\s+OUTFILE/i,
    /LOAD\s+DATA/i
  ];
  
  for (const pattern of dangerousPatterns) {
    if (pattern.test(query)) {
      throw new Error("Potentially dangerous query detected");
    }
  }
  
  const client = await pool.connect();
  try {
    const result = await client.query(query, params);
    return {
      rows: result.rows,
      rowCount: result.rowCount,
      fields: result.fields.map(f => ({
        name: f.name,
        type: f.dataTypeID
      }))
    };
  } finally {
    client.release();
  }
}
```

### MySQL 集成

```typescript
import mysql from "mysql2/promise";

const pool = mysql.createPool({
  host: process.env.MYSQL_HOST || "localhost",
  port: parseInt(process.env.MYSQL_PORT || "3306"),
  database: process.env.MYSQL_DATABASE,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  connectionLimit: 10,
  waitForConnections: true
});

async function executeMySQLQuery(query: string, params: any[] = []) {
  const [rows, fields] = await pool.execute(query, params);
  
  return {
    rows: Array.isArray(rows) ? rows : [rows],
    fields: fields?.map(f => ({
      name: f.name,
      type: f.type
    }))
  };
}
```

### MongoDB 集成

```typescript
import { MongoClient, ObjectId } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI!);
const db = client.db(process.env.MONGODB_DATABASE);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "mongo_find",
      description: "Find documents in a collection",
      inputSchema: {
        type: "object",
        properties: {
          collection: { type: "string" },
          filter: { type: "object" },
          projection: { type: "object" },
          limit: { type: "integer", default: 100 },
          skip: { type: "integer", default: 0 }
        },
        required: ["collection"]
      }
    },
    {
      name: "mongo_aggregate",
      description: "Run an aggregation pipeline",
      inputSchema: {
        type: "object",
        properties: {
          collection: { type: "string" },
          pipeline: { type: "array" }
        },
        required: ["collection", "pipeline"]
      }
    },
    {
      name: "mongo_list_collections",
      description: "List all collections"
    }
  ]
}));

async function mongoFind(
  collection: string,
  filter: object = {},
  options: { projection?: object; limit?: number; skip?: number } = {}
) {
  const coll = db.collection(collection);
  
  let cursor = coll.find(filter);
  
  if (options.projection) {
    cursor = cursor.project(options.projection);
  }
  if (options.skip) {
    cursor = cursor.skip(options.skip);
  }
  if (options.limit) {
    cursor = cursor.limit(options.limit);
  }
  
  const docs = await cursor.toArray();
  
  // 转换 ObjectId 为字符串
  return docs.map(doc => ({
    ...doc,
    _id: doc._id.toString()
  }));
}
```

### Redis 集成

```typescript
import { createClient } from "redis";

const redis = createClient({
  url: process.env.REDIS_URL
});

await redis.connect();

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "redis_get",
      description: "Get a value by key",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string" }
        },
        required: ["key"]
      }
    },
    {
      name: "redis_set",
      description: "Set a key-value pair",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string" },
          value: { type: "string" },
          ttl: { type: "integer", description: "Time to live in seconds" }
        },
        required: ["key", "value"]
      }
    },
    {
      name: "redis_keys",
      description: "List keys matching a pattern",
      inputSchema: {
        type: "object",
        properties: {
          pattern: { type: "string", default: "*" }
        }
      }
    },
    {
      name: "redis_hgetall",
      description: "Get all fields and values of a hash",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string" }
        },
        required: ["key"]
      }
    }
  ]
}));
```

### SQLite 集成

```typescript
import Database from "better-sqlite3";

const db = new Database(process.env.SQLITE_PATH || "data.db");

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "sqlite_query",
      description: "Execute a SQLite query",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" },
          params: { type: "array" }
        },
        required: ["query"]
      }
    },
    {
      name: "sqlite_list_tables",
      description: "List all tables"
    }
  ]
}));

function sqliteQuery(query: string, params: any[] = []) {
  const stmt = db.prepare(query);
  
  if (query.trim().toUpperCase().startsWith("SELECT")) {
    return stmt.all(...params);
  } else {
    return stmt.run(...params);
  }
}
```

### 资源暴露

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  // 列出所有表/集合
  const tables = await listTables();
  
  return {
    resources: tables.map(table => ({
      uri: `db://${table.name}`,
      name: table.name,
      mimeType: "application/json"
    }))
  };
});

server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => ({
  resourceTemplates: [
    {
      uriTemplate: "db://{table}/{id}",
      name: "Database Record",
      description: "Get a specific record by ID",
      mimeType: "application/json"
    }
  ]
}));

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/db:\/\/([^/]+)(?:\/(.+))?/);
  
  if (!match) {
    throw new Error("Invalid database URI");
  }
  
  const [, table, id] = match;
  
  if (id) {
    // 获取单条记录
    const record = await getRecord(table, id);
    return {
      contents: [{
        uri,
        mimeType: "application/json",
        text: JSON.stringify(record, null, 2)
      }]
    };
  } else {
    // 获取表信息
    const info = await getTableInfo(table);
    return {
      contents: [{
        uri,
        mimeType: "application/json",
        text: JSON.stringify(info, null, 2)
      }]
    };
  }
});
```

### 查询安全

```typescript
class QueryValidator {
  private allowedTables: Set<string>;
  private maxRows: number;
  
  constructor(config: {
    allowedTables?: string[];
    maxRows?: number;
  }) {
    this.allowedTables = new Set(config.allowedTables || []);
    this.maxRows = config.maxRows || 1000;
  }
  
  validate(query: string): { valid: boolean; error?: string } {
    // 检查表名
    const tableMatches = query.match(/(?:FROM|JOIN|INTO|UPDATE)\s+([a-zA-Z_][a-zA-Z0-9_]*)/gi);
    
    if (tableMatches && this.allowedTables.size > 0) {
      for (const match of tableMatches) {
        const table = match.split(/\s+/)[1];
        if (!this.allowedTables.has(table)) {
          return { valid: false, error: `Table "${table}" is not allowed` };
        }
      }
    }
    
    return { valid: true };
  }
  
  addLimit(query: string): string {
    if (!/LIMIT\s+\d+/i.test(query)) {
      return `${query} LIMIT ${this.maxRows}`;
    }
    return query;
  }
}
```

### 连接池管理

```typescript
class ConnectionPoolManager {
  private pools: Map<string, any> = new Map();
  
  async getPool(name: string, config: any) {
    if (!this.pools.has(name)) {
      const pool = await this.createPool(config);
      this.pools.set(name, pool);
    }
    return this.pools.get(name);
  }
  
  async closeAll() {
    for (const [name, pool] of this.pools) {
      await pool.end();
      console.log(`Closed pool: ${name}`);
    }
    this.pools.clear();
  }
  
  getStats() {
    const stats: Record<string, any> = {};
    for (const [name, pool] of this.pools) {
      stats[name] = {
        totalCount: pool.totalCount,
        idleCount: pool.idleCount,
        waitingCount: pool.waitingCount
      };
    }
    return stats;
  }
}
```

### 最佳实践

1. **只读查询**: 默认只允许 SELECT 查询
2. **参数化查询**: 使用参数化查询防止 SQL 注入
3. **连接池**: 使用连接池管理数据库连接
4. **查询超时**: 设置查询超时时间
5. **结果限制**: 限制返回的行数
6. **敏感数据**: 不暴露敏感表和字段

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `sql-optimization` - SQL 优化
- `redis-caching` - Redis 缓存
- `mcp-security-best-practices` - MCP 安全最佳实践
