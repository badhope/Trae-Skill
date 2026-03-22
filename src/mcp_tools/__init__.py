"""MCP Tools Framework - Model Context Protocol tools

A comprehensive toolkit for AI-assisted software development, featuring:
- Code Analysis: Static analysis, complexity metrics, dependency parsing
- Code Generation: Unit tests, API clients, algorithms, boilerplate
- Documentation: API docs, README, changelogs
- Testing: Integration, performance, mutation, coverage
- Refactoring: Code smells, dead code detection
- API Tools: OpenAPI, GraphQL, mock servers
- Database: SQL generation, schema design
- DevOps: Docker, CI/CD configuration
- Security: Vulnerability scanning, secret detection
- Learning: Code explanation, tutorials
"""

from mcp_tools.framework import (
    MCPTool,
    MCPFramework,
    ToolDefinition,
    ToolResult,
    ToolStatus,
    ToolExecution,
)

from mcp_tools.mcu_tools import (
    MCUArchitecture,
    MCUPeripheral,
    MCUConfig,
    PinDefinition,
    PeripheralConfig,
    MCUProject,
    MCUTool,
    CodeGeneratorTool,
    PeripheralDriverTool,
    InterruptHandlerTool,
    MemoryLayoutTool,
    DebugProbeTool,
)

from mcp_tools.tools import (
    CodeQualityCheckerTool,
)

from mcp_tools.analyzers import (
    CodeQualityCheckerTool,
    ComplexityAnalyzerTool,
    DependencyParserTool,
    CodeMetricsCollectorTool,
    PatternDetectorTool,
    BugPatternScannerTool,
)

from mcp_tools.generators import (
    UnitTestGeneratorTool,
    APIClientGeneratorTool,
    AlgorithmImplementerTool,
    BoilerplateGeneratorTool,
    CRUDGeneratorTool,
    MockDataGeneratorTool,
)

from mcp_tools.documentation import (
    APIDocGeneratorTool,
    CodeCommentGeneratorTool,
    READMEGeneratorTool,
    ChangelogGeneratorTool,
)

from mcp_tools.testing import (
    IntegrationTestGeneratorTool,
    PerformanceTestGeneratorTool,
    MutationTestGeneratorTool,
    CoverageAnalyzerTool,
)

from mcp_tools.refactoring import (
    RefactoringAssistantTool,
    DeadCodeDetectorTool,
    CodeSmellDetectorTool,
)

from mcp_tools.api_tools import (
    OpenAPIGeneratorTool,
    GraphQLSchemaGeneratorTool,
    MockServerGeneratorTool,
)

from mcp_tools.database import (
    SQLQueryGeneratorTool,
    SchemaDesignerTool,
)

from mcp_tools.devops import (
    DockerfileGeneratorTool,
    CIConfigGeneratorTool,
)

from mcp_tools.security import (
    SecurityVulnerabilityScannerTool,
    SecretDetectorTool,
)

from mcp_tools.learning import (
    CodeExplainerTool,
)

__all__ = [
    "MCPTool",
    "MCPFramework",
    "ToolDefinition",
    "ToolResult",
    "ToolStatus",
    "ToolExecution",
    "MCUArchitecture",
    "MCUPeripheral",
    "MCUConfig",
    "PinDefinition",
    "PeripheralConfig",
    "MCUProject",
    "CodeGeneratorTool",
    "PeripheralDriverTool",
    "InterruptHandlerTool",
    "MemoryLayoutTool",
    "DebugProbeTool",
    "CodeQualityCheckerTool",
    "ComplexityAnalyzerTool",
    "DependencyParserTool",
    "CodeMetricsCollectorTool",
    "PatternDetectorTool",
    "BugPatternScannerTool",
    "UnitTestGeneratorTool",
    "APIClientGeneratorTool",
    "AlgorithmImplementerTool",
    "BoilerplateGeneratorTool",
    "CRUDGeneratorTool",
    "MockDataGeneratorTool",
    "APIDocGeneratorTool",
    "CodeCommentGeneratorTool",
    "READMEGeneratorTool",
    "ChangelogGeneratorTool",
    "IntegrationTestGeneratorTool",
    "PerformanceTestGeneratorTool",
    "MutationTestGeneratorTool",
    "CoverageAnalyzerTool",
    "RefactoringAssistantTool",
    "DeadCodeDetectorTool",
    "CodeSmellDetectorTool",
    "OpenAPIGeneratorTool",
    "GraphQLSchemaGeneratorTool",
    "MockServerGeneratorTool",
    "SQLQueryGeneratorTool",
    "SchemaDesignerTool",
    "DockerfileGeneratorTool",
    "CIConfigGeneratorTool",
    "SecurityVulnerabilityScannerTool",
    "SecretDetectorTool",
    "CodeExplainerTool",
]

__version__ = "2.0.0"
__all_tools__ = len(__all__)
