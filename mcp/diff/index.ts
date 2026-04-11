import { createMCPServer } from '../../packages/core/mcp/builder'

export default createMCPServer({
  name: 'diff',
  version: '1.0.0',
  description: '文件对比、差异高亮、合并建议、Patch生成工具',
  author: 'Trae Professional',
  icon: '📊'
})
  .addTool({
    name: 'diff_text',
    description: '对比两个文本的差异',
    parameters: {
      oldText: { type: 'string', description: '旧文本', required: true },
      newText: { type: 'string', description: '新文本', required: true },
      context: { type: 'number', description: '上下文行数', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const oldLines = params.oldText.split('\n')
      const newLines = params.newText.split('\n')
      const added: number[] = []
      const removed: number[] = []
      newLines.forEach((line: string, i: number) => {
        if (!oldLines.includes(line)) added.push(i)
      })
      oldLines.forEach((line: string, i: number) => {
        if (!newLines.includes(line)) removed.push(i)
      })
      const changes = Math.max(added.length, removed.length)
      return {
        success: true,
        added: { lines: added, count: added.length },
        removed: { lines: removed, count: removed.length },
        identical: changes === 0,
        changes
      }
    }
  })
  .addTool({
    name: 'diff_generate_patch',
    description: '生成Patch格式差异',
    parameters: {
      oldText: { type: 'string', description: '旧文本', required: true },
      newText: { type: 'string', description: '新文本', required: true },
      filename: { type: 'string', description: '文件名', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const oldLines = params.oldText.split('\n')
      const newLines = params.newText.split('\n')
      const patch: string[] = [`diff --git a/${params.filename || 'file'} b/${params.filename || 'file'}`]
      for (let i = 0; i < Math.max(oldLines.length, newLines.length); i++) {
        if (i >= oldLines.length) {
          patch.push(`+${newLines[i]}`)
        } else if (i >= newLines.length) {
          patch.push(`-${oldLines[i]}`)
        } else if (oldLines[i] !== newLines[i]) {
          patch.push(`-${oldLines[i]}`)
          patch.push(`+${newLines[i]}`)
        } else {
          patch.push(` ${oldLines[i]}`)
        }
      }
      return { success: true, patch: patch.join('\n'), lines: patch.length }
    }
  })
  .addTool({
    name: 'diff_stats',
    description: '差异统计信息',
    parameters: {
      oldText: { type: 'string', description: '旧文本', required: true },
      newText: { type: 'string', description: '新文本', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const oldLines = params.oldText.split('\n')
      const newLines = params.newText.split('\n')
      const oldSet = new Set(oldLines)
      const newSet = new Set(newLines)
      const added = [...newSet].filter(l => !oldSet.has(l)).length
      const removed = [...oldSet].filter(l => !newSet.has(l)).length
      const unchanged = [...oldSet].filter(l => newSet.has(l)).length
      return {
        success: true,
        added,
        removed,
        unchanged,
        totalOld: oldLines.length,
        totalNew: newLines.length,
        changeRate: Math.round(((added + removed) / Math.max(oldLines.length, 1)) * 100)
      }
    }
  })
  .addTool({
    name: 'diff_merge',
    description: '智能合并两个版本',
    parameters: {
      baseText: { type: 'string', description: '基础版本', required: true },
      yourText: { type: 'string', description: '你的修改', required: true },
      theirText: { type: 'string', description: '他们的修改', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const base = params.baseText.split('\n')
      const yours = params.yourText.split('\n')
      const theirs = params.theirText.split('\n')
      const conflicts: string[] = []
      const merged: string[] = []
      for (let i = 0; i < Math.max(base.length, yours.length, theirs.length); i++) {
        const b = base[i] ?? ''
        const y = yours[i] ?? ''
        const t = theirs[i] ?? ''
        if (y === t || y === b) merged.push(t)
        else if (t === b) merged.push(y)
        else {
          conflicts.push(`Line ${i + 1}`)
          merged.push('<<<<<<< YOURS', y, '=======', t, '>>>>>>> THEIRS')
        }
      }
      return { success: true, merged: merged.join('\n'), conflicts, hasConflicts: conflicts.length > 0 }
    }
  })
  .build()
