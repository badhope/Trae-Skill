---
name: error-analyzer
description: "Analyze errors and exceptions to identify root causes and solutions. Keywords: error, exception, stack trace, debug, 错误分析, 异常处理"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - debugging-workflow
  - code-review
  - aggregation-processor
capabilities:
  - error_parsing
  - root_cause_identification
  - solution_suggestion
  - pattern_recognition
triggers:
  keywords:
    - error
    - exception
    - stack trace
    - crash
    - bug
    - 错误
    - 异常
    - 堆栈
metrics:
  avg_execution_time: 2s
  success_rate: 0.88
  token_efficiency: 0.82
  root_cause_accuracy: 0.85
---

# Error Analyzer

分析错误和异常，识别根本原因并提供解决方案。

## 目的

为错误和异常提供系统性分析：
- 解析错误信息和堆栈跟踪
- 识别根本原因
- 提供修复建议
- 识别错误模式

## 能力

- **错误解析**: 解析错误信息和堆栈跟踪
- **根因识别**: 识别错误根本原因
- **解决方案建议**: 提供具体修复建议
- **模式识别**: 识别常见错误模式

## 错误类型

### 1. 编译/语法错误

| 类型 | 描述 | 常见原因 |
|------|------|----------|
| SyntaxError | 语法错误 | 括号不匹配、关键字拼写错误 |
| TypeError | 类型错误 | 类型不匹配、None操作 |
| NameError | 名称错误 | 变量未定义、作用域问题 |
| ImportError | 导入错误 | 模块不存在、路径问题 |

### 2. 运行时错误

| 类型 | 描述 | 常见原因 |
|------|------|----------|
| NullPointerException | 空指针 | 对象未初始化 |
| IndexError | 索引越界 | 数组访问超出范围 |
| KeyError | 键错误 | 字典键不存在 |
| ValueError | 值错误 | 参数值无效 |

### 3. 网络错误

| 类型 | 描述 | 常见原因 |
|------|------|----------|
| ConnectionError | 连接错误 | 网络不可达 |
| TimeoutError | 超时错误 | 请求超时 |
| HTTPError | HTTP错误 | 4xx/5xx响应 |

### 4. 数据库错误

| 类型 | 描述 | 常见原因 |
|------|------|----------|
| IntegrityError | 完整性错误 | 约束违反 |
| OperationalError | 操作错误 | 连接问题 |
| ProgrammingError | 编程错误 | SQL语法错误 |

## 分析流程

```
输入: 错误信息/堆栈跟踪
输出: 分析报告

步骤:
1. 解析错误类型
2. 提取关键信息
3. 定位错误位置
4. 分析根本原因
5. 生成解决方案
```

## 分析模板

### 错误分析报告

```markdown
# 错误分析报告

## 错误概述
- 类型: TypeError
- 消息: 'NoneType' object is not iterable
- 位置: app.py:45

## 堆栈跟踪
```
Traceback (most recent call last):
  File "app.py", line 45, in process_data
    for item in data:
TypeError: 'NoneType' object is not iterable
```

## 根本原因
函数 `get_data()` 在某些情况下返回 None，而调用方未处理这种情况。

## 解决方案

### 方案1: 添加空值检查
```python
data = get_data()
if data is not None:
    for item in data:
        process(item)
```

### 方案2: 返回默认值
```python
def get_data():
    # ...
    return result or []  # 返回空列表而非None
```

## 预防措施
1. 添加类型注解
2. 使用 Optional 类型明确表示可能为空
3. 添加单元测试覆盖边界情况
```

## 常见错误模式

### 模式1: 空值处理

```python
# 问题代码
def process(data):
    return data.strip()  # data可能为None

# 解决方案
def process(data):
    if data is None:
        return ""
    return data.strip()

# 或使用默认值
def process(data: Optional[str]) -> str:
    return (data or "").strip()
```

### 模式2: 索引访问

```python
# 问题代码
first_item = items[0]  # items可能为空

# 解决方案
first_item = items[0] if items else None
# 或
first_item = next(iter(items), None)
```

### 模式3: 异步错误处理

```javascript
// 问题代码
const data = await fetchData();  // 未处理错误

// 解决方案
try {
    const data = await fetchData();
} catch (error) {
    console.error('Failed to fetch:', error);
    // 处理错误
}
```

## 使用示例

### 示例: Python错误分析

```
用户: "分析这个错误: TypeError: 'NoneType' object is not subscriptable"

执行:
1. 识别错误类型: TypeError
2. 分析错误消息: NoneType不可下标访问
3. 识别常见原因
4. 提供解决方案

输出:
# 错误分析

## 原因
尝试对 None 值使用下标访问 (如 obj['key'] 或 obj[0])

## 常见场景
1. 函数返回 None 但调用方期望返回值
2. 字典查找失败返回 None
3. 条件分支遗漏返回语句

## 解决方案
1. 添加 None 检查
2. 使用 .get() 方法带默认值
3. 使用 walrus 操作符 (Python 3.8+)
```

## 错误处理最佳实践

### Python

```python
# 使用类型注解
from typing import Optional

def get_user(id: int) -> Optional[User]:
    ...

# 使用异常链
try:
    process(data)
except ValueError as e:
    raise ProcessingError("Failed to process") from e

# 使用上下文管理器
with open('file.txt') as f:
    content = f.read()
```

### JavaScript/TypeScript

```typescript
// 使用可选链
const name = user?.profile?.name;

// 使用空值合并
const value = data ?? defaultValue;

// 使用 Result 类型
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
```

## 相关技能

- [debugging-workflow](../../workflows/debugging-workflow) - 调试工作流
- [code-review](../code-review) - 代码审查
- [test-generator](../test/test-generator) - 测试生成
