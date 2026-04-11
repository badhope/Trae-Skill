import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

async function safeExec(command: string): Promise<string> {
  try {
    const { stdout } = await execAsync(command, { timeout: 30000 })
    return stdout.trim()
  } catch (e: any) {
    return e.stdout?.trim() || e.message || String(e)
  }
}

export default createMCPServer({
  name: 'test-generator',
  version: '1.0.0',
  description: 'Automated test generation - unit tests, integration tests, coverage reporting',
  author: 'Trae Official',
  icon: '🧪'
})  .forTrae({
    categories: ['Testing, Quality'],
    rating: 'intermediate',
    features: ['Unit Tests, Coverage, TDD']
  })
  .addTool({
    name: 'detect_test_framework',
    description: 'Automated test generation - unit tests, integration tests, coverage reporting',
    parameters: {},
    execute: async () => {
      const pkg = await fs.readFile('package.json', 'utf-8').catch(() => '{}')
      const pkgJson = JSON.parse(pkg)
      const deps = { ...pkgJson.dependencies, ...pkgJson.devDependencies }
      
      let framework = 'unknown'
      if (deps.jest) framework = 'jest'
      else if (deps.vitest) framework = 'vitest'
      else if (deps.mocha) framework = 'mocha'
      else if (await fs.access('pytest.ini').catch(() => false)) framework = 'pytest'
      
      return { framework, hasCoverage: !!deps.nyc || !!deps['@vitest/coverage-v8'] }
    }
  })  .forTrae({
    categories: ['Testing, Quality'],
    rating: 'intermediate',
    features: ['Unit Tests, Coverage, TDD']
  })
  .addTool({
    name: 'generate_unit_test',
    description: 'Automated test generation - unit tests, integration tests, coverage reporting',
    parameters: {
      sourceFile: {
        type: 'string',
        description: 'Automated test generation - unit tests, integration tests, coverage reporting',
        required: true
      },
      framework: {
        type: 'string',
        description: 'Automated test generation - unit tests, integration tests, coverage reporting',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const source = await fs.readFile(params.sourceFile, 'utf-8').catch(() => '')
      const ext = path.extname(params.sourceFile)
      const testFile = params.sourceFile.replace(ext, `.test${ext}`)
      
      return {
        sourceFile: params.sourceFile,
        testFile,
        sourceContent: source,
        framework: params.framework || 'jest'
      }
    }
  })  .forTrae({
    categories: ['Testing, Quality'],
    rating: 'intermediate',
    features: ['Unit Tests, Coverage, TDD']
  })
  .addTool({
    name: 'run_tests_with_coverage',
    description: 'Automated test generation - unit tests, integration tests, coverage reporting',
    parameters: {
      file: {
        type: 'string',
        description: 'Automated test generation - unit tests, integration tests, coverage reporting',
        required: false
      }
    },
    execute: async (params: Record<string, any>) => {
      const file = params.file ? ` ${params.file}` : ''
      return {
        testOutput: await safeExec(`npm test -- --coverage${file}`),
        coverage: await safeExec('npx istanbul report text 2>/dev/null || echo "N/A"')
      }
    }
  })
  .addPrompt({
    name: 'write-tests',
    description: 'Automated test generation - unit tests, integration tests, coverage reporting',
    arguments: [
      {
        name: 'file',
        description: 'Automated test generation - unit tests, integration tests, coverage reporting',
        required: true
      }
    ],
    generate: async (args?: Record<string, any>) => {
      return `
## 🧪 测试生成任务

### 任务
为 \`${args?.file}\` 生成完整的单元测试

### 步骤
1. 调用 \`detect_test_framework\` 确认测试框架
2. 调用 \`generate_unit_test\` 获取源代码
3. 分析: 导出的函数/类、边界条件
4. 生成: 至少 80% 覆盖率的测试用例
5. 调用 \`run_tests_with_coverage\` 验证

### 要求
- 包含正常场景、边界场景、异常场景
- 使用 AAA 模式: Arrange-Act-Assert
- 每个测试描述清晰说明测试意图
      `.trim()
    }
  })
  .addResource({
    uri: 'trae://test/coverage-summary',
    name: '测试覆盖率摘要',
    description: 'Automated test generation - unit tests, integration tests, coverage reporting',
    get: async () => {
      return {
        timestamp: new Date().toISOString(),
        coverage: await safeExec('npx vitest run --coverage.enabled --coverage.reporter=text-summary 2>/dev/null | tail -10 || echo "N/A"')
      }
    }
  })
  .build()
