# MCP Prompt Templates

## Description
MCP 提示词模板专家。帮助设计、实现和管理 MCP 提示词模板，提供可复用的提示词模式。

## Details

### 功能特性
- 提示词模板设计
- 参数化提示词
- 多轮对话模板
- 提示词组合
- 模板版本管理
- 提示词最佳实践

### 提示词模板基础

#### 静态提示词
```typescript
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "code_review",
      description: "Review code for best practices and potential issues"
    },
    {
      name: "explain_code",
      description: "Explain what a piece of code does"
    }
  ]
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name } = request.params;
  
  if (name === "code_review") {
    return {
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: "Please review the following code for best practices, potential bugs, and improvements:\n\n```\n{code}\n```"
        }
      }]
    };
  }
});
```

#### 参数化提示词
```typescript
server.setRequestHandler(ListPromptsRequestSchema, async () => ({
  prompts: [
    {
      name: "analyze_data",
      description: "Analyze data with a specific focus",
      arguments: [
        {
          name: "data",
          description: "The data to analyze",
          required: true
        },
        {
          name: "focus",
          description: "What to focus on in the analysis",
          required: false
        },
        {
          name: "format",
          description: "Output format (summary, detailed, bullet)",
          required: false
        }
      ]
    }
  ]
}));

server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "analyze_data") {
    const focus = args.focus || "general patterns and insights";
    const format = args.format || "summary";
    
    return {
      messages: [{
        role: "user",
        content: {
          type: "text",
          text: `Analyze the following data with a focus on ${focus}.

Data:
${args.data}

Please provide your analysis in ${format} format.`
        }
      }]
    };
  }
});
```

### 多轮对话模板

#### 带系统提示的模板
```typescript
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "expert_consultation") {
    return {
      messages: [
        {
          role: "system",
          content: {
            type: "text",
            text: `You are an expert in ${args.domain}. 
Provide detailed, accurate, and helpful responses.
Use technical terminology appropriate for ${args.expertise_level} level.`
          }
        },
        {
          role: "user",
          content: {
            type: "text",
            text: args.question
          }
        }
      ]
    };
  }
});
```

#### 带历史上下文的模板
```typescript
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "continue_conversation") {
    const history = args.conversation_history || [];
    const messages = [];
    
    // 添加历史消息
    for (const msg of history) {
      messages.push({
        role: msg.role,
        content: { type: "text", text: msg.content }
      });
    }
    
    // 添加当前问题
    messages.push({
      role: "user",
      content: {
        type: "text",
        text: args.current_question
      }
    });
    
    return { messages };
  }
});
```

### 提示词模板库

#### 代码相关模板
```typescript
const codePrompts = {
  code_review: {
    name: "code_review",
    description: "Comprehensive code review",
    arguments: [
      { name: "code", required: true },
      { name: "language", required: false },
      { name: "focus_areas", required: false }
    ],
    template: (args: any) => `Review the following ${args.language || ''} code:

\`\`\`${args.language || ''}
${args.code}
\`\`\`

Focus areas: ${args.focus_areas || 'code quality, potential bugs, performance, security'}

Provide:
1. Overall assessment
2. Specific issues found
3. Suggested improvements
4. Best practice recommendations`
  },
  
  debug_code: {
    name: "debug_code",
    description: "Debug code issues",
    arguments: [
      { name: "code", required: true },
      { name: "error", required: false },
      { name: "expected_behavior", required: false }
    ],
    template: (args: any) => `Debug the following code:

\`\`\`
${args.code}
\`\`\`

${args.error ? `Error encountered:\n${args.error}\n` : ''}
${args.expected_behavior ? `Expected behavior:\n${args.expected_behavior}\n` : ''}

Please:
1. Identify the root cause
2. Explain why the issue occurs
3. Provide a fix
4. Suggest how to prevent similar issues`
  },
  
  refactor_code: {
    name: "refactor_code",
    description: "Refactor code for better quality",
    arguments: [
      { name: "code", required: true },
      { name: "goals", required: false }
    ],
    template: (args: any) => `Refactor the following code:

\`\`\`
${args.code}
\`\`\`

Refactoring goals: ${args.goals || 'readability, maintainability, performance'}

Provide:
1. Refactored code
2. Explanation of changes
3. Benefits of the refactoring`
  }
};
```

#### 文档相关模板
```typescript
const docPrompts = {
  write_readme: {
    name: "write_readme",
    description: "Generate README documentation",
    arguments: [
      { name: "project_name", required: true },
      { name: "description", required: true },
      { name: "features", required: false },
      { name: "installation", required: false }
    ],
    template: (args: any) => `Create a comprehensive README.md for:

Project: ${args.project_name}
Description: ${args.description}
${args.features ? `Features:\n${args.features}\n` : ''}
${args.installation ? `Installation steps:\n${args.installation}\n` : ''}

Include:
- Project title and badges
- Description
- Features list
- Installation instructions
- Usage examples
- Configuration options
- Contributing guidelines
- License`
  },
  
  write_api_docs: {
    name: "write_api_docs",
    description: "Generate API documentation",
    arguments: [
      { name: "endpoints", required: true },
      { name: "base_url", required: false },
      { name: "auth_method", required: false }
    ],
    template: (args: any) => `Generate API documentation for:

Base URL: ${args.base_url || 'https://api.example.com'}
Authentication: ${args.auth_method || 'Bearer token'}

Endpoints:
${args.endpoints}

Include for each endpoint:
- HTTP method and path
- Description
- Request parameters
- Request body schema
- Response schema
- Error codes
- Example requests and responses`
  }
};
```

#### 分析相关模板
```typescript
const analysisPrompts = {
  analyze_requirements: {
    name: "analyze_requirements",
    description: "Analyze and structure requirements",
    arguments: [
      { name: "requirements", required: true },
      { name: "context", required: false }
    ],
    template: (args: any) => `Analyze the following requirements:

${args.requirements}

${args.context ? `Context: ${args.context}\n` : ''}

Provide:
1. Functional requirements breakdown
2. Non-functional requirements
3. User stories
4. Acceptance criteria
5. Potential risks
6. Dependencies
7. Questions/clarifications needed`
  },
  
  analyze_architecture: {
    name: "analyze_architecture",
    description: "Analyze system architecture",
    arguments: [
      { name: "system_description", required: true },
      { name: "concerns", required: false }
    ],
    template: (args: any) => `Analyze the following system architecture:

${args.system_description}

${args.concerns ? `Specific concerns: ${args.concerns}\n` : ''}

Evaluate:
1. Architecture patterns used
2. Component interactions
3. Scalability considerations
4. Security considerations
5. Performance implications
6. Potential bottlenecks
7. Improvement suggestions`
  }
};
```

### 提示词组合

#### 链式提示词
```typescript
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === "full_code_review") {
    // 返回一个提示词链
    return {
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Perform a comprehensive code review for:

\`\`\`
${args.code}
\`\`\`

Step 1: Analyze code structure and patterns
Step 2: Identify potential bugs and issues
Step 3: Check for security vulnerabilities
Step 4: Evaluate performance implications
Step 5: Suggest improvements

Provide detailed findings for each step.`
          }
        }
      ],
      // 可以包含下一步提示词的建议
      metadata: {
        suggestedFollowUp: "implement_improvements"
      }
    };
  }
});
```

### 模板版本管理

```typescript
interface PromptVersion {
  name: string;
  version: string;
  deprecated: boolean;
  template: (args: any) => string;
  changelog: string;
}

const promptVersions: Map<string, PromptVersion[]> = new Map([
  ["code_review", [
    {
      name: "code_review",
      version: "2.0.0",
      deprecated: false,
      template: (args) => `...`,
      changelog: "Added security analysis"
    },
    {
      name: "code_review",
      version: "1.0.0",
      deprecated: true,
      template: (args) => `...`,
      changelog: "Initial version"
    }
  ]]
]);

server.setRequestHandler(ListPromptsRequestSchema, async () => {
  const prompts = [];
  
  for (const [name, versions] of promptVersions) {
    const latest = versions.find(v => !v.deprecated);
    if (latest) {
      prompts.push({
        name,
        description: `Version ${latest.version}: ${latest.changelog}`
      });
    }
  }
  
  return { prompts };
});
```

### 最佳实践

1. **清晰的参数定义**: 每个参数都有描述和是否必需
2. **合理的默认值**: 为可选参数提供合理的默认值
3. **输入验证**: 验证参数格式和内容
4. **错误提示**: 提供清晰的错误信息
5. **版本管理**: 管理模板版本，支持平滑升级
6. **文档完善**: 为每个模板提供使用说明和示例

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `prompt-composition` - 提示词组合
- `instruction-refinement` - 指令润色
