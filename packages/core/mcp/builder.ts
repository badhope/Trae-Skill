import { 
  MCPServerConfig, 
  ToolDefinition, 
  Resource, 
  PromptDefinition, 
  MCPServer,
  ToolResult 
} from './types'

export class MCPServerBuilder {
  private config: MCPServerConfig
  private tools: ToolDefinition[] = []
  private resources: Resource[] = []
  private prompts: PromptDefinition[] = []

  constructor(config: MCPServerConfig) {
    this.config = {
      ...config,
      author: config.author || 'Trae Official',
      trae: {
        visibility: 'public',
        rating: 'intermediate',
        categories: config.trae?.categories || ['Development'],
        features: config.trae?.features || [],
        ...config.trae
      }
    }
  }

  forTrae(options: {
    categories?: string[]
    rating?: 'beginner' | 'intermediate' | 'advanced'
    features?: string[]
  }): this {
    this.config.trae = {
      ...this.config.trae,
      ...options
    }
    return this
  }

  addTool(tool: ToolDefinition): this {
    this.tools.push(tool)
    return this
  }

  addResource(resource: Resource): this {
    this.resources.push(resource)
    return this
  }

  addPrompt(prompt: PromptDefinition): this {
    this.prompts.push(prompt)
    return this
  }

  build(): MCPServer {
    return {
      config: this.config,
      tools: this.tools,
      resources: this.resources,
      prompts: this.prompts
    }
  }
}

export function createMCPServer(config: MCPServerConfig): MCPServerBuilder {
  return new MCPServerBuilder(config)
}

export async function callTool(
  server: MCPServer, 
  toolName: string, 
  params: Record<string, any>
): Promise<ToolResult> {
  try {
    const tool = server.tools.find((t: ToolDefinition) => t.name === toolName)
    if (!tool) {
      return { success: false, error: `Tool ${toolName} not found` }
    }
    const data = await tool.execute(params)
    return { success: true, data }
  } catch (e: any) {
    return { success: false, error: e.message }
  }
}

export async function getResource(
  server: MCPServer, 
  uri: string
): Promise<ToolResult> {
  try {
    const resource = server.resources.find((r: Resource) => r.uri === uri)
    if (!resource) {
      return { success: false, error: `Resource ${uri} not found` }
    }
    const data = await resource.get()
    return { success: true, data }
  } catch (e: any) {
    return { success: false, error: e.message }
  }
}

export async function generatePrompt(
  server: MCPServer, 
  promptName: string,
  args?: Record<string, any>
): Promise<ToolResult> {
  try {
    const prompt = server.prompts.find((p: PromptDefinition) => p.name === promptName)
    if (!prompt) {
      return { success: false, error: `Prompt ${promptName} not found` }
    }
    const data = await prompt.generate(args)
    return { success: true, data }
  } catch (e: any) {
    return { success: false, error: e.message }
  }
}
