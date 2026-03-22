import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from coding_engine.analyzer import (
    Language,
    CodeSnippet,
    SyntaxError,
    CodeAnalysis,
    SyntaxAnalyzer,
    AutoCompletionEngine,
)
from coding_engine.algorithms import (
    SortingAlgorithms,
    SearchAlgorithms,
    DynamicProgramming,
    AlgorithmLibrary,
)
from coding_engine.patterns import (
    PatternLibrary,
    Singleton,
    FactoryMethod,
    Observer,
    Strategy,
)
from coding_engine.quality import (
    PatternDetector,
    CodeOptimizer,
    DebugAssistant,
    CodeQualityChecker,
)


class TestSyntaxAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = SyntaxAnalyzer()

    def test_python_valid_code(self):
        code = '''
def hello(name):
    """Say hello to someone."""
    return f"Hello, {name}!"

result = hello("World")
'''
        result = self.analyzer.analyze(code, Language.PYTHON)

        self.assertTrue(result.is_valid_syntax)
        self.assertEqual(len(result.errors), 0)

    def test_python_metrics(self):
        code = '''
def add(a, b):
    return a + b

class Calculator:
    pass
'''
        result = self.analyzer.analyze(code, Language.PYTHON)

        self.assertEqual(result.metrics["function_count"], 1)
        self.assertEqual(result.metrics["class_count"], 1)

    def test_js_brace_matching(self):
        code = '''
function test() {
    if (true) {
        console.log("test");
    }
}
'''
        result = self.analyzer.analyze(code, Language.JAVASCRIPT)

        self.assertTrue(result.is_valid_syntax)

    def test_basic_metrics(self):
        code = "line1\nline2\nline3\n\n# comment\n\nline6"

        result = self.analyzer.analyze(code, Language.PYTHON)

        self.assertGreater(result.metrics["total_lines"], 0)
        self.assertGreater(result.metrics["code_lines"], 0)


class TestAutoCompletion(unittest.TestCase):
    def setUp(self):
        self.completer = AutoCompletionEngine()

    def test_python_class_completion(self):
        completion = self.completer.generate_completion(
            template_type="class",
            language=Language.PYTHON,
            name="MyClass",
            params="self, value",
            body="self.value = value"
        )

        self.assertIn("class MyClass", completion)
        self.assertIn("def __init__", completion)

    def test_python_function_completion(self):
        completion = self.completer.generate_completion(
            template_type="function",
            language=Language.PYTHON,
            name="calculate",
            params="x, y",
            body="return x + y"
        )

        self.assertIn("def calculate", completion)
        self.assertIn("x, y", completion)

    def test_js_class_completion(self):
        completion = self.completer.generate_completion(
            template_type="class",
            language=Language.JAVASCRIPT,
            name="MyClass",
            params="value",
            body="this.value = value"
        )

        self.assertIn("class MyClass", completion)
        self.assertIn("constructor", completion)


class TestSortingAlgorithms(unittest.TestCase):
    def test_quicksort(self):
        arr = [3, 6, 8, 10, 1, 2, 1]
        result = SortingAlgorithms.quicksort(arr)

        self.assertEqual(result, [1, 1, 2, 3, 6, 8, 10])

    def test_mergesort(self):
        arr = [38, 27, 43, 3, 9, 82, 10]
        result = SortingAlgorithms.mergesort(arr)

        self.assertEqual(result, [3, 9, 10, 27, 38, 43, 82])

    def test_heapsort(self):
        arr = [5, 3, 8, 4, 2, 6, 1]
        result = SortingAlgorithms.heapsort(arr.copy())

        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 8])

    def test_bubblesort(self):
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = SortingAlgorithms.bubblesort(arr.copy())

        self.assertEqual(result, [11, 12, 22, 25, 34, 64, 90])

    def test_sorts_empty_and_single(self):
        arr_empty = []
        self.assertEqual(SortingAlgorithms.quicksort(arr_empty), [])
        self.assertEqual(SortingAlgorithms.mergesort(arr_empty), [])

        arr_single = [42]
        self.assertEqual(SortingAlgorithms.quicksort(arr_single.copy()), [42])


class TestSearchAlgorithms(unittest.TestCase):
    def test_binary_search_found(self):
        arr = [1, 3, 5, 7, 9, 11]
        result = SearchAlgorithms.binary_search(arr, 7)

        self.assertEqual(result, 3)

    def test_binary_search_not_found(self):
        arr = [1, 3, 5, 7, 9, 11]
        result = SearchAlgorithms.binary_search(arr, 6)

        self.assertEqual(result, -1)

    def test_bfs(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }

        result = SearchAlgorithms.bfs(graph, 'A')

        self.assertEqual(result[0], 'A')
        self.assertIn('B', result)
        self.assertIn('C', result)

    def test_dfs(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }

        result = SearchAlgorithms.dfs(graph, 'A')

        self.assertEqual(result[0], 'A')

    def test_dijkstra(self):
        graph = {
            'A': [('B', 1), ('C', 4)],
            'B': [('C', 2), ('D', 5)],
            'C': [('D', 1)],
            'D': []
        }

        distances = SearchAlgorithms.dijkstra(graph, 'A')

        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 1)
        self.assertEqual(distances['C'], 3)


class TestDynamicProgramming(unittest.TestCase):
    def test_fibonacci(self):
        self.assertEqual(DynamicProgramming.fibonacci(0), 0)
        self.assertEqual(DynamicProgramming.fibonacci(1), 1)
        self.assertEqual(DynamicProgramming.fibonacci(10), 55)

    def test_fibonacci_memo(self):
        result = DynamicProgramming.fibonacci_memo(10)
        self.assertEqual(result, 55)

    def test_knapsack(self):
        values = [60, 100, 120]
        weights = [10, 20, 30]
        capacity = 50

        result = DynamicProgramming.knapsack(values, weights, capacity)

        self.assertEqual(result, 220)

    def test_lcs(self):
        s1 = "AGGTAB"
        s2 = "GXTXAYB"

        result = DynamicProgramming.longest_common_subsequence(s1, s2)

        self.assertEqual(result, 4)

    def test_edit_distance(self):
        s1 = "kitten"
        s2 = "sitting"

        result = DynamicProgramming.edit_distance(s1, s2)

        self.assertEqual(result, 3)


class TestAlgorithmLibrary(unittest.TestCase):
    def setUp(self):
        self.library = AlgorithmLibrary()

    def test_get_algorithm(self):
        algo = self.library.get_algorithm("quicksort")
        self.assertIsNotNone(algo)

        result = algo([3, 1, 2])
        self.assertEqual(result, [1, 2, 3])

    def test_list_algorithms(self):
        algorithms = self.library.list_algorithms()

        self.assertIsInstance(algorithms, list)
        self.assertGreater(len(algorithms), 0)


class TestDesignPatterns(unittest.TestCase):
    def test_singleton(self):
        singleton = Singleton()
        info = singleton.get_info()

        self.assertEqual(info.name, "Singleton")
        self.assertEqual(info.category, "Creational")

        code = singleton.generate_code(class_name="ConfigManager")
        self.assertIn("class ConfigManager", code)

    def test_factory_method(self):
        factory = FactoryMethod()
        code = factory.generate_code(product_name="Product", num_products=3)

        self.assertIn("class Product", code)
        self.assertIn("ConcreteProduct1", code)

    def test_observer(self):
        observer = Observer()
        info = observer.get_info()

        self.assertEqual(info.name, "Observer")
        self.assertEqual(info.category, "Behavioral")

    def test_strategy(self):
        strategy = Strategy()
        code = strategy.generate_code(
            context_name="Context",
            strategies=["QuickSort", "MergeSort"]
        )

        self.assertIn("Context", code)


class TestPatternLibrary(unittest.TestCase):
    def setUp(self):
        self.library = PatternLibrary()

    def test_get_pattern(self):
        pattern = self.library.get_pattern("singleton")

        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.get_info().name, "Singleton")

    def test_list_patterns(self):
        patterns = self.library.list_patterns()

        self.assertGreater(len(patterns), 0)

    def test_list_by_category(self):
        creational = self.library.list_by_category("Creational")

        for p in creational:
            self.assertEqual(p.category, "Creational")

    def test_generate_pattern(self):
        code = self.library.generate("singleton", class_name="Logger")

        self.assertIn("class Logger", code)


class TestPatternDetector(unittest.TestCase):
    def setUp(self):
        self.detector = PatternDetector()

    def test_detect_list_comprehension(self):
        code = '''
result = []
for item in items:
    result.append(item * 2)
'''
        issues = self.detector.detect(code)

        self.assertGreater(len(issues), 0)

    def test_detect_hardcoded_password(self):
        code = 'password = "secret123"'

        issues = self.detector.detect(code)

        self.assertTrue(any(i.category.value == "security" for i in issues))

    def test_detect_sql_injection(self):
        code = 'cursor.execute("SELECT * FROM users WHERE id=%s" % user_id)'

        issues = self.detector.detect(code)

        self.assertTrue(any(i.category.value == "security" for i in issues))


class TestCodeOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = CodeOptimizer()

    def test_optimize_list_comprehension(self):
        code = '''
result = []
for item in items:
    result.append(item * 2)
'''
        result = self.optimizer.optimize(code, "python")

        self.assertIn("for item in items", result.optimized_code)

    def test_estimate_speedup(self):
        improvements = ["list comprehension optimization", "enumerate optimization"]
        speedup = self.optimizer._estimate_speedup(improvements)

        self.assertGreater(speedup, 1.0)


class TestDebugAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = DebugAssistant()

    def test_analyze_name_error(self):
        error = "NameError: name 'undefined_var' is not defined"

        result = self.assistant.analyze_error(error)

        self.assertEqual(result["error_type"], "NameError")
        self.assertIn("variable", result["analysis"].lower())

    def test_analyze_syntax_error(self):
        error = "SyntaxError: invalid syntax"

        result = self.assistant.analyze_error(error)

        self.assertEqual(result["error_type"], "SyntaxError")

    def test_analyze_index_error(self):
        error = "IndexError: list index out of range"

        result = self.assistant.analyze_error(error)

        self.assertEqual(result["error_type"], "IndexError")


class TestCodeQualityChecker(unittest.TestCase):
    def setUp(self):
        self.checker = CodeQualityChecker()

    def test_quality_check(self):
        code = '''
def add(a, b):
    return a + b
'''
        result = self.checker.check_quality(code, "python")

        self.assertIn("quality_score", result)
        self.assertIn("issues", result)
        self.assertIn("grade", result)

    def test_quality_grade(self):
        code_good = '''
def add(a, b):
    """Add two numbers."""
    return int(a) + int(b)
'''

        code_bad = "def add(a,b):return a+b"

        result_good = self.checker.check_quality(code_good, "python")
        result_bad = self.checker.check_quality(code_bad, "python")

        self.assertIn("quality_score", result_good)
        self.assertIn("quality_score", result_bad)


if __name__ == "__main__":
    unittest.main()
