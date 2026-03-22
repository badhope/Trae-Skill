import asyncio
import unittest
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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
    VectorOperations,
    SemanticSearchEngine,
    ImportanceScorer,
    DecayEngine,
    ConflictResolver,
)
from context_memory.manager import MemoryManager, ContextAssembler


class TestMemoryStores(unittest.TestCase):
    def setUp(self):
        self.short_term = ShortTermMemoryStore(max_size=10, ttl_seconds=3600)
        self.medium_term = MediumTermMemoryStore(session_timeout_minutes=120)
        self.long_term = LongTermMemoryStore()

    def test_short_term_store(self):
        entry = MemoryEntry(
            id="test1",
            content="Test content",
            importance_score=0.5,
        )

        result = asyncio.run(self.short_term.store(entry))
        self.assertTrue(result)

    def test_short_term_get(self):
        entry = MemoryEntry(
            id="test_get",
            content="Test content",
            importance_score=0.5,
        )

        asyncio.run(self.short_term.store(entry))
        retrieved = asyncio.run(self.short_term.get("test_get"))

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "Test content")

    def test_short_term_max_size(self):
        for i in range(15):
            entry = MemoryEntry(
                id=f"test_{i}",
                content=f"Content {i}",
                importance_score=0.5,
            )
            asyncio.run(self.short_term.store(entry))

        entries = asyncio.run(self.short_term.get_recent(limit=100))
        self.assertLessEqual(len(entries), 10)

    def test_medium_term_session(self):
        entry = MemoryEntry(
            id="session_test",
            content="Session content",
            importance_score=0.5,
            metadata={"session_id": "test_session"}
        )

        asyncio.run(self.medium_term.store(entry))
        session_entries = asyncio.run(self.medium_term.get_session_entries("test_session"))

        self.assertEqual(len(session_entries), 1)
        self.assertEqual(session_entries[0].content, "Session content")

    def test_long_term_tags(self):
        entry = MemoryEntry(
            id="tag_test",
            content="Tagged content",
            importance_score=0.5,
            tags={"python", "testing"}
        )

        asyncio.run(self.long_term.store(entry))
        tagged = asyncio.run(self.long_term.search_by_tags({"python"}))

        self.assertEqual(len(tagged), 1)
        self.assertIn("Tagged", tagged[0].content)

    def test_long_term_importance(self):
        entries = [
            MemoryEntry(id=f"imp_{i}", content=f"Content {i}", importance_score=i * 0.1)
            for i in range(5)
        ]

        for entry in entries:
            asyncio.run(self.long_term.store(entry))

        high_importance = asyncio.run(self.long_term.get_by_importance(0.3))

        self.assertGreaterEqual(len(high_importance), 2)
        for entry in high_importance:
            self.assertGreaterEqual(entry.importance_score, 0.3)


class TestSemanticSearch(unittest.TestCase):
    def test_cosine_similarity(self):
        vec_ops = VectorOperations()

        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        self.assertAlmostEqual(vec_ops.cosine_similarity(vec1, vec2), 1.0, places=5)

        vec3 = [0.0, 1.0, 0.0]
        self.assertAlmostEqual(vec_ops.cosine_similarity(vec1, vec3), 0.0, places=5)

        vec4 = [0.707, 0.707, 0.0]
        similarity = vec_ops.cosine_similarity(vec1, vec4)
        self.assertGreater(similarity, 0.7)
        self.assertLess(similarity, 1.0)

    def test_euclidean_distance(self):
        vec_ops = VectorOperations()

        vec1 = [0.0, 0.0]
        vec2 = [3.0, 4.0]
        self.assertAlmostEqual(vec_ops.euclidean_distance(vec1, vec2), 5.0, places=5)

    def test_manhattan_distance(self):
        vec_ops = VectorOperations()

        vec1 = [0.0, 0.0]
        vec2 = [3.0, 4.0]
        self.assertAlmostEqual(vec_ops.manhattan_distance(vec1, vec2), 7.0, places=5)

    def test_semantic_search_ranking(self):
        engine = SemanticSearchEngine(max_results=3)

        query = [1.0, 0.0, 0.0]
        candidates = [
            [1.0, 0.0, 0.0],
            [0.5, 0.5, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]

        similarities = engine.compute_similarity(query, candidates, method="cosine")
        ranked = engine.rank_results(similarities, top_k=3)

        self.assertEqual(ranked[0][0], 0)
        self.assertEqual(ranked[0][1], 1.0)
        self.assertLess(ranked[1][1], 1.0)

    def test_importance_scorer(self):
        scorer = ImportanceScorer()

        timestamp = datetime.now() - timedelta(hours=2)
        score = scorer.calculate(
            timestamp=timestamp,
            access_count=5,
            explicit_score=0.8
        )

        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_decay_engine(self):
        decay = DecayEngine(base_decay_rate=0.95, min_importance=0.1)

        current = 0.8
        decayed = decay.apply_decay(current, time_delta_hours=24, priority="medium")

        self.assertLess(decayed, current)
        self.assertGreaterEqual(decayed, 0.1)

    def test_conflict_resolution_timestamp(self):
        resolver = ConflictResolver()

        existing = MemoryEntry(
            id="conflict",
            content="Old content",
            importance_score=0.5,
            timestamp=datetime.now() - timedelta(hours=1)
        )

        new = MemoryEntry(
            id="conflict_new",
            content="New content",
            importance_score=0.5,
            timestamp=datetime.now()
        )

        resolved = resolver.resolve(existing, new, strategy="timestamp")
        self.assertEqual(resolved.content, "New content")


class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = MemoryManager()

    def test_store_and_retrieve(self):
        entry = asyncio.run(self.manager.store(
            content="Test memory",
            importance_score=0.7,
            tags={"test"}
        ))

        self.assertIsNotNone(entry.id)

        retrieved = asyncio.run(self.manager.get(entry.id))
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, "Test memory")

    def test_search(self):
        asyncio.run(self.manager.store(
            content="Python programming language",
            importance_score=0.8,
            tags={"python"}
        ))

        asyncio.run(self.manager.store(
            content="JavaScript web development",
            importance_score=0.6,
            tags={"javascript"}
        ))

        results = asyncio.run(self.manager.search(
            query_text="python",
            threshold=0.3
        ))

        self.assertIsNotNone(results)

    def test_promote_to_long_term(self):
        entry = asyncio.run(self.manager.store(
            content="Important information",
            importance_score=0.9,
            memory_type=MemoryType.SHORT_TERM
        ))

        result = asyncio.run(self.manager.promote_to_long_term(entry.id))
        self.assertTrue(result)

    def test_consolidate_memories(self):
        for i in range(10):
            asyncio.run(self.manager.store(
                content=f"Content {i}",
                importance_score=0.95 if i < 3 else 0.3,
                memory_type=MemoryType.SHORT_TERM
            ))

        stats = asyncio.run(self.manager.consolidate_memories())
        self.assertIn("promoted", stats)


class TestContextAssembler(unittest.TestCase):
    def setUp(self):
        self.manager = MemoryManager()
        self.assembler = ContextAssembler(self.manager)

    def test_assemble_context(self):
        asyncio.run(self.manager.store(
            content="Recent conversation",
            importance_score=0.7,
            metadata={"session_id": "test_session"}
        ))

        context = asyncio.run(self.assembler.assemble_context(
            current_query="What am I working on?",
            session_id="test_session"
        ))

        self.assertIn("short_term", context)
        self.assertIn("medium_term", context)
        self.assertIn("long_term", context)


if __name__ == "__main__":
    unittest.main()
