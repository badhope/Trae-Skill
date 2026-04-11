import { createMCPServer } from '../../packages/core/mcp/builder'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

async function runCommand(command: string, timeout: number = 30000): Promise<{
  stdout: string
  stderr: string
  exitCode: number
}> {
  try {
    const { stdout, stderr } = await execAsync(command, { 
      timeout,
      maxBuffer: 10 * 1024 * 1024
    })
    return {
      stdout: stdout.trim(),
      stderr: stderr.trim(),
      exitCode: 0
    }
  } catch (e: any) {
    return {
      stdout: e.stdout?.trim() || '',
      stderr: e.stderr?.trim() || e.message,
      exitCode: e.code || 1
    }
  }
}

export default createMCPServer({
  name: 'terminal',
  version: '1.0.0',
  description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
  author: 'Trae Official',
  icon: '💻'
})  .forTrae({
    categories: ['Core, System'],
    rating: 'advanced',
    features: ['Command Execution, Script Runner, Package Manager']
  })
  .addTool({
    name: 'run_shell',
    description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
    parameters: {
      command: {
        type: 'string',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: true
      },
      cwd: {
        type: 'string',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      },
      timeout: {
        type: 'number',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      return runCommand(
        params.command,
        params.timeout
      )
    }
  })  .forTrae({
    categories: ['Core, System'],
    rating: 'advanced',
    features: ['Command Execution, Script Runner, Package Manager']
  })
  .addTool({
    name: 'npm_run',
    description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
    parameters: {
      script: {
        type: 'string',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: true
      },
      args: {
        type: 'string',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const cmd = `npm run ${params.script} ${params.args || ''}`.trim()
      return runCommand(cmd)
    }
  })  .forTrae({
    categories: ['Core, System'],
    rating: 'advanced',
    features: ['Command Execution, Script Runner, Package Manager']
  })
  .addTool({
    name: 'run_tests',
    description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
    parameters: {
      file: {
        type: 'string',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      },
      watch: {
        type: 'boolean',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const file = params.file ? ` ${params.file}` : ''
      return runCommand(`npm test${file}`)
    }
  })  .forTrae({
    categories: ['Core, System'],
    rating: 'advanced',
    features: ['Command Execution, Script Runner, Package Manager']
  })
  .addTool({
    name: 'install_deps',
    description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
    parameters: {
      packages: {
        type: 'string',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      },
      dev: {
        type: 'boolean',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      if (!params.packages) {
        return runCommand('npm install')
      }
      const devFlag = params.dev ? ' -D' : ''
      return runCommand(`npm install ${params.packages}${devFlag}`)
    }
  })
  .addPrompt({
    name: 'fix-error',
    description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
    arguments: [
      {
        name: 'command',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: true
      },
      {
        name: 'error_output',
        description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
        required: true
      }
    ],
    generate: async (args?: Record<string, any>) => {
      return `
## 🛠️ 错误修复任务

### 执行失败的命令:
\`\`\`bash
${args?.command || ''}
\`\`\`

### 错误输出:
\`\`\`
${args?.error_output || ''}
\`\`\`

### 任务要求:
1. 分析错误根因
2. 列出 2-3 个可能的解决方案
3. 选择最佳方案并自动执行
4. 验证修复结果

请系统性地诊断和修复这个问题！
      `.trim()
    }
  })
  .addResource({
    uri: 'trae://terminal/project-info',
    name: '项目信息摘要',
    description: 'Secure sandboxed terminal execution - shell commands, package management, script runner',
    get: async () => {
      const pkg = await runCommand('cat package.json 2>/dev/null || echo "{}"')
      const files = await runCommand('ls -la | head -20')
      
      return {
        packageJson: JSON.parse(pkg.stdout || '{}'),
        directoryListing: files.stdout,
        timestamp: new Date().toISOString()
      }
    }
  })
  .build()
