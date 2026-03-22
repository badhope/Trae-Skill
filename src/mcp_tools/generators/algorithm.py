"""Algorithm Implementer Tool - Generate implementations of common algorithms"""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional
from mcp_tools.framework import MCPTool, ToolDefinition, ToolResult


class AlgorithmImplementerTool(MCPTool):
    ALGORITHMS = {
        "sorting": {
            "bubble_sort": {
                "description": "Simple comparison-based sorting algorithm",
                "time_complexity": "O(n^2)",
                "space_complexity": "O(1)"
            },
            "quick_sort": {
                "description": "Efficient divide-and-conquer sorting",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(log n)"
            },
            "merge_sort": {
                "description": "Stable divide-and-conquer sorting",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)"
            },
        },
        "searching": {
            "binary_search": {
                "description": "Efficient search in sorted arrays",
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)"
            },
            "depth_first_search": {
                "description": "Graph/tree traversal algorithm",
                "time_complexity": "O(V + E)",
                "space_complexity": "O(V)"
            },
            "breadth_first_search": {
                "description": "Level-order graph/tree traversal",
                "time_complexity": "O(V + E)",
                "space_complexity": "O(V)"
            },
        },
        "data_structures": {
            "stack": {
                "description": "LIFO data structure",
                "time_complexity": "O(1)",
                "space_complexity": "O(n)"
            },
            "queue": {
                "description": "FIFO data structure",
                "time_complexity": "O(1)",
                "space_complexity": "O(n)"
            },
            "hash_table": {
                "description": "Key-value storage with O(1) average access",
                "time_complexity": "O(1) avg",
                "space_complexity": "O(n)"
            },
        },
        "dynamic_programming": {
            "fibonacci": {
                "description": "Classic DP example with memoization",
                "time_complexity": "O(n)",
                "space_complexity": "O(n) or O(1)"
            },
            "longest_common_subsequence": {
                "description": "Find longest subsequence in two strings",
                "time_complexity": "O(mn)",
                "space_complexity": "O(mn)"
            },
            "knapsack": {
                "description": "0/1 knapsack problem",
                "time_complexity": "O(nW)",
                "space_complexity": "O(nW)"
            },
        },
        "graph": {
            "dijkstra": {
                "description": "Shortest path in weighted graph",
                "time_complexity": "O((V+E) log V)",
                "space_complexity": "O(V)"
            },
            "bellman_ford": {
                "description": "Shortest path with negative weights",
                "time_complexity": "O(VE)",
                "space_complexity": "O(V)"
            },
        },
        "string": {
            "kmp": {
                "description": "Knuth-Morris-Pratt pattern matching",
                "time_complexity": "O(m+n)",
                "space_complexity": "O(m)"
            },
            "rabin_karp": {
                "description": "Hash-based pattern matching",
                "time_complexity": "O(mn) avg O(m+n)",
                "space_complexity": "O(1)"
            },
        }
    }

    def __init__(self):
        super().__init__()

    def get_definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="algorithm_implementer",
            description="Generates implementations of common algorithms and data structures. Supports sorting, searching, dynamic programming, graph algorithms, and more.",
            input_schema={
                "type": "object",
                "properties": {
                    "algorithm_name": {
                        "type": "string",
                        "description": "Name of the algorithm to implement",
                        "enum": [
                            "bubble_sort", "quick_sort", "merge_sort",
                            "binary_search", "depth_first_search", "breadth_first_search",
                            "stack", "queue", "hash_table",
                            "fibonacci", "longest_common_subsequence", "knapsack",
                            "dijkstra", "bellman_ford",
                            "kmp", "rabin_karp"
                        ]
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language",
                        "enum": ["python", "javascript", "typescript", "java", "go", "rust"]
                    },
                    "include_tests": {
                        "type": "boolean",
                        "description": "Include unit tests",
                        "default": False
                    },
                    "optimized": {
                        "type": "boolean",
                        "description": "Use optimized version",
                        "default": True
                    }
                },
                "required": ["algorithm_name", "language"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Generated algorithm implementation"},
                    "tests": {"type": "string", "description": "Unit tests if requested"},
                    "time_complexity": {"type": "string", "description": "Time complexity"},
                    "space_complexity": {"type": "string", "description": "Space complexity"},
                    "description": {"type": "string", "description": "Algorithm description"}
                }
            },
            tags={"code", "generation", "algorithm", "data-structures", "implementation"},
            category="generators",
            version="1.0.0"
        )

    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        start_time = datetime.now()
        algorithm_name = params["algorithm_name"]
        language = params["language"]
        include_tests = params.get("include_tests", False)
        optimized = params.get("optimized", True)

        try:
            code = self._generate_algorithm(algorithm_name, language, optimized)
            tests = self._generate_tests(algorithm_name, language) if include_tests else None

            alg_info = self._find_algorithm_info(algorithm_name)

            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            return ToolResult(
                tool_name="algorithm_implementer",
                success=True,
                data={
                    "code": code,
                    "tests": tests,
                    "time_complexity": alg_info.get("time_complexity", "Unknown"),
                    "space_complexity": alg_info.get("space_complexity", "Unknown"),
                    "description": alg_info.get("description", "")
                },
                execution_time_ms=execution_time,
                metadata={"algorithm": algorithm_name, "language": language}
            )

        except Exception as e:
            return ToolResult(
                tool_name="algorithm_implementer",
                success=False,
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )

    def _generate_algorithm(self, name: str, language: str, optimized: bool) -> str:
        if name == "binary_search":
            return self._generate_binary_search(language, optimized)
        elif name == "quick_sort":
            return self._generate_quick_sort(language, optimized)
        elif name == "merge_sort":
            return self._generate_merge_sort(language, optimized)
        elif name == "fibonacci":
            return self._generate_fibonacci(language, optimized)
        elif name == "depth_first_search":
            return self._generate_dfs(language)
        elif name == "breadth_first_search":
            return self._generate_bfs(language)
        elif name == "dijkstra":
            return self._generate_dijkstra(language)
        elif name == "stack":
            return self._generate_stack(language)
        elif name == "queue":
            return self._generate_queue(language)
        else:
            return f"// Implementation for {name} in {language}"

    def _generate_binary_search(self, language: str, optimized: bool) -> str:
        if language == "python":
            return '''
def binary_search(arr: list, target: int) -> int:
    """
    Binary search in a sorted array.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def binary_search_recursive(arr: list, target: int, left: int = 0, right: int = None) -> int:
    """Recursive version"""
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = left + (right - left) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
'''

        elif language == "javascript":
            return '''
function binarySearch(arr, target) {
    let left = 0;
    let right = arr.length - 1;

    while (left <= right) {
        const mid = left + Math.floor((right - left) / 2);

        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}

function binarySearchRecursive(arr, target, left = 0, right = arr.length - 1) {
    if (left > right) return -1;

    const mid = left + Math.floor((right - left) / 2);

    if (arr[mid] === target) return mid;
    else if (arr[mid] < target) return binarySearchRecursive(arr, target, mid + 1, right);
    else return binarySearchRecursive(arr, target, left, mid - 1);
}
'''

        return f"// Binary search implementation in {language}"

    def _generate_quick_sort(self, language: str, optimized: bool) -> str:
        if language == "python":
            return '''
def quick_sort(arr: list) -> list:
    """
    Quick sort algorithm.
    Time: O(n log n) avg, O(n^2) worst, Space: O(log n)
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_in_place(arr: list, low: int = 0, high: int = None) -> None:
    """In-place quick sort"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high)
        quick_sort_in_place(arr, low, pi - 1)
        quick_sort_in_place(arr, pi + 1, high)


def partition(arr: list, low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
'''

        elif language == "javascript":
            return '''
function quickSort(arr) {
    if (arr.length <= 1) return arr;

    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);

    return [...quickSort(left), ...middle, ...quickSort(right)];
}

function quickSortInPlace(arr, low = 0, high = arr.length - 1) {
    if (low < high) {
        const pi = partition(arr, low, high);
        quickSortInPlace(arr, low, pi - 1);
        quickSortInPlace(arr, pi + 1, high);
    }
    return arr;
}

function partition(arr, low, high) {
    const pivot = arr[high];
    let i = low - 1;

    for (let j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    return i + 1;
}
'''

        return f"// Quick sort implementation in {language}"

    def _generate_merge_sort(self, language: str, optimized: bool) -> str:
        if language == "python":
            return '''
def merge_sort(arr: list) -> list:
    """
    Merge sort algorithm.
    Time: O(n log n), Space: O(n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left: list, right: list) -> list:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
'''

        elif language == "javascript":
            return '''
function mergeSort(arr) {
    if (arr.length <= 1) return arr;

    const mid = Math.floor(arr.length / 2);
    const left = mergeSort(arr.slice(0, mid));
    const right = mergeSort(arr.slice(mid));

    return merge(left, right);
}

function merge(left, right) {
    const result = [];
    let i = 0, j = 0;

    while (i < left.length && j < right.length) {
        if (left[i] <= right[j]) {
            result.push(left[i++]);
        } else {
            result.push(right[j++]);
        }
    }

    return [...result, ...left.slice(i), ...right.slice(j)];
}
'''

        return f"// Merge sort implementation in {language}"

    def _generate_fibonacci(self, language: str, optimized: bool) -> str:
        if language == "python":
            return '''
def fibonacci_iterative(n: int) -> int:
    """O(n) time, O(1) space"""
    if n <= 1:
        return n

    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr


def fibonacci_recursive(n: int) -> int:
    """O(2^n) time - NOT recommended"""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """O(n) time with memoization"""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def fibonacci_matrix(n: int) -> int:
    """O(log n) time using matrix exponentiation"""
    if n <= 1:
        return n

    def matrix_mult(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]

    def matrix_pow(M, p):
        result = [[1, 0], [0, 1]]
        base = M
        while p:
            if p & 1:
                result = matrix_mult(result, base)
            base = matrix_mult(base, base)
            p >>= 1
        return result

    result = matrix_pow([[1, 1], [1, 0]], n)
    return result[0][1]
'''

        elif language == "javascript":
            return '''
function fibonacciIterative(n) {
    if (n <= 1) return n;

    let prev = 0, curr = 1;
    for (let i = 2; i <= n; i++) {
        [prev, curr] = [curr, prev + curr];
    }
    return curr;
}

function fibonacciRecursive(n) {
    if (n <= 1) return n;
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

const fibonacciMemoized = (() => {
    const cache = new Map();
    return function fib(n) {
        if (cache.has(n)) return cache.get(n);
        if (n <= 1) return n;
        const result = fib(n - 1) + fib(n - 2);
        cache.set(n, result);
        return result;
    };
})();
'''

        return f"// Fibonacci implementation in {language}"

    def _generate_dfs(self, language: str) -> str:
        if language == "python":
            return '''
from collections import defaultdict

def dfs(graph: dict, start: str, visited: set = None) -> list:
    """
    Depth-First Search.
    Time: O(V + E), Space: O(V)
    """
    if visited is None:
        visited = set()

    visited.add(start)
    result = [start]

    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))

    return result


def dfs_iterative(graph: dict, start: str) -> list:
    """Iterative DFS using stack"""
    visited = set()
    stack = [start]
    result = []

    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            result.append(node)

            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)

    return result
'''

        elif language == "javascript":
            return '''
function dfs(graph, start, visited = new Set()) {
    visited.add(start);
    const result = [start];

    for (const neighbor of graph.get(start) || []) {
        if (!visited.has(neighbor)) {
            result.push(...dfs(graph, neighbor, visited));
        }
    }

    return result;
}

function dfsIterative(graph, start) {
    const visited = new Set();
    const stack = [start];
    const result = [];

    while (stack.length > 0) {
        const node = stack.pop();
        if (!visited.has(node)) {
            visited.add(node);
            result.push(node);

            const neighbors = graph.get(node) || [];
            for (let i = neighbors.length - 1; i >= 0; i--) {
                if (!visited.has(neighbors[i])) {
                    stack.push(neighbors[i]);
                }
            }
        }
    }

    return result;
}
'''

        return f"// DFS implementation in {language}"

    def _generate_bfs(self, language: str) -> str:
        if language == "python":
            return '''
from collections import deque

def bfs(graph: dict, start: str) -> list:
    """
    Breadth-First Search.
    Time: O(V + E), Space: O(V)
    """
    visited = set([start])
    queue = deque([start])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return result
'''

        elif language == "javascript":
            return '''
function bfs(graph, start) {
    const visited = new Set([start]);
    const queue = [start];
    const result = [];

    while (queue.length > 0) {
        const node = queue.shift();
        result.push(node);

        for (const neighbor of graph.get(node) || []) {
            if (!visited.has(neighbor)) {
                visited.add(neighbor);
                queue.push(neighbor);
            }
        }
    }

    return result;
}
'''

        return f"// BFS implementation in {language}"

    def _generate_dijkstra(self, language: str) -> str:
        if language == "python":
            return '''
import heapq

def dijkstra(graph: dict, start: str) -> dict:
    """
    Dijkstra's shortest path algorithm.
    Time: O((V + E) log V), Space: O(V)
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current_dist > dist[current]:
            continue

        for neighbor, weight in graph.get(current, []):
            distance = current_dist + weight

            if distance < dist[neighbor]:
                dist[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return dist
'''

        elif language == "javascript":
            return '''
function dijkstra(graph, start) {
    const dist = {};
    const visited = new Set();
    const pq = [[0, start]];

    for (const node in graph) {
        dist[node] = Infinity;
    }
    dist[start] = 0;

    while (pq.length > 0) {
        const [currentDist, current] = pq.shift();

        if (visited.has(current)) continue;
        visited.add(current);

        for (const [neighbor, weight] of graph.get(current) || []) {
            const distance = currentDist + weight;
            if (distance < dist[neighbor]) {
                dist[neighbor] = distance;
                pq.push([distance, neighbor]);
                pq.sort((a, b) => a[0] - b[0]);
            }
        }
    }

    return dist;
}
'''

        return f"// Dijkstra implementation in {language}"

    def _generate_stack(self, language: str) -> str:
        if language == "python":
            return '''
class Stack:
    """LIFO data structure"""
    def __init__(self):
        self._items = []

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"Stack({self._items})"
'''

        elif language == "javascript":
            return '''
class Stack {
    constructor() {
        this.items = [];
    }

    push(item) {
        this.items.push(item);
    }

    pop() {
        if (this.isEmpty()) {
            throw new Error("Stack is empty");
        }
        return this.items.pop();
    }

    peek() {
        if (this.isEmpty()) {
            throw new Error("Stack is empty");
        }
        return this.items[this.items.length - 1];
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }
}
'''

        return f"// Stack implementation in {language}"

    def _generate_queue(self, language: str) -> str:
        if language == "python":
            return '''
from collections import deque

class Queue:
    """FIFO data structure"""
    def __init__(self):
        self._items = deque()

    def enqueue(self, item) -> None:
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.popleft()

    def front(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)
'''

        elif language == "javascript":
            return '''
class Queue {
    constructor() {
        this.items = [];
    }

    enqueue(item) {
        this.items.push(item);
    }

    dequeue() {
        if (this.isEmpty()) {
            throw new Error("Queue is empty");
        }
        return this.items.shift();
    }

    front() {
        if (this.isEmpty()) {
            throw new Error("Queue is empty");
        }
        return this.items[0];
    }

    isEmpty() {
        return this.items.length === 0;
    }

    size() {
        return this.items.length;
    }
}
'''

        return f"// Queue implementation in {language}"

    def _generate_tests(self, name: str, language: str) -> str:
        if language == "python":
            return f'''
import pytest

class Test{name.title().replace("_", "")}:
    def test_{name}(self):
        # Add your test cases here
        pass
'''
        return ""

    def _find_algorithm_info(self, name: str) -> Dict[str, str]:
        for category, algs in self.ALGORITHMS.items():
            if name in algs:
                return algs[name]
        return {}
