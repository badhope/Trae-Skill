# 🧪 Unit Tests for Folder-as-Agent Platform
# Folder-as-Agent Platform v2.0
import unittest
import yaml
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAgentConfig(unittest.TestCase):
    """Test agent configuration"""
    
    def setUp(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agent.yaml')
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from YAML file"""
        config = {}
        with open(self.config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents = content.split('---')
            for doc in documents:
                if doc.strip():
                    doc_config = yaml.safe_load(doc)
                    if doc_config:
                        config.update(doc_config)
        return config
    
    def test_config_exists(self):
        """Test configuration file exists"""
        self.assertTrue(os.path.exists(self.config_path), "Config file should exist")
    
    def test_config_has_required_sections(self):
        """Test config has all required sections"""
        required_sections = ['name', 'role', 'version', 'description',
                            'executionFlow', 'expertEngines', 'metaAgents',
                            'routingStrategy', 'memorySystem', 'checklists',
                            'usageGuide', 'compatibility']
        for section in required_sections:
            self.assertIn(section, self.config, f"Config should have {section}")
    
    def test_execution_flow_complete(self):
        """Test execution flow has all 8 phases"""
        flow = self.config.get('executionFlow', {})
        required_steps = [
            'step1_intentRecognition',
            'step2_expertMatching',
            'step3_taskPlanning',
            'step4_expertExecution',
            'step5_toolCalling',
            'step6_resultIntegration',
            'step7_qualityCheck',
            'step8_finalOutput'
        ]
        for step in required_steps:
            self.assertIn(step, flow, f"Execution flow should have {step}")
    
    def test_expert_engines_valid(self):
        """Test expert engines configuration"""
        engines = self.config.get('expertEngines', [])
        self.assertIsInstance(engines, list, "expertEngines should be a list")
        self.assertGreater(len(engines), 0, "Should have at least one expert engine")
        
        for engine in engines:
            required_fields = ['id', 'name', 'description', 'keywords']
            for field in required_fields:
                self.assertIn(field, engine, f"Expert engine should have {field}")
            self.assertIsInstance(engine['keywords'], list, "keywords should be a list")
    
    def test_meta_agents_valid(self):
        """Test meta agents configuration"""
        agents = self.config.get('metaAgents', [])
        self.assertIsInstance(agents, list, "metaAgents should be a list")
        self.assertGreater(len(agents), 0, "Should have at least one meta agent")
        
        for agent in agents:
            required_fields = ['id', 'name', 'description', 'keywords']
            for field in required_fields:
                self.assertIn(field, agent, f"Meta agent should have {field}")
    
    def test_routing_rules_valid(self):
        """Test routing rules configuration"""
        routing = self.config.get('routingStrategy', {})
        self.assertIn('defaultEngine', routing, "routingStrategy should have defaultEngine")
        self.assertIn('routingRules', routing, "routingStrategy should have routingRules")
        
        rules = routing.get('routingRules', [])
        for rule in rules:
            required_fields = ['keywords', 'targetType', 'target']
            for field in required_fields:
                self.assertIn(field, rule, f"Routing rule should have {field}")
    
    def test_memory_system_enabled(self):
        """Test memory system is enabled"""
        memory = self.config.get('memorySystem', {})
        self.assertTrue(memory.get('enabled', False), "Memory system should be enabled")
    
    def test_checklists_complete(self):
        """Test checklists configuration"""
        checklists = self.config.get('checklists', {})
        required_checklists = ['inputCheck', 'executionCheck', 'outputCheck', 'qualityCheck']
        for checklist in required_checklists:
            self.assertIn(checklist, checklists, f"Should have {checklist}")
    
    def test_skill_files_exist(self):
        """Test all expert engine skill files exist"""
        engines = self.config.get('expertEngines', [])
        for engine in engines:
            skill_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'skills', 'engines', engine['id'], 'SKILL.md'
            )
            self.assertTrue(os.path.exists(skill_path), f"SKILL file missing for {engine['id']}")

class TestRoutingStrategy(unittest.TestCase):
    """Test routing strategy logic"""
    
    def test_keyword_matching(self):
        """Test keyword matching algorithm"""
        routing_rules = [
            {'keywords': ['topic', 'research question'], 'target': 'topic-expert'},
            {'keywords': ['literature', 'review'], 'target': 'literature-expert'},
            {'keywords': ['structure', 'outline'], 'target': 'structure-expert'},
        ]
        
        def match_rule(user_input, rules):
            """Simple keyword matching"""
            input_lower = user_input.lower()
            for rule in rules:
                for keyword in rule['keywords']:
                    if keyword.lower() in input_lower:
                        return rule['target']
            return 'default'
        
        self.assertEqual(match_rule('help me find a research topic', routing_rules), 'topic-expert')
        self.assertEqual(match_rule('write literature review', routing_rules), 'literature-expert')
        self.assertEqual(match_rule('create thesis outline', routing_rules), 'structure-expert')
        self.assertEqual(match_rule('hello world', routing_rules), 'default')
    
    def test_priority_matching(self):
        """Test priority-based matching"""
        rules_with_priority = [
            {'keywords': ['plan', 'workflow'], 'target': 'task-planner', 'priority': 10},
            {'keywords': ['topic'], 'target': 'topic-expert', 'priority': 5},
            {'keywords': ['writing'], 'target': 'writing-expert', 'priority': 3},
        ]
        
        def match_with_priority(user_input, rules):
            input_lower = user_input.lower()
            best_match = None
            best_priority = -1
            
            for rule in rules:
                for keyword in rule['keywords']:
                    if keyword.lower() in input_lower:
                        priority = rule.get('priority', 0)
                        if priority > best_priority:
                            best_priority = priority
                            best_match = rule['target']
            return best_match or 'default'
        
        self.assertEqual(match_with_priority('help me plan my thesis writing', rules_with_priority), 'task-planner')

class TestMemoryOperations(unittest.TestCase):
    """Test memory system operations"""
    
    def test_memory_store_retrieve(self):
        """Test basic store and retrieve operations"""
        memory_store = {}
        
        def store(key, value):
            memory_store[key] = value
        
        def retrieve(key):
            return memory_store.get(key, None)
        
        store('user_preference', 'academic')
        self.assertEqual(retrieve('user_preference'), 'academic')
        self.assertIsNone(retrieve('nonexistent'))
    
    def test_memory_search(self):
        """Test memory search functionality"""
        knowledge_base = [
            {'title': 'Machine Learning Basics', 'content': 'Introduction to ML', 'tags': ['ml', 'ai']},
            {'title': 'Deep Learning', 'content': 'Neural networks', 'tags': ['dl', 'nn']},
            {'title': 'Natural Language Processing', 'content': 'NLP techniques', 'tags': ['nlp', 'text']},
        ]
        
        def search_memory(query, store):
            results = []
            query_lower = query.lower()
            for item in store:
                if (query_lower in item['title'].lower() or
                    query_lower in item['content'].lower() or
                    any(query_lower in tag.lower() for tag in item['tags'])):
                    results.append(item)
            return results
        
        results = search_memory('learning', knowledge_base)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Machine Learning Basics')

class TestChecklists(unittest.TestCase):
    """Test verification checklists"""
    
    def test_input_verification(self):
        """Test input verification checklist"""
        checklist = [
            'Is user input clear and unambiguous?',
            'Do we need to ask user for more information?',
            'Are there any ambiguities that need clarification?'
        ]
        
        def verify_input(user_input):
            results = []
            results.append(len(user_input.strip()) > 0)
            results.append(len(user_input.strip()) > 10)
            results.append('?' not in user_input or user_input.count('?') <= 2)
            return all(results)
        
        self.assertTrue(verify_input('I need help writing a literature review for my computer science thesis'))
        self.assertFalse(verify_input(''))
        self.assertFalse(verify_input('Help?'))

class TestOutputFormatting(unittest.TestCase):
    """Test output formatting standards"""
    
    def test_markdown_formatting(self):
        """Test output follows markdown standards"""
        def is_valid_markdown(content):
            if not content:
                return False
            lines = content.split('\n')
            heading_count = sum(1 for line in lines if line.startswith('#'))
            return heading_count >= 1
        
        sample_output = """# Thesis Topic Suggestion

## Topic: Machine Learning Applications

### Research Question
What is the impact of ML on healthcare?"""
        
        self.assertTrue(is_valid_markdown(sample_output))
        self.assertFalse(is_valid_markdown('Just plain text'))

if __name__ == '__main__':
    unittest.main()
