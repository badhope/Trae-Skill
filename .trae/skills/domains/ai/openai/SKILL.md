---
name: openai
description: "OpenAI API integration for GPT, DALL-E, and Whisper models. Keywords: openai, gpt, chatgpt, dall-e, whisper, AI"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
  - javascript
  - typescript
frameworks:
  - openai
  - langchain
invoked_by:
  - coding-workflow
  - ai-agent
capabilities:
  - text_generation
  - image_generation
  - speech_recognition
  - embeddings
  - fine_tuning
---

# OpenAI

OpenAI API集成专家，专注于GPT、DALL-E和Whisper模型的应用开发。

## 适用场景

- 文本生成与对话
- 图像生成
- 语音识别
- 文本嵌入
- 模型微调

## 核心架构

### 1. Chat Completions

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

interface Message {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

interface ChatOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  stream?: boolean;
}

async function chat(
  messages: Message[],
  options: ChatOptions = {}
): Promise<string> {
  const response = await openai.chat.completions.create({
    model: options.model || 'gpt-4-turbo-preview',
    messages,
    temperature: options.temperature ?? 0.7,
    max_tokens: options.maxTokens,
  });
  
  return response.choices[0].message.content || '';
}

async function chatStream(
  messages: Message[],
  onChunk: (chunk: string) => void,
  options: ChatOptions = {}
): Promise<void> {
  const stream = await openai.chat.completions.create({
    model: options.model || 'gpt-4-turbo-preview',
    messages,
    temperature: options.temperature ?? 0.7,
    max_tokens: options.maxTokens,
    stream: true,
  });
  
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    onChunk(content);
  }
}

async function chatWithFunctions(
  messages: Message[],
  functions: OpenAI.Chat.ChatCompletionCreateParams['functions']
): Promise<any> {
  const response = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages,
    functions,
    function_call: 'auto',
  });
  
  const message = response.choices[0].message;
  
  if (message.function_call) {
    return {
      type: 'function_call',
      name: message.function_call.name,
      arguments: JSON.parse(message.function_call.arguments),
    };
  }
  
  return {
    type: 'message',
    content: message.content,
  };
}

const weatherFunction = {
  name: 'get_weather',
  description: 'Get the current weather in a location',
  parameters: {
    type: 'object',
    properties: {
      location: {
        type: 'string',
        description: 'City and country, e.g., "Beijing, China"',
      },
      unit: {
        type: 'string',
        enum: ['celsius', 'fahrenheit'],
      },
    },
    required: ['location'],
  },
};

const result = await chatWithFunctions(
  [{ role: 'user', content: 'What is the weather in Beijing?' }],
  [weatherFunction]
);
```

### 2. Assistants API

```typescript
async function createAssistant() {
  const assistant = await openai.beta.assistants.create({
    name: 'Code Helper',
    instructions: 'You are a helpful coding assistant.',
    tools: [{ type: 'code_interpreter' }, { type: 'retrieval' }],
    model: 'gpt-4-turbo-preview',
  });
  
  return assistant;
}

async function createThread() {
  return openai.beta.threads.create();
}

async function addMessage(threadId: string, content: string) {
  return openai.beta.threads.messages.create(threadId, {
    role: 'user',
    content,
  });
}

async function runAssistant(threadId: string, assistantId: string) {
  const run = await openai.beta.threads.runs.create(threadId, {
    assistant_id: assistantId,
  });
  
  let status = run.status;
  
  while (status === 'queued' || status === 'in_progress') {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    const runStatus = await openai.beta.threads.runs.retrieve(
      threadId,
      run.id
    );
    status = runStatus.status;
    
    if (status === 'requires_action') {
      const toolCalls = runStatus.required_action?.submit_tool_outputs.tool_calls;
      
      if (toolCalls) {
        const outputs = await Promise.all(
          toolCalls.map(async (call) => {
            const result = await executeToolCall(call);
            return {
              tool_call_id: call.id,
              output: JSON.stringify(result),
            };
          })
        );
        
        await openai.beta.threads.runs.submitToolOutputs(
          threadId,
          run.id,
          { tool_outputs: outputs }
        );
      }
    }
  }
  
  const messages = await openai.beta.threads.messages.list(threadId);
  return messages.data[0].content[0].text.value;
}
```

### 3. Image Generation

```typescript
async function generateImage(
  prompt: string,
  options: {
    size?: '256x256' | '512x512' | '1024x1024';
    quality?: 'standard' | 'hd';
    n?: number;
  } = {}
): Promise<string[]> {
  const response = await openai.images.generate({
    model: 'dall-e-3',
    prompt,
    size: options.size || '1024x1024',
    quality: options.quality || 'standard',
    n: options.n || 1,
  });
  
  return response.data.map(img => img.url!);
}

async function editImage(
  imagePath: string,
  prompt: string,
  maskPath?: string
): Promise<string[]> {
  const response = await openai.images.edit({
    image: fs.createReadStream(imagePath),
    mask: maskPath ? fs.createReadStream(maskPath) : undefined,
    prompt,
    size: '1024x1024',
  });
  
  return response.data.map(img => img.url!);
}

async function createImageVariation(imagePath: string): Promise<string[]> {
  const response = await openai.images.createVariation({
    image: fs.createReadStream(imagePath),
    size: '1024x1024',
    n: 1,
  });
  
  return response.data.map(img => img.url!);
}
```

### 4. Audio Processing

```typescript
async function transcribeAudio(
  audioPath: string,
  options: {
    language?: string;
    prompt?: string;
  } = {}
): Promise<string> {
  const response = await openai.audio.transcriptions.create({
    file: fs.createReadStream(audioPath),
    model: 'whisper-1',
    language: options.language,
    prompt: options.prompt,
  });
  
  return response.text;
}

async function translateAudio(audioPath: string): Promise<string> {
  const response = await openai.audio.translations.create({
    file: fs.createReadStream(audioPath),
    model: 'whisper-1',
  });
  
  return response.text;
}

async function textToSpeech(
  text: string,
  options: {
    voice?: 'alloy' | 'echo' | 'fable' | 'onyx' | 'nova' | 'shimmer';
    speed?: number;
  } = {}
): Promise<Buffer> {
  const response = await openai.audio.speech.create({
    model: 'tts-1',
    input: text,
    voice: options.voice || 'alloy',
    speed: options.speed,
  });
  
  return Buffer.from(await response.arrayBuffer());
}
```

### 5. Embeddings

```typescript
async function createEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text,
  });
  
  return response.data[0].embedding;
}

async function createBatchEmbeddings(texts: string[]): Promise<number[][]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: texts,
  });
  
  return response.data.map(d => d.embedding);
}

function cosineSimilarity(a: number[], b: number[]): number {
  const dotProduct = a.reduce((sum, val, i) => sum + val * b[i], 0);
  const magnitudeA = Math.sqrt(a.reduce((sum, val) => sum + val * val, 0));
  const magnitudeB = Math.sqrt(b.reduce((sum, val) => sum + val * val, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

async function semanticSearch(
  query: string,
  documents: string[],
  topK: number = 5
): Promise<{ document: string; score: number }[]> {
  const queryEmbedding = await createEmbedding(query);
  const docEmbeddings = await createBatchEmbeddings(documents);
  
  const scores = docEmbeddings.map((embedding, i) => ({
    document: documents[i],
    score: cosineSimilarity(queryEmbedding, embedding),
  }));
  
  return scores.sort((a, b) => b.score - a.score).slice(0, topK);
}
```

### 6. Fine-tuning

```typescript
async function uploadTrainingFile(filePath: string): Promise<string> {
  const response = await openai.files.create({
    file: fs.createReadStream(filePath),
    purpose: 'fine-tune',
  });
  
  return response.id;
}

async function createFineTuneJob(
  trainingFileId: string,
  model: string = 'gpt-3.5-turbo'
): Promise<string> {
  const response = await openai.fineTuning.jobs.create({
    training_file: trainingFileId,
    model,
  });
  
  return response.id;
}

async function getFineTuneStatus(jobId: string) {
  return openai.fineTuning.jobs.retrieve(jobId);
}

async function listFineTunedModels() {
  return openai.fineTuning.jobs.list();
}

async function useFineTunedModel(
  modelId: string,
  messages: Message[]
): Promise<string> {
  const response = await openai.chat.completions.create({
    model: modelId,
    messages,
  });
  
  return response.choices[0].message.content || '';
}
```

## 最佳实践

1. **Token管理**: 监控token使用量
2. **错误处理**: 实现重试机制
3. **流式输出**: 使用streaming提升体验
4. **成本控制**: 选择合适的模型
5. **安全存储**: 保护API密钥
6. **内容审核**: 检查生成内容

## 相关技能

- [langchain](../langchain) - LangChain框架
- [vector-database](../vector-database) - 向量数据库
- [ai-agent](../../meta/ai-agent) - AI代理
