# MCP Memory & Context

## Description
MCP 记忆与上下文管理专家。帮助实现 MCP 服务器的记忆存储、上下文管理和状态持久化。

## Details

### 功能特性
- 会话记忆存储
- 长期记忆管理
- 上下文压缩
- 状态持久化
- 记忆检索
- 向量存储集成

### 记忆架构

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Memory System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Short     │  │   Long      │  │   Vector    │        │
│  │   Term      │  │   Term      │  │   Store     │        │
│  │   Memory    │  │   Memory    │  │             │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │
│         └────────────────┼────────────────┘                │
│                          │                                 │
│                  ┌───────▼───────┐                        │
│                  │   Memory      │                        │
│                  │   Manager     │                        │
│                  └───────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 短期记忆

```typescript
interface ShortTermMemory {
  sessionId: string;
  messages: Message[];
  context: Record<string, any>;
  createdAt: Date;
  lastAccessedAt: Date;
}

class ShortTermMemoryStore {
  private memories: Map<string, ShortTermMemory> = new Map();
  private maxMessages: number = 100;
  private ttl: number = 3600000; // 1 hour
  
  create(sessionId: string): ShortTermMemory {
    const memory: ShortTermMemory = {
      sessionId,
      messages: [],
      context: {},
      createdAt: new Date(),
      lastAccessedAt: new Date()
    };
    this.memories.set(sessionId, memory);
    return memory;
  }
  
  get(sessionId: string): ShortTermMemory | undefined {
    const memory = this.memories.get(sessionId);
    if (memory) {
      memory.lastAccessedAt = new Date();
    }
    return memory;
  }
  
  addMessage(sessionId: string, message: Message) {
    const memory = this.get(sessionId);
    if (!memory) return;
    
    memory.messages.push(message);
    
    // 限制消息数量
    if (memory.messages.length > this.maxMessages) {
      memory.messages = memory.messages.slice(-this.maxMessages);
    }
  }
  
  setContext(sessionId: string, key: string, value: any) {
    const memory = this.get(sessionId);
    if (memory) {
      memory.context[key] = value;
    }
  }
  
  cleanup() {
    const now = Date.now();
    for (const [id, memory] of this.memories) {
      if (now - memory.lastAccessedAt.getTime() > this.ttl) {
        this.memories.delete(id);
      }
    }
  }
}
```

### 长期记忆

```typescript
interface LongTermMemory {
  id: string;
  type: "fact" | "preference" | "conversation" | "document";
  content: string;
  metadata: Record<string, any>;
  embedding?: number[];
  createdAt: Date;
  updatedAt: Date;
  accessCount: number;
}

class LongTermMemoryStore {
  private store: Map<string, LongTermMemory> = new Map();
  private index: Map<string, Set<string>> = new Map(); // type -> ids
  
  async store(memory: Omit<LongTermMemory, "id" | "createdAt" | "updatedAt" | "accessCount">): Promise<string> {
    const id = this.generateId();
    const entry: LongTermMemory = {
      ...memory,
      id,
      createdAt: new Date(),
      updatedAt: new Date(),
      accessCount: 0
    };
    
    this.store.set(id, entry);
    
    // 更新索引
    if (!this.index.has(memory.type)) {
      this.index.set(memory.type, new Set());
    }
    this.index.get(memory.type)!.add(id);
    
    return id;
  }
  
  async retrieve(id: string): Promise<LongTermMemory | undefined> {
    const memory = this.store.get(id);
    if (memory) {
      memory.accessCount++;
      memory.updatedAt = new Date();
    }
    return memory;
  }
  
  async search(query: string, options: {
    type?: string;
    limit?: number;
  } = {}): Promise<LongTermMemory[]> {
    let results: LongTermMemory[] = [];
    
    if (options.type) {
      const ids = this.index.get(options.type) || new Set();
      results = Array.from(ids)
        .map(id => this.store.get(id)!)
        .filter(Boolean);
    } else {
      results = Array.from(this.store.values());
    }
    
    // 简单文本搜索
    const lowerQuery = query.toLowerCase();
    results = results.filter(m => 
      m.content.toLowerCase().includes(lowerQuery) ||
      JSON.stringify(m.metadata).toLowerCase().includes(lowerQuery)
    );
    
    return results.slice(0, options.limit || 10);
  }
  
  async update(id: string, updates: Partial<LongTermMemory>): Promise<boolean> {
    const memory = this.store.get(id);
    if (!memory) return false;
    
    Object.assign(memory, updates, { updatedAt: new Date() });
    return true;
  }
  
  async delete(id: string): Promise<boolean> {
    const memory = this.store.get(id);
    if (!memory) return false;
    
    this.store.delete(id);
    this.index.get(memory.type)?.delete(id);
    return true;
  }
  
  private generateId(): string {
    return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

### 向量存储集成

```typescript
interface VectorStore {
  upsert(id: string, embedding: number[], metadata: Record<string, any>): Promise<void>;
  query(embedding: number[], topK: number): Promise<Array<{ id: string; score: number; metadata: any }>>;
  delete(id: string): Promise<void>;
}

class MemoryVectorStore implements VectorStore {
  private vectors: Map<string, { embedding: number[]; metadata: any }> = new Map();
  
  async upsert(id: string, embedding: number[], metadata: Record<string, any>): Promise<void> {
    this.vectors.set(id, { embedding, metadata });
  }
  
  async query(embedding: number[], topK: number): Promise<Array<{ id: string; score: number; metadata: any }>> {
    const results: Array<{ id: string; score: number; metadata: any }> = [];
    
    for (const [id, data] of this.vectors) {
      const score = this.cosineSimilarity(embedding, data.embedding);
      results.push({ id, score, metadata: data.metadata });
    }
    
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, topK);
  }
  
  async delete(id: string): Promise<void> {
    this.vectors.delete(id);
  }
  
  private cosineSimilarity(a: number[], b: number[]): number {
    if (a.length !== b.length) return 0;
    
    let dotProduct = 0;
    let normA = 0;
    let normB = 0;
    
    for (let i = 0; i < a.length; i++) {
      dotProduct += a[i] * b[i];
      normA += a[i] * a[i];
      normB += b[i] * b[i];
    }
    
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
}
```

### MCP 工具实现

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "memory_store",
      description: "Store a memory",
      inputSchema: {
        type: "object",
        properties: {
          type: {
            type: "string",
            enum: ["fact", "preference", "conversation", "document"]
          },
          content: { type: "string" },
          metadata: { type: "object" }
        },
        required: ["type", "content"]
      }
    },
    {
      name: "memory_retrieve",
      description: "Retrieve a memory by ID",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string" }
        },
        required: ["id"]
      }
    },
    {
      name: "memory_search",
      description: "Search memories",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string" },
          type: { type: "string" },
          limit: { type: "integer", default: 10 }
        },
        required: ["query"]
      }
    },
    {
      name: "memory_update",
      description: "Update a memory",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string" },
          content: { type: "string" },
          metadata: { type: "object" }
        },
        required: ["id"]
      }
    },
    {
      name: "memory_delete",
      description: "Delete a memory",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string" }
        },
        required: ["id"]
      }
    },
    {
      name: "context_set",
      description: "Set context for current session",
      inputSchema: {
        type: "object",
        properties: {
          key: { type: "string" },
          value: { type: "string" }
        },
        required: ["key", "value"]
      }
    },
    {
      name: "context_get",
      description: "Get context from current session",
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

### 上下文压缩

```typescript
class ContextCompressor {
  private maxTokens: number = 4000;
  
  compress(messages: Message[]): Message[] {
    if (this.estimateTokens(messages) <= this.maxTokens) {
      return messages;
    }
    
    // 保留最近的对话
    const recentMessages = messages.slice(-10);
    
    // 压缩历史对话
    const historicalMessages = messages.slice(0, -10);
    const summary = this.summarize(historicalMessages);
    
    return [
      { role: "system", content: `Previous conversation summary: ${summary}` },
      ...recentMessages
    ];
  }
  
  private estimateTokens(messages: Message[]): number {
    return messages.reduce((sum, msg) => 
      sum + Math.ceil(msg.content.length / 4), 0
    );
  }
  
  private summarize(messages: Message[]): string {
    // 简单摘要：提取关键信息
    const keyPoints: string[] = [];
    
    for (const msg of messages) {
      if (msg.role === "user") {
        const sentences = msg.content.split(/[.!?]+/);
        keyPoints.push(...sentences.slice(0, 2));
      }
    }
    
    return keyPoints.slice(0, 5).join(". ");
  }
}
```

### 持久化存储

```typescript
import fs from "fs/promises";
import path from "path";

class PersistentMemoryStore {
  private dataDir: string;
  
  constructor(dataDir: string) {
    this.dataDir = dataDir;
  }
  
  async save(sessionId: string, data: any): Promise<void> {
    const filePath = path.join(this.dataDir, `${sessionId}.json`);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));
  }
  
  async load(sessionId: string): Promise<any | null> {
    try {
      const filePath = path.join(this.dataDir, `${sessionId}.json`);
      const content = await fs.readFile(filePath, "utf-8");
      return JSON.parse(content);
    } catch {
      return null;
    }
  }
  
  async list(): Promise<string[]> {
    const files = await fs.readdir(this.dataDir);
    return files
      .filter(f => f.endsWith(".json"))
      .map(f => f.replace(".json", ""));
  }
  
  async delete(sessionId: string): Promise<void> {
    const filePath = path.join(this.dataDir, `${sessionId}.json`);
    await fs.unlink(filePath);
  }
}
```

### 资源暴露

```typescript
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const memories = await longTermMemoryStore.search("", { limit: 100 });
  
  return {
    resources: memories.map(m => ({
      uri: `memory://${m.id}`,
      name: m.content.slice(0, 50),
      mimeType: "application/json"
    }))
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const id = uri.replace("memory://", "");
  
  const memory = await longTermMemoryStore.retrieve(id);
  if (!memory) {
    throw new Error("Memory not found");
  }
  
  return {
    contents: [{
      uri,
      mimeType: "application/json",
      text: JSON.stringify(memory, null, 2)
    }]
  };
});
```

### 最佳实践

1. **分层存储**: 短期记忆用内存，长期记忆用持久化
2. **自动清理**: 定期清理过期的会话记忆
3. **压缩策略**: 对长对话进行上下文压缩
4. **索引优化**: 为频繁查询的字段建立索引
5. **备份机制**: 定期备份重要记忆数据

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `context-compressor` - 上下文压缩
- `self-memory-manager` - 自记忆管理
