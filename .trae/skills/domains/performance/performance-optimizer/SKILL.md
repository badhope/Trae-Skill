---
name: performance-optimizer
description: "Performance optimization expert for analyzing bottlenecks, memory usage, and optimization strategies. Keywords: performance, optimization, profiling, memory, benchmark"
layer: domain
role: specialist
version: 2.0.0
domain: performance
invoked_by:
  - coding-workflow
  - debugging-workflow
capabilities:
  - performance_analysis
  - bottleneck_identification
  - memory_optimization
  - algorithm_optimization
  - caching_strategy
---

# Performance Optimizer

性能优化专家。

## 适用场景

- 代码运行缓慢
- 内存使用过高
- 需要优化扩展性
- 性能分析
- 基准测试

## 时间复杂度

| 复杂度 | 名称 | 示例 | 评级 |
|--------|------|------|------|
| O(1) | 常数 | 哈希查找 | 优秀 |
| O(log n) | 对数 | 二分查找 | 很好 |
| O(n) | 线性 | 简单循环 | 良好 |
| O(n²) | 平方 | 嵌套循环 | 差 |

## 常见问题

### N+1查询

```typescript
// 差
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findByUserId(user.id);
}

// 好
const users = await User.findAll({
  include: [{ model: Post }]
});
```

### 并行I/O

```typescript
// 慢 - 顺序
for (const url of urls) {
  results.push(await fetch(url));
}

// 快 - 并行
const results = await Promise.all(urls.map(url => fetch(url)));
```

## 优化策略

### 缓存

```typescript
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
```

### 防抖/节流

```typescript
const debounce = (fn, delay) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
};
```

## 性能分析工具

- Chrome DevTools Performance
- Node.js --prof
- Python cProfile

## 相关技能

- [debugging-workflow](../../workflows/debugging-workflow) - 调试工作流
- [test-generator](../../actions/test/test-generator) - 测试生成
