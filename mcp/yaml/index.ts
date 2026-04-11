import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'yaml',
  version: '1.0.0',
  description: 'YAML格式化、校验、JSON转换、Schema验证工具',
  author: 'Trae Professional',
  icon: '📝'
})
  .addTool({
    name: 'yaml_parse',
    description: '解析YAML字符串为JS对象',
    parameters: {
      input: { type: 'string', description: 'YAML字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const lines = params.input.split('\n')
      const result: any = {}
      const stack: { indent: number; obj: any }[] = [{ indent: -1, obj: result }]
      for (const line of lines) {
        if (!line.trim() || line.trim().startsWith('#')) continue
        const indent = line.search(/\S/)
        const content = line.trim()
        while (stack.length > 1 && stack[stack.length - 1].indent >= indent) stack.pop()
        const parent = stack[stack.length - 1].obj
        if (content.startsWith('- ')) {
          const lastKey = Object.keys(parent).pop()
          if (lastKey) {
            if (!Array.isArray(parent[lastKey])) parent[lastKey] = []
            parent[lastKey].push(content.slice(2).trim())
          }
        } else if (content.includes(':')) {
          const [key, ...valueParts] = content.split(':')
          const value = valueParts.join(':').trim()
          if (value) {
            parent[key.trim()] = value
          } else {
            parent[key.trim()] = {}
            stack.push({ indent, obj: parent[key.trim()] })
          }
        }
      }
      return { success: true, data: result }
    }
  })
  .addTool({
    name: 'yaml_stringify',
    description: 'JS对象转换为YAML字符串',
    parameters: {
      input: { type: 'string', description: 'JSON字符串或对象', required: true },
      indent: { type: 'number', description: '缩进空格数，默认2', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const obj = typeof params.input === 'string' ? JSON.parse(params.input) : params.input
      const toYaml = (o: any, level: number): string => {
        const spaces = '  '.repeat(level)
        let result = ''
        for (const [k, v] of Object.entries(o)) {
          if (Array.isArray(v)) {
            result += `${spaces}${k}:\n`
            v.forEach(item => result += `${spaces}  - ${item}\n`)
          } else if (typeof v === 'object' && v !== null) {
            result += `${spaces}${k}:\n${toYaml(v, level + 1)}`
          } else {
            result += `${spaces}${k}: ${v}\n`
          }
        }
        return result
      }
      return { success: true, yaml: toYaml(obj, 0).trim() }
    }
  })
  .addTool({
    name: 'json_to_yaml',
    description: 'JSON转换为YAML格式',
    parameters: {
      input: { type: 'string', description: 'JSON字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const obj = JSON.parse(params.input)
      const toYaml = (o: any, level: number): string => {
        const spaces = '  '.repeat(level)
        let result = ''
        for (const [k, v] of Object.entries(o)) {
          if (Array.isArray(v)) {
            result += `${spaces}${k}:\n`
            v.forEach(item => result += `${spaces}  - ${item}\n`)
          } else if (typeof v === 'object' && v !== null) {
            result += `${spaces}${k}:\n${toYaml(v, level + 1)}`
          } else {
            result += `${spaces}${k}: ${v}\n`
          }
        }
        return result
      }
      return { success: true, yaml: toYaml(obj, 0).trim() }
    }
  })
  .addTool({
    name: 'yaml_to_json',
    description: 'YAML转换为JSON格式',
    parameters: {
      input: { type: 'string', description: 'YAML字符串', required: true },
      pretty: { type: 'boolean', description: '是否格式化输出', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const lines = params.input.split('\n')
      const result: any = {}
      const stack: { indent: number; obj: any }[] = [{ indent: -1, obj: result }]
      for (const line of lines) {
        if (!line.trim() || line.trim().startsWith('#')) continue
        const indent = line.search(/\S/)
        const content = line.trim()
        while (stack.length > 1 && stack[stack.length - 1].indent >= indent) stack.pop()
        const parent = stack[stack.length - 1].obj
        if (content.startsWith('- ')) {
          const lastKey = Object.keys(parent).pop()
          if (lastKey) {
            if (!Array.isArray(parent[lastKey])) parent[lastKey] = []
            parent[lastKey].push(content.slice(2).trim())
          }
        } else if (content.includes(':')) {
          const [key, ...valueParts] = content.split(':')
          const value = valueParts.join(':').trim()
          if (value) {
            parent[key.trim()] = value
          } else {
            parent[key.trim()] = {}
            stack.push({ indent, obj: parent[key.trim()] })
          }
        }
      }
      return { success: true, json: params.pretty ? JSON.stringify(result, null, 2) : JSON.stringify(result) }
    }
  })
  .build()
