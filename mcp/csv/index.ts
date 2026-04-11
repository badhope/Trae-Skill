import { createMCPServer } from '../../packages/core/mcp/builder'

function parseCSV(input: string, delimiter: string = ','): any[] {
  const lines = input.trim().split('\n')
  if (lines.length < 2) return []
  const headers = parseCSVLine(lines[0], delimiter)
  const result: any[] = []
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i], delimiter)
    const row: Record<string, string> = {}
    headers.forEach((h, idx) => {
      row[h] = values[idx] || ''
    })
    result.push(row)
  }
  return result
}

function parseCSVLine(line: string, delimiter: string): string[] {
  const result: string[] = []
  let current = ''
  let inQuotes = false
  for (let i = 0; i < line.length; i++) {
    const char = line[i]
    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"'
        i++
      } else {
        inQuotes = !inQuotes
      }
    } else if (char === delimiter && !inQuotes) {
      result.push(current.trim())
      current = ''
    } else {
      current += char
    }
  }
  result.push(current.trim())
  return result
}

function toCSV(data: any[], delimiter: string = ','): string {
  if (data.length === 0) return ''
  const headers = Object.keys(data[0])
  const headerLine = headers.map(h => `"${h}"`).join(delimiter)
  const dataLines = data.map(row => {
    return headers.map(h => {
      const value = String(row[h] || '')
      if (value.includes(delimiter) || value.includes('"') || value.includes('\n')) {
        return `"${value.replace(/"/g, '""')}"`
      }
      return value
    }).join(delimiter)
  })
  return [headerLine, ...dataLines].join('\n')
}

export default createMCPServer({
  name: 'csv',
  version: '1.0.0',
  description: 'CSV处理工具集 - 解析、转换、格式化、合并、过滤',
  author: 'Trae Professional',
  icon: '📊'
})
  .addTool({
    name: 'csv_parse',
    description: '解析CSV字符串为JSON对象数组',
    parameters: {
      input: { type: 'string', description: 'CSV字符串', required: true },
      delimiter: { type: 'string', description: '分隔符，默认逗号', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const delimiter = params.delimiter || ','
      const data = parseCSV(params.input, delimiter)
      return { success: true, rowCount: data.length, headers: data.length > 0 ? Object.keys(data[0]) : [], data }
    }
  })
  .addTool({
    name: 'csv_stringify',
    description: 'JSON对象数组转换为CSV字符串',
    parameters: {
      input: { type: 'string', description: 'JSON数组字符串', required: true },
      delimiter: { type: 'string', description: '分隔符，默认逗号', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const data = JSON.parse(params.input)
      const delimiter = params.delimiter || ','
      const csv = toCSV(data, delimiter)
      return { success: true, rowCount: data.length, csv }
    }
  })
  .addTool({
    name: 'csv_to_markdown',
    description: 'CSV转换为Markdown表格',
    parameters: {
      input: { type: 'string', description: 'CSV字符串', required: true },
      delimiter: { type: 'string', description: '分隔符，默认逗号', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const delimiter = params.delimiter || ','
      const data = parseCSV(params.input, delimiter)
      if (data.length === 0) return { success: true, markdown: '' }
      const headers = Object.keys(data[0])
      const headerLine = `| ${headers.join(' | ')} |`
      const separatorLine = `| ${headers.map(() => '---').join(' | ')} |`
      const dataLines = data.map(row => `| ${headers.map(h => row[h] || '').join(' | ')} |`)
      return { success: true, rowCount: data.length, markdown: [headerLine, separatorLine, ...dataLines].join('\n') }
    }
  })
  .addTool({
    name: 'csv_filter',
    description: '按条件过滤CSV数据',
    parameters: {
      input: { type: 'string', description: 'CSV字符串', required: true },
      column: { type: 'string', description: '列名', required: true },
      value: { type: 'string', description: '匹配值', required: true },
      exact: { type: 'boolean', description: '精确匹配', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const data = parseCSV(params.input)
      const filtered = data.filter((row: any) => {
        const cellValue = String(row[params.column] || '').toLowerCase()
        const matchValue = String(params.value).toLowerCase()
        return params.exact ? cellValue === matchValue : cellValue.includes(matchValue)
      })
      return { success: true, originalCount: data.length, filteredCount: filtered.length, data: filtered }
    }
  })
  .addTool({
    name: 'csv_transpose',
    description: '转置CSV（行列互换）',
    parameters: {
      input: { type: 'string', description: 'CSV字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const data = parseCSV(params.input)
      if (data.length === 0) return { success: true, csv: '' }
      const headers = Object.keys(data[0])
      const transposed: any[] = headers.map(header => {
        const row: Record<string, string> = { field: header }
        data.forEach((r, idx) => {
          row[`row${idx + 1}`] = r[header] || ''
        })
        return row
      })
      return { success: true, csv: toCSV(transposed) }
    }
  })
  .addTool({
    name: 'csv_summary',
    description: '生成CSV数据摘要统计',
    parameters: {
      input: { type: 'string', description: 'CSV字符串', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const data = parseCSV(params.input)
      if (data.length === 0) return { success: true, summary: '空数据' }
      const headers = Object.keys(data[0])
      const summary: any = {
        rows: data.length,
        columns: headers.length,
        fields: headers,
        fieldStats: {}
      }
      headers.forEach(h => {
        const values = data.map((r: any) => r[h]).filter(Boolean)
        const uniqueValues = [...new Set(values)]
        const numericValues = values.map(Number).filter(n => !isNaN(n))
        summary.fieldStats[h] = {
          nonEmpty: values.length,
          unique: uniqueValues.length,
          sampleValues: uniqueValues.slice(0, 5),
          isNumeric: numericValues.length === values.length && values.length > 0,
          min: numericValues.length > 0 ? Math.min(...numericValues) : null,
          max: numericValues.length > 0 ? Math.max(...numericValues) : null,
          avg: numericValues.length > 0 ? numericValues.reduce((a, b) => a + b, 0) / numericValues.length : null
        }
      })
      return { success: true, summary }
    }
  })
  .build()
