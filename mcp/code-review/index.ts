import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

function calculateCyclomaticComplexity(code: string): number {
  let complexity = 1
  const patterns = [
    /\bif\b/g, /\belse\s+if\b/g, /\bfor\b/g, /\bwhile\b/g,
    /\bcase\b/g, /\bcatch\b/g, /\?/g, /\|\|/g, /&&/g,
    /\bswitch\b/g, /\bthrow\b/g, /\breturn\s+.+/g
  ]
  patterns.forEach(pattern => {
    const matches = code.match(pattern)
    if (matches) complexity += matches.length
  })
  return complexity
}

function countLines(code: string): { total: number; code: number; comment: number; blank: number } {
  const lines = code.split('\n')
  let comment = 0
  let blank = 0
  let inBlockComment = false
  
  lines.forEach(line => {
    const trimmed = line.trim()
    if (!trimmed) {
      blank++
    } else if (trimmed.startsWith('/*')) {
      inBlockComment = true
      comment++
    } else if (inBlockComment) {
      comment++
      if (trimmed.includes('*/')) inBlockComment = false
    } else if (trimmed.startsWith('//') || trimmed.startsWith('*')) {
      comment++
    }
  })
  
  return {
    total: lines.length,
    code: lines.length - comment - blank,
    comment,
    blank
  }
}

function detectBugs(code: string): Array<{ type: string; line: number; message: string; severity: 'low' | 'medium' | 'high' }> {
  const issues: Array<{ type: string; line: number; message: string; severity: 'low' | 'medium' | 'high' }> = []
  const lines = code.split('\n')
  
  lines.forEach((line, idx) => {
    const lineNum = idx + 1
    
    if (/(=|==|!=|!==|<|>|<=|>=)\s*$/.test(line.trim()) && !line.includes('?')) {
      issues.push({
        type: 'Possible Bug',
        line: lineNum,
        message: '表达式可能未完成，跨行断裂风险',
        severity: 'medium'
      })
    }
    
    if (line.includes('console.log') && !line.includes('//')) {
      issues.push({
        type: 'Code Smell',
        line: lineNum,
        message: '生产代码应移除 console.log',
        severity: 'low'
      })
    }
    
    if (line.includes('debugger') && !line.includes('//')) {
      issues.push({
        type: 'Critical',
        line: lineNum,
        message: '生产代码绝对不能包含 debugger 语句',
        severity: 'high'
      })
    }
    
    if (/eval\s*\(/.test(line) && !line.includes('//')) {
      issues.push({
        type: 'Security',
        line: lineNum,
        message: 'eval() 存在严重代码注入安全风险',
        severity: 'high'
      })
    }
    
    if (/innerHTML\s*=|outerHTML\s*=/.test(line) && !line.includes('//')) {
      issues.push({
        type: 'Security',
        line: lineNum,
        message: 'innerHTML 可能导致 XSS 攻击，请使用 textContent 或安全转义',
        severity: 'medium'
      })
    }
    
    if (/setTimeout\s*\(\s*["']/.test(line)) {
      issues.push({
        type: 'Security',
        line: lineNum,
        message: 'setTimeout 字符串参数等同于 eval，存在代码注入风险',
        severity: 'high'
      })
    }
    
    if (/typeof\s+(\w+)\s*===\s*["']undefined["']/.test(line)) {
      issues.push({
        type: 'Improvement',
        line: lineNum,
        message: '建议使用 "typeof x === \"undefined\"" 或更现代的可选链操作符',
        severity: 'low'
      })
    }
    
    if (/Array\.prototype\.\w+\.call\(/.test(line)) {
      issues.push({
        type: 'Improvement',
        line: lineNum,
        message: '考虑使用更现代的 Array.from 或扩展运算符',
        severity: 'low'
      })
    }
    
    if (/function\s*\w*\s*\([^)]*\)\s*\{[^}]*$/.test(line) && idx + 50 < lines.length) {
      issues.push({
        type: 'Maintainability',
        line: lineNum,
        message: '函数可能过大，建议拆分为更小的函数',
        severity: 'medium'
      })
    }
  })
  
  return issues
}

function detectCodeStyle(code: string): Array<{ type: string; line: number; message: string }> {
  const issues: Array<{ type: string; line: number; message: string }> = []
  const lines = code.split('\n')
  
  lines.forEach((line, idx) => {
    const lineNum = idx + 1
    
    if (line.includes('\t')) {
      issues.push({
        type: 'Style',
        line: lineNum,
        message: '使用了 Tab 缩进，建议使用空格'
      })
    }
    
    if (line.length > 120) {
      issues.push({
        type: 'Style',
        line: lineNum,
        message: `行过长 (${line.length} chars)，建议控制在120字符内`
      })
    }
    
    if (/\s+$/.test(line)) {
      issues.push({
        type: 'Style',
        line: lineNum,
        message: '行尾有多余空格'
      })
    }
    
    if (/let\s+\w+\s*=\s*(null|undefined)/.test(line)) {
      issues.push({
        type: 'Style',
        line: lineNum,
        message: '建议使用 const 如果变量不会被重新赋值'
      })
    }
    
    if (/(var)\s+\w+/.test(line)) {
      issues.push({
        type: 'Style',
        line: lineNum,
        message: '建议使用 let/const 替代 var'
      })
    }
  })
  
  return issues
}

function calculateMaintainabilityIndex(metrics: any): string {
  const score = 171
    - 5.2 * Math.log(metrics.complexity)
    - 0.23 * metrics.loc.code
    - 16.2 * Math.log(metrics.loc.total)
  
  if (score >= 100) return 'A - 极易维护'
  if (score >= 75) return 'B - 良好维护性'
  if (score >= 50) return 'C - 中等维护性'
  if (score >= 25) return 'D - 较难维护'
  return 'F - 难以维护'
}

export default createMCPServer({
  name: 'code-review',
  version: '2.0.0',
  description: 'AI-powered 深度代码审查 - 圈复杂度、Bug检测、安全扫描、代码规范、可维护性分析',
  author: 'Trae Professional',
  icon: '🔍'
})
  .addTool({
    name: 'analyze_complexity',
    description: '计算代码圈复杂度 Cyclomatic Complexity',
    parameters: {
      code: { type: 'string', description: '代码内容', required: false },
      filepath: { type: 'string', description: '文件路径', required: false }
    },
    execute: async (params: Record<string, any>) => {
      let code = params.code
      if (params.filepath) {
        code = await fs.readFile(params.filepath, 'utf-8')
      }
      const complexity = calculateCyclomaticComplexity(code)
      const loc = countLines(code)
      const functions = (code.match(/function\s+\w+|const\s+\w+\s*=\s*\(|async\s+\(|=>\s*\{/g) || []).length
      
      let rating = 'A - 优'
      let recommendation = '复杂度控制优秀'
      if (complexity > 50) { rating = 'F - 极复杂'; recommendation = '强烈建议立即重构' }
      else if (complexity > 30) { rating = 'D - 复杂'; recommendation = '需要重点重构' }
      else if (complexity > 20) { rating = 'C - 中等'; recommendation = '建议重构拆分' }
      else if (complexity > 10) { rating = 'B - 良好'; recommendation = '可以考虑进一步拆分' }
      
      return {
        success: true,
        filepath: params.filepath,
        cyclomaticComplexity: complexity,
        complexityRating: rating,
        functions,
        avgComplexityPerFunction: functions > 0 ? (complexity / functions).toFixed(2) : 'N/A',
        linesOfCode: loc,
        recommendation,
        industryStandard: '业界推荐单文件圈复杂度 < 50，单函数 < 10'
      }
    }
  })
  .addTool({
    name: 'detect_bugs',
    description: '静态代码Bug检测 - 常见陷阱、安全漏洞、代码异味',
    parameters: {
      code: { type: 'string', description: '代码内容', required: false },
      filepath: { type: 'string', description: '文件路径', required: false }
    },
    execute: async (params: Record<string, any>) => {
      let code = params.code
      if (params.filepath) {
        code = await fs.readFile(params.filepath, 'utf-8')
      }
      const bugs = detectBugs(code)
      const style = detectCodeStyle(code)
      
      const severityCount = {
        high: bugs.filter(b => b.severity === 'high').length,
        medium: bugs.filter(b => b.severity === 'medium').length,
        low: bugs.filter(b => b.severity === 'low').length
      }
      
      return {
        success: true,
        filepath: params.filepath,
        summary: {
          totalIssues: bugs.length + style.length,
          bugs: bugs.length,
          styleIssues: style.length,
          severityCount,
          securityIssues: bugs.filter(b => b.type === 'Security').length
        },
        bugs,
        styleIssues: style
      }
    }
  })
  .addTool({
    name: 'maintainability_analysis',
    description: '代码可维护性指数分析 Maintainability Index',
    parameters: {
      filepath: { type: 'string', description: '文件路径', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const code = await fs.readFile(params.filepath, 'utf-8')
      const complexity = calculateCyclomaticComplexity(code)
      const loc = countLines(code)
      const halsteadVolume = code.length * Math.log2(new Set(code.split(/\s+/)).size || 1)
      const metrics = { complexity, loc, halsteadVolume }
      const maintainability = calculateMaintainabilityIndex(metrics)
      
      return {
        success: true,
        filepath: params.filepath,
        maintainabilityIndex: maintainability,
        metrics: {
          cyclomaticComplexity: complexity,
          linesOfCode: loc,
          halsteadVolume: Math.round(halsteadVolume),
          commentRatio: loc.total > 0 ? ((loc.comment / loc.total) * 100).toFixed(1) + '%' : 'N/A'
        },
        suggestions: [
          '注释率建议控制在 20-30%',
          '圈复杂度建议 < 50',
          '单个函数建议不超过 50 行代码'
        ]
      }
    }
  })
  .addTool({
    name: 'full_code_review',
    description: '完整代码审查报告 - 全方位质量扫描',
    parameters: {
      filepath: { type: 'string', description: '文件路径', required: true },
      focus: { type: 'string', description: '审查重点: all, bugs, style, security, complexity', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const code = await fs.readFile(params.filepath, 'utf-8')
      const focus = params.focus || 'all'
      
      const complexity = calculateCyclomaticComplexity(code)
      const loc = countLines(code)
      const bugs = detectBugs(code)
      const style = detectCodeStyle(code)
      const metrics = { complexity, loc }
      const maintainability = calculateMaintainabilityIndex(metrics)
      
      const score = Math.max(0, 100
        - Math.min(30, bugs.filter(b => b.severity === 'high').length * 15)
        - Math.min(20, bugs.filter(b => b.severity === 'medium').length * 5)
        - Math.min(10, bugs.filter(b => b.severity === 'low').length * 2)
        - Math.min(20, style.length)
        - Math.min(20, Math.max(0, complexity - 20)))
      
      let grade = 'F'
      if (score >= 90) grade = 'A'
      else if (score >= 80) grade = 'B'
      else if (score >= 70) grade = 'C'
      else if (score >= 60) grade = 'D'
      
      return {
        success: true,
        filepath: params.filepath,
        reviewFocus: focus,
        overallScore: score,
        overallGrade: grade,
        maintainability,
        metrics: {
          cyclomaticComplexity: complexity,
          linesOfCode: loc,
          bugsFound: bugs.length,
          styleIssues: style.length,
          securityVulnerabilities: bugs.filter(b => b.type === 'Security').length
        },
        topIssues: bugs.slice(0, 5),
        recommendations: [
          score >= 80 ? '✅ 代码质量优秀，继续保持！' : '⚠️ 建议改进代码质量',
          bugs.filter(b => b.severity === 'high').length > 0 ? '🔴 需要优先修复高严重级别问题' : '✅ 无高危问题',
          complexity > 30 ? '🟡 复杂度偏高，考虑重构拆分' : '✅ 复杂度控制良好',
          style.length > 10 ? '🟡 代码规范问题较多，建议统一格式化' : '✅ 代码规范良好'
        ].filter(Boolean)
      }
    }
  })
  .addPrompt({
    name: 'deep-review',
    description: 'AI 深度代码审查工作流',
    arguments: [
      { name: 'filepath', description: '要审查的文件路径', required: true }
    ],
    generate: async (args?: Record<string, any>) => `
## 🔍 AI深度代码审查: ${args?.filepath || '未知文件'}

### 📊 执行步骤

**第1步: 基础质量扫描**
调用 \`full_code_review\` 获取整体评分和概览

**第2步: 深度Bug检测**
调用 \`detect_bugs\` 找出所有潜在问题

**第3步: 复杂度分析**  
调用 \`analyze_complexity\` 评估代码复杂度

**第4步: 可维护性分析**
调用 \`maintainability_analysis\`

**第5步: AI 综合建议**
基于以上数据，给出：
1. 🔴 必须修复的阻断性问题
2. 🟡 应该改进的代码异味  
3. 🟢 值得肯定的优点
4. 📋 具体可行的重构建议

### 🎯 审查标准
- 安全漏洞零容忍
- 圈复杂度 < 50
- 高危Bug = 0
- 整体评分 >= 80分
    `.trim()
  })
  .build()
