from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
import uuid
import asyncio

from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class MCUArchitecture(Enum):
    AVR = "avr"
    ARM_CORTEX_M = "arm_cortex_m"
    RISCV = "riscv"
    ESP32 = "esp32"
    STM32 = "stm32"
    PIC = "pic"
    MSP430 = "msp430"


class MCUPeripheral(Enum):
    GPIO = "gpio"
    UART = "uart"
    SPI = "spi"
    I2C = "i2c"
    ADC = "adc"
    DAC = "dac"
    TIMER = "timer"
    PWM = "pwm"
    INTERRUPT = "interrupt"
    DMA = "dma"
    WATCHDOG = "watchdog"
    RTC = "rtc"


@dataclass
class MCUConfig:
    architecture: MCUArchitecture
    clock_frequency_hz: int
    flash_size_bytes: int
    ram_size_bytes: int
    peripherals: Set[MCUPeripheral]
    voltage_range: tuple[float, float]
    temperature_range: tuple[float, float]


@dataclass
class PinDefinition:
    pin_number: int
    port: str
    function: str
    alternate_functions: List[str]
    pull_config: Optional[str] = None


@dataclass
class PeripheralConfig:
    peripheral_type: MCUPeripheral
    base_address: int
    irq_vector: Optional[int] = None
    configuration: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCUProject:
    name: str
    mcu_config: MCUConfig
    pin_map: Dict[str, PinDefinition]
    peripheral_configs: Dict[str, PeripheralConfig]
    linker_script: Optional[str] = None
    startup_code: Optional[str] = None
    hal_layer: Optional[str] = None


@dataclass
class MCUToolResult:
    tool_name: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MCUTool(ABC):
    def __init__(self):
        self._supported_architectures: Set[MCUArchitecture] = set()

    @abstractmethod
    async def execute(self, params: Dict[str, Any]) -> MCUToolResult:
        pass

    @abstractmethod
    def get_definition(self) -> Dict[str, Any]:
        pass

    def supports_architecture(self, arch: MCUArchitecture) -> bool:
        return arch in self._supported_architectures


class CodeGeneratorTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._supported_architectures = {
            MCUArchitecture.ARM_CORTEX_M,
            MCUArchitecture.ESP32,
            MCUArchitecture.AVR,
            MCUArchitecture.RISCV,
        }

    def supports_architecture(self, arch: MCUArchitecture) -> bool:
        return arch in self._supported_architectures

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mcu_code_generator",
            description="Generates MCU initialization code, peripheral drivers, and application code",
            input_schema={
                "type": "object",
                "properties": {
                    "architecture": {"type": "string"},
                    "peripherals": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "project_name": {"type": "string"},
                    "clock_frequency": {"type": "integer"},
                },
                "required": ["architecture", "peripherals", "project_name"]
            },
            output_schema={"type": "object"},
            tags={"mcu", "code-generation", "embedded"},
            category="mcu"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        pass


class PeripheralDriverTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mcu_peripheral_driver",
            description="Generates peripheral driver code for GPIO, UART, SPI, I2C, etc.",
            input_schema={
                "type": "object",
                "properties": {
                    "peripheral_type": {"type": "string"},
                    "configuration": {"type": "object"},
                },
                "required": ["peripheral_type"]
            },
            output_schema={"type": "object"},
            tags={"mcu", "driver", "peripheral"},
            category="mcu"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        pass


class InterruptHandlerTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mcu_interrupt_handler",
            description="Generates interrupt handlers with proper vector table entries",
            input_schema={
                "type": "object",
                "properties": {
                    "irq_vector": {"type": "integer"},
                    "priority": {"type": "integer"},
                    "handler_name": {"type": "string"},
                    "architecture": {"type": "string"},
                },
                "required": ["irq_vector", "handler_name", "architecture"]
            },
            output_schema={"type": "object"},
            tags={"mcu", "interrupt", "handler"},
            category="mcu"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        pass


class MemoryLayoutTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mcu_memory_layout",
            description="Analyzes and generates memory layout for flash, RAM, and peripherals",
            input_schema={
                "type": "object",
                "properties": {
                    "flash_size": {"type": "integer"},
                    "ram_size": {"type": "integer"},
                    "sections": {"type": "object"},
                },
                "required": ["flash_size", "ram_size"]
            },
            output_schema={"type": "object"},
            tags={"mcu", "memory", "linker"},
            category="mcu"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        pass


class DebugProbeTool(MCPTool):
    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mcu_debug_probe",
            description="Generates debug probe configurations for SWD, JTAG, etc.",
            input_schema={
                "type": "object",
                "properties": {
                    "probe_type": {"type": "string"},
                    "interface": {"type": "string"},
                    "speed": {"type": "integer"},
                },
                "required": ["probe_type", "interface"]
            },
            output_schema={"type": "object"},
            tags={"mcu", "debug", "probe"},
            category="mcu"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        pass
