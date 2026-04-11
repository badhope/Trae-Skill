import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'

export default createMCPServer({
  name: 'typescript',
  version: '1.0.0',
  description: 'TypeScript type mastery - advanced types, generics, type safety best practices',
  author: 'Trae Official',
  icon: '📘'
})  .forTrae({
    categories: ['TypeScript, Types'],
    rating: 'advanced',
    features: ['Type Safety, Generics, Best Practices']
  })
  .addTool({
    name: 'check_ts_config',
    description: 'TypeScript type mastery - advanced types, generics, type safety best practices',
    parameters: {},
    execute: async () => {
      const cfg = JSON.parse(await fs.readFile('tsconfig.json', 'utf-8').catch(() => '{}'))
      return {
        strict: cfg.compilerOptions?.strict || false,
        strictNullChecks: cfg.compilerOptions?.strictNullChecks || false,
        noImplicitAny: cfg.compilerOptions?.noImplicitAny || false
      }
    }
  })  .forTrae({
    categories: ['TypeScript, Types'],
    rating: 'advanced',
    features: ['Type Safety, Generics, Best Practices']
  })
  .addTool({
    name: 'extract_types',
    description: 'TypeScript type mastery - advanced types, generics, type safety best practices',
    parameters: {
      file: { type: 'string', description: 'TypeScript type mastery - advanced types, generics, type safety best practices', required: true }
    },
    execute: async (params: Record<string, any>) => ({
      file: params.file,
      content: await fs.readFile(params.file, 'utf-8').catch(() => '')
    })
  })  .forTrae({
    categories: ['TypeScript, Types'],
    rating: 'advanced',
    features: ['Type Safety, Generics, Best Practices']
  })
  .addTool({
    name: 'fix_any_types',
    description: 'TypeScript type mastery - advanced types, generics, type safety best practices',
    parameters: {
      file: { type: 'string', description: 'TypeScript type mastery - advanced types, generics, type safety best practices', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const content = await fs.readFile(params.file, 'utf-8').catch(() => '')
      const anyCount = (content.match(/: any\b/g) || []).length
      return { file: params.file, anyCount, content }
    }
  })
  .addPrompt({
    name: 'type-safe',
    description: 'TypeScript type mastery - advanced types, generics, type safety best practices',
    arguments: [{ name: 'file', description: 'TypeScript type mastery - advanced types, generics, type safety best practices', required: true }],
    generate: async (args?: Record<string, any>) => `
## 📘 TypeScript 类型安全改造

### 文件: ${args?.file}

### 改造优先级
1. 🔴 消除所有 any 类型
2. 🟠 添加正确的范型约束
3. 🟡 使用联合类型替代枚举
4. 🟢 充分利用类型推断

### 高级类型技巧
- 使用 keyof T 替代字符串字面量
- 使用 ReturnType/Parameters 获取函数类型
- 使用 Discriminated Unions 做类型守卫
- 使用 Template Literal Types 做字符串约束
    `.trim()
  })
  .build()
