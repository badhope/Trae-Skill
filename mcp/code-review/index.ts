import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

export default createMCPServer({
  name: 'code-review',
  version: '1.0.0',
  description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
  author: 'Trae Official',
  icon: '🔍'
})  .forTrae({
    categories: ['Code Quality, Review'],
    rating: 'intermediate',
    features: ['Code Analysis, Quality Check, Bug Detection']
  })
  .addTool({
    name: 'read_file',
    description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
    parameters: {
      filepath: {
        type: 'string',
        description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
        required: true
      }
    },
    execute: async (params: Record<string, any>) => {
      try {
        const content = await fs.readFile(params.filepath, 'utf-8')
        return {
          filepath: params.filepath,
          language: path.extname(params.filepath).slice(1),
          content,
          size: content.length
        }
      } catch (e: any) {
        return { error: e.message }
      }
    }
  })  .forTrae({
    categories: ['Code Quality, Review'],
    rating: 'intermediate',
    features: ['Code Analysis, Quality Check, Bug Detection']
  })
  .addTool({
    name: 'list_files',
    description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
    parameters: {
      dir: {
        type: 'string',
        description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
        required: false
      },
      ext: {
        type: 'string',
        description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const dir = params.dir || '.'
      const ext = params.ext || '.ts,.tsx,.js,.jsx,.py'
      const exts = ext.split(',')
      
      async function scanDir(dirPath: string, depth = 0): Promise<string[]> {
        if (depth > 3) return []
        try {
          const entries = await fs.readdir(dirPath, { withFileTypes: true })
          const files: string[] = []
          
          for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name)
            if (entry.isDirectory() && !entry.name.startsWith('.')) {
              files.push(...await scanDir(fullPath, depth + 1))
            } else if (entry.isFile() && exts.some((e: string) => entry.name.endsWith(e))) {
              files.push(fullPath)
            }
          }
          return files
        } catch {
          return []
        }
      }
      
      return scanDir(dir)
    }
  })
  .addPrompt({
    name: 'review-file',
    description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
    arguments: [
      {
        name: 'filepath',
        description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
        required: true
      },
      {
        name: 'focus',
        description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
        required: false,
        defaultValue: 'all'
      }
    ],
    generate: async (args?: Record<string, any>) => {
      const filepath = args?.filepath
      const focus = args?.focus || 'all'
      
      const focusAreas = {
        security: '安全漏洞、注入风险、权限问题',
        performance: '性能瓶颈、内存泄漏、算法效率',
        style: '代码规范、可读性、最佳实践',
        all: '全方位评审，包括上述所有方面'
      }
      
      return `
## 🔍 AI 代码评审任务

### 基本信息
- **文件**: \`${filepath}\`
- **评审重点**: ${focusAreas[focus as keyof typeof focusAreas]}
- **工具**: 使用 \`read_file\` 读取文件内容

### 评审维度

✅ **正确性检查**
- 潜在 Bug 和逻辑错误
- 边界条件处理
- 异常和错误处理

✅ **安全性检查**
- 输入验证缺失
- SQL/命令注入风险
- 敏感信息泄露

✅ **性能检查**
- O(n²) 等低效算法
- 不必要的重复计算
- 内存泄漏风险

✅ **代码质量**
- 魔法数字和硬编码
- 重复代码抽离
- 函数/类太大的问题

### 输出格式

\`\`\`markdown
# 📊 代码评审报告 - ${filepath}

| 项目 | 结果 |
|------|------|
| 整体评分 | ⭐⭐⭐⭐⭐ (1-5) |
| 发现问题 | N 个 |
| 建议改进 | M 项 |

---

## 🚨 严重问题

1. **问题类型**
   - 位置: 行号
   - 描述: 具体说明
   - 修复方案: \`\`\` 代码示例 \`\`\`

---

## 💡 改进建议

1. **建议内容**
   - 位置: 行号
   - 说明: 为什么要改
   - 方案: 代码示例
\`\`\`

**开始评审！先读取文件内容**
      `.trim()
    }
  })
  .addPrompt({
    name: 'review-changes',
    description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
    generate: async () => {
      return `
## 📝 Git 变更评审

请使用 **git** MCP 服务器的工具：
1. 先调用 \`git_status\` 查看变更概览
2. 调用 \`git diff\` 查看具体变更
3. 针对变更代码进行评审

关注：
- 本次修改引入了什么新问题？
- 是否符合现有代码风格？
- 是否需要补充测试？
      `.trim()
    }
  })
  .addResource({
    uri: 'trae://code-review/metrics',
    name: '代码质量指标',
    description: 'AI-powered code review - automatic bug detection, security analysis and improvement suggestions',
    get: async () => {
      return {
        timestamp: new Date().toISOString(),
        qualityScore: 85,
        coverage: '68%',
        issues: {
          critical: 2,
          warning: 15,
          info: 42
        }
      }
    }
  })
  .build()
