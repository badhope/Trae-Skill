---
name: rag-system
description: "RAG (Retrieval-Augmented Generation) system implementation for knowledge retrieval. Keywords: rag, retrieval, vector, embedding, chromadb, pinecone, 检索增强生成"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
  - typescript
frameworks:
  - langchain
  - chromadb
  - pinecone
  - weaviate
invoked_by:
  - langchain
  - agent-development
capabilities:
  - vector_storage
  - embedding_generation
  - retrieval_optimization
  - context_management
triggers:
  keywords:
    - rag
    - retrieval
    - vector
    - embedding
    - chromadb
    - pinecone
    - weaviate
    - 检索
    - 向量数据库
metrics:
  avg_execution_time: 5s
  success_rate: 0.92
  retrieval_accuracy: 0.88
---

# RAG System

RAG (检索增强生成) 系统实现，用于知识检索和增强生成。

## 目的

提供RAG系统的最佳实践：
- 向量存储和检索
- 嵌入向量生成
- 检索优化策略
- 上下文管理

## 能力

- **向量存储**: 向量数据库配置和使用
- **嵌入生成**: 文本嵌入向量生成
- **检索优化**: 检索策略优化
- **上下文管理**: 检索上下文管理

## RAG架构

```
┌─────────────────────────────────────────┐
│              RAG Pipeline               │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  Query  │→ │Retrieve │→ │ Augment │ │
│  └─────────┘  └─────────┘  └─────────┘ │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │Generate │← │ Context │← │ Vector  │ │
│  └─────────┘  └─────────┘  │  Store  │ │
│                            └─────────┘ │
└─────────────────────────────────────────┘
```

## 向量数据库

### ChromaDB

```python
import chromadb
from chromadb.utils import embedding_functions

client = chromadb.Client()
embedding_func = embedding_functions.DefaultEmbeddingFunction()

collection = client.create_collection(
    name="documents",
    embedding_function=embedding_func
)

# 添加文档
collection.add(
    documents=["Document 1 content", "Document 2 content"],
    ids=["doc1", "doc2"],
    metadatas=[{"source": "file1"}, {"source": "file2"}]
)

# 查询
results = collection.query(
    query_texts=["search query"],
    n_results=5
)
```

### Pinecone

```python
import pinecone

pinecone.init(api_key="your-api-key", environment="us-west1")
index = pinecone.Index("documents")

# 插入向量
index.upsert([
    ("doc1", embedding_vector, {"text": "content", "source": "file1"}),
    ("doc2", embedding_vector, {"text": "content", "source": "file2"})
])

# 查询
results = index.query(
    vector=query_embedding,
    top_k=5,
    include_metadata=True
)
```

### Weaviate

```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# 创建类
class_obj = {
    "class": "Document",
    "properties": [
        {"name": "content", "dataType": ["text"]},
        {"name": "source", "dataType": ["string"]}
    ]
}
client.schema.create_class(class_obj)

# 添加文档
client.data_object.create(
    {"content": "Document content", "source": "file1"},
    "Document"
)

# 查询
result = (
    client.query
    .get("Document", ["content", "source"])
    .with_near_text({"concepts": ["search query"]})
    .with_limit(5)
    .do()
)
```

## 嵌入模型

### OpenAI Embeddings

```python
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)
embedding = response.data[0].embedding
```

### HuggingFace Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["text1", "text2"])
```

## 检索策略

### 1. 密集检索

```python
def dense_retrieval(query: str, k: int = 5):
    query_embedding = embed(query)
    results = vector_store.search(query_embedding, k=k)
    return results
```

### 2. 混合检索

```python
def hybrid_retrieval(query: str, k: int = 5, alpha: float = 0.5):
    # 密集检索
    dense_results = dense_retrieval(query, k=k*2)
    
    # 稀疏检索 (BM25)
    sparse_results = bm25_search(query, k=k*2)
    
    # 融合排序
    combined = reciprocal_rank_fusion(
        dense_results, 
        sparse_results, 
        alpha=alpha
    )
    return combined[:k]
```

### 3. 重排序

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query: str, documents: list, top_k: int = 5):
    pairs = [(query, doc) for doc in documents]
    scores = reranker.predict(pairs)
    
    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )
    return [doc for doc, _ in ranked[:top_k]]
```

## RAG最佳实践

### 分块策略

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_text(document)
```

### 上下文窗口优化

```python
def optimize_context(query: str, max_tokens: int = 4000):
    docs = retrieve(query)
    
    context = ""
    total_tokens = 0
    
    for doc in docs:
        doc_tokens = count_tokens(doc)
        if total_tokens + doc_tokens <= max_tokens:
            context += doc + "\n\n"
            total_tokens += doc_tokens
        else:
            break
    
    return context
```

## 相关技能

- [langchain](../langchain) - LangChain框架
- [openai](../openai) - OpenAI API
- [llm-evaluation](../llm-evaluation) - LLM评估
