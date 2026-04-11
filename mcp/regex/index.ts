import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'regex',
  version: '1.0.0',
  description: '正则表达式构建、测试、可视化、常用模式库',
  author: 'Trae Professional',
  icon: '🔍'
})
  .addTool({
    name: 'regex_test',
    description: '测试正则表达式匹配结果',
    parameters: {
      pattern: { type: 'string', description: '正则表达式', required: true },
      input: { type: 'string', description: '测试字符串', required: true },
      flags: { type: 'string', description: '标志: g, i, m, s, u, y', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const flags = params.flags || 'g'
      try {
        const regex = new RegExp(params.pattern, flags)
        const matches = [...params.input.matchAll(regex)]
        return {
          success: true,
          valid: true,
          matches: matches.map((m: any) => ({ match: m[0], index: m.index, groups: m.groups })),
          count: matches.length
        }
      } catch (e: any) {
        return { success: true, valid: false, error: e.message }
      }
    }
  })
  .addTool({
    name: 'regex_explain',
    description: '解释正则表达式各部分含义',
    parameters: {
      pattern: { type: 'string', description: '正则表达式', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const explanations: Record<string, string> = {
        '\\d': '匹配数字 [0-9]',
        '\\w': '匹配单词字符 [a-zA-Z0-9_]',
        '\\s': '匹配空白字符',
        '\\b': '单词边界',
        '.': '匹配任意字符(除换行)',
        '*': '匹配0次或多次',
        '+': '匹配1次或多次',
        '?': '匹配0次或1次',
        '{n}': '匹配n次',
        '{n,}': '匹配至少n次',
        '{n,m}': '匹配n到m次',
        '^': '字符串开头',
        '$': '字符串结尾',
        '[]': '字符集',
        '()': '捕获组',
        '(?:)': '非捕获组',
        '(?=)': '正向先行断言',
        '(?!': '负向先行断言'
      }
      const result: string[] = []
      for (const [token, desc] of Object.entries(explanations)) {
        if (params.pattern.includes(token.replace('\\', '\\\\'))) {
          result.push(`${token} → ${desc}`)
        }
      }
      return { success: true, pattern: params.pattern, explanations: result }
    }
  })
  .addTool({
    name: 'regex_library',
    description: '获取常用正则表达式模式',
    parameters: {
      category: { type: 'string', description: '类别: email, url, phone, idcard, ip, date, color', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const library: Record<string, { name: string; pattern: string; example: string }> = {
        email: { name: '邮箱', pattern: '^[\\w.-]+@[\\w.-]+\\.\\w+$', example: 'test@example.com' },
        url: { name: 'URL链接', pattern: 'https?://[\\w./?=#&-]+', example: 'https://github.com' },
        phone: { name: '手机号', pattern: '^1[3-9]\\d{9}$', example: '13800138000' },
        idcard: { name: '身份证', pattern: '^[1-9]\\d{5}(18|19|20)\\d{9}[\\dXx]$', example: '110101199003077758' },
        ip: { name: 'IP地址', pattern: '^(?:\\d{1,3}\\.){3}\\d{1,3}$', example: '192.168.1.1' },
        date: { name: '日期', pattern: '^\\d{4}-\\d{2}-\\d{2}$', example: '2024-01-15' },
        color: { name: 'HEX颜色', pattern: '^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', example: '#FFFFFF' },
        uuid: { name: 'UUID', pattern: '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', example: 'a1b2c3d4-...' }
      }
      if (params.category) {
        return { success: true, result: library[params.category] }
      }
      return { success: true, library: Object.keys(library), patterns: library }
    }
  })
  .addTool({
    name: 'regex_replace',
    description: '正则表达式替换',
    parameters: {
      input: { type: 'string', description: '输入字符串', required: true },
      pattern: { type: 'string', description: '正则表达式', required: true },
      replacement: { type: 'string', description: '替换字符串，支持$1分组', required: true },
      flags: { type: 'string', description: '标志', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const result = params.input.replace(new RegExp(params.pattern, params.flags || 'g'), params.replacement)
      return { success: true, original: params.input, result, changed: params.input !== result }
    }
  })
  .build()
