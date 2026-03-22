"""MCP Tools Framework - Model Context Protocol tools"""

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
]

__version__ = "1.1.0"
