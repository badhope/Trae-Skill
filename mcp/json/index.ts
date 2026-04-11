import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'json',
  version: '1.0.0',
  description: 'JSON格式化、校验、转换、路径查询、对比工具集',
  author: 'Trae Professional',
  icon: '📋'
})
  .addTool({
    name: 'json_format',
    description: '格式化JSON字符串，支持缩进配置',
    parameters: {
      input: { type: 'string', description: 'JSON字符串或对象', required: true },
      indent: { type: 'number', description: '缩进空格数，默认2', required: false },
      sortKeys: { type: 'boolean', description: '是否按键名排序', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const obj = typeof params.input === 'string' ? JSON.parse(params.input) : params.input
      if (params.sortKeys) {
        const sorted: Record<string, any> = {}
        Object.keys(obj).sort().forEach(k => sorted[k] = obj[k])
        return { success: true, formatted: JSON.stringify(sorted, null, params.indent || 2) }
      }
      return { success: true, formatted: JSON.stringify(obj, null, params.indent || 2) }
    }
  })
  .addTool({
    name: 'json_minify',
    description: '压缩JSON，去除所有空格',
    parameters: {
      input: { type: 'string', description: 'JSON字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const obj = JSON.parse(params.input)
      return { success: true, minified: JSON.stringify(obj), originalSize: params.input.length, minifiedSize: JSON.stringify(obj).length, ratio: Math.round((1 - JSON.stringify(obj).length / params.input.length) * 100) }
    }
  })
  .addTool({
    name: 'json_validate',
    description: '验证JSON是否合法，返回详细错误',
    parameters: {
      input: { type: 'string', description: 'JSON字符串', required: true },
      schema: { type: 'string', description: 'JSON Schema字符串', required: false }
    },
    execute: async (params: Record<string, any>) => {
      try {
        const obj = JSON.parse(params.input)
        return { success: true, valid: true, message: 'JSON格式合法', type: Array.isArray(obj) ? 'array' : typeof obj, keys: typeof obj === 'object' && !Array.isArray(obj) ? Object.keys(obj) : [] }
      } catch (e: any) {
        return { success: true, valid: false, error: e.message, position: e.at || 'unknown' }
      }
    }
  })
  .addTool({
    name: 'json_query',
    description: '使用JSON Path查询对象值',
    parameters: {
      input: { type: 'string', description: 'JSON字符串或对象', required: true },
      path: { type: 'string', description: '查询路径，如 user.address.city', required: true },
      defaultValue: { type: 'string', description: '默认值', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const obj = typeof params.input === 'string' ? JSON.parse(params.input) : params.input
      const value = params.path.split('.').reduce((o: any, k: string) => o?.[k], obj)
      return { success: true, path: params.path, value: value ?? params.defaultValue, exists: value !== undefined && value !== null }
    }
  })
  .addTool({
    name: 'json_to_csv',
    description: 'JSON数组转换为CSV格式',
    parameters: {
      input: { type: 'string', description: 'JSON数组字符串', required: true },
      delimiter: { type: 'string', description: '分隔符，默认逗号', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const arr = JSON.parse(params.input)
      if (!Array.isArray(arr) || arr.length === 0) return { success: false, error: '需要非空数组' }
      const del = params.delimiter || ','
      const keys = Object.keys(arr[0])
      const header = keys.join(del)
      const rows = arr.map((item: any) => keys.map(k => `"${String(item[k] ?? '').replace(/"/g, '""')}"`).join(del))
      return { success: true, csv: [header, ...rows].join('\n'), rows: arr.length, columns: keys.length }
    }
  })
  .addTool({
    name: 'json_diff',
    description: '对比两个JSON对象的差异',
    parameters: {
      old: { type: 'string', description: '旧JSON字符串', required: true },
      new: { type: 'string', description: '新JSON字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const oldObj = JSON.parse(params.old)
      const newObj = JSON.parse(params.new)
      const added: string[] = []
      const removed: string[] = []
      const changed: string[] = []
      const allKeys = new Set([...Object.keys(oldObj), ...Object.keys(newObj)])
      for (const key of allKeys) {
        if (!(key in oldObj)) added.push(key)
        else if (!(key in newObj)) removed.push(key)
        else if (JSON.stringify(oldObj[key]) !== JSON.stringify(newObj[key])) changed.push(key)
      }
      return { success: true, added, removed, changed, identical: added.length + removed.length + changed.length === 0 }
    }
  })
  .build()
