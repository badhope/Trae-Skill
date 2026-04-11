import { createMCPServer } from '../../packages/core/mcp/builder'
import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'

const execAsync = promisify(exec)
async function safeExec(cmd: string): Promise<string> {
  try { const { stdout } = await execAsync(cmd, { timeout: 30000 }); return stdout.trim() }
  catch (e: any) { return e.stdout || e.message }
}

export default createMCPServer({
  name: 'docker',
  version: '1.0.0',
  description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds',
  author: 'Trae Official',
  icon: '🐳'
})  .forTrae({
    categories: ['DevOps, Container'],
    rating: 'intermediate',
    features: ['Dockerfile, Image Build, Compose']
  })
  .addTool({
    name: 'detect_project_for_docker',
    description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds',
    parameters: {},
    execute: async () => {
      const pkg = JSON.parse(await fs.readFile('package.json', 'utf-8').catch(() => '{}'))
      const hasNode = await fs.access('package.json').then(() => true).catch(() => false)
      const hasPython = await fs.access('requirements.txt').then(() => true).catch(() => false)
      return { type: hasNode ? 'node' : hasPython ? 'python' : 'unknown', pkg }
    }
  })  .forTrae({
    categories: ['DevOps, Container'],
    rating: 'intermediate',
    features: ['Dockerfile, Image Build, Compose']
  })
  .addTool({
    name: 'list_running_containers',
    description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds',
    parameters: {},
    execute: async () => ({ containers: await safeExec('docker ps --format "{{.Names}} {{.Image}} {{.Status}}"') })
  })  .forTrae({
    categories: ['DevOps, Container'],
    rating: 'intermediate',
    features: ['Dockerfile, Image Build, Compose']
  })
  .addTool({
    name: 'build_image',
    description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds',
    parameters: {
      tag: { type: 'string', description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds', required: true },
      noCache: { type: 'boolean', description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds', required: false }
    },
    execute: async (params: Record<string, any>) => ({ result: await safeExec(`docker build ${params.noCache ? '--no-cache' : ''} -t ${params.tag} .`) })
  })
  .addPrompt({
    name: 'dockerize',
    description: 'Docker containerization - best practice Dockerfiles, image optimization, multi-stage builds',
    generate: async () => `
## 🐳 容器化项目

### 步骤
1. 调用 \`detect_project_for_docker\` 确认项目类型
2. 生成多阶段构建的 Dockerfile
3. 生成 .dockerignore
4. 生成 docker-compose.yml

### Node.js 最佳实践
- 使用 alpine 基础镜像
- 先复制 package.json 安装依赖
- 再复制源码利用缓存
- 非 root 用户运行
- 健康检查配置
    `.trim()
  })
  .build()
