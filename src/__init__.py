"""AI Programming Assistant System - Core Package"""

from context_memory.manager import MemoryManager, ContextAssembler
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
    VectorOperations,
)

from rl_engine.engine import RLEngine, RLConfig
from rl_engine.reward import (
    CodeAction,
    CodeActionType,
    ExecutionResult,
    RewardCalculator,
    Experience,
    ExperienceBuffer,
    PrioritizedReplayBuffer,
)
from rl_engine.ppo import PolicyNetwork, ValueNetwork, PPOTrainer

from coding_engine.analyzer import (
    Language,
    CodeSnippet,
    SyntaxError,
    CodeAnalysis,
    SyntaxAnalyzer,
    AutoCompletionEngine,
)
from coding_engine.algorithms import (
    AlgorithmLibrary,
    SortingAlgorithms,
    SearchAlgorithms,
    DynamicProgramming,
)
from coding_engine.patterns import (
    PatternLibrary,
    PatternInfo,
    DesignPattern,
)
from coding_engine.quality import (
    CodeQualityChecker,
    PatternDetector,
    CodeOptimizer,
    DebugAssistant,
)

from mcp_tools.framework import (
    MCPFramework,
    MCPTool,
    ToolDefinition,
    ToolResult,
    ToolStatus,
    ToolExecution,
)
from mcp_tools.tools import (
    CodeQualityCheckerTool,
    UnitTestGeneratorTool,
    APIDocGeneratorTool,
    RefactoringAssistantTool,
)

from network.communication import (
    NetworkModule,
    ServiceRegistry,
    LoadBalancer,
    CircuitBreaker,
    InMemoryBroker,
    Message,
    MessageType,
    ServiceStatus,
    ServiceEndpoint,
)

__version__ = "1.0.0"

__all__ = [
    "MemoryManager",
    "ContextAssembler",
    "MemoryEntry",
    "MemoryQuery",
    "MemorySearchResult",
    "MemoryType",
    "RLEngine",
    "RLConfig",
    "CodeAction",
    "CodeActionType",
    "ExecutionResult",
    "RewardCalculator",
    "Language",
    "SyntaxAnalyzer",
    "AutoCompletionEngine",
    "AlgorithmLibrary",
    "PatternLibrary",
    "CodeQualityChecker",
    "DebugAssistant",
    "MCPFramework",
    "MCPTool",
    "ToolDefinition",
    "ToolResult",
    "CodeQualityCheckerTool",
    "UnitTestGeneratorTool",
    "APIDocGeneratorTool",
    "RefactoringAssistantTool",
    "NetworkModule",
    "ServiceRegistry",
]
