import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

async function safeExec(cmd: string): Promise<string> {
  try {
    const { stdout } = await execAsync(cmd, { timeout: 15000 })
    return stdout.trim()
  } catch (e: any) { return e.stdout || e.message }
}

export default createMCPServer({
  name: 'dependency-analyzer',
  version: '1.0.0',
  description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
  author: 'Trae Official',
  icon: '📦'
})  .forTrae({
    categories: ['Dependencies, Security'],
    rating: 'intermediate',
    features: ['Audit, Version Check, Unused']
  })
  .addTool({
    name: 'list_dependencies',
    description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
    parameters: {},
    execute: async () => {
      const pkg = JSON.parse(await fs.readFile('package.json', 'utf-8').catch(() => '{}'))
      return {
        dependencies: pkg.dependencies || {},
        devDependencies: pkg.devDependencies || {},
        count: Object.keys(pkg.dependencies || {}).length
      }
    }
  })  .forTrae({
    categories: ['Dependencies, Security'],
    rating: 'intermediate',
    features: ['Audit, Version Check, Unused']
  })
  .addTool({
    name: 'find_unused_dependencies',
    description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
    parameters: {},
    execute: async () => ({
      depcheck: await safeExec('npx depcheck --json 2>/dev/null || echo "{}"').then(JSON.parse).catch(() => ({})),
      unused: []
    })
  })  .forTrae({
    categories: ['Dependencies, Security'],
    rating: 'intermediate',
    features: ['Audit, Version Check, Unused']
  })
  .addTool({
    name: 'check_outdated',
    description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
    parameters: {},
    execute: async () => ({
      outdated: await safeExec('npm outdated --json 2>/dev/null').then(JSON.parse).catch(() => ({}))
    })
  })  .forTrae({
    categories: ['Dependencies, Security'],
    rating: 'intermediate',
    features: ['Audit, Version Check, Unused']
  })
  .addTool({
    name: 'audit_security',
    description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
    parameters: {},
    execute: async () => ({
      audit: await safeExec('npm audit --json 2>/dev/null').then(JSON.parse).catch(() => ({}))
    })
  })
  .addPrompt({
    name: 'clean-deps',
    description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
    generate: async () => `
## 📦 依赖清理任务

### 步骤
1. 调用 \`list_dependencies\` 查看当前依赖
2. 调用 \`find_unused_dependencies\` 发现未使用的包
3. 调用 \`check_outdated\` 发现可升级的包
4. 调用 \`audit_security\` 安全审计
5. 生成清理建议报告

### 输出格式
| 包名 | 当前版本 | 最新版本 | 动作 | 理由 |
|------|---------|---------|------|------|
| pkg-a | 1.0.0   | 2.0.0   | 升级 | 安全修复 |
| pkg-b | 3.0.0   | 3.0.0   | 删除 | 未使用 |
    `.trim()
  })
  .addResource({
    uri: 'trae://dependencies/health',
    name: '依赖健康度报告',
    description: 'Dependency analysis - unused package detection, version conflict resolution, security auditing',
    get: async () => ({
      timestamp: new Date().toISOString(),
      total: Object.keys(JSON.parse(await fs.readFile('package.json', 'utf-8').catch(() => '{}')).dependencies || {}).length
    })
  })
  .build()
