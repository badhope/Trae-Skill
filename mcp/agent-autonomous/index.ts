import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

interface Task {
  id: string
  title: string
  description: string
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  priority: number
  dependencies: string[]
  result?: string
  createdAt: number
  completedAt?: number
}

interface AgentState {
  objective: string
  tasks: Task[]
  iteration: number
  maxIterations: number
  isRunning: boolean
  completedTasks: string[]
  failedTasks: string[]
}

function generateTaskId(): string {
  return 'task_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 6)
}

export default createMCPServer({
  name: 'autonomous-agent',
  version: '1.0.0',
  description: 'AutoGPT-style autonomous agent - BabyAGI inspired task loop',
  author: 'Trae Professional',
  icon: '🤖'
})
  .addTool({
    name: 'initialize_objective',
    description: 'Initialize autonomous agent with main objective - Start BabyAGI loop',
    parameters: {
      objective: { type: 'string', description: 'The main goal to achieve', required: true },
      maxIterations: { type: 'number', description: 'Maximum iterations default 20', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const maxIter = params.maxIterations || 20
      const initialTasks: Task[] = [
        {
          id: generateTaskId(),
          title: 'Analyze objective and create task breakdown',
          description: `Analyze: "${params.objective}". Break into 3-5 specific, actionable subtasks.`,
          status: 'pending',
          priority: 10,
          dependencies: [],
          createdAt: Date.now()
        }
      ]
      const state: AgentState = {
        objective: params.objective,
        tasks: initialTasks,
        iteration: 0,
        maxIterations: maxIter,
        isRunning: true,
        completedTasks: [],
        failedTasks: []
      }
      return {
        success: true,
        agentStarted: true,
        state,
        nextStep: `
## 🤖 Autonomous Agent Initialized

**🎯 Objective:** ${params.objective}

**📋 Execute the following workflow repeatedly:**

1. 🔍 Select highest priority READY task (no uncompleted dependencies)
2. ⚡ Execute this task thoroughly
3. ✅ Call complete_task with result
4. 🧠 Call process_task_result to generate new tasks
5. 🔄 Repeat until objective is achieved

⚠️ Stop condition: ${maxIter} iterations OR objective achieved OR no meaningful progress
        `.trim()
      }
    }
  })
  .addTool({
    name: 'generate_next_tasks',
    description: 'Generate new tasks based on completed task result - BabyAGI task creation',
    parameters: {
      objective: { type: 'string', description: 'Main objective', required: true },
      completedTaskResult: { type: 'string', description: 'Result from previous task', required: true },
      currentTaskList: { type: 'string', description: 'JSON string of current tasks array', required: true }
    },
    execute: async (params: Record<string, any>) => {
      let tasks: Task[] = []
      try {
        tasks = JSON.parse(params.currentTaskList)
      } catch (e) {}
      return {
        success: true,
        taskCreation: 'BabyAGI Task Generator',
        prompt: `
## 🧠 Task Generation Engine

Based on:
**Objective:** ${params.objective}
**Previous Result:** ${params.completedTaskResult}

**Generate 2-4 NEW tasks following these rules:**
1. Each task MUST move us closer to the final objective
2. Tasks should be SPECIFIC and ACTIONABLE
3. Avoid duplicating existing tasks:
${tasks.map((t: Task) => `- ${t.title}`).join('\\n')}

**For each new task provide:**
- TITLE: Short, action-oriented title
- DESCRIPTION: Detailed execution instructions
- PRIORITY: 1-10 (10 highest)
- DEPENDENCIES: Array of task IDs (if any)

⚠️ IMPORTANT: Stop generating when objective is clearly achieved!
        `.trim(),
        recommendation: 'Prioritize tasks that remove blockers and provide critical information first'
      }
    }
  })
  .addTool({
    name: 'reprioritize_tasks',
    description: 'Re-prioritize task queue - BabyAGI prioritization agent',
    parameters: {
      objective: { type: 'string', description: 'Main objective', required: true },
      taskListJson: { type: 'string', description: 'JSON array of all tasks', required: true }
    },
    execute: async (params: Record<string, any>) => {
      let tasks: Task[] = []
      try {
        tasks = JSON.parse(params.taskListJson)
      } catch (e) {}
      const pending = tasks.filter(t => t.status === 'pending')
      const inProgress = tasks.filter(t => t.status === 'in_progress')
      const completed = tasks.filter(t => t.status === 'completed')
      return {
        success: true,
        prioritizationComplete: true,
        summary: {
          total: tasks.length,
          pending: pending.length,
          inProgress: inProgress.length,
          completed: completed.length,
          progress: Math.round((completed.length / Math.max(1, tasks.length)) * 100) + '%'
        },
        nextTask: pending.sort((a, b) => b.priority - a.priority)[0],
        prioritizationFramework: `
## 📊 Priority Framework

Rank tasks by:
1. 🎯 **Objective Alignment** - Does this directly achieve our goal: "${params.objective}"?
2. ⛓️ **Dependency Impact** - How many other tasks depend on this?
3. ⚡ **Information Value** - Does this unlock unknowns?
4. 🚀 **Quick Wins** - Can this be completed in 1 step?

**Current pending tasks by priority:**
${pending.sort((a, b) => b.priority - a.priority).map((t, i) => `${i + 1}. [${t.priority}] ${t.title}`).join('\\n')}
        `.trim()
      }
    }
  })
  .addTool({
    name: 'complete_task',
    description: 'Mark task as completed with result',
    parameters: {
      taskId: { type: 'string', description: 'Task ID', required: true },
      result: { type: 'string', description: 'Execution result', required: true }
    },
    execute: async (params: Record<string, any>) => {
      return {
        success: true,
        taskCompleted: true,
        taskId: params.taskId,
        resultSummary: params.result.slice(0, 500),
        nextAction: `
Now call:
1. **reprioritize_tasks** - Update remaining task priorities
2. **generate_next_tasks** - Create follow-up tasks
3. Select the next highest priority task and execute!
        `.trim()
      }
    }
  })
  .addTool({
    name: 'check_objective_achieved',
    description: 'Evaluate if objective is complete - termination condition',
    parameters: {
      objective: { type: 'string', description: 'Original objective', required: true },
      allResults: { type: 'string', description: 'All completed task results', required: true },
      iteration: { type: 'number', description: 'Current iteration number', required: true },
      maxIterations: { type: 'number', description: 'Maximum iterations', required: true }
    },
    execute: async (params: Record<string, any>) => {
      const progress = Math.min(100, Math.round((params.iteration / params.maxIterations) * 100))
      const shouldContinue = params.iteration < params.maxIterations
      return {
        success: true,
        iteration: params.iteration,
        maxIterations: params.maxIterations,
        budgetRemaining: (params.maxIterations - params.iteration) + ' iterations',
        progress: progress + '%',
        shouldContinue,
        evaluationPrompt: `
## 🎯 Objective Achievement Evaluation

**Objective:** ${params.objective}

**Iteration ${params.iteration}/${params.maxIterations}**

Evaluate:
1. ✅ Has the objective been FULLY achieved based on results?
2. 📋 Is there any remaining work to do?
3. 🔄 Would additional iterations produce SIGNIFICANT improvements?

**Results to evaluate:**
${params.allResults.slice(0, 2000)}

---
${shouldContinue ? '✅ Continue execution loop' : '⚠️ Max iterations reached - summarize and exit'}
        `.trim()
      }
    }
  })
  .addPrompt({
    name: 'autogpt-executor',
    description: 'Full AutoGPT autonomous execution loop',
    arguments: [
      { name: 'objective', description: 'Your main goal to achieve', required: true }
    ],
    generate: async (args?: Record<string, any>) => `
## 🤖 AUTOGPT MODE ACTIVATED

I am now an **autonomous agent**. I will work without intervention until:
- Objective is achieved
- Max iterations reached
- I detect I'm stuck in a loop

---

### ⚙️ EXECUTION LOOP

I WILL FOLLOW THIS LOOP **EXACTLY**, STEP BY STEP:

1. **🔍 THINK** - What should I do right now?
2. **⚡ EXECUTE** - Call the necessary tools to complete the task
3. **✅ RECORD** - Call complete_task with result
4. **🧠 ADAPT** - Call generate_next_tasks to create follow-ups
5. **📋 REPRIORITIZE** - Call reprioritize_tasks and select highest priority
6. **🔁 REPEAT** - Go back to step 1

---

### 🚀 STARTING OBJECTIVE

> ${args?.objective || 'User did not specify objective'}

---

### ❌ STRICT RULES I WILL FOLLOW

1. **NO DIRECT ANSWERS** - EVERY action goes through this tool system
2. **ONE TASK AT A TIME** - I will NOT skip steps or batch process
3. **HONEST PROGRESS** - I will track iteration count and terminate properly
4. **FULL AUTONOMY** - I will NOT ask for user input during execution
5. **RESOURCEFUL** - I will use ANY tools available to me in this environment

---

▶️ **INITIALIZATION COMPLETE - STARTING AUTONOMOUS MODE**
    `.trim()
  })
  .build()
