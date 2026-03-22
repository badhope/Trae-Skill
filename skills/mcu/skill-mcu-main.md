---
id: skill-mcu-main-v1
name: MCU Development
summary: 微控制器单元开发与嵌入式系统设计指南
type: skill
category: mcu
tags: [mcu, embedded, microcontroller, arm, avr, riscv, esp32, stm32]
keywords: [微控制器, 嵌入式, ARM, AVR, RISC-V, ESP32, STM32]
intent: 提供微控制器开发、驱动编写、硬件抽象层设计的完整技术指导
use_cases:
  - 需要开发嵌入式系统时
  - 需要编写MCU外设驱动时
  - 需要设计硬件抽象层时
  - 需要优化嵌入式代码时
inputs:
  - name: architecture
    type: string
    required: true
    description: MCU架构类型
  - name: peripherals
    type: array
    required: true
    description: 需要配置的外设列表
  - name: project_name
    type: string
    required: false
    description: 项目名称
outputs:
  - name: code
    type: code
    description: 生成的代码
  - name: configuration
    type: object
    description: 外设配置
prerequisites:
  - 了解C/C++编程基础
  - 了解基本电路知识
steps:
  - step: 1
    action: 选择MCU架构和芯片型号
  - step: 2
    action: 配置时钟系统和电源
  - step: 3
    action: 配置GPIO和外设
  - step: 4
    action: 编写驱动代码
  - step: 5
    action: 编写应用代码
  - step: 6
    action: 调试和优化
examples:
  - input: "architecture: stm32f4, peripherals: gpio, uart, spi"
    output: "complete project template with HAL configuration"
    notes: 展示STM32项目创建
related_skills:
  - skill-coding-v1
  - skill-debugging-v1
related_prompts:
  - prompt-task-mcu-generate-gpio-driver
  - prompt-task-mcu-generate-uart-driver
  - prompt-task-mcu-design-hal-layer
notes: |
  重要提示：
  - 始终查阅芯片数据手册
  - 注意电源和时序要求
  - 做好内存管理规划
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
deprecated: false
---

# MCU Development Skill

微控制器单元开发与嵌入式系统设计的完整指南。

## 支持的MCU架构

### 架构对比

| 架构 | 代表芯片 | 特点 | 适用场景 |
|------|----------|------|----------|
| ARM Cortex-M | STM32, LPC | 高性能,生态好 | 工业控制,消费电子 |
| AVR | ATmega, ATtiny | 简单,低功耗 | 简单控制,Arduino |
| RISC-V | GD32V, FE310-G | 开源,灵活 | IoT,学术研究 |
| ESP32 | ESP32系列 | WiFi+BT,双核 | IoT,智能家居 |
| PIC | PIC16/18/32 | 高可靠性 | 汽车电子,工业 |

### 架构选择指南

```markdown
## 选择决策树

开始
  │
  ├─► 需要无线连接?
  │     ├─ YES → ESP32 / STM32WB
  │     └─ NO
  │           │
  │           ├─► 性能要求高?
  │           │     ├─ YES → ARM Cortex-M4/M7
  │           │     └─ NO
  │           │           │
  │           │           ├─► 资源受限?
  │           │           │     ├─ YES → AVR / RISC-V
  │           │           │     └─ NO
  │           │           │           └─► PIC32 / Cortex-M3
```

## 外设配置

### GPIO配置

```c
// STM32 HAL GPIO配置示例
void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // 使能时钟
    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();

    // 配置LED引脚 (PA5)
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // 配置按钮引脚 (PB0)
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
}
```

### UART配置

```c
// UART初始化和中断处理
UART_HandleTypeDef huart2;

void MX_USART2_UART_Init(void) {
    huart2.Instance = USART2;
    huart2.Init.BaudRate = 115200;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    HAL_UART_Init(&huart2);
}

// 发送字符串
void UART_Send_String(UART_HandleTypeDef *huart, char *str) {
    HAL_UART_Transmit(huart, (uint8_t*)str, strlen(str), HAL_MAX_DELAY);
}

// 接收完成回调
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    // 处理接收到的数据
}
```

### SPI配置

```c
SPI_HandleTypeDef hspi1;

void MX_SPI1_Init(void) {
    hspi1.Instance = SPI1;
    hspi1.Init.Mode = SPI_MODE_MASTER;
    hspi1.Init.Direction = SPI_DIRECTION_2LINES;
    hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
    hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;
    hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;
    hspi1.Init.NSS = SPI_NSS_SOFT;
    hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16;
    hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
    HAL_SPI_Init(&hspi1);
}

// SPI数据传输
uint8_t SPI_Transfer(SPI_HandleTypeDef *hspi, uint8_t data) {
    uint8_t received;
    HAL_SPI_TransmitReceive(hspi, &data, &received, 1, HAL_MAX_DELAY);
    return received;
}
```

### I2C配置

```c
I2C_HandleTypeDef hi2c1;

void MX_I2C1_Init(void) {
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 400000;  // 400kHz Fast Mode
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
    hi2c1.Init.OwnAddress1 = 0;
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
    hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
    HAL_I2C_Init(&hi2c1);
}

// I2C读取传感器
HAL_StatusTypeDef I2C_Read_Sensor(uint16_t DevAddress, uint8_t Reg, uint8_t *pData, uint16_t Size) {
    return HAL_I2C_Mem_Read(&hi2c1, DevAddress, Reg, I2C_MEMADD_SIZE_8BIT, pData, Size, HAL_MAX_DELAY);
}

// I2C写入传感器
HAL_StatusTypeDef I2C_Write_Sensor(uint16_t DevAddress, uint8_t Reg, uint8_t *pData, uint16_t Size) {
    return HAL_I2C_Mem_Write(&hi2c1, DevAddress, Reg, I2C_MEMADD_SIZE_8BIT, pData, Size, HAL_MAX_DELAY);
}
```

## 驱动开发

### 驱动层次结构

```markdown
## 嵌入式软件架构

┌─────────────────────────────────────────────┐
│           Application Layer                 │
│         (用户应用代码)                       │
├─────────────────────────────────────────────┤
│            HAL Layer                        │
│      (硬件抽象层 - HAL Drivers)              │
├─────────────────────────────────────────────┤
│         Peripheral Drivers                  │
│       (外设驱动 - SPI, UART, I2C)           │
├─────────────────────────────────────────────┤
│            BSP Layer                         │
│       (板级支持包 - Board Support)          │
├─────────────────────────────────────────────┤
│              MCU                             │
│         (微控制器 - STM32, ESP32)           │
└─────────────────────────────────────────────┘
```

### 驱动模板

```c
// my_driver.h
#ifndef MY_DRIVER_H
#define MY_DRIVER_H

#include "stm32f4xx_hal.h"

typedef struct {
    SPI_HandleTypeDef *hspi;
    GPIO_TypeDef *cs_port;
    uint16_t cs_pin;
    uint8_t initialized;
} MyDriver_HandleTypeDef;

HAL_StatusTypeDef MyDriver_Init(MyDriver_HandleTypeDef *hdriver, SPI_HandleTypeDef *hspi);
HAL_StatusTypeDef MyDriver_Read(MyDriver_HandleTypeDef *hdriver, uint8_t reg, uint8_t *pData, uint16_t size);
HAL_StatusTypeDef MyDriver_Write(MyDriver_HandleTypeDef *hdriver, uint8_t reg, uint8_t *pData, uint16_t size);

#endif

// my_driver.c
#include "my_driver.h"

HAL_StatusTypeDef MyDriver_Init(MyDriver_HandleTypeDef *hdriver, SPI_HandleTypeDef *hspi) {
    if (hdriver == NULL || hspi == NULL) {
        return HAL_ERROR;
    }
    
    hdriver->hspi = hspi;
    hdriver->initialized = 1;
    
    return HAL_OK;
}

HAL_StatusTypeDef MyDriver_Read(MyDriver_HandleTypeDef *hdriver, uint8_t reg, uint8_t *pData, uint16_t size) {
    if (!hdriver->initialized || hdriver->hspi == NULL) {
        return HAL_ERROR;
    }
    
    // 片选拉低
    HAL_GPIO_WritePin(hdriver->cs_port, hdriver->cs_pin, GPIO_PIN_RESET);
    
    // 发送读命令
    uint8_t cmd = reg | 0x80;
    HAL_SPI_Transmit(hdriver->hspi, &cmd, 1, HAL_MAX_DELAY);
    
    // 读取数据
    HAL_SPI_Receive(hdriver->hspi, pData, size, HAL_MAX_DELAY);
    
    // 片选拉高
    HAL_GPIO_WritePin(hdriver->cs_port, hdriver->cs_pin, GPIO_PIN_SET);
    
    return HAL_OK;
}
```

## 中断处理

### 中断优先级配置

```c
// 配置EXTI中断 (按钮)
void MX_EXTI_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // 使能SYSCFG时钟
    __HAL_RCC_SYSCFG_CLK_ENABLE();

    // 配置PB0为外部中断
    GPIO_InitStruct.Pin = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    // 设置中断优先级 (抢占优先级2, 子优先级0)
    HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);
    
    // 使能中断
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}

// 中断服务程序
void EXTI0_IRQHandler(void) {
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

// 中断回调函数
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_0) {
        // 处理按钮按下事件
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}
```

### 定时器中断

```c
// 配置TIM2为1ms中断
void MX_TIM2_Init(void) {
    TIM_HandleTypeDef htim2;
    
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 7200 - 1;  // 10kHz计数频率
    htim2.Init.Period = 10 - 1;        // 1ms中断
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_Base_Init(&htim2);
    
    // 设置中断优先级
    HAL_NVIC_SetPriority(TIM2_IRQn, 1, 0);
    HAL_NVIC_EnableIRQ(TIM2_IRQn);
}

// 启动定时器
HAL_StatusTypeDef Start_Timer(void) {
    return HAL_TIM_Base_Start_IT(&htim2);
}

// 定时器中断处理
void TIM2_IRQHandler(void) {
    HAL_TIM_IRQHandler(&htim2);
}

// 定时器回调
uint32_t timer_tick = 0;
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim) {
    if (htim->Instance == TIM2) {
        timer_tick++;
    }
}
```

## 内存管理

### 链接脚本配置

```ld
/* STM32F407VG链接脚本片段 */

MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 1024K
    RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 192K
}

/* 代码段 */
.text :
{
    . = ALIGN(4);
    *(.text)
    *(.text*)
    *(.rodata)
    *(.rodata*)
    . = ALIGN(4);
    _etext = .;
} > FLASH

/* 数据段 */
.data :
{
    _sdata = .;
    *(.data)
    *(.data*)
    . = ALIGN(4);
    _edata = .;
} > RAM AT > FLASH

/* BSS段 */
.bss :
{
    . = ALIGN(4);
    _sbss = .;
    *(.bss)
    *(.bss*)
    *(COMMON)
    . = ALIGN(4);
    _ebss = .;
} > RAM
```

### 堆栈配置

```c
// 在startup文件中配置堆栈大小
// 通常在链接脚本中设置

/* 默认堆栈大小 0x400 (1KB) */
Stack_Size      EQU     0x400

/* 默认堆大小 0x200 (512B) */
Heap_Size       EQU     0x200

// 对于大型应用可能需要增加
Stack_Size      EQU     0x1000      /* 4KB stack */
Heap_Size       EQU     0x800       /* 2KB heap */
```

## 调试技术

### SWD调试接口

```markdown
## SWD引脚连接

| MCU Pin | SWD Pin | 说明 |
|---------|---------|------|
| PA13 | SWDIO | 双向数据 |
| PA14 | SWCK | 时钟 |
| NRST | RST | 复位 |
| VCC | VCC | 供电 |
| GND | GND | 地 |

## 调试配置 (OpenOCD)
```

openocd -f interface/stlink.cfg -f target/stm32f4x.cfg
```

### 常见问题排查

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 程序不运行 | 时钟配置错误 | 检查HSE/HSI配置 |
| 串口无输出 | 波特率不匹配 | 确认两边设置一致 |
| 外设不工作 | 时钟未使能 | 调用__HAL_RCC_xxx_CLK_ENABLE() |
| 进入HardFault | 内存越界/空指针 | 使用调试器查看寄存器 |
| 电流过大 | 短路/配置错误 | 检查电路板和IO配置 |

## 功耗优化

### 低功耗模式

```c
// 进入睡眠模式
void Enter_Sleep_Mode(void) {
    // 配置唤醒源 (例如: 外部中断)
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1);
    
    // 进入睡眠模式
    HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
}

// 进入停机模式 (更低功耗)
void Enter_Stop_Mode(void) {
    // 配置RTC闹钟唤醒
    HAL_RTC_SetAlarm(&hrtc, ...);
    
    // 进入停机模式
    HAL_PWR_EnterSTOPMode(PWR_LOWPOWERMODE_STOP, PWR_SLEEPENTRY_WFI);
    
    // 唤醒后重新配置时钟
    SystemClock_Config();
}
```

### 动态调频

```c
// 运行时调整CPU频率
void Set_CPU_Frequency(uint32_t PLL_M, uint32_t PLL_N, uint32_t PLL_P) {
    HAL_RCC_DeInit();
    
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
    
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    RCC_OscInitStruct.HSEState = RCC_HSE_ON;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    RCC_OscInitStruct.PLL.PLLM = PLL_M;
    RCC_OscInitStruct.PLL.PLLN = PLL_N;
    RCC_OscInitStruct.PLL.PLLP = PLL_P;
    HAL_RCC_OscConfig(&RCC_OscInitStruct);
    
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2);
}
```

## 项目模板

### 目录结构

```
project/
├── Core/
│   ├── Inc/
│   │   ├── main.h
│   │   ├── stm32f4xx_hal_conf.h
│   │   └── stm32f4xx_it.h
│   └── Src/
│       ├── main.c
│       ├── stm32f4xx_hal_msp.c
│       └── stm32f4xx_it.c
├── Drivers/
│   ├── CMSIS/
│   └── HAL_Drivers/
├── MyDrivers/
│   ├── Inc/
│   │   └── my_driver.h
│   └── Src/
│       └── my_driver.c
├── Middlewares/
├── .cproject
├── Makefile
└── STM32F407VGtx_FLASH.ld
```

### Makefile模板

```makefile
TARGET = firmware

# 编译器设置
PREFIX = arm-none-eabi-
CC = $(PREFIX)gcc
AS = $(PREFIX)gcc -x assembler-with-cpp
CP = $(PREFIX)objcopy
SZ = $(PREFIX)size

# 优化级别
OPT = -Og

# 包含路径
INCLUDES = -ICore/Inc -IDrivers/CMSIS/Inc -IDrivers/HAL_Drivers/Inc

# 源文件
C_SOURCES =  \
Core/Src/main.c \
Core/Src/stm32f4xx_hal_msp.c \
MyDrivers/Src/my_driver.c

# 汇编源文件
ASM_SOURCES =  \
Core/Src/startup_stm32f407xx.s

# 链接脚本
LDSCRIPT = STM32F407VGtx_FLASH.ld

# 库文件
LIBS = -lc -lm -lnosys
LIBDIR =
LDFLAGS = -T$(LDSCRIPT) $(LIBDIR) $(LIBS) -Map=$(TARGET).map --specs=nano.specs

# 编译目标
all: $(TARGET).elf $(TARGET).bin $(TARGET).hex

%.o: %.c
	$(CC) -c $(OPT) $(INCLUDES) $< -o $@

$(TARGET).elf: $(OBJECTS)
	$(CC) $(OPT) $(INCLUDES) $(OBJECTS) $(LDFLAGS) -o $@
	$(SZ) $@

$(TARGET).bin: $(TARGET).elf
	$(CP) -O binary $< $@

$(TARGET).hex: $(TARGET).elf
	$(CP) -O ihex $< $@
```
