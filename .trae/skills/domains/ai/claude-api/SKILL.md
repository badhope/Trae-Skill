---
name: claude-api
description: "Claude API integration expert for Anthropic's Claude models. Keywords: claude, anthropic, llm, api, messages, claude api"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
  - typescript
frameworks:
  - anthropic
  - langchain
invoked_by:
  - code-generator
  - langchain
capabilities:
  - api_integration
  - prompt_optimization
  - streaming_handling
  - tool_use
triggers:
  keywords:
    - claude
    - anthropic
    - claude api
    - claude-3
    - claude-sonnet
    - claude-opus
    - claude-haiku
metrics:
  avg_execution_time: 3s
  success_rate: 0.95
  api_efficiency: 0.91
---

# Claude API

Claude API集成专家，用于Anthropic的Claude模型开发。

## 目的

提供Claude API的最佳实践和集成指南：
- API调用和配置
- 消息格式和结构
- 工具使用和函数调用
- 流式响应处理

## 能力

- **API集成**: Claude API调用和配置
- **Prompt优化**: Claude特定提示优化
- **流式处理**: 流式响应处理
- **工具使用**: Claude工具使用功能

## 模型对比

| 模型 | 上下文 | 特点 | 适用场景 |
|------|--------|------|----------|
| Claude 3.5 Sonnet | 200K | 平衡性能 | 通用任务、编码 |
| Claude 3 Opus | 200K | 最强能力 | 复杂推理、创作 |
| Claude 3 Haiku | 200K | 快速响应 | 简单任务、批量处理 |

## API基础

### 安装

```bash
pip install anthropic
```

### 基本调用

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)

print(message.content)
```

### 流式响应

```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a poem"}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## 消息格式

### 系统提示

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Help me write a function"}
    ]
)
```

### 多轮对话

```python
messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "What are its main features?"}
]

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=messages
)
```

### 多模态输入

```python
import base64

with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe this image"
                }
            ]
        }
    ]
)
```

## 工具使用

### 定义工具

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]
```

### 使用工具

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ]
)

# 处理工具调用
if message.stop_reason == "tool_use":
    for block in message.content:
        if block.type == "tool_use":
            tool_name = block.name
            tool_input = block.input
            # 执行工具并返回结果
```

### 工具响应

```python
messages.append({"role": "user", "content": [
    {
        "type": "tool_result",
        "tool_use_id": tool_use_block.id,
        "content": "Temperature: 25°C, Sunny"
    }
]})

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=tools,
    messages=messages
)
```

## Prompt最佳实践

### 1. 使用XML标签

```python
prompt = """
Please analyze the following code:

<code>
def hello():
    print("Hello, World!")
</code>

Provide:
1. A summary
2. Potential improvements
3. Test cases
"""
```

### 2. 角色设定

```python
system = """You are an expert Python developer with 15 years of experience.
You specialize in:
- Clean code and SOLID principles
- Performance optimization
- Security best practices

Always provide:
1. Working code examples
2. Explanation of your approach
3. Potential edge cases"""
```

### 3. 结构化输出

```python
prompt = """
Analyze the text and output in the following JSON format:

<output_format>
{
    "sentiment": "positive|negative|neutral",
    "key_topics": ["topic1", "topic2"],
    "summary": "brief summary"
}
</output_format>

Text to analyze:
<text>
{input_text}
</text>
"""
```

## 错误处理

```python
from anthropic import Anthropic, APIError, RateLimitError

try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # 实现退避重试
except APIError as e:
    print(f"API error: {e}")
```

## 最佳实践

1. **使用系统提示**: 将角色和上下文放在系统提示中
2. **限制输出长度**: 使用 max_tokens 控制响应长度
3. **处理截断**: 检查 stop_reason 处理不完整响应
4. **使用工具**: 对于需要外部数据的任务使用工具
5. **流式处理**: 对于长响应使用流式处理

## 相关技能

- [openai](../ai/openai) - OpenAI API
- [langchain](../ai/langchain) - LangChain框架
- [prompt-engineering](../ai/prompt-engineering) - Prompt工程
- [rag-system](../ai/rag-system) - RAG系统
