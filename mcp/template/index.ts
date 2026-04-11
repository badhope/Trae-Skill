import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'your-skill-name',
  version: '1.0.0',
  description: '一句话描述这个技能的核心价值',
  author: 'Your Name',
  icon: '✨'
})
  .addTool({
    name: 'example_tool',
    description: '工具功能说明，要足够具体让 AI 理解何时调用',
    parameters: {
      param1: {
        type: 'string',
        description: '参数说明',
        required: true
      },
      optionalParam: {
        type: 'number',
        description: '可选参数',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const result = { message: `Hello ${params.param1}` }
      return result
    }
  })
  .addPrompt({
    name: 'example_prompt',
    description: '输入 /example_prompt 时触发的提示词',
    arguments: [
      {
        name: 'arg1',
        description: '参数说明',
        required: true,
        defaultValue: 'default'
      }
    ],
    generate: async (args?: Record<string, any>) => {
      return `
## 生成的提示词

用户传入参数: ${args?.arg1}

在这里写完整的 LLM 提示词...
      `.trim()
    }
  })
  .addResource({
    uri: 'trae://your-skill/data',
    name: '资源名称',
    description: '这个资源提供什么数据',
    get: async () => {
      return {
        timestamp: new Date().toISOString(),
        data: {}
      }
    }
  })
  .build()
