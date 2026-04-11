import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'datetime',
  version: '1.0.0',
  description: '时间转换、时区处理、格式化、日历计算',
  author: 'Trae Professional',
  icon: '🕐'
})
  .addTool({
    name: 'dt_now',
    description: '获取当前时间，支持时区和格式化',
    parameters: {
      timezone: { type: 'string', description: '时区，如 Asia/Shanghai', required: false },
      format: { type: 'string', description: '输出格式: iso, timestamp, friendly, unix', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const now = new Date()
      const format = params.format || 'iso'
      const result: Record<string, any> = {
        iso: now.toISOString(),
        timestamp: now.getTime(),
        unix: Math.floor(now.getTime() / 1000),
        friendly: now.toLocaleString('zh-CN', { timeZone: params.timezone || 'Asia/Shanghai' })
      }
      return { success: true, now: result[format], timezone: params.timezone || 'UTC' }
    }
  })
  .addTool({
    name: 'dt_format',
    description: '时间戳/字符串格式化',
    parameters: {
      timestamp: { type: 'number', description: '时间戳ms', required: false },
      dateString: { type: 'string', description: '日期字符串', required: false },
      pattern: { type: 'string', description: '格式: YYYY-MM-DD HH:mm:ss', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const date = params.timestamp ? new Date(params.timestamp) : new Date(params.dateString || Date.now())
      const pad = (n: number) => String(n).padStart(2, '0')
      const pattern = params.pattern || 'YYYY-MM-DD HH:mm:ss'
      const formatted = pattern
        .replace('YYYY', String(date.getFullYear()))
        .replace('MM', pad(date.getMonth() + 1))
        .replace('DD', pad(date.getDate()))
        .replace('HH', pad(date.getHours()))
        .replace('mm', pad(date.getMinutes()))
        .replace('ss', pad(date.getSeconds()))
      return { success: true, formatted, timestamp: date.getTime() }
    }
  })
  .addTool({
    name: 'dt_diff',
    description: '计算两个日期的时间差',
    parameters: {
      start: { type: 'string', description: '开始日期/时间戳', required: true },
      end: { type: 'string', description: '结束日期/时间戳', required: true },
      unit: { type: 'string', description: '单位: days, hours, minutes, seconds', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const start = new Date(params.start).getTime()
      const end = new Date(params.end).getTime()
      const diff = Math.abs(end - start)
      const unit = params.unit || 'days'
      const units: Record<string, number> = {
        days: 86400000,
        hours: 3600000,
        minutes: 60000,
        seconds: 1000
      }
      return {
        success: true,
        diff: Math.round(diff / units[unit]),
        unit,
        humanReadable: `${Math.round(diff / units[unit])} ${unit}`
      }
    }
  })
  .addTool({
    name: 'dt_calendar',
    description: '生成指定月份的日历',
    parameters: {
      year: { type: 'number', description: '年份', required: false },
      month: { type: 'number', description: '月份 1-12', required: false },
      weekStart: { type: 'number', description: '每周起始日 0=日 1=一', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const now = new Date()
      const y = params.year || now.getFullYear()
      const m = params.month || now.getMonth() + 1
      const firstDay = new Date(y, m - 1, 1)
      const lastDay = new Date(y, m, 0)
      const days = lastDay.getDate()
      const startWeekday = firstDay.getDay()
      const calendar: (number | null)[] = Array(startWeekday).fill(null)
      for (let i = 1; i <= days; i++) calendar.push(i)
      const weeks: (number | null)[][] = []
      for (let i = 0; i < calendar.length; i += 7) weeks.push(calendar.slice(i, i + 7))
      return { success: true, year: y, month: m, weeks, today: now.getDate() }
    }
  })
  .addTool({
    name: 'dt_relative',
    description: '生成相对时间描述（如"3分钟前"）',
    parameters: {
      timestamp: { type: 'number', description: '时间戳ms', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const now = Date.now()
      const diff = now - params.timestamp
      const ranges = [
        { limit: 60000, unit: 1000, name: '秒' },
        { limit: 3600000, unit: 60000, name: '分钟' },
        { limit: 86400000, unit: 3600000, name: '小时' },
        { limit: 2592000000, unit: 86400000, name: '天' }
      ]
      for (const r of ranges) {
        if (diff < r.limit) {
          const n = Math.round(diff / r.unit)
          return { success: true, relative: `${n}${r.name}前`, ago: true }
        }
      }
      return { success: true, relative: new Date(params.timestamp).toLocaleDateString() }
    }
  })
  .build()
