import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'markdown',
  version: '1.0.0',
  description: 'Markdown增强工具：表格、目录、TOC、格式转换、文档生成',
  author: 'Trae Professional',
  icon: '📄'
})
  .addTool({
    name: 'md_table',
    description: '生成Markdown表格，支持对齐和格式化',
    parameters: {
      headers: { type: 'array', description: '表头数组', required: true },
      rows: { type: 'array', description: '数据行二维数组', required: true },
      align: { type: 'string', description: '对齐方式: left, center, right', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const align = params.align || 'left'
      const sep: Record<string, string> = { left: ':---', center: ':---:', right: '---:' }
      const headerRow = `| ${params.headers.join(' | ')} |`
      const separatorRow = `| ${params.headers.map(() => sep[align]).join(' | ')} |`
      const dataRows = params.rows.map((row: any[]) => `| ${row.join(' | ')} |`)
      return { success: true, table: [headerRow, separatorRow, ...dataRows].join('\n') }
    }
  })
  .addTool({
    name: 'md_toc',
    description: '生成Markdown目录TOC，根据标题层级',
    parameters: {
      content: { type: 'string', description: 'Markdown内容', required: true },
      maxLevel: { type: 'number', description: '最大标题级别，默认3', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const maxLevel = params.maxLevel || 3
      const regex = /^(#{1,6})\s+(.+)$/gm
      const toc: string[] = []
      let match
      while ((match = regex.exec(params.content)) !== null) {
        const level = match[1].length
        if (level <= maxLevel) {
          const indent = '  '.repeat(level - 1)
          const text = match[2].trim()
          const link = text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')
          toc.push(`${indent}- [${text}](#${link})`)
        }
      }
      return { success: true, toc: toc.join('\n'), count: toc.length }
    }
  })
  .addTool({
    name: 'md_badge',
    description: '生成README徽章',
    parameters: {
      type: { type: 'string', description: '类型: version, license, stars, build, custom', required: true },
      text: { type: 'string', description: '徽章左侧文字', required: false },
      value: { type: 'string', description: '徽章右侧值', required: false },
      color: { type: 'string', description: '颜色: blue, green, red, yellow', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const badges: Record<string, string> = {
        version: 'https://img.shields.io/badge/version-1.0.0-blue',
        license: 'https://img.shields.io/badge/license-MIT-green',
        stars: 'https://img.shields.io/github/stars/user/repo',
        build: 'https://img.shields.io/badge/build-passing-brightgreen'
      }
      let url = badges[params.type as keyof typeof badges]
      if (params.type === 'custom' && params.text && params.value) {
        url = `https://img.shields.io/badge/${encodeURIComponent(params.text)}-${encodeURIComponent(params.value)}-${params.color || 'blue'}`
      }
      return { success: true, markdown: `![${params.type}](${url})`, url }
    }
  })
  .addTool({
    name: 'md_checklist',
    description: '生成Checklist任务列表',
    parameters: {
      items: { type: 'array', description: '任务项数组', required: true },
      checked: { type: 'array', description: '已完成的索引', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const checked = params.checked || []
      const list = params.items.map((item: string, i: number) =>
        `- [${checked.includes(i) ? 'x' : ' '}] ${item}`
      )
      return { success: true, checklist: list.join('\n'), completed: checked.length, total: params.items.length }
    }
  })
  .addTool({
    name: 'md_alert',
    description: '生成GitHub风格Alert提示框',
    parameters: {
      type: { type: 'string', description: '类型: note, tip, important, warning, caution', required: true },
      content: { type: 'string', description: '提示内容', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const alert = `> [!${params.type.toUpperCase()}]\n> ${params.content}`
      return { success: true, alert }
    }
  })
  .build()
