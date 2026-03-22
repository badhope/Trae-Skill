"""Context Memory Module - Hierarchical memory architecture with semantic search"""

from context_memory.manager import MemoryManager, ContextAssembler
from context_memory.stores import (
    MemoryType,
    MemoryPriority,
    MemoryEntry,
    MemoryQuery,
    MemorySearchResult,
    IMemoryStorage,
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

__all__ = [
    "MemoryManager",
    "ContextAssembler",
    "MemoryType",
    "MemoryPriority",
    "MemoryEntry",
    "MemoryQuery",
    "MemorySearchResult",
    "IMemoryStorage",
    "ShortTermMemoryStore",
    "MediumTermMemoryStore",
    "LongTermMemoryStore",
    "VectorOperations",
    "SemanticSearchEngine",
    "ImportanceScorer",
    "DecayEngine",
    "ConflictResolver",
]

__version__ = "1.1.0"
