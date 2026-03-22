import asyncio
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_tools.framework import (
    ToolDefinition,
    ToolResult,
    ToolStatus,
    MCPTool,
    MCPFramework,
)
from mcp_tools.tools import (
    CodeQualityCheckerTool,
    UnitTestGeneratorTool,
    APIDocGeneratorTool,
    RefactoringAssistantTool,
)
from network.communication import (
    Message,
    MessageType,
    ServiceStatus,
    ServiceEndpoint,
    InMemoryBroker,
    LoadBalancer,
    CircuitBreaker,
    ServiceRegistry,
    NetworkModule,
)


class TestMCPFramework(unittest.TestCase):
    def setUp(self):
        self.framework = MCPFramework()

    def test_register_tool(self):
        tool = CodeQualityCheckerTool()

        result = self.framework.register_tool(tool)

        self.assertTrue(result)
        self.assertEqual(len(self.framework.list_tools()), 1)

    def test_unregister_tool(self):
        tool = CodeQualityCheckerTool()
        self.framework.register_tool(tool)

        result = self.framework.unregister_tool("code_quality_checker")

        self.assertTrue(result)
        self.assertEqual(len(self.framework.list_tools()), 0)

    def test_get_tool(self):
        tool = CodeQualityCheckerTool()
        self.framework.register_tool(tool)

        retrieved = self.framework.get_tool("code_quality_checker")

        self.assertIsNotNone(retrieved)

    def test_list_tools_by_category(self):
        self.framework.register_tool(CodeQualityCheckerTool())
        self.framework.register_tool(UnitTestGeneratorTool())
        self.framework.register_tool(APIDocGeneratorTool())

        coding_tools = self.framework.list_tools(category="coding")

        self.assertGreaterEqual(len(coding_tools), 2)

    def test_execute_tool(self):
        self.framework.register_tool(CodeQualityCheckerTool())

        code = '''
def add(a, b):
    return a + b
'''
        result = asyncio.run(self.framework.execute_tool(
            "code_quality_checker",
            {"code": code, "language": "python"}
        ))

        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)

    def test_execute_nonexistent_tool(self):
        result = asyncio.run(self.framework.execute_tool(
            "nonexistent_tool",
            {}
        ))

        self.assertFalse(result.success)
        self.assertIn("not found", result.error)

    def test_execute_chain(self):
        self.framework.register_tool(CodeQualityCheckerTool())
        self.framework.register_tool(UnitTestGeneratorTool())

        chain = [
            ("code_quality_checker", {"code": "def test(): pass", "language": "python"}),
            ("test_generator", {"code": "def test(): pass", "language": "python"}),
        ]

        results = asyncio.run(self.framework.execute_chain(chain))

        self.assertEqual(len(results), 2)

    def test_framework_statistics(self):
        self.framework.register_tool(CodeQualityCheckerTool())

        asyncio.run(self.framework.execute_tool(
            "code_quality_checker",
            {"code": "x = 1", "language": "python"}
        ))

        stats = self.framework.get_statistics()

        self.assertIn("total_tools", stats)
        self.assertIn("total_executions", stats)


class TestCodeQualityCheckerTool(unittest.TestCase):
    def setUp(self):
        self.tool = CodeQualityCheckerTool()

    def test_definition(self):
        definition = self.tool.get_definition()

        self.assertEqual(definition.name, "code_quality_checker")
        self.assertIn("quality", definition.description.lower())

    def test_execute_with_clean_code(self):
        code = '''
def add(a, b):
    """Add two numbers."""
    return int(a) + int(b)
'''
        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python"
        }))

        self.assertTrue(result.success)
        self.assertGreater(result.data["quality_score"], 80)

    def test_execute_with_issues(self):
        code = '''
password = "hardcoded"
eval("print('dangerous')")
x=1
'''
        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python"
        }))

        self.assertTrue(result.success)
        self.assertGreaterEqual(result.data["summary"]["errors"], 1)


class TestUnitTestGeneratorTool(unittest.TestCase):
    def setUp(self):
        self.tool = UnitTestGeneratorTool()

    def test_generate_python_tests(self):
        code = '''
def add(a, b):
    return a + b

def multiply(x, y):
    return x * y
'''
        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python",
            "test_framework": "pytest"
        }))

        self.assertTrue(result.success)
        self.assertIn("test_code", result.data)
        self.assertIn("def test_add", result.data["test_code"])

    def test_generate_with_edge_cases(self):
        code = "def divide(a, b): return a / b"

        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python",
            "include_edge_cases": True
        }))

        self.assertTrue(result.success)
        self.assertIn("pytest.raises", result.data["test_code"])


class TestAPIDocGeneratorTool(unittest.TestCase):
    def setUp(self):
        self.tool = APIDocGeneratorTool()

    def test_generate_openapi_spec(self):
        code = '''
def get_user(user_id):
    return {"id": user_id}

def create_user(name, email):
    return {"id": 1, "name": name}
'''
        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python",
            "title": "User API",
            "version": "1.0.0"
        }))

        self.assertTrue(result.success)
        self.assertIn("openapi_spec", result.data)
        self.assertEqual(result.data["openapi_spec"]["info"]["title"], "User API")

    def test_generate_markdown(self):
        code = "def hello(): pass"

        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python"
        }))

        self.assertIn("markdown_doc", result.data)


class TestRefactoringAssistantTool(unittest.TestCase):
    def setUp(self):
        self.tool = RefactoringAssistantTool()

    def test_suggest_factory_pattern(self):
        code = '''
if isinstance(product, TypeA):
    return TypeAProduct()
elif isinstance(product, TypeB):
    return TypeBProduct()
elif isinstance(product, TypeC):
    return TypeCProduct()
'''
        result = asyncio.run(self.tool.execute({
            "code": code,
            "language": "python",
            "target_pattern": "factory"
        }))

        self.assertTrue(result.success)
        self.assertGreater(len(result.data["suggestions"]), 0)


class TestNetworkCommunication(unittest.TestCase):
    def setUp(self):
        self.broker = InMemoryBroker()

    def test_publish_subscribe(self):
        received = []

        async def handler(msg):
            received.append(msg)

        asyncio.run(self.broker.subscribe("test_channel", handler))
        message = Message(
            id="1",
            type=MessageType.REQUEST,
            source="test",
            target="test_channel",
            payload={"data": "test"}
        )

        asyncio.run(self.broker.publish("test_channel", message))

        asyncio.run(asyncio.sleep(0.1))

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].payload["data"], "test")

    def test_request_response(self):
        async def handler(msg):
            response = Message(
                id="resp_1",
                type=MessageType.RESPONSE,
                source="service",
                target="client",
                payload={"result": "processed"},
                correlation_id=msg.correlation_id
            )
            await self.broker.publish("client", response)

        asyncio.run(self.broker.subscribe("service", handler))

        result = asyncio.run(self.broker.request("service", {"data": "test"}, timeout=0.5))

        if result is not None:
            self.assertEqual(result.payload.get("result"), "processed")


class TestLoadBalancer(unittest.TestCase):
    def setUp(self):
        self.lb = LoadBalancer(strategy="round_robin")

    def test_select_from_healthy_endpoints(self):
        endpoints = [
            ServiceEndpoint("svc1", "host1", 8080, status=ServiceStatus.HEALTHY),
            ServiceEndpoint("svc2", "host2", 8080, status=ServiceStatus.HEALTHY),
        ]

        selected = asyncio.run(self.lb.select(endpoints))

        self.assertIsNotNone(selected)

    def test_ignore_unhealthy_endpoints(self):
        endpoints = [
            ServiceEndpoint("svc1", "host1", 8080, status=ServiceStatus.UNHEALTHY),
            ServiceEndpoint("svc2", "host2", 8080, status=ServiceStatus.HEALTHY),
        ]

        selected = asyncio.run(self.lb.select(endpoints))

        self.assertEqual(selected.host, "host2")


class TestCircuitBreaker(unittest.TestCase):
    def test_initial_state(self):
        cb = CircuitBreaker(failure_threshold=3)

        self.assertEqual(cb.state, "closed")
        self.assertTrue(asyncio.run(cb.can_execute()))

    def test_open_after_failures(self):
        cb = CircuitBreaker(failure_threshold=3)

        asyncio.run(cb.record_failure())
        asyncio.run(cb.record_failure())
        self.assertEqual(cb.state, "closed")

        asyncio.run(cb.record_failure())
        self.assertEqual(cb.state, "open")
        self.assertFalse(asyncio.run(cb.can_execute()))

    def test_recover_to_half_open(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

        asyncio.run(cb.record_failure())
        asyncio.run(cb.record_failure())

        import time
        time.sleep(0.15)

        can_exec = asyncio.run(cb.can_execute())

        self.assertTrue(can_exec)
        self.assertEqual(cb.state, "half_open")


class TestServiceRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ServiceRegistry()

    def test_register_endpoint(self):
        endpoint = ServiceEndpoint("test_service", "localhost", 8080)

        result = asyncio.run(self.registry.register(endpoint))

        self.assertTrue(result)

    def test_get_endpoints(self):
        endpoint = ServiceEndpoint("test_service", "localhost", 8080)
        asyncio.run(self.registry.register(endpoint))

        endpoints = asyncio.run(self.registry.get_endpoints("test_service"))

        self.assertEqual(len(endpoints), 1)

    def test_unregister(self):
        endpoint = ServiceEndpoint("test_service", "localhost", 8080)
        asyncio.run(self.registry.register(endpoint))

        result = asyncio.run(self.registry.unregister(endpoint))

        self.assertTrue(result)


class TestNetworkModule(unittest.TestCase):
    def setUp(self):
        self.module = NetworkModule()

    def test_register_service(self):
        endpoint = ServiceEndpoint("coding", "localhost", 8080)

        asyncio.run(self.module.register_service(endpoint))

        stats = asyncio.run(self.module.get_service_stats("coding"))

        self.assertIn("error_count", stats)


if __name__ == "__main__":
    unittest.main()
