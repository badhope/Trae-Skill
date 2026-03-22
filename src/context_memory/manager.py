import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from context_memory.stores import (
    MemoryEntry,
    MemoryQuery,
    MemorySearchResult,
    MemoryType,
    ShortTermMemoryStore,
    MediumTermMemoryStore,
    LongTermMemoryStore,
)
from context_memory.semantic_search import (
    SemanticSearchEngine,
    ImportanceScorer,
    DecayEngine,
    ConflictResolver,
)


class MemoryManager:
    def __init__(
        self,
        short_term_size: int = 100,
        short_term_ttl: int = 3600,
        session_timeout_minutes: int = 120,
    ):
        self._short_term = ShortTermMemoryStore(max_size=short_term_size, ttl_seconds=short_term_ttl)
        self._medium_term = MediumTermMemoryStore(session_timeout_minutes=session_timeout_minutes)
        self._long_term = LongTermMemoryStore()

        self._semantic_search = SemanticSearchEngine()
        self._importance_scorer = ImportanceScorer()
        self._decay_engine = DecayEngine()
        self._conflict_resolver = ConflictResolver()

        self._embedding_cache: Dict[str, List[float]] = {}
        self._lock = asyncio.Lock()

    async def store(
        self,
        content: str,
        importance_score: float = 0.5,
        memory_type: Optional[MemoryType] = None,
        tags: Optional[Set[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> MemoryEntry:
        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            content=content,
            embedding=embedding,
            memory_type=memory_type or MemoryType.SHORT_TERM,
            importance_score=importance_score,
            timestamp=datetime.now(),
            version=1,
            metadata=metadata or {},
            tags=tags or set(),
        )

        if memory_type == MemoryType.SHORT_TERM or memory_type is None:
            await self._short_term.store(entry)
        elif memory_type == MemoryType.MEDIUM_TERM:
            await self._medium_term.store(entry)
        elif memory_type == MemoryType.LONG_TERM:
            await self._long_term.store(entry)

        return entry

    async def get(self, entry_id: str, memory_type: Optional[MemoryType] = None) -> Optional[MemoryEntry]:
        stores = [self._short_term, self._medium_term, self._long_term] if memory_type is None else [
            self._get_store(memory_type)
        ]

        for store in stores:
            if store:
                entry = await store.get(entry_id)
                if entry:
                    return entry
        return None

    async def update(self, entry: MemoryEntry) -> bool:
        store = self._get_store(entry.memory_type)
        if store:
            return await store.update(entry)
        return False

    async def delete(self, entry_id: str, memory_type: Optional[MemoryType] = None) -> bool:
        stores = [self._short_term, self._medium_term, self._long_term] if memory_type is None else [
            self._get_store(memory_type)
        ]

        for store in stores:
            if store and await store.delete(entry_id):
                return True
        return False

    async def search(
        self,
        query_embedding: Optional[List[float]] = None,
        query_text: Optional[str] = None,
        top_k: int = 10,
        threshold: float = 0.7,
        memory_types: Optional[List[MemoryType]] = None,
        tags: Optional[Set[str]] = None,
    ) -> List[MemorySearchResult]:
        if memory_types is None:
            memory_types = list(MemoryType)

        query = MemoryQuery(
            query_embedding=query_embedding,
            query_text=query_text,
            top_k=top_k,
            threshold=threshold,
            memory_types=memory_types,
            tags=tags,
        )

        results: List[MemorySearchResult] = []
        seen_ids: Set[str] = set()

        for mem_type in memory_types:
            store = self._get_store(mem_type)
            if store:
                type_results = await store.search_by_embedding(query)
                for result in type_results:
                    if result.entry.id not in seen_ids:
                        results.append(result)
                        seen_ids.add(result.entry.id)

        if tags:
            lt_results = await self._long_term.search_by_tags(tags, limit=top_k)
            for entry in lt_results:
                if entry.id not in seen_ids:
                    sim = self._calculate_similarity_heuristic(entry, query_text)
                    if sim >= threshold:
                        results.append(MemorySearchResult(entry=entry, similarity_score=sim, rank=len(results)))
                        seen_ids.add(entry.id)

        results.sort(key=lambda r: r.similarity_score, reverse=True)
        for i, result in enumerate(results[:top_k]):
            result.rank = i + 1

        return results[:top_k]

    def _calculate_similarity_heuristic(self, entry: MemoryEntry, query_text: Optional[str]) -> float:
        if not query_text:
            return entry.importance_score

        query_lower = query_text.lower()
        content_lower = entry.content.lower()

        if query_lower in content_lower:
            return 0.9

        query_words = set(query_lower.split())
        content_words = set(content_lower.split())
        overlap = len(query_words & content_words)

        if overlap > 0:
            return min(0.5 + (overlap / len(query_words)) * 0.4, 0.9)

        return entry.importance_score * 0.5

    async def promote_to_long_term(self, entry_id: str) -> bool:
        entry = await self.get(entry_id)
        if not entry:
            return False

        entry.memory_type = MemoryType.LONG_TERM
        entry.importance_score = min(entry.importance_score * 1.5, 1.0)

        await self.delete(entry_id)
        return await self._long_term.store(entry)

    async def demote_to_medium_term(self, entry_id: str) -> bool:
        entry = await self.get(entry_id)
        if not entry:
            return False

        await self.delete(entry_id)
        entry.memory_type = MemoryType.MEDIUM_TERM
        return await self._medium_term.store(entry)

    async def get_session_context(self, session_id: str) -> List[MemoryEntry]:
        return await self._medium_term.get_session_entries(session_id)

    async def clear_session(self, session_id: str) -> int:
        return await self._medium_term.clear_session(session_id)

    async def get_recent_memories(
        self,
        limit: int = 20,
        memory_types: Optional[List[MemoryType]] = None
    ) -> List[MemoryEntry]:
        if memory_types is None:
            memory_types = [MemoryType.SHORT_TERM, MemoryType.MEDIUM_TERM]

        all_entries: List[MemoryEntry] = []
        for mem_type in memory_types:
            store = self._get_store(mem_type)
            if store:
                entries = await store.get_recent(limit=limit)
                all_entries.extend(entries)

        all_entries.sort(key=lambda e: e.timestamp, reverse=True)
        return all_entries[:limit]

    async def apply_decay(self, hours_elapsed: float = 1.0) -> int:
        decayed_count = 0

        for store in [self._short_term, self._medium_term, self._long_term]:
            entries = await store.get_recent(limit=1000)
            for entry in entries:
                new_importance = self._decay_engine.apply_decay(
                    entry.importance_score,
                    hours_elapsed,
                    priority=self._get_priority_from_score(entry.importance_score)
                )

                if self._decay_engine.should_evict(new_importance, entry.access_count):
                    await store.delete(entry.id)
                    decayed_count += 1
                elif new_importance != entry.importance_score:
                    entry.importance_score = new_importance
                    await store.update(entry)
                    decayed_count += 1

        return decayed_count

    def _get_priority_from_score(self, score: float) -> str:
        if score >= 0.9:
            return "critical"
        elif score >= 0.7:
            return "high"
        elif score >= 0.4:
            return "medium"
        return "low"

    async def consolidate_memories(self) -> Dict[str, int]:
        stats = {"promoted": 0, "demoted": 0, "evicted": 0}

        recent = await self.get_recent_memories(limit=1000)

        for entry in recent:
            if entry.importance_score >= 0.85 and entry.memory_type != MemoryType.LONG_TERM:
                if await self.promote_to_long_term(entry.id):
                    stats["promoted"] += 1
            elif entry.importance_score < 0.3 and entry.memory_type != MemoryType.SHORT_TERM:
                if entry.memory_type == MemoryType.LONG_TERM:
                    entry.memory_type = MemoryType.MEDIUM_TERM
                    await self._long_term.delete(entry.id)
                    await self._medium_term.store(entry)
                    stats["demoted"] += 1

        return stats

    def _get_store(self, memory_type: MemoryType):
        if memory_type == MemoryType.SHORT_TERM:
            return self._short_term
        elif memory_type == MemoryType.MEDIUM_TERM:
            return self._medium_term
        elif memory_type == MemoryType.LONG_TERM:
            return self._long_term
        return None


class ContextAssembler:
    def __init__(self, memory_manager: MemoryManager):
        self._memory_manager = memory_manager
        self._short_term_window = 10
        self._medium_term_window = 50

    async def assemble_context(
        self,
        current_query: str,
        session_id: str,
        embedding: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        short_term = await self._memory_manager.get_recent_memories(
            limit=self._short_term_window,
            memory_types=[MemoryType.SHORT_TERM]
        )

        medium_term = await self._memory_manager.get_session_context(session_id)
        medium_term = medium_term[-self._medium_term_window:]

        relevant_long_term = []
        if embedding:
            search_results = await self._memory_manager.search(
                query_embedding=embedding,
                top_k=5,
                threshold=0.75,
                memory_types=[MemoryType.LONG_TERM]
            )
            relevant_long_term = [r.entry for r in search_results]

        return {
            "short_term": [e.content for e in short_term],
            "medium_term": [e.content for e in medium_term],
            "long_term": [e.content for e in relevant_long_term],
            "metadata": {
                "short_term_count": len(short_term),
                "medium_term_count": len(medium_term),
                "long_term_count": len(relevant_long_term),
            }
        }

    def format_context_prompt(self, context: Dict[str, Any]) -> str:
        parts = []

        if context["metadata"]["long_term_count"] > 0:
            parts.append("=== Long-term Context (Relevant Historical Information) ===")
            for content in context["long_term"]:
                parts.append(f"- {content}")

        if context["metadata"]["medium_term_count"] > 0:
            parts.append("\n=== Current Session History ===")
            for content in context["medium_term"]:
                parts.append(f"- {content}")

        if context["metadata"]["short_term_count"] > 0:
            parts.append("\n=== Recent Conversation (Last 10 turns) ===")
            for content in context["short_term"]:
                parts.append(f"- {content}")

        return "\n".join(parts) if parts else ""


__all__ = [
    "MemoryManager",
    "ContextAssembler",
    "MemoryEntry",
    "MemoryQuery",
    "MemorySearchResult",
    "MemoryType",
    "ShortTermMemoryStore",
    "MediumTermMemoryStore",
    "LongTermMemoryStore",
    "SemanticSearchEngine",
    "ImportanceScorer",
    "DecayEngine",
    "ConflictResolver",
]
