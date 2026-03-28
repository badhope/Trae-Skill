---
name: prompt-engineering
description: "Prompt engineering for LLM optimization with techniques, patterns, and best practices. Keywords: prompt, llm, gpt, claude, 提示词, 提示工程"
layer: domain
role: specialist
version: 2.0.0
domain: ai
languages:
  - text
frameworks:
  - openai
  - anthropic
invoked_by:
  - coding-workflow
  - ai-agent
  - langchain
capabilities:
  - prompt_design
  - few_shot_learning
  - chain_of_thought
  - structured_output
  - prompt_optimization
---

# Prompt Engineering

Prompt工程专家，专注于LLM提示词优化、模式设计和最佳实践。

## 适用场景

- LLM应用开发
- 提示词优化
- 输出格式控制
- 复杂推理任务
- 多轮对话设计

## 核心技术

### 1. 基础Prompt模式

```python
SYSTEM_PROMPT = """You are an expert software architect with deep knowledge in:
- System design and architecture patterns
- Cloud-native development
- Microservices architecture
- Performance optimization

Your responses should be:
1. Technically accurate and detailed
2. Include code examples when relevant
3. Consider scalability and maintainability
4. Follow industry best practices"""

USER_PROMPT_TEMPLATE = """
Task: {task_description}

Context:
{context}

Requirements:
{requirements}

Constraints:
{constraints}

Please provide a detailed solution.
"""

def create_prompt(system: str, user: str, examples: list = None) -> str:
    parts = [f"System: {system}"]
    
    if examples:
        parts.append("\nExamples:")
        for ex in examples:
            parts.append(f"Input: {ex['input']}")
            parts.append(f"Output: {ex['output']}")
    
    parts.append(f"\nUser: {user}")
    
    return "\n".join(parts)
```

### 2. Few-Shot Learning

```python
FEW_SHOT_PROMPT = """
You are a code reviewer. Analyze the following code and provide feedback.

Examples:

Code:
```python
def calc(a, b):
    return a + b
```

Review:
- Function name is too vague, consider `add_numbers` or `sum_values`
- Missing type hints for parameters and return value
- No docstring explaining the function purpose
- No input validation for edge cases

Code:
```python
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)
```

Review:
- Good: Type hints are present
- Good: Docstring explains the function purpose
- Good: Handles empty list edge case
- Suggestion: Consider using `statistics.mean()` for clarity

Now review this code:

Code:
```python
{code}
```

Review:
"""

def create_few_shot_prompt(
    task_description: str,
    examples: list[dict],
    input_text: str
) -> str:
    prompt = f"Task: {task_description}\n\n"
    
    for i, example in enumerate(examples, 1):
        prompt += f"Example {i}:\n"
        prompt += f"Input: {example['input']}\n"
        prompt += f"Output: {example['output']}\n\n"
    
    prompt += f"Now process this input:\n{input_text}\n\nOutput:"
    
    return prompt
```

### 3. Chain of Thought

```python
CHAIN_OF_THOUGHT_PROMPT = """
Solve the following problem step by step. Show your reasoning process.

Problem: {problem}

Let's think through this step by step:

1. First, let's understand what we're being asked:
   [Analyze the problem]

2. Let's identify the key information:
   [Extract relevant details]

3. Now, let's work through the solution:
   [Step-by-step reasoning]

4. Let's verify our answer:
   [Validation]

5. Final answer:
   [Conclusion]
"""

COT_WITH_SELF_CONSISTENCY = """
Solve this problem using multiple approaches and find the most consistent answer.

Problem: {problem}

Approach 1:
[First method of solving]

Approach 2:
[Second method of solving]

Approach 3:
[Third method of solving]

Comparison:
[Compare results from different approaches]

Most consistent answer:
[Final conclusion]
"""

TREE_OF_THOUGHTS_PROMPT = """
Explore multiple solution paths for this problem.

Problem: {problem}

Generate 3 different initial approaches:

Thought 1:
[First approach and its reasoning]

Thought 2:
[Second approach and its reasoning]

Thought 3:
[Third approach and its reasoning]

Evaluate each thought:
- Thought 1 evaluation: [Pros and cons]
- Thought 2 evaluation: [Pros and cons]
- Thought 3 evaluation: [Pros and cons]

Best approach:
[Select and justify the best approach]

Final solution:
[Implement the chosen approach]
"""
```

### 4. 结构化输出

```python
from pydantic import BaseModel, Field
from typing import List, Optional
import json

class CodeReview(BaseModel):
    overall_score: int = Field(ge=1, le=10, description="Overall code quality score")
    issues: List[dict] = Field(description="List of issues found")
    suggestions: List[str] = Field(description="Improvement suggestions")
    security_concerns: List[str] = Field(default_factory=list)
    performance_notes: List[str] = Field(default_factory=list)

STRUCTURED_OUTPUT_PROMPT = """
Analyze the following code and provide a structured review.

Code:
```{language}
{code}
```

Provide your analysis in the following JSON format:
{schema}

Important:
- Ensure the output is valid JSON
- All fields are required
- Use empty arrays for categories with no issues
"""

def create_structured_prompt(
    code: str,
    language: str,
    schema: type[BaseModel]
) -> str:
    schema_json = json.dumps(schema.model_json_schema(), indent=2)
    
    return STRUCTURED_OUTPUT_PROMPT.format(
        language=language,
        code=code,
        schema=schema_json
    )

XML_OUTPUT_PROMPT = """
Extract information from the text and format as XML.

Text:
{text}

Output format:
<analysis>
  <entities>
    <entity type="PERSON">...</entity>
    <entity type="ORGANIZATION">...</entity>
    <entity type="LOCATION">...</entity>
  </entities>
  <sentiment>positive|negative|neutral</sentiment>
  <summary>...</summary>
  <keywords>
    <keyword>...</keyword>
  </keywords>
</analysis>
"""
```

### 5. 高级技术

```python
ROLE_PLAYING_PROMPT = """
You are {role_name}, a {role_description}.

Your characteristics:
{characteristics}

Your expertise:
{expertise}

Your communication style:
{communication_style}

Current scenario:
{scenario}

Remember to stay in character throughout the conversation.
"""

METACOGNITION_PROMPT = """
Before answering, reflect on your understanding:

Question: {question}

1. What is the core of this question asking?
   [Your interpretation]

2. What knowledge do I need to answer this?
   [Required knowledge]

3. What are potential pitfalls or ambiguities?
   [Potential issues]

4. How confident am I in different aspects?
   [Confidence levels]

Now provide your answer:
[Your response]

After answering, evaluate:
- Did I address all parts of the question?
- Are there any gaps in my reasoning?
- Could I improve my answer?
"""

CONSTITUTIONAL_PROMPT = """
You must follow these principles when responding:

1. Be helpful but harmless
   - Provide useful information
   - Avoid harmful content

2. Be honest
   - Acknowledge uncertainty
   - Don't make up facts

3. Respect privacy
   - Don't share personal information
   - Protect sensitive data

4. Be balanced
   - Present multiple viewpoints
   - Acknowledge limitations

Now respond to: {input}
"""

SELF_REFINE_PROMPT = """
Initial Response:
{initial_response}

Critique the above response:
- What could be improved?
- What is missing?
- What could be more accurate?

Improved Response:
[Provide an improved version]

Final Response:
[The best version after refinement]
"""
```

### 6. Prompt模板库

```python
PROMPT_TEMPLATES = {
    "code_generation": """
Generate {language} code for the following requirement:

Requirement: {requirement}

Constraints:
{constraints}

Style guidelines:
{style_guidelines}

Provide:
1. The code implementation
2. Brief explanation
3. Usage example
""",

    "code_explanation": """
Explain this code in detail:

```{language}
{code}
```

Provide:
1. High-level overview
2. Line-by-line explanation
3. Key concepts used
4. Potential improvements
""",

    "debugging": """
Debug the following code:

```{language}
{code}
```

Error message:
{error}

Analyze:
1. What is the error?
2. Why does it occur?
3. How to fix it?

Provide the corrected code.
""",

    "refactoring": """
Refactor this code to improve its quality:

```{language}
{code}
```

Focus on:
- Readability
- Performance
- Maintainability
- Best practices

Provide the refactored code with explanations.
""",

    "documentation": """
Generate documentation for:

```{language}
{code}
```

Include:
1. Brief description
2. Parameters/Arguments
3. Return value
4. Usage examples
5. Edge cases
"""
}
```

## 最佳实践

1. **清晰指令**: 明确、具体地描述任务
2. **示例驱动**: 使用Few-Shot提供示例
3. **结构化输出**: 定义输出格式
4. **迭代优化**: 测试和改进Prompt
5. **版本控制**: 管理Prompt版本
6. **Token优化**: 控制Prompt长度

## 相关技能

- [langchain](../langchain) - LangChain框架
- [openai-api](../openai-api) - OpenAI API
- [rag-system](../rag-system) - RAG系统
