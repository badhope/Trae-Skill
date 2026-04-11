export interface ToolParameter {
  type: 'string' | 'number' | 'boolean' | 'object' | 'array'
  description?: string
  enum?: string[]
  required?: boolean
  properties?: Record<string, ToolParameter>
  items?: ToolParameter
}

export interface ToolDefinition {
  name: string
  description: string
  parameters: Record<string, ToolParameter>
  execute: (params: Record<string, any>) => Promise<any>
}

export interface Resource {
  uri: string
  name: string
  description: string
  mimeType?: string
  get: () => Promise<string | object>
}

export interface PromptArgument {
  name: string
  description: string
  required?: boolean
  defaultValue?: any
}

export interface PromptDefinition {
  name: string
  description: string
  arguments?: PromptArgument[]
  generate: (args?: Record<string, any>) => Promise<string>
}

export interface MCPServerConfig {
  name: string
  version: string
  description: string
  author?: string
  icon?: string
  trae?: {
    categories?: string[]
    visibility?: 'public' | 'private'
    rating?: 'beginner' | 'intermediate' | 'advanced'
    features?: string[]
  }
}

export interface MCPServer {
  config: MCPServerConfig
  tools: ToolDefinition[]
  resources: Resource[]
  prompts: PromptDefinition[]
}

export type ToolResult = {
  success: boolean
  data?: any
  error?: string
}

export type ResourceContent = {
  uri: string
  mimeType: string
  text: string
}

export type PromptGenerated = {
  messages: Array<{
    role: 'user' | 'assistant' | 'system'
    content: string
  }>
}

export interface SkillContext {
  currentFile: {
    path: string
    content: string
    language: string
  }
  ai: {
    chat: (prompt: string, options?: any) => Promise<string>
  }
  ide: {
    showNotification: (message: string, type?: string) => void
    showPanel: (content: string, title?: string) => void
  }
}

export interface SkillDefinition {
  name: string
  description: string
  icon?: string
  category?: string
  keywords?: string[]
  author?: string
  version?: string
  activationEvents?: string[]
  run: (context: SkillContext) => Promise<any>
}

export function defineSkill(def: SkillDefinition): SkillDefinition {
  return def
}
