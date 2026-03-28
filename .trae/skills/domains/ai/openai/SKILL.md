---
name: openai
description: "OpenAI API integration for GPT models, embeddings, and assistants. Keywords: openai, gpt, chatgpt, embeddings, dalle, whisper, openai api"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
  - typescript
frameworks:
  - openai
  - langchain
invoked_by:
  - code-generator
  - langchain
  - rag-system
capabilities:
  - chat_completion
  - embedding_generation
  - image_generation
  - audio_transcription
triggers:
  keywords:
    - openai
    - gpt
    - chatgpt
    - gpt-4
    - gpt-3.5
    - dalle
    - whisper
    - embeddings
metrics:
  avg_execution_time: 3s
  success_rate: 0.96
  api_efficiency: 0.92
---

# OpenAI

OpenAI API集成，用于GPT模型、嵌入和助手。

## 目的

提供OpenAI API的最佳实践：
- Chat Completions API
- Embeddings API
- DALL-E图像生成
- Whisper语音转录

## 能力

- **聊天补全**: GPT模型对话补全
- **嵌入生成**: 文本嵌入向量生成
- **图像生成**: DALL-E图像生成
- **语音转录**: Whisper语音识别

## 模型对比

| 模型 | 上下文 | 特点 | 适用场景 |
|------|--------|------|----------|
| gpt-4-turbo | 128K | 最新旗舰 | 复杂任务 |
| gpt-4 | 8K | 高质量 | 重要任务 |
| gpt-3.5-turbo | 16K | 快速经济 | 日常任务 |
| gpt-4-vision | 128K | 多模态 | 图像理解 |

## API基础

### 安装

```bash
pip install openai
```

### Chat Completions

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### 流式响应

```python
stream = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## 函数调用

### 定义函数

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### 使用函数

```python
response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    # 执行函数
    result = get_weather(arguments["location"])
    
    # 返回结果
    messages = [
        {"role": "user", "content": "What's the weather in Tokyo?"},
        response.choices[0].message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
    ]
    
    final_response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )
```

## Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Your text here"
)

embedding = response.data[0].embedding
```

## 图像生成

### DALL-E 3

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A serene mountain landscape at sunset",
    size="1024x1024",
    quality="standard",
    n=1
)

image_url = response.data[0].url
```

### 图像编辑

```python
response = client.images.edit(
    model="dall-e-2",
    image=open("input.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="Add a sunset",
    n=1,
    size="1024x1024"
)
```

## 语音API

### 转录

```python
response = client.audio.transcriptions.create(
    model="whisper-1",
    file=open("audio.mp3", "rb"),
    language="zh"
)

print(response.text)
```

### 翻译

```python
response = client.audio.translations.create(
    model="whisper-1",
    file=open("audio.mp3", "rb")
)

print(response.text)  # 输出英文
```

### TTS

```python
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello, world!"
)

response.stream_to_file("output.mp3")
```

## Assistants API

### 创建助手

```python
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a math tutor.",
    model="gpt-4-turbo",
    tools=[{"type": "code_interpreter"}]
)
```

### 运行助手

```python
thread = client.beta.threads.create()

client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Solve x^2 + 1 = 0"
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

messages = client.beta.threads.messages.list(thread_id=thread.id)
```

## 最佳实践

### 1. 错误处理

```python
from openai import APIError, RateLimitError, APIConnectionError

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    time.sleep(60)
    retry()
except APIConnectionError:
    handle_connection_error()
except APIError as e:
    log_error(e)
```

### 2. 成本优化

```python
# 使用更便宜的模型
model = "gpt-3.5-turbo" if simple_task else "gpt-4-turbo"

# 限制输出长度
response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=500
)
```

### 3. 缓存

```python
import hashlib

def cached_completion(messages, model="gpt-4-turbo"):
    cache_key = hashlib.md5(
        str(messages).encode() + model.encode()
    ).hexdigest()
    
    if cache := cache.get(cache_key):
        return cache
    
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    cache.set(cache_key, response.choices[0].message.content)
    return response.choices[0].message.content
```

## 相关技能

- [langchain](../langchain) - LangChain框架
- [rag-system](../rag-system) - RAG系统
- [claude-api](../claude-api) - Claude API
- [llm-evaluation](../llm-evaluation) - LLM评估
