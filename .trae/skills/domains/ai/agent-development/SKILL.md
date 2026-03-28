---
name: agent-development
description: "AI agent development for autonomous task execution, planning, and tool use. Keywords: agent, autonomous, planning, tool use, ai agent, 智能体, 代理"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - python
  - typescript
frameworks:
  - langchain
  - autogen
  - crewai
invoked_by:
  - langchain
  - task-planner
capabilities:
  - agent_architecture
  - planning_reasoning
  - tool_integration
  - memory_management
triggers:
  keywords:
    - agent
    - autonomous
    - planning
    - tool use
    - multi-agent
    - 智能体
    - 代理
    - 自主
metrics:
  avg_execution_time: 5s
  success_rate: 0.90
  task_completion_rate: 0.88
---

# Agent Development

AI智能体开发，用于自主任务执行、规划和工具使用。

## 目的

提供AI智能体开发的最佳实践：
- 智能体架构设计
- 规划和推理能力
- 工具集成和使用
- 记忆管理

## 能力

- **智能体架构**: 设计和实现智能体架构
- **规划推理**: 实现规划和推理能力
- **工具集成**: 集成外部工具和API
- **记忆管理**: 管理智能体记忆和状态

## 智能体架构

### 核心组件

```
┌─────────────────────────────────────────┐
│              Agent Core                  │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Planner │  │ Reasoner│  │ Executor│ │
│  └─────────┘  └─────────┘  └─────────┘ │
├─────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Memory  │  │  Tools  │  │  State  │ │
│  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────┘
```

### 智能体类型

| 类型 | 描述 | 示例 |
|------|------|------|
| ReAct | 推理+行动交替 | LangChain ReActAgent |
| Plan-and-Execute | 先规划后执行 | BabyAGI |
| Multi-Agent | 多智能体协作 | AutoGen, CrewAI |
| Hierarchical | 分层智能体 | MetaGPT |

## 框架对比

### LangChain Agent

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations"
    )
]

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({"input": "What is 2 + 2?"})
```

### AutoGen

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4"}
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "coding"}
)

user_proxy.initiate_chat(
    assistant,
    message="Write a Python script to analyze stock data"
)
```

### CrewAI

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Researcher",
    goal="Find relevant information",
    backstory="Expert researcher",
    tools=[search_tool]
)

writer = Agent(
    role="Writer",
    goal="Write engaging content",
    backstory="Professional writer"
)

task = Task(
    description="Research and write about AI",
    agent=researcher
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task]
)

result = crew.kickoff()
```

## 规划模式

### ReAct模式

```
Thought: I need to find the current weather
Action: get_weather
Action Input: {"location": "Tokyo"}
Observation: Temperature: 25°C, Sunny
Thought: I now have the weather information
Final Answer: The current weather in Tokyo is 25°C and sunny.
```

### Plan-and-Execute模式

```python
# 1. 规划阶段
plan = planner.plan(goal)
# ["Search for topic", "Summarize findings", "Write report"]

# 2. 执行阶段
for step in plan:
    result = executor.execute(step)
    state.update(result)

# 3. 反思阶段
reflection = reflector.reflect(results)
```

### Tree-of-Thought模式

```python
def tree_of_thought(problem, depth=3):
    thoughts = generate_thoughts(problem)
    
    for thought in thoughts:
        state = evaluate_thought(thought)
        if state.is_promising:
            expand_thought(thought, depth - 1)
    
    return select_best_path()
```

## 工具集成

### 工具定义

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CalculatorInput(BaseModel):
    expression: str = Field(description="Math expression to evaluate")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluate math expressions"
    args_schema = CalculatorInput
    
    def _run(self, expression: str) -> str:
        try:
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"
```

### MCP工具集成

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_mcp_tool():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("tool_name", arguments)
```

## 记忆管理

### 记忆类型

| 类型 | 描述 | 实现 |
|------|------|------|
| 短期记忆 | 当前对话上下文 | ConversationBuffer |
| 长期记忆 | 持久化存储 | VectorStore |
| 工作记忆 | 任务执行状态 | StateManager |
| 情景记忆 | 历史交互记录 | EpisodicMemory |

### 记忆实现

```python
from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory

# 短期记忆
short_term = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# 长期记忆
long_term = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever()
)

# 组合记忆
class AgentMemory:
    def __init__(self):
        self.short_term = short_term
        self.long_term = long_term
        self.working = {}
    
    def remember(self, key, value):
        self.working[key] = value
        self.long_term.save_context({key: value}, {})
    
    def recall(self, query):
        return self.long_term.load_memory_variables({"query": query})
```

## 多智能体协作

### 协作模式

```python
# 层级协作
manager = Agent(role="manager", can_delegate=True)
worker1 = Agent(role="worker1", can_delegate=False)
worker2 = Agent(role="worker2", can_delegate=False)

# 对等协作
agents = [agent1, agent2, agent3]
for agent in agents:
    agent.can_communicate_with(agents)

# 竞争协作
results = parallel_execute(task, agents)
best_result = select_best(results)
```

### 通信协议

```python
class AgentMessage:
    sender: str
    receiver: str
    content: str
    message_type: str  # request, response, broadcast
    metadata: dict

def broadcast(agents, message):
    for agent in agents:
        agent.receive(message)

def request_response(sender, receiver, request):
    response = receiver.process(request)
    sender.receive(response)
```

## 最佳实践

1. **明确目标**: 清晰定义智能体的目标和约束
2. **工具选择**: 只提供必要的工具
3. **错误处理**: 实现重试和回退机制
4. **状态管理**: 维护清晰的执行状态
5. **可观测性**: 记录决策过程和执行日志

## 相关技能

- [langchain](../langchain) - LangChain框架
- [mcp-server-development](../../mcp/server-development) - MCP服务器开发
- [task-planner](../../../meta/task-planner) - 任务规划
- [tool-use](../../../actions/tools/tool-use) - 工具使用
