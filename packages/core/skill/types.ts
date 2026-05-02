export interface SkillTrigger {
  keywords: string[];
  patterns: string[];
  conditions: string[];
}

export interface SkillMetrics {
  avg_execution_time: string;
  success_rate: number;
  token_efficiency: number;
  complexity_accuracy?: number;
}

export interface SkillMetadata {
  name: string;
  description: string;
  version: string;
  layer: 'meta' | 'engine' | 'workflow' | 'action';
  role: string;
  invokes: string[];
  invoked_by: string[];
  capabilities: string[];
  triggers: SkillTrigger;
  metrics?: SkillMetrics;
}

export interface WorkflowStep {
  id: string;
  description: string;
  type?: 'action' | 'tool' | 'invoke' | 'workflow' | 'loop' | 'conditional' | 'wait' | 'end';
  skill?: string;
  tool?: string;
  workflow?: string;
  loopCount?: number;
  condition?: string;
  params?: Record<string, any>;
  estimatedTime?: string;
  dependencies: string[];
  priority: 'low' | 'medium' | 'high' | 'critical';
  parallel?: boolean;
  waitDuration?: number;
  retries?: number;
  timeout?: number;
}

export interface WorkflowPhase {
  id: string;
  name: string;
  description?: string;
  tasks: WorkflowStep[];
}

export interface Workflow {
  id: string;
  name: string;
  description: string;
  phases: WorkflowPhase[];
}

export interface DecisionNode {
  id: string;
  question: string;
  yes?: string;
  no?: string;
  default?: string;
  children?: DecisionNode[];
}

export interface DecisionTree {
  id: string;
  name: string;
  root: DecisionNode;
}

export interface ToolReference {
  name: string;
  purpose: string;
  fallback: string;
}

export interface SkillDefinition {
  metadata: SkillMetadata;
  content: string;
  workflows: Workflow[];
  decisionTrees: DecisionTree[];
  tools: ToolReference[];
  examples: string[];
  constraints: Record<string, any>;
}

export interface TaskAnalysis {
  complexity: number;
  factors: string[];
  estimatedTime: string;
  confidence: number;
  matchedSkill: string;
  recommendedWorkflow: string;
}

export interface TaskContext {
  id: string;
  description: string;
  complexity: number;
  currentSkill: string;
  history: TaskStep[];
  results: Record<string, any>;
}

export interface TaskStep {
  skillName: string;
  input: any;
  output: any;
  timestamp: Date;
  status: 'success' | 'failed' | 'pending';
}

export interface TaskResult {
  success: boolean;
  data?: any;
  error?: string;
  steps: TaskStep[];
}