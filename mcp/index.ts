import { createMCPServer } from '../packages/core/mcp/builder'

const modules: Record<string, () => Promise<any>> = {
  agent: () => import('./agent'),
  'agent-autonomous': () => import('./agent-autonomous'),
  'agent-multi': () => import('./agent-multi'),
  'agent-reflection': () => import('./agent-reflection'),
  aliyun: () => import('./aliyun'),
  aws: () => import('./aws'),
  bitbucket: () => import('./bitbucket'),
  'browser-automation': () => import('./browser-automation'),
  cloudflare: () => import('./cloudflare'),
  'code-generator': () => import('./code-generator'),
  'code-rag': () => import('./code-rag'),
  'code-review': () => import('./code-review'),
  'coding-workflow': () => import('./coding-workflow'),
  colors: () => import('./colors'),
  compression: () => import('./compression'),
  csv: () => import('./csv'),
  database: () => import('./database'),
  datetime: () => import('./datetime'),
  'debugging-workflow': () => import('./debugging-workflow'),
  'dependency-analyzer': () => import('./dependency-analyzer'),
  diff: () => import('./diff'),
  docker: () => import('./docker'),
  documentation: () => import('./documentation'),
  encoding: () => import('./encoding'),
  env: () => import('./env'),
  filesystem: () => import('./filesystem'),
  fun: () => import('./fun'),
  git: () => import('./git'),
  github: () => import('./github'),
  gitlab: () => import('./gitlab'),
  gitee: () => import('./gitee'),
  images: () => import('./images'),
  jira: () => import('./jira'),
  json: () => import('./json'),
  kubernetes: () => import('./kubernetes'),
  llm: () => import('./llm'),
  markdown: () => import('./markdown'),
  math: () => import('./math'),
  memory: () => import('./memory'),
  mongodb: () => import('./mongodb'),
  network: () => import('./network'),
  npm: () => import('./npm'),
  openai: () => import('./openai'),
  pdf: () => import('./pdf'),
  'performance-optimizer': () => import('./performance-optimizer'),
  powerpoint: () => import('./powerpoint'),
  prompt: () => import('./prompt'),
  puppeteer: () => import('./puppeteer'),
  random: () => import('./random'),
  react: () => import('./react'),
  redis: () => import('./redis'),
  'refactoring-workflow': () => import('./refactoring-workflow'),
  regex: () => import('./regex'),
  search: () => import('./search'),
  'website-builder': () => import('./website-builder'),
  'web-search': () => import('./web-search'),
  thinking: () => import('./thinking'),
  'security-auditor': () => import('./security-auditor'),
  sentry: () => import('./sentry'),
  'site-generator': () => import('./site-generator'),
  spreadsheet: () => import('./spreadsheet'),
  ssh: () => import('./ssh'),
  terminal: () => import('./terminal'),
  'test-generator': () => import('./test-generator'),
  typescript: () => import('./typescript'),
  vector: () => import('./vector'),
  vercel: () => import('./vercel'),
  'web-crawler': () => import('./web-crawler'),
  word: () => import('./word'),
  yaml: () => import('./yaml')
}

export async function loadMCPModule(name: string) {
  const loader = modules[name]
  if (loader) {
    const module = await loader()
    return module.default
  }
  throw new Error(`MCP module not found: ${name}. Available: ${Object.keys(modules).join(', ')}`)
}

export function listAvailableModules() {
  return Object.keys(modules)
}

export function getModuleCategories() {
  return {
    basic: ['colors', 'datetime', 'diff', 'encoding', 'env', 'json', 'markdown', 'random', 'regex', 'yaml'],
    intermediate: ['compression', 'csv', 'filesystem', 'images', 'math', 'network', 'pdf', 'search', 'thinking'],
    advanced: [
      'agent', 'code-generator', 'code-rag', 'code-review', 'coding-workflow',
      'database', 'debugging-workflow', 'dependency-analyzer', 'documentation',
      'llm', 'memory', 'performance-optimizer', 'prompt', 'refactoring-workflow',
      'security-auditor', 'test-generator', 'typescript', 'vector'
    ],
    devops: [
      'aliyun', 'aws', 'cloudflare', 'docker', 'git', 'github', 'gitlab', 'gitee',
      'kubernetes', 'mongodb', 'npm', 'redis', 'ssh', 'terminal', 'vercel'
    ],
    integration: [
      'bitbucket', 'browser-automation', 'jira', 'openai', 'puppeteer',
      'sentry', 'site-generator', 'spreadsheet', 'powerpoint', 'word', 'web-crawler'
    ],
    fun: ['fun']
  }
}

if (require.main === module) {
  const moduleName = process.argv[2]
  if (moduleName === 'list') {
    console.log('📦 Available MCP Modules (65+):')
    const categories = getModuleCategories()
    for (const [category, mods] of Object.entries(categories)) {
      console.log(`\n${category.toUpperCase()} (${mods.length}):`)
      mods.forEach(m => console.log(`  - ${m}`))
    }
  } else if (moduleName && modules[moduleName]) {
    loadMCPModule(moduleName).catch(console.error)
  } else {
    console.log('Usage: node mcp/index.js <module-name>')
    console.log('  or: node mcp/index.js list')
    console.log('\nAvailable modules:', listAvailableModules().join(', '))
  }
}

export default createMCPServer({
  name: 'mcp-hub',
  version: '1.0.0',
  description: 'MCP Hub - 65+ Tools Unified Entry Point',
  author: 'Trae Professional',
  icon: '🔌'
})
  .addTool({
    name: 'list_modules',
    description: '列出所有可用的MCP模块',
    parameters: {},
    execute: async () => {
      return {
        success: true,
        total: Object.keys(modules).length,
        categories: getModuleCategories(),
        modules: listAvailableModules()
      }
    }
  })
  .addTool({
    name: 'load_module_info',
    description: '获取指定模块的详细信息',
    parameters: {
      name: { type: 'string', description: '模块名称', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const moduleNames = Object.keys(modules)
      const isExists = moduleNames.includes(params.name)
      return {
        success: true,
        module: params.name,
        exists: isExists,
        message: isExists ? `模块 ${params.name} 可用` : `未找到模块: ${params.name}`
      }
    }
  })
  .build()
