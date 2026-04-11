import { createMCPServer } from '../../packages/core/mcp/builder'
import * as crypto from 'crypto'

export default createMCPServer({
  name: 'encoding',
  version: '1.0.0',
  description: 'Base64、URL、Unicode、MD5、SHA等编解码工具集',
  author: 'Trae Professional',
  icon: '🔐'
})
  .addTool({
    name: 'base64_encode',
    description: 'Base64编码字符串',
    parameters: {
      input: { type: 'string', description: '输入字符串', required: true },
      urlSafe: { type: 'boolean', description: 'URL安全编码', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const encoded = params.urlSafe
        ? Buffer.from(params.input).toString('base64url')
        : Buffer.from(params.input).toString('base64')
      return { success: true, encoded, decoded: params.input }
    }
  })
  .addTool({
    name: 'base64_decode',
    description: 'Base64解码字符串',
    parameters: {
      input: { type: 'string', description: 'Base64字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const decoded = Buffer.from(params.input, 'base64').toString('utf8')
      return { success: true, decoded, encoded: params.input }
    }
  })
  .addTool({
    name: 'url_encode',
    description: 'URL编码',
    parameters: {
      input: { type: 'string', description: '输入字符串', required: true },
      full: { type: 'boolean', description: '完全编码', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const encoded = params.full
        ? encodeURIComponent(params.input)
        : encodeURI(params.input)
      return { success: true, encoded, original: params.input }
    }
  })
  .addTool({
    name: 'url_decode',
    description: 'URL解码',
    parameters: {
      input: { type: 'string', description: '编码的URL字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const decoded = decodeURIComponent(params.input)
      return { success: true, decoded, encoded: params.input }
    }
  })
  .addTool({
    name: 'hash',
    description: '生成哈希值 (MD5, SHA1, SHA256, SHA512)',
    parameters: {
      input: { type: 'string', description: '输入字符串', required: true },
      algorithm: { type: 'string', description: 'md5, sha1, sha256, sha512', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const algo = params.algorithm || 'md5'
      const hash = crypto.createHash(algo).update(params.input).digest('hex')
      return { success: true, algorithm: algo, hash }
    }
  })
  .addTool({
    name: 'unicode_encode',
    description: 'Unicode转义编码',
    parameters: {
      input: { type: 'string', description: '输入字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const encoded = [...params.input]
        .map(c => c.charCodeAt(0).toString(16).padStart(4, '0'))
        .map(hex => `\\u${hex}`)
        .join('')
      return { success: true, encoded }
    }
  })
  .addTool({
    name: 'html_entity',
    description: 'HTML实体编码',
    parameters: {
      input: { type: 'string', description: '输入HTML字符串', required: true },
      decode: { type: 'boolean', description: '解码模式', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const entities: Record<string, string> = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
      }
      if (params.decode) {
        let result = params.input
        for (const [char, entity] of Object.entries(entities)) {
          result = result.split(entity).join(char)
        }
        return { success: true, decoded: result }
      }
      const encoded = params.input.replace(/[&<>"']/g, (m: string) => entities[m])
      return { success: true, encoded }
    }
  })
  .build()
