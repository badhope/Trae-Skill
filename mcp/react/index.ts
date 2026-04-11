import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'

export default createMCPServer({
  name: 'react',
  version: '1.0.0',
  description: 'React + TypeScript best practices - Hooks, components, memoization optimization',
  author: 'Trae Official',
  icon: '⚛️'
})  .forTrae({
    categories: ['Frontend, React'],
    rating: 'intermediate',
    features: ['Hooks, Components, Performance']
  })
  .addTool({
    name: 'detect_react_config',
    description: 'React + TypeScript best practices - Hooks, components, memoization optimization',
    parameters: {},
    execute: async () => {
      const pkg = JSON.parse(await fs.readFile('package.json', 'utf-8').catch(() => '{}'))
      const deps = { ...pkg.dependencies, ...pkg.devDependencies }
      return {
        framework: deps.next ? 'nextjs' : deps.vite ? 'vite' : 'cra',
        router: deps['react-router-dom'] ? 'react-router' : deps.next ? 'next-router' : 'none',
        state: deps.zustand ? 'zustand' : deps.redux ? 'redux' : deps.jotai ? 'jotai' : 'context',
        styling: deps.tailwindcss ? 'tailwind' : deps['@emotion/react'] ? 'emotion' : 'css',
        hasTypeScript: !!deps.typescript
      }
    }
  })  .forTrae({
    categories: ['Frontend, React'],
    rating: 'intermediate',
    features: ['Hooks, Components, Performance']
  })
  .addTool({
    name: 'generate_hook',
    description: 'React + TypeScript best practices - Hooks, components, memoization optimization',
    parameters: {
      name: { type: 'string', description: 'React + TypeScript best practices - Hooks, components, memoization optimization', required: true },
      purpose: { type: 'string', description: 'React + TypeScript best practices - Hooks, components, memoization optimization', required: false }
    },
    execute: async (params: Record<string, any>) => ({ name: `use${params.name.replace(/^use/, '')}` })
  })  .forTrae({
    categories: ['Frontend, React'],
    rating: 'intermediate',
    features: ['Hooks, Components, Performance']
  })
  .addTool({
    name: 'optimize_renders',
    description: 'React + TypeScript best practices - Hooks, components, memoization optimization',
    parameters: {
      component: { type: 'string', description: 'React + TypeScript best practices - Hooks, components, memoization optimization', required: true }
    },
    execute: async (params: Record<string, any>) => ({
      file: params.component,
      content: await fs.readFile(params.component, 'utf-8').catch(() => '')
    })
  })
  .addPrompt({
    name: 'react-component',
    description: 'React + TypeScript best practices - Hooks, components, memoization optimization',
    arguments: [
      { name: 'name', description: 'React + TypeScript best practices - Hooks, components, memoization optimization', required: true },
      { name: 'type', description: 'React + TypeScript best practices - Hooks, components, memoization optimization', required: false }
    ],
    generate: async (args?: Record<string, any>) => `
## ⚛️ React 组件生成: ${args?.name}

### 步骤
1. 调用 \`detect_react_config\` 确认项目配置
2. 使用 TypeScript + 函数组件
3. 遵循以下规范:
   - 显式的 interface Props 定义
   - 默认值使用 ES6 默认参数
   - 合理使用 useCallback/useMemo
   - 统一的错误边界处理

### 性能检查清单
- 🔘 没有不必要的重渲染
- 🔘 依赖数组正确完整
- 🔘 没有在渲染中创建对象
- 🔘 列表有正确的 key
    `.trim()
  })
  .build()
