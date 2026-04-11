export * from './mcp/types'
export * from './mcp/builder'
export * from './mcp/registry'
export { loadSkillFromDirectory } from './loader'
export { SkillRegistry } from './registry'

import { globalMCPRegistry } from './mcp/registry'
import gitServer from '../../mcp/git/index'
import terminalServer from '../../mcp/terminal/index'
import codeReviewServer from '../../mcp/code-review/index'

globalMCPRegistry.register('git', gitServer)
globalMCPRegistry.register('terminal', terminalServer)
globalMCPRegistry.register('code-review', codeReviewServer)

export { globalMCPRegistry }

export function listInstalledMCP() {
  return globalMCPRegistry.listServers()
}

export function listAllTools() {
  return globalMCPRegistry.listAllTools()
}

export function listAllPrompts() {
  return globalMCPRegistry.listAllPrompts()
}
