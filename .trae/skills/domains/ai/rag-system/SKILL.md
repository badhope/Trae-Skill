---
name: rag-system
description: "RAG (Retrieval-Augmented Generation) system development with vector databases and retrieval strategies. Keywords: rag, vector, embedding, retrieval, 检索增强"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
frameworks:
  - langchain
  - llama-index
  - chromadb
  - pinecone
invoked_by:
  - coding-workflow
  - langchain
capabilities:
  - vector_storage
  - semantic_search
  - document_processing
  - retrieval_optimization
  - hybrid_search
---

# RAG System

RAG系统开发专家，专注于向量数据库、检索策略和文档处理。

## 适用场景

- 企业知识库
- 文档问答系统
- 智能客服
- 研究助手
- 内容推荐

## 核心架构

### 1. 文档处理管道

```python
from typing import List, Iterator
from langchain_community.document_loaders import (
    PyPDFLoader,
    WebBaseLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    DirectoryLoader
)
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    CodeSplitter
)
from langchain_core.documents import Document
import hashlib

class DocumentProcessor:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def load_documents(self, source: str, source_type: str) -> List[Document]:
        loaders = {
            "pdf": PyPDFLoader,
            "web": WebBaseLoader,
            "text": TextLoader,
            "markdown": UnstructuredMarkdownLoader,
            "directory": lambda p: DirectoryLoader(p, glob="**/*.pdf", loader_cls=PyPDFLoader)
        }
        
        loader_class = loaders.get(source_type)
        if not loader_class:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        loader = loader_class(source)
        return loader.load()
    
    def split_documents(
        self,
        documents: List[Document],
        strategy: str = "recursive"
    ) -> List[Document]:
        if strategy == "recursive":
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", ".", " ", ""]
            )
        elif strategy == "markdown":
            splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=[
                    ("#", "header1"),
                    ("##", "header2"),
                    ("###", "header3")
                ]
            )
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
        
        return splitter.split_documents(documents)
    
    def enrich_metadata(self, documents: List[Document]) -> List[Document]:
        for doc in documents:
            doc.metadata["chunk_id"] = self._generate_chunk_id(doc.page_content)
            doc.metadata["chunk_length"] = len(doc.page_content)
            doc.metadata["word_count"] = len(doc.page_content.split())
        
        return documents
    
    def _generate_chunk_id(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def process(
        self,
        source: str,
        source_type: str,
        split_strategy: str = "recursive"
    ) -> List[Document]:
        documents = self.load_documents(source, source_type)
        chunks = self.split_documents(documents, split_strategy)
        enriched = self.enrich_metadata(chunks)
        
        return enriched
```

### 2. 向量存储

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS, Pinecone
from langchain_core.vectorstores import VectorStore
from typing import List, Tuple, Optional
import chromadb

class VectorStoreManager:
    def __init__(
        self,
        embedding_model: str = "text-embedding-3-small",
        persist_directory: Optional[str] = None
    ):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.persist_directory = persist_directory
        self._store: Optional[VectorStore] = None
    
    def create_chroma_store(self, documents: List[Document]) -> Chroma:
        self._store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return self._store
    
    def create_faiss_store(self, documents: List[Document]) -> FAISS:
        self._store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        return self._store
    
    def load_store(self, store_type: str = "chroma") -> VectorStore:
        if store_type == "chroma":
            self._store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        return self._store
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        if not self._store:
            raise ValueError("Store not initialized")
        return self._store.add_documents(documents)
    
    def delete_documents(self, ids: List[str]) -> None:
        if not self._store:
            raise ValueError("Store not initialized")
        self._store.delete(ids)
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[dict] = None
    ) -> List[Document]:
        if not self._store:
            raise ValueError("Store not initialized")
        return self._store.similarity_search(query, k=k, filter=filter)
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4
    ) -> List[Tuple[Document, float]]:
        if not self._store:
            raise ValueError("Store not initialized")
        return self._store.similarity_search_with_score(query, k=k)
    
    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5
    ) -> List[Document]:
        if not self._store:
            raise ValueError("Store not initialized")
        return self._store.max_marginal_relevance_search(
            query, k=k, fetch_k=fetch_k, lambda_mult=lambda_mult
        )
```

### 3. 高级检索策略

```python
from langchain.retrievers import (
    ContextualCompressionRetriever,
    EnsembleRetriever,
    MultiQueryRetriever
)
from langchain.retrievers.document_compressors import (
    LLMChainExtractor,
    LLMChainFilter,
    EmbeddingsFilter
)
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from typing import List, Dict, Any

class AdvancedRetriever:
    def __init__(self, vectorstore: VectorStore, llm):
        self.vectorstore = vectorstore
        self.llm = llm
    
    def create_multi_query_retriever(self) -> MultiQueryRetriever:
        return MultiQueryRetriever.from_llm(
            retriever=self.vectorstore.as_retriever(),
            llm=self.llm
        )
    
    def create_compression_retriever(self) -> ContextualCompressionRetriever:
        compressor = LLMChainExtractor.from_llm(self.llm)
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=self.vectorstore.as_retriever()
        )
    
    def create_ensemble_retriever(
        self,
        retrievers: List[Any],
        weights: List[float] = None
    ) -> EnsembleRetriever:
        return EnsembleRetriever(
            retrievers=retrievers,
            weights=weights or [1/len(retrievers)] * len(retrievers)
        )
    
    def create_self_query_retriever(
        self,
        metadata_field_info: List[AttributeInfo]
    ) -> SelfQueryRetriever:
        return SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=self.vectorstore,
            document_contents="Documents about software development",
            metadata_field_info=metadata_field_info,
            verbose=True
        )

class HybridRetriever:
    def __init__(
        self,
        vectorstore: VectorStore,
        keyword_index: Dict[str, List[str]]
    ):
        self.vectorstore = vectorstore
        self.keyword_index = keyword_index
    
    def retrieve(
        self,
        query: str,
        k: int = 4,
        alpha: float = 0.5
    ) -> List[Document]:
        semantic_results = self.vectorstore.similarity_search_with_score(query, k=k*2)
        
        keyword_results = self._keyword_search(query, k=k*2)
        
        combined = self._combine_results(
            semantic_results,
            keyword_results,
            alpha=alpha
        )
        
        return combined[:k]
    
    def _keyword_search(self, query: str, k: int) -> List[Tuple[str, float]]:
        query_terms = query.lower().split()
        scores = {}
        
        for term in query_terms:
            if term in self.keyword_index:
                for doc_id in self.keyword_index[term]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1
        
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:k]
    
    def _combine_results(
        self,
        semantic: List[Tuple[Document, float]],
        keyword: List[Tuple[str, float]],
        alpha: float
    ) -> List[Document]:
        combined_scores = {}
        
        for doc, score in semantic:
            doc_id = doc.metadata.get("chunk_id")
            combined_scores[doc_id] = {
                "doc": doc,
                "score": alpha * (1 - score)
            }
        
        for doc_id, score in keyword:
            if doc_id in combined_scores:
                combined_scores[doc_id]["score"] += (1 - alpha) * score
            else:
                pass
        
        sorted_results = sorted(
            combined_scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        
        return [item["doc"] for item in sorted_results]
```

### 4. RAG Pipeline

```python
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class RAGPipeline:
    def __init__(
        self,
        vectorstore: VectorStore,
        llm,
        retriever_type: str = "basic"
    ):
        self.vectorstore = vectorstore
        self.llm = llm
        self.retriever = self._create_retriever(retriever_type)
    
    def _create_retriever(self, retriever_type: str):
        retrievers = {
            "basic": lambda: self.vectorstore.as_retriever(),
            "mmr": lambda: self.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": 4, "fetch_k": 20}
            ),
            "similarity": lambda: self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 4, "score_threshold": 0.8}
            )
        }
        return retrievers[retriever_type]()
    
    def create_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

Context: {context}"""),
            ("human", "{question}")
        ])
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain
    
    def query(self, question: str) -> Dict[str, Any]:
        chain = self.create_chain()
        
        retrieved_docs = self.retriever.invoke(question)
        
        answer = chain.invoke(question)
        
        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for doc in retrieved_docs
            ]
        }
    
    def query_with_sources(self, question: str) -> Dict[str, Any]:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Answer based on context. Include source citations [1], [2], etc.

Context: {context}"""),
            ("human", "{question}")
        ])
        
        def format_with_sources(docs):
            formatted = []
            for i, doc in enumerate(docs, 1):
                formatted.append(f"[{i}] {doc.page_content}")
            return "\n\n".join(formatted)
        
        chain = (
            {"context": self.retriever | format_with_sources, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain.invoke(question)
```

## 最佳实践

1. **分块策略**: 根据文档类型选择分块方法
2. **嵌入模型**: 选择合适的嵌入模型
3. **检索优化**: 使用混合检索提高准确率
4. **重排序**: 对检索结果进行重排序
5. **缓存策略**: 缓存常见查询结果
6. **评估指标**: 使用RAGAS评估系统性能

## 相关技能

- [langchain](../langchain) - LangChain框架
- [prompt-engineering](../prompt-engineering) - Prompt工程
- [backend-python](../../backend/python) - Python后端
