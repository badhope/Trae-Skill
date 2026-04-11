import { createMCPServer } from '../../packages/core/mcp/builder'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

async function safeExec(cmd: string): Promise<string> {
  try {
    const { stdout } = await execAsync(cmd, { timeout: 15000 })
    return stdout.trim()
  } catch (e: any) {
    return e.stdout?.trim() || e.message
  }
}

export default createMCPServer({
  name: 'git',
  version: '1.0.0',
  description: 'Git version control toolkit - commit, branch, diff, log and code review operations',
  icon: '📦'
})
  .forTrae({
    categories: ['Version Control', 'Core'],
    rating: 'beginner',
    features: ['Git Operations', 'Code Review', 'Branch Management']
  })
  .addTool({
    name: 'get_current_branch',
    description: 'Get the name of currently active git branch',
    parameters: {},
    execute: async () => ({ branch: await safeExec('git branch --show-current') })
  })
  .addTool({
    name: 'get_staged_diff',
    description: 'Get diff of all staged changes for code review',
    parameters: {},
    execute: async () => ({ diff: await safeExec('git diff --staged') })
  })
  .addTool({
    name: 'get_commit_history',
    description: 'View recent git commit history',
    parameters: {
      limit: {
        type: 'number',
        description: 'Number of recent commits to show, default 10',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => ({
      log: await safeExec(`git log --oneline -n ${params.limit || 10}`)
    })
  })
  .addTool({
    name: 'create_commit',
    description: 'Stage all changes and create conventional commit',
    parameters: {
      message: {
        type: 'string',
        description: 'Commit message following conventional format: type(scope): description',
        required: true
      }
    },
    execute: async (params: Record<string, any>) => ({
      add: await safeExec('git add .'),
      commit: await safeExec(`git commit -m "${params.message}"`)
    })
  })
  .addResource({
    uri: 'trae://git/status',
    name: 'Git Workspace Status',
    description: 'Current repository status with modified and staged files',
    get: async () => ({
      branch: await safeExec('git branch --show-current'),
      status: await safeExec('git status --short'),
      staged: await safeExec('git diff --staged --name-only'),
      unstaged: await safeExec('git diff --name-only')
    })
  })
  .addPrompt({
    name: 'review-my-changes',
    description: 'Review changes before committing',
    arguments: [{ name: 'files', description: 'Specific files to review', required: false }],
    generate: async (args?: Record<string, any>) => `
## 📝 Code Change Review Request

### Current Workspace Changes:
\`\`\`diff
${await safeExec('git diff')}
\`\`\`

### Task
Please perform a thorough code review and provide:

1. 🔍 **Bug Detection**: Find potential issues, edge cases, or logical errors
2. 🎯 **Best Practices**: Suggest improvements following coding standards
3. 🔒 **Security**: Identify any security vulnerabilities
4. ⚡ **Performance**: Mention any performance concerns
5. 💡 **Refactoring**: Suggest cleaner implementation approaches

Focus on the quality and maintainability of the code changes.
    `.trim()
  })
  .build()
