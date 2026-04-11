import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

export default createMCPServer({
  name: 'code-generator',
  version: '1.0.0',
  description: 'Intelligent code generation - CRUD APIs, components, template scaffolding',
  author: 'Trae Official',
  icon: '⚡'
})  .forTrae({
    categories: ['Code Generation'],
    rating: 'intermediate',
    features: ['CRUD, Components, Templates']
  })
  .addTool({
    name: 'detect_project_type',
    description: 'Intelligent code generation - CRUD APIs, components, template scaffolding',
    parameters: {},
    execute: async () => {
      const pkg = JSON.parse(await fs.readFile('package.json', 'utf-8').catch(() => '{}'))
      const deps = { ...pkg.dependencies, ...pkg.devDependencies }
      return {
        framework: deps.react ? 'react' : deps.vue ? 'vue' : deps.next ? 'nextjs' : 'unknown',
        language: deps.typescript ? 'typescript' : 'javascript',
        styling: deps.tailwindcss ? 'tailwind' : deps['@mui/material'] ? 'mui' : 'css'
      }
    }
  })  .forTrae({
    categories: ['Code Generation'],
    rating: 'intermediate',
    features: ['CRUD, Components, Templates']
  })
  .addTool({
    name: 'generate_crud_api',
    description: 'Intelligent code generation - CRUD APIs, components, template scaffolding',
    parameters: {
      model: { type: 'string', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: true },
      fields: { type: 'string', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: true },
      framework: { type: 'string', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: false }
    },
    execute: async (params: Record<string, any>) => ({
      model: params.model,
      fields: params.fields.split(','),
      framework: params.framework || 'express'
    })
  })  .forTrae({
    categories: ['Code Generation'],
    rating: 'intermediate',
    features: ['CRUD, Components, Templates']
  })
  .addTool({
    name: 'generate_component',
    description: 'Intelligent code generation - CRUD APIs, components, template scaffolding',
    parameters: {
      name: { type: 'string', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: true },
      props: { type: 'string', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: false },
      type: { type: 'string', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', enum: ['button', 'form', 'table', 'card', 'modal'], required: false }
    },
    execute: async (params: Record<string, any>) => ({
      componentName: params.name,
      props: params.props?.split(',') || [],
      type: params.type || 'card',
      config: await fs.readFile('package.json', 'utf-8').then(JSON.parse).catch(() => ({}))
    })
  })
  .addPrompt({
    name: 'gen-component',
    description: 'Intelligent code generation - CRUD APIs, components, template scaffolding',
    arguments: [
      { name: 'name', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: true },
      { name: 'type', description: 'Intelligent code generation - CRUD APIs, components, template scaffolding', required: false }
    ],
    generate: async (args?: Record<string, any>) => `
## ⚡ 组件生成: ${args?.name}

### 步骤
1. 调用 \`detect_project_type\` 确认技术栈
2. 调用 \`generate_component\` 获取配置
3. 生成完整代码:
   - TypeScript 类型定义
   - 组件 Props 接口
   - 组件实现
   - 默认导出
4. 遵守项目代码风格
    `.trim()
  })
  .build()
