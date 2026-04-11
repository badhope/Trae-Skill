import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

interface ThinkStep {
  id: number
  title: string
  content: string
  type: 'observation' | 'reasoning' | 'hypothesis' | 'verification' | 'conclusion'
  confidence: number
  next: string[]
  assumptions: string[]
}

export default createMCPServer({
  name: 'sequential-thinking',
  version: '1.0.0',
  description: '顺序思维链 - 让AI像人类一样思考，大幅提升复杂推理准确率',
  author: 'Trae Professional',
  icon: '🧠'
})
  .addTool({
    name: 'start_thinking',
    description: '开启深度思维模式 - 第1步：明确问题边界',
    parameters: {
      problem: { type: 'string', description: '需要解决的问题', required: true },
      context: { type: 'string', description: '已知背景信息', required: false }
    },
    execute: async (params: Record<string, any>) => {
      return {
        success: true,
        phase: 'problem_framing',
        step: 1,
        output: `
## 🧠 思维链启动

### 📌 问题定义
> ${params.problem}

### 🎯 标准化思维流程

**第1阶段: 问题拆解 (当前阶段)**
▢ 明确已知条件
▢ 识别隐含假设
▢ 定义成功标准
▢ 划定解决边界

**第2阶段: 多路径探索**
▢ 生成3-5种可能解法
▢ 评估每种路径的可行性
▢ 识别关键难点

**第3阶段: 深度验证**
▢ 逐步推导每一步
▢ 检查逻辑漏洞
▢ 交叉验证结论

**第4阶段: 结构化输出**
▢ 总结核心发现
▢ 列出遗留问题
▢ 给出行动建议

---
✅ 思维模式已激活，请按照以上框架进行深度思考！
        `.trim()
      }
    }
  })
  .addTool({
    name: 'add_thought',
    description: '记录一个思维节点',
    parameters: {
      stepNumber: { type: 'number', description: '思考步骤序号', required: true },
      title: { type: 'string', description: '本步思考标题', required: true },
      content: { type: 'string', description: '详细思考内容', required: true },
      type: { type: 'string', description: '思维类型', enum: ['observation', 'reasoning', 'hypothesis', 'verification', 'conclusion'], required: true },
      confidence: { type: 'number', description: '置信度 0-100', required: false },
      assumptions: { type: 'string', description: '本步依赖的假设(逗号分隔)', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const confidence = params.confidence || 80
      const assumptions = params.assumptions?.split(',') || []
      const confidenceEmoji = confidence >= 90 ? '🔵' : confidence >= 70 ? '🟢' : confidence >= 50 ? '🟡' : '🔴'
      
      const typeEmojis: Record<string, string> = {
        observation: '👁️',
        reasoning: '💭',
        hypothesis: '💡',
        verification: '✅',
        conclusion: '🎯'
      }
      
      return {
        success: true,
        thought: {
          step: params.stepNumber,
          title: params.title,
          type: params.type,
          typeEmoji: typeEmojis[params.type] || '💭',
          confidence,
          confidenceEmoji,
          confidenceLevel: confidence >= 90 ? '极高' : confidence >= 70 ? '高' : confidence >= 50 ? '中等' : '低',
          assumptions,
          content: params.content
        },
        recommendation: confidence < 50 ? '⚠️ 置信度偏低，建议验证假设' : '✅ 继续下一步思考'
      }
    }
  })
  .addTool({
    name: 'critical_review',
    description: '批判性审查当前思维 - 自动发现漏洞和盲区',
    parameters: {
      thoughtsJson: { type: 'string', description: '已有的思考节点JSON数组字符串', required: true },
      currentConclusion: { type: 'string', description: '当前的结论', required: true }
    },
    execute: async (params: Record<string, any>) => {
      let thoughts: ThinkStep[] = []
      try {
        thoughts = JSON.parse(params.thoughtsJson)
      } catch (e) {}
      
      const checkList = [
        {
          item: '逻辑链条完整性',
          passed: thoughts.length >= 3,
          message: thoughts.length >= 3 ? '✅ 思考步数充足' : `⚠️ 仅进行了 ${thoughts.length} 步思考，建议更深入`
        },
        {
          item: '假设显性化',
          passed: thoughts.every((t: ThinkStep) => t.assumptions && t.assumptions.length > 0),
          message: '🔍 建议明确每一步依赖的隐含假设'
        },
        {
          item: '置信度合理性',
          passed: !thoughts.some((t: ThinkStep) => (t.confidence || 80) < 50),
          message: thoughts.some((t: ThinkStep) => (t.confidence || 80) < 50) ? '🔴 存在置信度<50%的低置信步骤' : '✅ 所有步骤置信度合理'
        },
        {
          item: '反向验证环节',
          passed: thoughts.some((t: ThinkStep) => t.type === 'verification'),
          message: thoughts.some((t: ThinkStep) => t.type === 'verification') ? '✅ 包含验证步骤' : '⚠️ 缺少独立验证，建议尝试证伪'
        },
        {
          item: '备选方案考虑',
          passed: thoughts.some((t: ThinkStep) => t.next && t.next.length > 1),
          message: '💡 建议思考其他可能的推理路径'
        }
      ]
      
      return {
        success: true,
        reviewPhase: '批判性审查',
        score: Math.round(checkList.filter(c => c.passed).length / checkList.length * 100),
        checkList,
        cognitiveBiasesCheck: [
          '⚠️ 是否存在证实偏差？(只寻找支持已有结论的证据)',
          '⚠️ 是否存在锚定效应？(过度依赖最初信息)',
          '⚠️ 是否存在易得性偏差？(偏好容易想到的答案)',
          '⚠️ 是否存在框架效应？(问题表述影响了判断)'
        ],
        recommendation: `
📋 审查完成！请修正以上问题后继续思考。

黄金法则：
1. 慢思考，分细步，不要跳步
2. 显性化所有隐含假设
3. 主动尝试证伪，而不只是证实
4. 考虑至少2种替代方案
        `.trim()
      }
    }
  })
  .addTool({
    name: 'conclude_thinking',
    description: '总结完整思维链，生成最终报告',
    parameters: {
      problem: { type: 'string', description: '原始问题', required: true },
      finalAnswer: { type: 'string', description: '最终答案', required: true },
      confidence: { type: 'number', description: '整体置信度 0-100', required: true },
      remainingUncertainties: { type: 'string', description: '遗留不确定性(逗号分隔)', required: false },
      alternativeAnswers: { type: 'string', description: '备选答案(逗号分隔)', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const uncertainties = params.remainingUncertainties?.split(',') || []
      const alternatives = params.alternativeAnswers?.split(',') || []
      const grade = params.confidence >= 90 ? 'A+' : params.confidence >= 80 ? 'A' : params.confidence >= 70 ? 'B' : params.confidence >= 60 ? 'C' : 'D'
      
      return {
        success: true,
        thinkingComplete: true,
        finalReport: {
          originalProblem: params.problem,
          finalAnswer: params.finalAnswer,
          overallConfidence: params.confidence,
          confidenceGrade: grade,
          remainingUncertainties: uncertainties,
          alternativeSolutions: alternatives,
          qualityIndicators: {
            explicitUncertainties: uncertainties.length > 0 ? '✅ 已说明不确定性' : '💡 建议明确说明剩余不确定点',
            consideredAlternatives: alternatives.length > 0 ? '✅ 考虑了备选方案' : '💡 建议思考替代方案'
          }
        },
        closingRemarks: `
🧠 思维链完成！

${params.confidence >= 80 ? '✅' : '⚠️'} 整体置信度: ${params.confidence}% (${grade})
${uncertainties.length > 0 ? '❓ 遗留不确定性: ' + uncertainties.length + ' 项' : ''}
${alternatives.length > 0 ? '🔄 备选方案: ' + alternatives.length + ' 个' : ''}

---
💡 高阶思维小贴士：
真正的智慧不仅在于给出答案，更在于知道自己什么时候不知道。
        `.trim()
      }
    }
  })
  .addPrompt({
    name: 'chain-of-thought',
    description: '标准思维链工作流',
    arguments: [
      { name: 'problem', description: '要解决的复杂问题', required: true }
    ],
    generate: async (args?: Record<string, any>) => `
## 🧠 标准思维链工作流: ${args?.problem || '未知问题'}

### ⚙️ 系统指令
从现在开始，你必须**严格按照以下流程**进行思考，每一步都调用对应的工具来记录。

---

### 📌 第1步: 调用 \`start_thinking\`
参数:
- problem: "${args?.problem || ''}"
- context: "(补充你的背景知识)"

---

### 📌 第2-N步: 分细步思考，每步调用 \`add_thought\`

**要求:**
1. 每一个推理步骤都要单独调用
2. stepNumber 严格递增
3. 诚实评估置信度(0-100)，不要虚高
4. 明确写出本步依赖的假设
5. 如果发现错误，回溯到上一步重来

思维类型 type 说明:
- \`observation\`: 陈述已知事实
- \`reasoning\`: 逻辑推理步骤
- \`hypothesis\`: 提出假设
- \`verification\`: 验证/证伪假设
- \`conclusion\`: 得出子结论

---

### 📌 中间步骤: 调用 \`critical_review\` 自查
在得出最终结论前，必须进行一次批判性审查！

检查内容:
1. 逻辑有没有漏洞？
2. 隐含假设都显性化了吗？
3. 有没有考虑反例？
4. 有没有其他路径？

---

### 📌 最后一步: 调用 \`conclude_thinking\`
给出最终答案，并诚实说明:
- 整体置信度
- 还有哪些不确定性
- 有没有其他可能的答案

---
⚠️ **强制执行**: 不允许直接给出答案！必须走完以上完整流程。
⚠️ **慢思考**: 每一步只想清楚一件事，不要跳步！
    `.trim()
  })
  .build()
