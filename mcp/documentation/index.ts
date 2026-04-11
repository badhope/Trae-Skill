import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

export default createMCPServer({
  name: 'documentation',
  version: '1.0.0',
  description: 'Automated documentation generation - JSDoc, README, API documentation',
  author: 'Trae Official',
  icon: '📚'
})  .forTrae({
    categories: ['Documentation'],
    rating: 'beginner',
    features: ['JSDoc, README, API Docs']
  })
  .addTool({
    name: 'extract_public_apis',
    description: 'Automated documentation generation - JSDoc, README, API documentation',
    parameters: {
      files: {
        type: 'string',
        description: 'Automated documentation generation - JSDoc, README, API documentation',
        required: true
      }
    },
    execute: async (params: Record<string, any>) => {
      const fileList = params.files.split(',')
      const results: Record<string, any> = {}
      
      for (const file of fileList) {
        const content = await fs.readFile(file.trim(), 'utf-8').catch(() => '')
        results[file] = { content, size: content.length }
      }
      
      return { files: results }
    }
  })  .forTrae({
    categories: ['Documentation'],
    rating: 'beginner',
    features: ['JSDoc, README, API Docs']
  })
  .addTool({
    name: 'generate_jsdoc',
    description: 'Automated documentation generation - JSDoc, README, API documentation',
    parameters: {
      target: {
        type: 'string',
        description: 'Automated documentation generation - JSDoc, README, API documentation',
        required: true
      }
    },
    execute: async (params: Record<string, any>) => {
      const content = await fs.readFile(params.target, 'utf-8').catch(() => '')
      return { file: params.target, content }
    }
  })  .forTrae({
    categories: ['Documentation'],
    rating: 'beginner',
    features: ['JSDoc, README, API Docs']
  })
  .addTool({
    name: 'generate_readme',
    description: 'Automated documentation generation - JSDoc, README, API documentation',
    parameters: {
      type: {
        type: 'string',
        description: 'Automated documentation generation - JSDoc, README, API documentation',
        enum: ['library', 'cli', 'api', 'app'],
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const pkg = await fs.readFile('package.json', 'utf-8').catch(() => '{}')
      return {
        pkg: JSON.parse(pkg),
        projectType: params.type || 'library'
      }
    }
  })
  .addPrompt({
    name: 'document-file',
    description: 'Automated documentation generation - JSDoc, README, API documentation',
    arguments: [
      { name: 'file', description: 'Automated documentation generation - JSDoc, README, API documentation', required: true }
    ],
    generate: async (args?: Record<string, any>) => {
      return `
## 📚 文档生成任务

### 为 \`${args?.file}\` 添加完整文档

### 步骤
1. 调用 \`extract_public_apis\` 分析代码
2. 为每个导出的函数/类添加 JSDoc:
   - @description 功能说明
   - @param 参数说明
   - @returns 返回值说明
   - @example 使用示例
   - @throws 异常说明

### 要求
- 注释要具体有用，不要废话
- 必须包含至少一个真实的代码示例
- 复杂算法要说明思路
      `.trim()
    }
  })
  .addPrompt({
    name: 'write-readme',
    description: 'Automated documentation generation - JSDoc, README, API documentation',
    generate: async () => {
      return `
## 📖 生成项目 README

### 标准结构
1. 项目名称与一句话简介
2. ✨ 核心特性 (3-5 点)
3. 🚀 快速开始: 安装 + 最基本的使用示例
4. 📚 API 文档: 主要函数说明
5. 🤝 贡献指南
6. 📄 License

### 步骤
1. 调用 \`generate_readme\` 获取项目信息
2. 查看项目结构理解用途
3. 写出专业的市场级别的 README
      `.trim()
    }
  })
  .build()
