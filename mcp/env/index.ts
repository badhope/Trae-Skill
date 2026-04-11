import { createMCPServer } from '../../packages/core/mcp/builder'
import * as fs from 'fs'
import * as path from 'path'
import * as crypto from 'crypto'

export default createMCPServer({
  name: 'env',
  version: '1.0.0',
  description: '.env 文件管理、环境变量、密钥安全存储与校验工具',
  author: 'Trae Professional',
  icon: '🔐'
})
  .addTool({
    name: 'env_parse',
    description: '解析 .env 文件内容为键值对对象',
    parameters: {
      filePath: { type: 'string', description: '.env 文件路径', required: true },
      example: { type: 'boolean', description: '是否包含示例值', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const content = fs.readFileSync(params.filePath, 'utf8')
      const result: Record<string, { value: string; comment?: string }> = {}
      let lastComment = ''
      content.split('\n').forEach(line => {
        const trimmed = line.trim()
        if (trimmed.startsWith('#')) {
          lastComment = trimmed.slice(1).trim()
          return
        }
        if (!trimmed || !trimmed.includes('=')) return
        const [key, ...rest] = trimmed.split('=')
        const value = rest.join('=').replace(/^["']|["']$/g, '')
        result[key.trim()] = {
          value: params.example ? value : (value ? '***' : ''),
          comment: lastComment || undefined
        }
        lastComment = ''
      })
      return { success: true, variables: result, count: Object.keys(result).length }
    }
  })
  .addTool({
    name: 'env_add',
    description: '添加或更新环境变量到 .env 文件',
    parameters: {
      filePath: { type: 'string', description: '.env 文件路径', required: true },
      key: { type: 'string', description: '变量名', required: true },
      value: { type: 'string', description: '变量值', required: true },
      comment: { type: 'string', description: '注释说明', required: false }
    },
    execute: async (params: Record<string, any>) => {
      let content = fs.existsSync(params.filePath) ? fs.readFileSync(params.filePath, 'utf8') : ''
      const regex = new RegExp(`^${params.key}=.*$`, 'm')
      const newLine = params.comment ? `# ${params.comment}\n${params.key}=${params.value}` : `${params.key}=${params.value}`
      if (regex.test(content)) {
        content = content.replace(regex, newLine)
      } else {
        content = content.trim() + '\n' + newLine
      }
      fs.writeFileSync(params.filePath, content.trim() + '\n')
      return { success: true, key: params.key, message: '环境变量已更新' }
    }
  })
  .addTool({
    name: 'env_generate_secret',
    description: '生成安全的随机密钥字符串',
    parameters: {
      length: { type: 'number', description: '密钥长度，默认32', required: false },
      type: { type: 'string', description: '类型: hex, base64, url-safe, alphabet', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const len = params.length || 32
      const type = params.type || 'hex'
      let result = ''
      switch (type) {
        case 'base64':
          result = crypto.randomBytes(len).toString('base64').slice(0, len)
          break
        case 'url-safe':
          result = crypto.randomBytes(len).toString('base64url').slice(0, len)
          break
        case 'alphabet':
          const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789'
          const bytes = crypto.randomBytes(len)
          for (let i = 0; i < len; i++) {
            result += chars[bytes[i] % chars.length]
          }
          break
        default:
          result = crypto.randomBytes(Math.ceil(len / 2)).toString('hex').slice(0, len)
      }
      return { success: true, secret: result, length: result.length, strength: len >= 32 ? 'STRONG' : len >= 16 ? 'MEDIUM' : 'WEAK' }
    }
  })
  .addTool({
    name: 'env_example_generate',
    description: '根据 .env 生成 .env.example 模板文件',
    parameters: {
      sourcePath: { type: 'string', description: '源 .env 文件路径', required: true },
      targetPath: { type: 'string', description: '目标 .env.example 路径', required: false },
      keepEmpty: { type: 'boolean', description: '是否保留空值', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const content = fs.readFileSync(params.sourcePath, 'utf8')
      let example = content
        .replace(/^(.+?=).+$/gm, (_, key) => params.keepEmpty ? key : key + 'your_value_here')
        .replace(/^(.+?=)["'].+["']$/gm, (_, key) => params.keepEmpty ? key : key + '"value"')
      const targetPath = params.targetPath || params.sourcePath.replace(/\.env.*$/, '.env.example')
      fs.writeFileSync(targetPath, example)
      return { success: true, targetPath, message: '.env.example 已生成' }
    }
  })
  .addTool({
    name: 'env_diff',
    description: '对比两个 env 文件的变量差异',
    parameters: {
      file1: { type: 'string', description: '第一个文件路径', required: true },
      file2: { type: 'string', description: '第二个文件路径', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const parse = (f: string) => {
        const r: Record<string, string> = {}
        fs.readFileSync(f, 'utf8').split('\n').forEach(line => {
          if (line.trim() && !line.trim().startsWith('#') && line.includes('=')) {
            const [k, ...v] = line.split('=')
            r[k.trim()] = v.join('=')
          }
        })
        return r
      }
      const env1 = parse(params.file1)
      const env2 = parse(params.file2)
      const onlyIn1 = Object.keys(env1).filter(k => !(k in env2))
      const onlyIn2 = Object.keys(env2).filter(k => !(k in env1))
      const different = Object.keys(env1).filter(k => k in env2 && env1[k] !== env2[k])
      return { success: true, onlyInFirst: onlyIn1, onlyInSecond: onlyIn2, valueDifferent: different }
    }
  })
  .build()
