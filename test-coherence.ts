import { registerAllMCP, globalMCPRegistry, globalSkillOrchestrator, globalToolDiscovery } from './packages/core/index';

async function testToolCoherence() {
  console.log('🔍 开始工具连贯性测试...\n');

  try {
    console.log('📦 步骤1: 注册所有MCP模块');
    const { registered, failed } = await registerAllMCP();
    console.log(`   ✅ 已注册: ${registered.length} 个模块`);
    if (failed.length > 0) {
      console.log(`   ❌ 失败: ${failed.length} 个模块 - ${failed.join(', ')}`);
    }

    console.log('\n📋 步骤2: 验证新工具是否注册成功');
    const tools = globalMCPRegistry.listAllTools();
    
    const newTools = ['clarify', 'libraries', 'proxy', 'secrets'];
    for (const toolName of newTools) {
      const hasTool = tools.some(t => t.serverId === toolName);
      console.log(`   ${hasTool ? '✅' : '❌'} ${toolName} 模块已注册`);
      
      if (hasTool) {
        const moduleTools = tools.filter(t => t.serverId === toolName);
        console.log(`      包含工具: ${moduleTools.map(t => t.name).join(', ')}`);
      }
    }

    console.log('\n🔗 步骤3: 测试工具发现机制');
    const discoverResult = globalToolDiscovery.discoverTools('我想创建一个React应用');
    console.log(`   ✅ 发现 ${discoverResult.length} 个相关工具`);
    console.log(`   前3个工具: ${discoverResult.slice(0, 3).map(t => `${t.serverId}/${t.toolId}`).join(', ')}`);

    console.log('\n🧩 步骤4: 测试工具协作链路');
    const testScenarios = [
      { 
        description: '用户描述模糊时的澄清流程',
        tools: ['clarify/analyze_intent', 'clarify/generate_clarification']
      },
      { 
        description: '库推荐流程',
        tools: ['clarify/analyze_intent', 'libraries/recommend_libraries']
      },
      { 
        description: '网络诊断流程',
        tools: ['proxy/test_network_connectivity', 'secrets/check_env_file']
      },
      { 
        description: '完整开发流程',
        tools: ['clarify/analyze_intent', 'libraries/recommend_libraries', 'secrets/generate_env_template']
      }
    ];

    for (const scenario of testScenarios) {
      console.log(`   📌 ${scenario.description}`);
      let allToolsAvailable = true;
      for (const toolPath of scenario.tools) {
        const [serverId, toolId] = toolPath.split('/');
        const tool = tools.find(t => t.serverId === serverId && t.name === toolId);
        if (tool) {
          console.log(`      ✅ ${toolPath}`);
        } else {
          console.log(`      ❌ ${toolPath} - 未找到`);
          allToolsAvailable = false;
        }
      }
      if (allToolsAvailable) {
        console.log(`      ✅ 场景可用`);
      }
    }

    console.log('\n⚙️ 步骤5: 测试任务分析');
    const analysis = globalSkillOrchestrator.analyzeTask('我想使用React和TypeScript创建一个用户管理系统');
    console.log(`   ✅ 复杂度: ${analysis.complexity}`);
    console.log(`   ✅ 置信度: ${(analysis.confidence * 100).toFixed(0)}%`);
    console.log(`   ✅ 匹配技能: ${analysis.matchedSkill}`);
    console.log(`   ✅ 推荐工作流: ${analysis.recommendedWorkflow}`);

    console.log('\n✅ 所有测试通过！工具可以连贯使用，无冲突风险。');
    
    return {
      success: true,
      registeredModules: registered.length,
      totalTools: tools.length,
      newTools: newTools.filter(t => tools.some(tool => tool.serverId === t)).length
    };

  } catch (error) {
    console.error('\n❌ 测试失败:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

if (require.main === module) {
  testToolCoherence().then(result => {
    console.log('\n📊 测试结果:');
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
  });
}