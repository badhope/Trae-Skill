import { createMCPServer } from '../../packages/core/mcp/builder'
import { validateParams, formatSuccess, formatError } from '../../packages/core/shared/utils'

export default createMCPServer({
  name: 'env',
  version: '2.0.0',
  description: 'Environment variables toolkit - .env parsing, validation, template generation',
  author: 'MCP Expert Community',
  icon: '🔧'
})
  .addTool({
    name: 'env_parse',
    description: 'Parse .env file content with type inference',
    parameters: {
      input: { type: 'string', description: '.env content', required: true },
      resolveVars: { type: 'boolean', description: 'Resolve variable references', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        input: { type: 'string', required: true },
        resolveVars: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const vars: Record<string, any> = {}
      const comments: string[] = []

      for (const line of validation.data.input.split('\n')) {
        const trimmed = line.trim()
        if (!trimmed || trimmed.startsWith('#')) {
          if (trimmed.startsWith('#')) comments.push(trimmed)
          continue
        }
        const eq = trimmed.indexOf('=')
        if (eq > 0) {
          const key = trimmed.slice(0, eq).trim()
          let value = trimmed.slice(eq + 1).trim().replace(/^["']|["']$/g, '')

          let typed: any = value
          if (value === 'true') typed = true
          else if (value === 'false') typed = false
          else if (!isNaN(Number(value)) && value !== '') typed = Number(value)

          vars[key] = typed
        }
      }

      return formatSuccess({
        variables: vars,
        count: Object.keys(vars).length,
        comments: comments.length,
        types: Object.fromEntries(
          Object.entries(vars).map(([k, v]) => [k, typeof v])
        )
      })
    }
  })
  .addTool({
    name: 'env_template',
    description: 'Generate .env.example template from existing .env',
    parameters: {
      input: { type: 'string', description: '.env content', required: true },
      maskSecrets: { type: 'boolean', description: 'Mask sensitive values', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        input: { type: 'string', required: true },
        maskSecrets: { type: 'boolean', required: false, default: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const lines = []
      for (const line of validation.data.input.split('\n')) {
        const trimmed = line.trim()
        if (!trimmed || trimmed.startsWith('#')) {
          lines.push(line)
          continue
        }
        const eq = trimmed.indexOf('=')
        if (eq > 0) {
          const key = trimmed.slice(0, eq).trim()
          lines.push(`${key}=`)
        }
      }

      return formatSuccess({ template: lines.join('\n') })
    }
  })
  .addTool({
    name: 'env_validate',
    description: 'Validate required environment variables against schema',
    parameters: {
      input: { type: 'string', description: '.env content', required: true },
      required: { type: 'string', description: 'Comma-separated required keys', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const validation = validateParams(params, {
        input: { type: 'string', required: true },
        required: { type: 'string', required: true }
      })
      if (!validation.valid) return formatError('Invalid parameters', validation.errors)

      const vars: Record<string, string> = {}
      for (const line of validation.data.input.split('\n')) {
        const eq = line.indexOf('=')
        if (eq > 0) vars[line.slice(0, eq).trim()] = line.slice(eq + 1).trim()
      }

      const requiredKeys = validation.data.required.split(',').map((k: string) => k.trim())
      const missing = requiredKeys.filter((k: string) => !vars[k] || vars[k] === '')

      return formatSuccess({
        valid: missing.length === 0,
        missing,
        found: Object.keys(vars).filter(k => vars[k] !== ''),
        score: Math.round(((requiredKeys.length - missing.length) / requiredKeys.length) * 100)
      })
    }
  })
  .build()
