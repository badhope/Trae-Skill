from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import asyncio
import json
import uuid


class MemoryType(Enum):
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"


class MemoryPriority(Enum):
    LOW = 0.25
    MEDIUM = 0.5
    HIGH = 0.75
    CRITICAL = 1.0


@dataclass
class MemoryEntry:
    id: str
    content: str
    embedding: Optional[List[float]] = None
    memory_type: MemoryType = MemoryType.SHORT_TERM
    importance_score: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    access_count: int = 0
    last_accessed: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "embedding": self.embedding,
            "memory_type": self.memory_type.value,
            "importance_score": self.importance_score,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "metadata": self.metadata,
            "tags": list(self.tags),
            "access_count": self.access_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        return cls(
            id=data["id"],
            content=data["content"],
            embedding=data.get("embedding"),
            memory_type=MemoryType(data["memory_type"]),
            importance_score=data["importance_score"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            version=data["version"],
            metadata=data.get("metadata", {}),
            tags=set(data.get("tags", [])),
            access_count=data.get("access_count", 0),
            last_accessed=datetime.fromisoformat(data["last_accessed"]) if data.get("last_accessed") else None
        )


@dataclass
class MemoryQuery:
    query_embedding: Optional[List[float]] = None
    query_text: Optional[str] = None
    top_k: int = 10
    threshold: float = 0.7
    memory_types: List[MemoryType] = field(default_factory=lambda: list(MemoryType))
    tags: Optional[Set[str]] = None
    time_range: Optional[tuple[datetime, datetime]] = None


@dataclass
class MemorySearchResult:
    entry: MemoryEntry
    similarity_score: float
    rank: int


class IMemoryStorage(ABC):
    @abstractmethod
    async def store(self, entry: MemoryEntry) -> bool:
        pass

    @abstractmethod
    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        pass

    @abstractmethod
    async def update(self, entry: MemoryEntry) -> bool:
        pass

    @abstractmethod
    async def delete(self, entry_id: str) -> bool:
        pass

    @abstractmethod
    async def search_by_embedding(self, query: MemoryQuery) -> List[MemorySearchResult]:
        pass

    @abstractmethod
    async def get_by_type(self, memory_type: MemoryType, limit: int = 100) -> List[MemoryEntry]:
        pass

    @abstractmethod
    async def get_recent(self, limit: int = 50) -> List[MemoryEntry]:
        pass


class ShortTermMemoryStore(IMemoryStorage):
    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        self._store: Dict[str, MemoryEntry] = {}
        self._access_order: List[str] = []
        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._lock = asyncio.Lock()

    async def store(self, entry: MemoryEntry) -> bool:
        async with self._lock:
            if len(self._store) >= self._max_size:
                oldest_id = self._access_order.pop(0)
                del self._store[oldest_id]

            entry.memory_type = MemoryType.SHORT_TERM
            self._store[entry.id] = entry
            self._access_order.append(entry.id)
            return True

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        async with self._lock:
            entry = self._store.get(entry_id)
            if entry:
                entry.access_count += 1
                entry.last_accessed = datetime.now()
                self._access_order.remove(entry_id)
                self._access_order.append(entry_id)
            return entry

    async def update(self, entry: MemoryEntry) -> bool:
        async with self._lock:
            if entry.id in self._store:
                entry.version += 1
                self._store[entry.id] = entry
                return True
            return False

    async def delete(self, entry_id: str) -> bool:
        async with self._lock:
            if entry_id in self._store:
                del self._store[entry_id]
                self._access_order.remove(entry_id)
                return True
            return False

    async def search_by_embedding(self, query: MemoryQuery) -> List[MemorySearchResult]:
        if not query.query_embedding:
            return []

        from context_memory.semantic_search import VectorOperations
        vec_ops = VectorOperations()

        results = []
        for i, entry in enumerate(self._store.values()):
            if entry.embedding:
                similarity = vec_ops.cosine_similarity(query.query_embedding, entry.embedding)
                if similarity >= query.threshold:
                    results.append(MemorySearchResult(entry=entry, similarity_score=similarity, rank=i))

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:query.top_k]

    async def get_by_type(self, memory_type: MemoryType, limit: int = 100) -> List[MemoryEntry]:
        async with self._lock:
            return [e for e in self._store.values() if e.memory_type == memory_type][:limit]

    async def get_recent(self, limit: int = 50) -> List[MemoryEntry]:
        async with self._lock:
            return [self._store[id] for id in self._access_order[-limit:]]


class MediumTermMemoryStore(IMemoryStorage):
    def __init__(self, session_timeout_minutes: int = 120):
        self._store: Dict[str, MemoryEntry] = {}
        self._session_id_to_entries: Dict[str, Set[str]] = {}
        self._lock = asyncio.Lock()

    async def store(self, entry: MemoryEntry) -> bool:
        async with self._lock:
            entry.memory_type = MemoryType.MEDIUM_TERM
            self._store[entry.id] = entry

            session_id = entry.metadata.get("session_id", "default")
            if session_id not in self._session_id_to_entries:
                self._session_id_to_entries[session_id] = set()
            self._session_id_to_entries[session_id].add(entry.id)
            return True

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        async with self._lock:
            entry = self._store.get(entry_id)
            if entry:
                entry.access_count += 1
                entry.last_accessed = datetime.now()
            return entry

    async def update(self, entry: MemoryEntry) -> bool:
        async with self._lock:
            if entry.id in self._store:
                entry.version += 1
                self._store[entry.id] = entry
                return True
            return False

    async def delete(self, entry_id: str) -> bool:
        async with self._lock:
            entry = self._store.get(entry_id)
            if entry:
                session_id = entry.metadata.get("session_id", "default")
                if session_id in self._session_id_to_entries:
                    self._session_id_to_entries[session_id].discard(entry_id)
                del self._store[entry_id]
                return True
            return False

    async def search_by_embedding(self, query: MemoryQuery) -> List[MemorySearchResult]:
        if not query.query_embedding:
            return []

        from context_memory.semantic_search import VectorOperations
        vec_ops = VectorOperations()

        results = []
        for i, entry in enumerate(self._store.values()):
            if entry.embedding:
                similarity = vec_ops.cosine_similarity(query.query_embedding, entry.embedding)
                if similarity >= query.threshold:
                    results.append(MemorySearchResult(entry=entry, similarity_score=similarity, rank=i))

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:query.top_k]

    async def get_by_type(self, memory_type: MemoryType, limit: int = 100) -> List[MemoryEntry]:
        async with self._lock:
            return list(self._store.values())[:limit]

    async def get_recent(self, limit: int = 50) -> List[MemoryEntry]:
        async with self._lock:
            sorted_entries = sorted(self._store.values(), key=lambda e: e.timestamp, reverse=True)
            return sorted_entries[:limit]

    async def get_session_entries(self, session_id: str) -> List[MemoryEntry]:
        async with self._lock:
            entry_ids = self._session_id_to_entries.get(session_id, set())
            return [self._store[eid] for eid in entry_ids if eid in self._store]

    async def clear_session(self, session_id: str) -> int:
        async with self._lock:
            entry_ids = self._session_id_to_entries.get(session_id, set())
            count = len(entry_ids)
            for eid in entry_ids:
                if eid in self._store:
                    del self._store[eid]
            del self._session_id_to_entries[session_id]
            return count


class LongTermMemoryStore(IMemoryStorage):
    def __init__(self):
        self._store: Dict[str, MemoryEntry] = {}
        self._tag_index: Dict[str, Set[str]] = {}
        self._importance_index: List[str] = []
        self._lock = asyncio.Lock()

    async def store(self, entry: MemoryEntry) -> bool:
        async with self._lock:
            entry.memory_type = MemoryType.LONG_TERM
            self._store[entry.id] = entry

            for tag in entry.tags:
                if tag not in self._tag_index:
                    self._tag_index[tag] = set()
                self._tag_index[tag].add(entry.id)

            self._rebuild_importance_index()
            return True

    async def get(self, entry_id: str) -> Optional[MemoryEntry]:
        async with self._lock:
            entry = self._store.get(entry_id)
            if entry:
                entry.access_count += 1
                entry.last_accessed = datetime.now()
            return entry

    async def update(self, entry: MemoryEntry) -> bool:
        async with self._lock:
            if entry.id in self._store:
                entry.version += 1
                self._store[entry.id] = entry
                self._rebuild_importance_index()
                return True
            return False

    async def delete(self, entry_id: str) -> bool:
        async with self._lock:
            if entry_id in self._store:
                entry = self._store[entry_id]
                for tag in entry.tags:
                    if tag in self._tag_index:
                        self._tag_index[tag].discard(entry_id)
                del self._store[entry_id]
                self._rebuild_importance_index()
                return True
            return False

    async def search_by_embedding(self, query: MemoryQuery) -> List[MemorySearchResult]:
        if not query.query_embedding:
            return []

        from context_memory.semantic_search import VectorOperations
        vec_ops = VectorOperations()

        results = []
        for i, entry in enumerate(self._store.values()):
            if entry.embedding:
                similarity = vec_ops.cosine_similarity(query.query_embedding, entry.embedding)
                if similarity >= query.threshold:
                    results.append(MemorySearchResult(entry=entry, similarity_score=similarity, rank=i))

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:query.top_k]

    async def get_by_type(self, memory_type: MemoryType, limit: int = 100) -> List[MemoryEntry]:
        async with self._lock:
            return list(self._store.values())[:limit]

    async def get_recent(self, limit: int = 50) -> List[MemoryEntry]:
        async with self._lock:
            sorted_entries = sorted(self._store.values(), key=lambda e: e.timestamp, reverse=True)
            return sorted_entries[:limit]

    async def search_by_tags(self, tags: Set[str], limit: int = 50) -> List[MemoryEntry]:
        async with self._lock:
            result_ids = set()
            for tag in tags:
                if tag in self._tag_index:
                    result_ids.update(self._tag_index[tag])
            return [self._store[eid] for eid in list(result_ids)[:limit] if eid in self._store]

    async def get_by_importance(self, min_importance: float, limit: int = 50) -> List[MemoryEntry]:
        async with self._lock:
            return [self._store[eid] for eid in self._importance_index
                    if eid in self._store and self._store[eid].importance_score >= min_importance][:limit]

    def _rebuild_importance_index(self):
        self._importance_index = sorted(
            self._store.keys(),
            key=lambda eid: self._store[eid].importance_score,
            reverse=True
        )
