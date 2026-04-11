import { MCPServer } from './types'
import { callTool, getResource, generatePrompt } from './builder'
import fs from 'fs/promises'
import path from 'path'

export class MCPRegistry {
  private servers: Map<string, MCPServer> = new Map()

  register(serverId: string, server: MCPServer): void {
    this.servers.set(serverId, server)
  }

  unregister(serverId: string): boolean {
    return this.servers.delete(serverId)
  }

  getServer(serverId: string): MCPServer | undefined {
    return this.servers.get(serverId)
  }

  listServers(): Array<{ id: string; config: MCPServer['config'] }> {
    return Array.from(this.servers.entries()).map(([id, server]) => ({
      id,
      config: server.config
    }))
  }

  listAllTools(): Array<{ serverId: string; name: string; description: string }> {
    const result: Array<{ serverId: string; name: string; description: string }> = []
    for (const [serverId, server] of this.servers.entries()) {
      for (const tool of server.tools) {
        result.push({
          serverId,
          name: tool.name,
          description: tool.description
        })
      }
    }
    return result
  }

  listAllPrompts(): Array<{ serverId: string; name: string; description: string }> {
    const result: Array<{ serverId: string; name: string; description: string }> = []
    for (const [serverId, server] of this.servers.entries()) {
      for (const prompt of server.prompts) {
        result.push({
          serverId,
          name: prompt.name,
          description: prompt.description
        })
      }
    }
    return result
  }

  async callTool(serverId: string, toolName: string, params: Record<string, any>) {
    const server = this.servers.get(serverId)
    if (!server) throw new Error(`MCP Server ${serverId} not found`)
    return callTool(server, toolName, params)
  }

  async getResource(serverId: string, uri: string) {
    const server = this.servers.get(serverId)
    if (!server) throw new Error(`MCP Server ${serverId} not found`)
    return getResource(server, uri)
  }

  async generatePrompt(serverId: string, promptName: string, args?: Record<string, any>) {
    const server = this.servers.get(serverId)
    if (!server) throw new Error(`MCP Server ${serverId} not found`)
    return generatePrompt(server, promptName, args)
  }
}

export const globalMCPRegistry = new MCPRegistry()

export async function loadMCPFromDirectory(
  dirPath: string
): Promise<MCPServer | null> {
  try {
    const indexPath = path.join(dirPath, 'index.ts')
    const stats = await fs.stat(indexPath).catch(() => null)
    
    if (!stats) return null
    
    const module = await import(indexPath)
    if (module.default && module.default.config) {
      return module.default as MCPServer
    }
    return null
  } catch (e) {
    console.error(`Failed to load MCP from ${dirPath}:`, e)
    return null
  }
}
