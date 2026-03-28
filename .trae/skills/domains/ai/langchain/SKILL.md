---
name: langchain
description: "LangChain framework for building LLM-powered applications with chains, agents, and memory. Keywords: langchain, llm, chain, agent, rag, prompt"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
  - typescript
frameworks:
  - langchain
  - openai
  - anthropic
invoked_by:
  - coding-workflow
  - ai-agent
capabilities:
  - chain_building
  - agent_development
  - rag_implementation
  - memory_management
  - tool_integration
---

# LangChain

LangChain框架专家，专注于构建LLM应用、链式调用和智能代理。

## 适用场景

- RAG应用开发
- 智能对话系统
- 文档问答
- 自动化工作流
- 多Agent协作

## 核心架构

### 1. Chain构建

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import BaseModel, Field
from typing import List, Optional

llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

class AnalysisResult(BaseModel):
    sentiment: str = Field(description="Sentiment: positive, negative, or neutral")
    confidence: float = Field(description="Confidence score between 0 and 1")
    keywords: List[str] = Field(description="Extracted keywords")
    summary: str = Field(description="Brief summary of the text")

json_parser = JsonOutputParser(pydantic_object=AnalysisResult)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert text analyzer. Analyze the following text and provide structured output."),
    ("human", "{text}"),
    ("system", "Format instructions: {format_instructions}")
])

chain = prompt | llm | json_parser

result = chain.invoke({
    "text": "I love this product! It exceeded my expectations.",
    "format_instructions": json_parser.get_format_instructions()
})

prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain_with_history = prompt_with_history | llm | StrOutputParser()

chain_with_message_history = RunnableWithMessageHistory(
    chain_with_history,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

response = chain_with_message_history.invoke(
    {"input": "What's the weather like?"},
    config={"configurable": {"session_id": "user123"}}
)

def retrieve_documents(query: str) -> List[str]:
    return ["Document 1 content", "Document 2 content"]

rag_chain = (
    {"context": retrieve_documents, "question": RunnablePassthrough()}
    | ChatPromptTemplate.from_template("""
Answer the question based on the context:
Context: {context}
Question: {question}
Answer:
""")
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is the main topic?")
```

### 2. Agent开发

```python
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool, StructuredTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool

def get_current_weather(location: str, unit: str = "celsius") -> str:
    return f"The weather in {location} is sunny, 25°{unit[0].upper()}"

weather_tool = StructuredTool.from_function(
    func=get_current_weather,
    name="get_current_weather",
    description="Get the current weather for a location"
)

search_tool = DuckDuckGoSearchRun()
python_tool = PythonREPLTool()

tools = [
    Tool(
        name="search",
        func=search_tool.run,
        description="Useful for searching the internet for current information"
    ),
    weather_tool,
    Tool(
        name="python_repl",
        func=python_tool.run,
        description="Execute Python code. Use for calculations and data processing."
    )
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

result = agent_executor.invoke({
    "input": "What's the weather in Tokyo and calculate 25 * 4?"
})
```

### 3. RAG实现

```python
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.retrievers import ContextualCompressionRetriever, EnsembleRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers.multi_query import MultiQueryRetriever

loader = PyPDFLoader("document.pdf")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

basic_retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5}
)

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=basic_retriever,
    llm=llm
)

compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=basic_retriever
)

ensemble_retriever = EnsembleRetriever(
    retrievers=[basic_retriever, mmr_retriever],
    weights=[0.5, 0.5]
)

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

retrieval_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, say that you don't know.
Use three sentences maximum and keep the answer concise.

Context: {context}"""),
    ("human", "{input}")
])

combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_prompt)
rag_chain = create_retrieval_chain(basic_retriever, combine_docs_chain)

response = rag_chain.invoke({"input": "What is the document about?"})
```

### 4. Memory管理

```python
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain.memory import ConversationSummaryMemory, VectorStoreRetrieverMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory

buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

window_memory = ConversationBufferWindowMemory(
    k=5,
    memory_key="chat_history",
    return_messages=True
)

summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

def get_redis_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379"
    )

vector_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
)

from langchain.chains import ConversationalRetrievalChain

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=basic_retriever,
    memory=buffer_memory,
    return_source_documents=True,
    verbose=True
)

result = qa_chain({"question": "What is the main topic?"})
```

### 5. 工具集成

```python
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, Type
import requests

class WeatherInput(BaseModel):
    location: str = Field(description="City name or coordinates")
    unit: Optional[str] = Field(default="celsius", description="Temperature unit")

class WeatherTool(BaseTool):
    name = "weather"
    description = "Get weather information for a location"
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, location: str, unit: str = "celsius") -> str:
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json",
            params={"key": "YOUR_API_KEY", "q": location}
        )
        data = response.json()
        return f"Weather in {location}: {data['current']['temp_c']}°C"

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

tools = [
    WeatherTool(),
    calculate,
    search_web
]
```

## 最佳实践

1. **Prompt工程**: 使用结构化Prompt模板
2. **错误处理**: 添加重试和fallback机制
3. **Token管理**: 监控和控制Token使用
4. **缓存策略**: 缓存嵌入和响应
5. **流式输出**: 使用流式响应提升体验
6. **安全考虑**: 验证输入和输出

## 相关技能

- [openai-api](../openai-api) - OpenAI API
- [rag-system](../rag-system) - RAG系统
- [prompt-engineering](../prompt-engineering) - Prompt工程
- [backend-python](../../backend/python) - Python后端
