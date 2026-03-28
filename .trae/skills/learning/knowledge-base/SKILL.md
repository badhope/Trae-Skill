---
name: knowledge-base
description: "Persistent knowledge storage and retrieval system for accumulating and leveraging execution knowledge. Keywords: knowledge, storage, retrieval, learning, 知识库"
layer: learning
role: storage
version: 2.0.0
invokes: []
invoked_by:
  - reflector
  - strategy-learner
  - self-enhancer
capabilities:
  - knowledge_storage
  - semantic_search
  - knowledge_graph
  - automatic_indexing
triggers:
  keywords:
    - knowledge
    - learn
    - remember
    - retrieve
    - 知识
    - 学习
metrics:
  knowledge_items: 10000
  categories: 50
  avg_query_time: 50ms
---

# Knowledge Base

持久化知识存储与检索系统，积累和利用执行知识。

## 目的

实现知识的持久化管理：
- 知识存储：存储各类知识条目
- 语义搜索：基于语义的知识检索
- 知识图谱：构建知识关联网络
- 自动索引：自动分类和索引

## 核心组件

### 1. 知识数据模型

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class KnowledgeType(Enum):
    FACT = "fact"                    # 事实知识
    PATTERN = "pattern"              # 模式知识
    PROCEDURE = "procedure"          # 过程知识
    INSIGHT = "insight"              # 洞察知识
    ERROR_SOLUTION = "error_solution" # 错误解决方案
    BEST_PRACTICE = "best_practice"  # 最佳实践

class KnowledgeStatus(Enum):
    DRAFT = "draft"
    VERIFIED = "verified"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

@dataclass
class KnowledgeItem:
    item_id: str
    type: KnowledgeType
    category: str
    title: str
    content: str
    summary: str
    keywords: List[str]
    tags: List[str]
    source: str
    confidence: float
    usage_count: int
    success_rate: float
    status: KnowledgeStatus
    created_at: datetime
    updated_at: datetime
    last_used: datetime
    expires_at: Optional[datetime]
    metadata: Dict[str, Any]
    related_items: List[str]
    embedding: Optional[List[float]]
    
@dataclass
class KnowledgeRelation:
    relation_id: str
    source_id: str
    target_id: str
    relation_type: str
    strength: float
    created_at: datetime
```

### 2. 知识存储器

```python
import sqlite3
import json
from typing import List, Optional
from contextlib import contextmanager

class KnowledgeStorage:
    def __init__(self, db_path: str = "knowledge.db"):
        self.db_path = db_path
        self._init_db()
        
    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.enable_load_extension(True)
        try:
            yield conn
        finally:
            conn.close()
            
    def _init_db(self):
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS knowledge_items (
                    item_id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    summary TEXT,
                    keywords TEXT,
                    tags TEXT,
                    source TEXT,
                    confidence REAL DEFAULT 0.5,
                    usage_count INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.5,
                    status TEXT DEFAULT 'draft',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    last_used TEXT,
                    expires_at TEXT,
                    metadata TEXT,
                    embedding BLOB
                );
                
                CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts 
                USING fts5(title, content, summary, keywords, tags);
                
                CREATE TABLE IF NOT EXISTS knowledge_relations (
                    relation_id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    strength REAL DEFAULT 1.0,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES knowledge_items(item_id),
                    FOREIGN KEY (target_id) REFERENCES knowledge_items(item_id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_category ON knowledge_items(category);
                CREATE INDEX IF NOT EXISTS idx_type ON knowledge_items(type);
                CREATE INDEX IF NOT EXISTS idx_status ON knowledge_items(status);
                CREATE INDEX IF NOT EXISTS idx_confidence ON knowledge_items(confidence);
                CREATE INDEX IF NOT EXISTS idx_source ON knowledge_relations(source_id);
                CREATE INDEX IF NOT EXISTS idx_target ON knowledge_relations(target_id);
            """)
            
    async def store(self, item: KnowledgeItem) -> str:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO knowledge_items (
                    item_id, type, category, title, content, summary,
                    keywords, tags, source, confidence, usage_count,
                    success_rate, status, created_at, updated_at,
                    last_used, expires_at, metadata, embedding
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.item_id, item.type.value, item.category,
                item.title, item.content, item.summary,
                json.dumps(item.keywords), json.dumps(item.tags),
                item.source, item.confidence, item.usage_count,
                item.success_rate, item.status.value,
                item.created_at.isoformat(), item.updated_at.isoformat(),
                item.last_used.isoformat() if item.last_used else None,
                item.expires_at.isoformat() if item.expires_at else None,
                json.dumps(item.metadata),
                json.dumps(item.embedding) if item.embedding else None
            ))
            
            # 更新全文索引
            conn.execute("""
                INSERT INTO knowledge_fts (rowid, title, content, summary, keywords, tags)
                VALUES ((SELECT rowid FROM knowledge_items WHERE item_id = ?), ?, ?, ?, ?, ?)
            """, (
                item.item_id, item.title, item.content, item.summary,
                ' '.join(item.keywords), ' '.join(item.tags)
            ))
            
        return item.item_id
```

### 3. 语义搜索引擎

```python
class SemanticSearch:
    def __init__(self, storage: KnowledgeStorage, embedding_model):
        self.storage = storage
        self.embedding_model = embedding_model
        
    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        knowledge_type: Optional[KnowledgeType] = None,
        limit: int = 10,
        min_confidence: float = 0.3
    ) -> List[KnowledgeItem]:
        # 生成查询向量
        query_embedding = await self._get_embedding(query)
        
        # 全文搜索
        fts_results = await self._fts_search(query, limit * 2)
        
        # 向量搜索
        vector_results = await self._vector_search(
            query_embedding, limit * 2
        )
        
        # 混合排序
        combined = self._combine_results(
            fts_results, vector_results, query
        )
        
        # 过滤
        filtered = self._filter_results(
            combined, category, knowledge_type, min_confidence
        )
        
        return filtered[:limit]
        
    async def _get_embedding(self, text: str) -> List[float]:
        return await self.embedding_model.embed(text)
        
    async def _fts_search(
        self,
        query: str,
        limit: int
    ) -> List[Dict]:
        with self.storage._get_connection() as conn:
            rows = conn.execute("""
                SELECT k.*, fts.rank
                FROM knowledge_items k
                JOIN knowledge_fts fts ON k.rowid = fts.rowid
                WHERE knowledge_fts MATCH ?
                ORDER BY fts.rank
                LIMIT ?
            """, (query, limit)).fetchall()
            
            return [self._row_to_dict(row) for row in rows]
            
    async def _vector_search(
        self,
        embedding: List[float],
        limit: int
    ) -> List[Dict]:
        with self.storage._get_connection() as conn:
            rows = conn.execute("""
                SELECT *, 
                    json_array_length(embedding) as emb_len
                FROM knowledge_items
                WHERE embedding IS NOT NULL
            """).fetchall()
            
            results = []
            for row in rows:
                stored_emb = json.loads(row["embedding"])
                similarity = self._cosine_similarity(embedding, stored_emb)
                results.append({
                    "item": self._row_to_dict(row),
                    "similarity": similarity
                })
                
            results.sort(key=lambda x: x["similarity"], reverse=True)
            return results[:limit]
            
    def _cosine_similarity(
        self,
        a: List[float],
        b: List[float]
    ) -> float:
        import numpy as np
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
    def _combine_results(
        self,
        fts_results: List[Dict],
        vector_results: List[Dict],
        query: str
    ) -> List[KnowledgeItem]:
        combined_scores = {}
        
        for i, result in enumerate(fts_results):
            item_id = result["item_id"]
            combined_scores[item_id] = {
                "item": result,
                "score": 0.6 * (1 - i / len(fts_results))
            }
            
        for i, result in enumerate(vector_results):
            item_id = result["item"]["item_id"]
            if item_id in combined_scores:
                combined_scores[item_id]["score"] += 0.4 * result["similarity"]
            else:
                combined_scores[item_id] = {
                    "item": result["item"],
                    "score": 0.4 * result["similarity"]
                }
                
        sorted_items = sorted(
            combined_scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        return [item["item"] for item in sorted_items]
```

### 4. 知识图谱

```python
class KnowledgeGraph:
    def __init__(self, storage: KnowledgeStorage):
        self.storage = storage
        
    async def add_relation(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        strength: float = 1.0
    ) -> str:
        relation = KnowledgeRelation(
            relation_id=str(uuid.uuid4()),
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            strength=strength,
            created_at=datetime.now()
        )
        
        with self.storage._get_connection() as conn:
            conn.execute("""
                INSERT INTO knowledge_relations (
                    relation_id, source_id, target_id, relation_type, strength, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                relation.relation_id, relation.source_id, relation.target_id,
                relation.relation_type, relation.strength, relation.created_at.isoformat()
            ))
            
        return relation.relation_id
        
    async def get_related(
        self,
        item_id: str,
        relation_type: Optional[str] = None,
        max_depth: int = 2
    ) -> List[Dict]:
        visited = set()
        result = []
        
        async def traverse(current_id: str, depth: int, path: List[str]):
            if depth > max_depth or current_id in visited:
                return
                
            visited.add(current_id)
            
            with self.storage._get_connection() as conn:
                query = """
                    SELECT k.*, r.relation_type, r.strength
                    FROM knowledge_items k
                    JOIN knowledge_relations r ON k.item_id = r.target_id
                    WHERE r.source_id = ?
                """
                params = [current_id]
                
                if relation_type:
                    query += " AND r.relation_type = ?"
                    params.append(relation_type)
                    
                rows = conn.execute(query, params).fetchall()
                
                for row in rows:
                    result.append({
                        "item": self._row_to_dict(row),
                        "relation_type": row["relation_type"],
                        "strength": row["strength"],
                        "path": path + [row["item_id"]]
                    })
                    
                    await traverse(row["item_id"], depth + 1, path + [row["item_id"]])
                    
        await traverse(item_id, 0, [item_id])
        return result
        
    async def find_path(
        self,
        source_id: str,
        target_id: str
    ) -> Optional[List[str]]:
        """找到两个知识点之间的最短路径"""
        from collections import deque
        
        queue = deque([(source_id, [source_id])])
        visited = {source_id}
        
        with self.storage._get_connection() as conn:
            while queue:
                current, path = queue.popleft()
                
                if current == target_id:
                    return path
                    
                rows = conn.execute("""
                    SELECT target_id FROM knowledge_relations
                    WHERE source_id = ?
                """, (current,)).fetchall()
                
                for row in rows:
                    if row["target_id"] not in visited:
                        visited.add(row["target_id"])
                        queue.append((row["target_id"], path + [row["target_id"]]))
                        
        return None
```

### 5. 完整知识库

```python
class KnowledgeBase:
    def __init__(self, db_path: str = "knowledge.db"):
        self.storage = KnowledgeStorage(db_path)
        self.search = SemanticSearch(self.storage, None)
        self.graph = KnowledgeGraph(self.storage)
        
    async def add(
        self,
        type: KnowledgeType,
        category: str,
        title: str,
        content: str,
        keywords: List[str],
        tags: List[str],
        source: str = "manual",
        summary: Optional[str] = None
    ) -> str:
        item = KnowledgeItem(
            item_id=str(uuid.uuid4()),
            type=type,
            category=category,
            title=title,
            content=content,
            summary=summary or self._generate_summary(content),
            keywords=keywords,
            tags=tags,
            source=source,
            confidence=0.5,
            usage_count=0,
            success_rate=0.5,
            status=KnowledgeStatus.DRAFT,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_used=datetime.now(),
            expires_at=None,
            metadata={},
            related_items=[],
            embedding=None
        )
        
        # 生成向量
        item.embedding = await self.search._get_embedding(content)
        
        return await self.storage.store(item)
        
    async def get(self, item_id: str) -> Optional[KnowledgeItem]:
        with self.storage._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM knowledge_items WHERE item_id = ?",
                (item_id,)
            ).fetchone()
            
            if row:
                # 更新使用计数
                conn.execute(
                    "UPDATE knowledge_items SET usage_count = usage_count + 1, last_used = ? WHERE item_id = ?",
                    (datetime.now().isoformat(), item_id)
                )
                
            return self._row_to_item(row) if row else None
            
    async def update_confidence(
        self,
        item_id: str,
        success: bool
    ):
        with self.storage._get_connection() as conn:
            if success:
                conn.execute("""
                    UPDATE knowledge_items 
                    SET confidence = MIN(confidence + 0.05, 1.0),
                        success_rate = (success_rate * usage_count + 1) / (usage_count + 1),
                        usage_count = usage_count + 1,
                        updated_at = ?
                    WHERE item_id = ?
                """, (datetime.now().isoformat(), item_id))
            else:
                conn.execute("""
                    UPDATE knowledge_items 
                    SET confidence = MAX(confidence - 0.05, 0.0),
                        success_rate = (success_rate * usage_count) / (usage_count + 1),
                        usage_count = usage_count + 1,
                        updated_at = ?
                    WHERE item_id = ?
                """, (datetime.now().isoformat(), item_id))
                
    def _generate_summary(self, content: str) -> str:
        return content[:200] + "..." if len(content) > 200 else content
```

## 知识分类体系

```yaml
categories:
  - name: "error_solutions"
    description: "错误解决方案"
    types: [error_solution]
    
  - name: "best_practices"
    description: "最佳实践"
    types: [best_practice]
    
  - name: "patterns"
    description: "设计模式"
    types: [pattern]
    
  - name: "procedures"
    description: "操作流程"
    types: [procedure]
    
  - name: "insights"
    description: "洞察总结"
    types: [insight]
    
  - name: "facts"
    description: "事实知识"
    types: [fact]
```

## 最佳实践

1. **及时记录**: 发现知识立即记录
2. **准确分类: 正确分类知识类型
3. **关联构建**: 建立知识关联
4. **定期维护**: 清理过期知识
5. **反馈更新**: 根据使用反馈更新

## 相关技能

- [reflector](./reflector) - 反思系统
- [strategy-learner](./strategy-learner) - 策略学习
- [self-enhancer](./self-enhancer) - 自我增强
