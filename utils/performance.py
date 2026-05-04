# Performance Optimizer
# Performance monitoring and optimization utilities
# Thesis Specialist Platform v2.2

import time
import functools
from typing import Dict, Any, Optional, Callable
from datetime import datetime

class PerformanceMonitor:
    """Performance monitoring and optimization"""

    def __init__(self):
        self.timings = {}
        self.counters = {}
        self.start_time = time.time()

    def time_function(self, func: Callable) -> Callable:
        """Decorator to measure function execution time"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start

            func_name = func.__name__
            if func_name not in self.timings:
                self.timings[func_name] = []
            self.timings[func_name].append(elapsed)

            self.counters[func_name] = self.counters.get(func_name, 0) + 1

            return result
        return wrapper

    def measure_time(self, operation_name: str):
        """Context manager for timing operations"""
        return _Timer(self, operation_name)

    def get_stats(self) -> Dict:
        """Get performance statistics"""
        stats = {}

        for func_name, times in self.timings.items():
            if times:
                stats[func_name] = {
                    'count': len(times),
                    'min': min(times),
                    'max': max(times),
                    'avg': sum(times) / len(times),
                    'total': sum(times)
                }

        return {
            'uptime': time.time() - self.start_time,
            'operations': self.counters,
            'timings': stats
        }

    def get_slowest_operations(self, limit: int = 5) -> list:
        """Get slowest operations"""
        stats = self.get_stats()['timings']
        sorted_ops = sorted(stats.items(), key=lambda x: x[1]['avg'], reverse=True)
        return sorted_ops[:limit]

    def reset(self):
        """Reset all measurements"""
        self.timings = {}
        self.counters = {}
        self.start_time = time.time()

class _Timer:
    """Timer context manager"""

    def __init__(self, monitor: PerformanceMonitor, operation_name: str):
        self.monitor = monitor
        self.operation_name = operation_name

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start

        if self.operation_name not in self.monitor.timings:
            self.monitor.timings[self.operation_name] = []
        self.monitor.timings[self.operation_name].append(elapsed)

        self.monitor.counters[self.operation_name] = self.monitor.counters.get(self.operation_name, 0) + 1

class CachingLayer:
    """Intelligent caching layer"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                self.hits += 1
                return entry['value']
            else:
                del self.cache[key]

        self.misses += 1
        return None

    def set(self, key: str, value: Any):
        """Set value in cache"""
        if len(self.cache) >= self.max_size:
            self._evict()

        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }

    def _evict(self):
        """Evict oldest entries"""
        sorted_keys = sorted(
            self.cache.keys(),
            key=lambda k: self.cache[k]['timestamp'],
            reverse=True
        )
        keys_to_remove = sorted_keys[self.max_size // 2:]
        for key in keys_to_remove:
            del self.cache[key]

    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0

        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'ttl': self.ttl
        }

    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

class LazyLoader:
    """Lazy loading utility"""

    def __init__(self):
        self.loaded_modules = {}

    def load(self, module_name: str, loader: Callable) -> Any:
        """Load module lazily"""
        if module_name not in self.loaded_modules:
            self.loaded_modules[module_name] = loader()
        return self.loaded_modules[module_name]

    def is_loaded(self, module_name: str) -> bool:
        """Check if module is loaded"""
        return module_name in self.loaded_modules

    def unload(self, module_name: str):
        """Unload module"""
        if module_name in self.loaded_modules:
            del self.loaded_modules[module_name]

    def get_stats(self) -> Dict:
        """Get loading statistics"""
        return {
            'loaded_modules': list(self.loaded_modules.keys()),
            'count': len(self.loaded_modules)
        }

performance_monitor = PerformanceMonitor()
caching_layer = CachingLayer()
lazy_loader = LazyLoader()

if __name__ == '__main__':
    monitor = PerformanceMonitor()

    @monitor.time_function
    def slow_function():
        time.sleep(0.1)
        return "done"

    for _ in range(3):
        slow_function()

    print("Performance Stats:")
    print(monitor.get_stats())

    print("\nSlowest Operations:")
    for op, stats in monitor.get_slowest_operations():
        print(f"  {op}: avg={stats['avg']:.4f}s")

    cache = CachingLayer(max_size=100, ttl_seconds=60)

    cache.set('key1', 'value1')
    result1 = cache.get('key1')
    result2 = cache.get('key1')
    result3 = cache.get('key2')

    print("\nCache Stats:")
    print(cache.get_stats())

    loader = LazyLoader()
    loaded = loader.load('example', lambda: {"loaded": True})
    print("\nLazy Loader Stats:")
    print(loader.get_stats())
