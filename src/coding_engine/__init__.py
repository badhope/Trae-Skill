"""Coding Engine - Code analysis, generation, and optimization"""

from coding_engine.analyzer import (
    Language,
    CodeSnippet,
    SyntaxError,
    CodeAnalysis,
    SyntaxAnalyzer,
    AutoCompletionEngine,
)
from coding_engine.quality import (
    IssueSeverity,
    IssueCategory,
    CodeIssue,
    OptimizationResult,
    PatternDetector,
    CodeOptimizer,
    DebugAssistant,
    CodeQualityChecker,
)
from coding_engine.patterns import (
    PatternInfo,
    DesignPattern,
    Singleton,
    FactoryMethod,
    AbstractFactory,
    Builder,
    Observer,
    Strategy,
    Decorator,
    Facade,
    PatternLibrary,
)
from coding_engine.algorithms import (
    AlgorithmResult,
    SortingAlgorithms,
    SearchAlgorithms,
    DynamicProgramming,
    DataStructures,
    AlgorithmLibrary,
)

__all__ = [
    "Language",
    "CodeSnippet",
    "SyntaxError",
    "CodeAnalysis",
    "SyntaxAnalyzer",
    "AutoCompletionEngine",
    "IssueSeverity",
    "IssueCategory",
    "CodeIssue",
    "OptimizationResult",
    "PatternDetector",
    "CodeOptimizer",
    "DebugAssistant",
    "CodeQualityChecker",
    "PatternInfo",
    "DesignPattern",
    "Singleton",
    "FactoryMethod",
    "AbstractFactory",
    "Builder",
    "Observer",
    "Strategy",
    "Decorator",
    "Facade",
    "PatternLibrary",
    "AlgorithmResult",
    "SortingAlgorithms",
    "SearchAlgorithms",
    "DynamicProgramming",
    "DataStructures",
    "AlgorithmLibrary",
]

__version__ = "1.1.0"
