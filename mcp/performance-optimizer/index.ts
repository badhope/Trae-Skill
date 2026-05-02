import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)
async function safeExec(cmd: string): Promise<string> {
  try { const { stdout } = await execAsync(cmd, { timeout: 30000 }); return stdout.trim() }
  catch (e: any) { return e.stdout || e.message }
}

export default createMCPServer({
  name: 'performance-optimizer',
  version: '1.0.0',
  description: 'Performance optimization - build speed, bundle analysis, dead code elimination',
  author: 'MCP Expert Community',
  icon: '⚡'
})
  .addTool({
    name: 'analyze_bundle',
    description: 'Performance optimization - build speed, bundle analysis, dead code elimination',
    parameters: {},
    execute: async () => ({
      hasAnalyzer: await fs.access('node_modules/webpack-bundle-analyzer').then(() => true).catch(() => false),
      distSize: await safeExec('du -sh dist 2>/dev/null || echo "N/A"')
    })
  })
  .addTool({
    name: 'find_large_files',
    description: 'Performance optimization - build speed, bundle analysis, dead code elimination',
    parameters: {
      thresholdKB: { type: 'number', description: 'Performance optimization - build speed, bundle analysis, dead code elimination', required: false }
    },
    execute: async (params: Record<string, any>) => ({
      largeFiles: await safeExec(`find . -type f -size +${params.thresholdKB || 50}k -name "*.js" -o -name "*.ts" | head -20`)
    })
  })
  .addTool({
    name: 'check_unused_code',
    description: 'Performance optimization - build speed, bundle analysis, dead code elimination',
    parameters: {},
    execute: async () => ({
      unusedExports: await safeExec('npx ts-prune 2>/dev/null | head -30 || echo "N/A"')
    })
  })
  .addPrompt({
    name: 'optimize-app',
    description: 'Performance optimization - build speed, bundle analysis, dead code elimination',
    generate: async () => `
## ⚡ 性能优化任务

### 优化维度
| 层面 | 检查项 |
|------|--------|
| 📦 构建体积 | Tree Shaking、Code Splitting、按需加载 |
| ⚙️  构建速度 | 缓存、并行、增量构建 |
| 🖥️  运行时 | 重渲染、内存泄漏、防抖节流 |

### 执行步骤
1. 调用 \`analyze_bundle\` 体积分析
2. 调用 \`find_large_files\` 大文件检测
3. 调用 \`check_unused_code\` 死代码清理
4. 生成优化建议报告
    `.trim()
  })
  .build()
