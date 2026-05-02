export * from './types';
export { SkillLoader } from './loader';
export { SkillRegistry } from './registry';
export { SkillOrchestrator } from './orchestrator';
export { ToolDiscoveryEngine, ToolMatch, ToolRecommendation } from './toolDiscovery';
export { ToolExecutor, ToolExecutionResult, globalToolExecutor } from './toolExecutor';
export { WorkflowEngine, WorkflowExecutionConfig } from './workflowEngine';
export { ErrorHandler, ErrorRecovery, ErrorRecord, ErrorType, SafeErrorResponse, globalErrorHandler } from './errorHandler';
export { Monitor, Metric, PerformanceReport, OperationLog, globalMonitor } from './monitor';
export { AgentRunner, AgentConfig, AgentResponse } from './agentRunner';
export { TaskStateManager, TaskState, TaskHistoryEntry, ResumeResult, globalTaskStateManager } from './taskStateManager';
export { AgentMemory, Interaction, MemorySearchResult, MemorySummary, InvertedIndexEntry, globalAgentMemory } from './agentMemory';
export { SkillVersionManager, SkillVersion, VersionDiff, Change, VersionHistory, globalVersionManager } from './versionManager';
export { SkillCache, ExecutionCache, ResultReuseManager, CacheEntry, CacheStats, ExecutionCacheKey, ExecutionCacheEntry, globalResultReuseManager, globalSkillCache, globalExecutionCache } from './performanceOptimizer';
export { HumanInTheLoopManager, ConfirmationRequest, ConfirmationType, ConfirmationOption, ConfirmationResponse, globalHumanInTheLoopManager } from './humanInTheLoop';
export { TaskVisualizationManager, TaskProgress, PhaseProgress, TaskStepProgress, WorkflowVisualization, GraphNode, VisualizationSummary, globalTaskVisualizationManager } from './taskVisualization';
export { PermissionManager, Role, Permission, User, PermissionCheck, globalPermissionManager, requirePermission, requireAllPermissions } from './permissionManager';
export { ConcurrencyManager, ConcurrencyLimit, RateLimit, TaskSlot, globalConcurrencyManager } from './concurrencyManager';

import { SkillLoader } from './loader';
import { SkillRegistry } from './registry';
import { SkillOrchestrator } from './orchestrator';
import { ToolDiscoveryEngine } from './toolDiscovery';
import { globalToolExecutor } from './toolExecutor';
import { WorkflowEngine } from './workflowEngine';
import { globalErrorHandler } from './errorHandler';
import { globalMonitor } from './monitor';
import { AgentRunner } from './agentRunner';

export const globalSkillRegistry = new SkillRegistry();
export const globalSkillLoader = new SkillLoader();
export const globalSkillOrchestrator = new SkillOrchestrator(globalSkillRegistry);
export const globalToolDiscovery = new ToolDiscoveryEngine(globalSkillRegistry);
export const globalWorkflowEngine = new WorkflowEngine(globalSkillRegistry);
export const globalAgentRunner = new AgentRunner(globalSkillRegistry);

export async function loadSkillsFromDirectory(dirPath: string): Promise<{
  loaded: number;
  failed: number;
}> {
  const skills = await globalSkillLoader.loadFromSkillDir(dirPath);
  let failed = 0;

  for (const skill of skills) {
    try {
      globalSkillRegistry.registerSkill(skill);
    } catch {
      failed++;
    }
  }

  return {
    loaded: skills.length - failed,
    failed
  };
}

export async function executeSkill(taskDescription: string): Promise<any> {
  const agentRunner = new AgentRunner(globalSkillRegistry);
  return agentRunner.run(taskDescription);
}

export function findSkills(taskDescription: string) {
  return globalSkillRegistry.matchSkills(taskDescription);
}

export function discoverTools(taskDescription: string) {
  return globalToolDiscovery.discoverTools(taskDescription);
}

export function getAgentRunner(): AgentRunner {
  return globalAgentRunner;
}

export async function diagnoseTask(taskDescription: string): Promise<any> {
  return globalAgentRunner.diagnose(taskDescription);
}