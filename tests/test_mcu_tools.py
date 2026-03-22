import pytest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.mcp_tools.mcu_tools import (
    MCUArchitecture,
    MCUPeripheral,
    MCUConfig,
    PinDefinition,
    PeripheralConfig,
    MCUProject,
    CodeGeneratorTool,
    PeripheralDriverTool,
    InterruptHandlerTool,
    MemoryLayoutTool,
    DebugProbeTool,
    MCUTool,
)


class TestMCUConfig:
    def test_mcu_config_creation(self):
        config = MCUConfig(
            architecture=MCUArchitecture.STM32,
            clock_frequency_hz=72000000,
            flash_size_bytes=524288,
            ram_size_bytes=98304,
            peripherals={MCUPeripheral.GPIO, MCUPeripheral.UART, MCUPeripheral.SPI},
            voltage_range=(1.8, 3.6),
            temperature_range=(-40, 85)
        )
        assert config.architecture == MCUArchitecture.STM32
        assert config.clock_frequency_hz == 72000000
        assert MCUPeripheral.GPIO in config.peripherals

    def test_mcu_config_defaults(self):
        config = MCUConfig(
            architecture=MCUArchitecture.ESP32,
            clock_frequency_hz=240000000,
            flash_size_bytes=4194304,
            ram_size_bytes=524288,
            peripherals={MCUPeripheral.GPIO},
            voltage_range=(2.5, 3.6),
            temperature_range=(-40, 125)
        )
        assert config.architecture == MCUArchitecture.ESP32


class TestPinDefinition:
    def test_pin_definition_creation(self):
        pin = PinDefinition(
            pin_number=13,
            port="A",
            function="GPIO",
            alternate_functions=["UART2_TX", "SPI1_MOSI"],
            pull_config="pull_up"
        )
        assert pin.pin_number == 13
        assert pin.port == "A"
        assert len(pin.alternate_functions) == 2

    def test_pin_definition_minimal(self):
        pin = PinDefinition(
            pin_number=1,
            port="B",
            function="GPIO",
            alternate_functions=[]
        )
        assert pin.pull_config is None


class TestPeripheralConfig:
    def test_peripheral_config_creation(self):
        config = PeripheralConfig(
            peripheral_type=MCUPeripheral.UART,
            base_address=0x40004400,
            irq_vector=38,
            configuration={"baudrate": 115200, "parity": "none"}
        )
        assert config.peripheral_type == MCUPeripheral.UART
        assert config.irq_vector == 38
        assert config.configuration["baudrate"] == 115200


class TestMCUProject:
    def test_mcu_project_creation(self):
        mcu_config = MCUConfig(
            architecture=MCUArchitecture.ARM_CORTEX_M,
            clock_frequency_hz=168000000,
            flash_size_bytes=1048576,
            ram_size_bytes=196608,
            peripherals={MCUPeripheral.GPIO, MCUPeripheral.UART},
            voltage_range=(1.8, 3.6),
            temperature_range=(-40, 85)
        )
        pin_map = {
            "LED_PIN": PinDefinition(13, "A", "GPIO", [], "pull_up")
        }
        peripheral_configs = {
            "UART1": PeripheralConfig(MCUPeripheral.UART, 0x40004400, 38)
        }
        project = MCUProject(
            name="test_project",
            mcu_config=mcu_config,
            pin_map=pin_map,
            peripheral_configs=peripheral_configs
        )
        assert project.name == "test_project"
        assert len(project.pin_map) == 1
        assert len(project.peripheral_configs) == 1


class TestCodeGeneratorTool:
    @pytest.fixture
    def tool(self):
        return CodeGeneratorTool()

    def test_get_definition(self, tool):
        definition = tool.get_definition()
        assert definition.name == "mcu_code_generator"
        assert definition.category == "mcu"
        assert "architecture" in definition.input_schema["required"]

    def test_supports_architecture(self, tool):
        assert tool.supports_architecture(MCUArchitecture.ARM_CORTEX_M) is True
        assert tool.supports_architecture(MCUArchitecture.ESP32) is True
        assert tool.supports_architecture(MCUArchitecture.PIC) is False


class TestPeripheralDriverTool:
    @pytest.fixture
    def tool(self):
        return PeripheralDriverTool()

    def test_get_definition(self, tool):
        definition = tool.get_definition()
        assert definition.name == "mcu_peripheral_driver"
        assert definition.category == "mcu"
        assert "peripheral_type" in definition.input_schema["required"]


class TestInterruptHandlerTool:
    @pytest.fixture
    def tool(self):
        return InterruptHandlerTool()

    def test_get_definition(self, tool):
        definition = tool.get_definition()
        assert definition.name == "mcu_interrupt_handler"
        assert "irq_vector" in definition.input_schema["required"]
        assert "handler_name" in definition.input_schema["required"]


class TestMemoryLayoutTool:
    @pytest.fixture
    def tool(self):
        return MemoryLayoutTool()

    def test_get_definition(self, tool):
        definition = tool.get_definition()
        assert definition.name == "mcu_memory_layout"
        assert "flash_size" in definition.input_schema["required"]


class TestDebugProbeTool:
    @pytest.fixture
    def tool(self):
        return DebugProbeTool()

    def test_get_definition(self, tool):
        definition = tool.get_definition()
        assert definition.name == "mcu_debug_probe"
        assert "probe_type" in definition.input_schema["required"]


class TestMCUArchitecture:
    def test_all_architectures(self):
        architectures = list(MCUArchitecture)
        assert len(architectures) >= 6
        assert MCUArchitecture.STM32 in architectures
        assert MCUArchitecture.ESP32 in architectures

    def test_architecture_values(self):
        assert MCUArchitecture.AVR.value == "avr"
        assert MCUArchitecture.ARM_CORTEX_M.value == "arm_cortex_m"
        assert MCUArchitecture.RISCV.value == "riscv"


class TestMCUPeripheral:
    def test_all_peripherals(self):
        peripherals = list(MCUPeripheral)
        assert len(peripherals) >= 10
        assert MCUPeripheral.GPIO in peripherals
        assert MCUPeripheral.UART in peripherals
        assert MCUPeripheral.SPI in peripherals
        assert MCUPeripheral.I2C in peripherals

    def test_peripheral_values(self):
        assert MCUPeripheral.GPIO.value == "gpio"
        assert MCUPeripheral.ADC.value == "adc"
        assert MCUPeripheral.DMA.value == "dma"
