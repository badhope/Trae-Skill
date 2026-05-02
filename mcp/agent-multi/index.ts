import { createMCPServer } from '../../packages/core/mcp/builder'

const AGENT_ROLES = {
  'product-manager': {
    name: '📦 Product Manager',
    expertise: 'Requirements, roadmap, user stories, prioritization',
    systemPrompt: `You are an expert Product Manager. Focus on:
- User-centric requirements and user stories
- Feature prioritization and roadmap
- Success metrics and acceptance criteria
- Risk assessment and mitigation
Always think in terms of business value and user impact.`
  },
  'tech-lead': {
    name: '👨‍💻 Tech Lead',
    expertise: 'Architecture, design patterns, technical decisions',
    systemPrompt: `You are a Senior Tech Lead / Architect. Focus on:
- System architecture and component design
- Design patterns and best practices
- Technology stack selection
- Performance and scalability concerns
- Technical debt management
Provide concrete technical direction and justify your decisions.`
  },
  'senior-developer': {
    name: '⚡ Senior Developer',
    expertise: 'Implementation, code quality, debugging',
    systemPrompt: `You are a Senior Full-Stack Developer. Focus on:
- Clean, maintainable code implementation
- Type safety and error handling
- Testing strategies
- Performance optimization
- Refactoring recommendations
Provide specific, actionable code examples and explanations.`
  },
  'devops-engineer': {
    name: '🚀 DevOps Engineer',
    expertise: 'Deployment, CI/CD, infrastructure',
    systemPrompt: `You are a DevOps and SRE expert. Focus on:
- CI/CD pipeline design
- Docker and containerization
- Kubernetes orchestration
- Monitoring and observability
- Cloud infrastructure best practices
Provide production-ready configuration examples.`
  },
  'qa-engineer': {
    name: '🔍 QA Engineer',
    expertise: 'Testing, quality assurance, edge cases',
    systemPrompt: `You are a meticulous QA Engineer. Focus on:
- Test strategy and test coverage
- Edge cases and boundary conditions
- Regression testing concerns
- User acceptance criteria validation
- Bug scenarios and reproduction steps
Be THOROUGH - find what others miss!`
  },
  'ux-designer': {
    name: '🎨 UX Designer',
    expertise: 'User experience, accessibility, design systems',
    systemPrompt: `You are an expert UX/UI Designer. Focus on:
- User flow and interaction design
- Accessibility (WCAG) compliance
- Design system consistency
- Mobile responsiveness
- Micro-interactions and delight
Think about the user's emotional journey and experience.`
  }
}

export default createMCPServer({
  name: 'multi-agent',
  version: '1.0.0',
  description: 'Multi-Agent Collaboration System - Expert panel for decision making',
  author: 'MCP Expert Community',
  icon: '👥'
})
  .addTool({
    name: 'list_agents',
    description: 'List all available expert agents and their expertise',
    parameters: {},
    execute: async () => {
      return {
        success: true,
        availableAgents: Object.entries(AGENT_ROLES).map(([id, agent]) => ({
          id,
          name: agent.name,
          expertise: agent.expertise
        })),
        recommendation: `
## 👥 Expert Panel Ready

**Suggested workflows:**

1. **Design Review**: Tech Lead + Senior Dev + UX Designer
2. **Launch Prep**: PM + DevOps + QA Engineer
3. **Feature Planning**: Product Manager + Tech Lead
4. **Full Stack Decision**: All 6 experts!
        `.trim()
      }
    }
  })
  .addTool({
    name: 'activate_agent',
    description: 'Activate a specific expert agent to provide input',
    parameters: {
      agentId: {
        type: 'string',
        description: 'Agent role ID',
        enum: Object.keys(AGENT_ROLES),
        required: true
      },
      topic: { type: 'string', description: 'Topic to discuss', required: true },
      context: { type: 'string', description: 'Background context', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const agent = AGENT_ROLES[params.agentId as keyof typeof AGENT_ROLES]
      return {
        success: true,
        agentActivated: agent.name,
        expertise: agent.expertise,
        agentPrompt: `
## ${agent.name} ACTIVATED

**Topic:** ${params.topic}

---

### 🎯 YOUR EXPERT PERSONA

${agent.systemPrompt}

---

### 📋 CONTEXT

${params.context}

---

### 📝 YOUR INPUT NEEDED

Provide your expert opinion on:
1. Key risks and concerns specific to ${agent.name.split(' ').slice(1).join(' ')}
2. Concrete recommendations
3. 3 follow-up questions that need clarification
4. Your confidence level in current approach (0-100%)

Format as structured, actionable advice.
        `.trim()
      }
    }
  })
  .addTool({
    name: 'debate_topic',
    description: 'Have multiple experts debate a topic - panel discussion',
    parameters: {
      topic: { type: 'string', description: 'Topic to debate', required: true },
      agentIds: { type: 'string', description: 'Agent IDs comma separated', required: true },
      currentProposal: { type: 'string', description: 'Current proposed solution', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const agentIds = params.agentIds.split(',')
      const agents = agentIds.map((id: string) => AGENT_ROLES[id.trim() as keyof typeof AGENT_ROLES]).filter(Boolean)
      return {
        success: true,
        panel: agents.map((a: any) => a.name),
        panelSize: agents.length,
        debateFramework: `
## 👥 EXPERT PANEL DEBATE

**Topic:** ${params.topic}

**Current Proposal:** ${params.currentProposal}

---

### 🎯 DEBATE FORMAT

EACH expert will speak in turn. For each expert:

1. **✅ AGREE** - Which parts of the proposal do you support?
2. **❌ CHALLENGE** - Which parts do you question?
3. **💡 PROPOSE** - What changes would you recommend?
4. **🎯 ASK** - One question for other panel members

---

### 🎭 EXPERT ROLES

${agents.map((a: any, i: number) => `**${i + 1}. ${a.name}**
   Expertise: ${a.expertise}`).join('\n\n')}

---

### ⚖️ FACILITATOR INSTRUCTIONS

After all experts speak:
1. Summarize points of AGREEMENT
2. Highlight points of CONTENTION
3. Call for consensus or recommend additional research

💡 Remember: Good decisions come from DISAGREEMENT! Healthy debate = better outcomes.
        `.trim()
      }
    }
  })
  .addTool({
    name: 'synthesize_decision',
    description: 'Synthesize panel input into a decision record',
    parameters: {
      topic: { type: 'string', description: 'Decision topic', required: true },
      allExpertInputs: { type: 'string', description: 'All expert inputs combined', required: true },
      optionsConsidered: { type: 'string', description: 'Options considered (comma separated)', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const options = params.optionsConsidered.split(',')
      return {
        success: true,
        decisionRecordReady: true,
        synthesisTemplate: `
## 📋 DECISION RECORD

**Decision Topic:** ${params.topic}
**Date:** ${new Date().toISOString().split('T')[0]}

---

### 🎛️ OPTIONS CONSIDERED

${options.map((o: string, i: number) => `${i + 1}. ${o.trim()}`).join('\n')}

---

### 📊 EXPERT INPUT SYNTHESIS

**Based on ALL expert input:**

**✅ AREAS OF AGREEMENT:**
(Extract points ALL experts supported)

**⚠️ AREAS OF CONCERN:**
(Extract risks experts identified)

**💡 KEY RECOMMENDATIONS:**
(Extract highest-confidence advice)

---

### 🎯 FINAL DECISION

> [State clear, actionable decision here]

---

### 📝 JUSTIFICATION

1. Why this decision was made
2. What trade-offs were accepted
3. How concerns will be mitigated

---

### 🔄 NEXT STEPS

1. [First action item]
2. [Second action item]
3. Decision review date: [Date]

---

💡 **Decision Quality Check:**
- Did we consider dissenting opinions?
- Were all legitimate concerns mitigated?
- Is the decision reversible?
- Is the implementation path clear?
        `.trim()
      }
    }
  })
  .addPrompt({
    name: 'expert-consultation',
    description: 'Full expert panel consultation workflow',
    arguments: [
      { name: 'decisionTopic', description: 'The decision to be made', required: true }
    ],
    generate: async (args?: Record<string, any>) => `
## 👥 MULTI-AGENT CONSULTATION ACTIVATED

We will now make high-quality decisions using expert panel input.

---

### 🎯 DECISION TOPIC:

> ${args?.decisionTopic || 'User did not specify decision topic'}

---

### ⚙️ CONSULTATION WORKFLOW

**Step 1: ASSEMBLE THE PANEL**
Call \`list_agents\` and select 3-5 relevant experts for this decision.

**Step 2: HEAR FROM EACH EXPERT**
For each selected expert:
- Call \`activate_agent\` with full context
- Record their input, concerns, and recommendations

**Step 3: OPTIONAL PANEL DEBATE**
For controversial decisions, call \`debate_topic\` to have experts respond to each other.

**Step 4: SYNTHESIZE AND DECIDE**
Call \`synthesize_decision\` to create formal decision record.

---

### ❌ RULES FOR GOOD DECISION MAKING

1. **DO NOT SKIP** any expert input
2. **DO NOT IGNORE** concerns - address them explicitly
3. **DO NOT RUSH** - quality > speed
4. **DISSENT IS GOOD** - we want to hear disagreements
5. **BE EXPLICIT** about trade-offs accepted

No expert is ever 100% wrong. No expert is ever 100% right.
    `.trim()
  })
  .build()
