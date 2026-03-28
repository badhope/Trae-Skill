---
name: code-search
description: "Code search and analysis for finding patterns, usages, and definitions. Keywords: search, find, grep, usage, definition, 搜索, 查找"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - coding-workflow
  - debugging-workflow
  - refactoring-workflow
capabilities:
  - pattern_search
  - usage_finding
  - definition_finding
  - symbol_analysis
  - dependency_analysis
triggers:
  keywords:
    - search
    - find
    - grep
    - locate
    - where
    - 搜索
    - 查找
metrics:
  avg_execution_time: 1s
  success_rate: 0.98
---

# Code Search

代码搜索专家，快速定位代码模式、用法和定义。

## 适用场景

- 查找函数定义
- 追踪变量用法
- 分析依赖关系
- 搜索代码模式
- 重构前影响分析

## 搜索模式

### 1. 定义搜索

```typescript
interface SearchResult {
  file: string;
  line: number;
  column: number;
  match: string;
  context: string[];
  type: 'definition' | 'usage' | 'import' | 'export';
}

interface SearchOptions {
  pattern: string | RegExp;
  fileType?: string[];
  exclude?: string[];
  contextLines?: number;
  caseSensitive?: boolean;
  wholeWord?: boolean;
}

function findDefinition(symbol: string, options?: SearchOptions): SearchResult[] {
  const patterns = [
    new RegExp(`(function|class|interface|type|const|let|var)\\s+${symbol}\\b`),
    new RegExp(`${symbol}\\s*[:=]\\s*(function|\\(|async)`),
  ];
  
  return searchPatterns(patterns, options);
}

function findClassDefinition(className: string): SearchResult[] {
  return searchPattern(
    new RegExp(`class\\s+${className}\\s*(?:extends|implements|\\{)`, 'g')
  );
}

function findFunctionDefinition(funcName: string): SearchResult[] {
  return searchPattern(
    new RegExp(`(?:function\\s+${funcName}|${funcName}\\s*[=:]\\s*(?:async\\s*)?(?:function|\\())`, 'g')
  );
}

function findInterfaceDefinition(ifaceName: string): SearchResult[] {
  return searchPattern(
    new RegExp(`interface\\s+${ifaceName}\\s*(?:extends|\\{)`, 'g')
  );
}
```

### 2. 用法搜索

```typescript
function findUsages(symbol: string, options?: SearchOptions): SearchResult[] {
  const results: SearchResult[] = [];
  
  results.push(...findImports(symbol, options));
  results.push(...findExports(symbol, options));
  results.push(...findReferences(symbol, options));
  
  return results;
}

function findImports(symbol: string, options?: SearchOptions): SearchResult[] {
  const patterns = [
    new RegExp(`import\\s+.*\\b${symbol}\\b.*from`),
    new RegExp(`import\\s+\\{[^}]*\\b${symbol}\\b[^}]*\\}`),
    new RegExp(`import\\s+\\*\\s+as\\s+${symbol}\\b`),
    new RegExp(`require\\(['"].*['"]\\)\\.${symbol}`),
  ];
  
  return searchPatterns(patterns, options);
}

function findReferences(symbol: string, options?: SearchOptions): SearchResult[] {
  return searchPattern(
    new RegExp(`\\b${symbol}\\b`, 'g'),
    { ...options, exclude: [...(options?.exclude || []), 'node_modules'] }
  );
}

function findMethodCalls(methodName: string): SearchResult[] {
  return searchPattern(
    new RegExp(`\\.${methodName}\\s*\\(`, 'g')
  );
}

function findPropertyAccess(propertyName: string): SearchResult[] {
  return searchPattern(
    new RegExp(`\\.${propertyName}\\b`, 'g')
  );
}
```

### 3. 模式搜索

```typescript
function findPattern(pattern: string | RegExp, options?: SearchOptions): SearchResult[] {
  const regex = typeof pattern === 'string' ? new RegExp(pattern, 'g') : pattern;
  return searchPattern(regex, options);
}

function findTodoComments(): SearchResult[] {
  return searchPattern(
    /(?:TODO|FIXME|HACK|XXX|BUG):?\s*(.+)/g
  );
}

function findConsoleLogs(): SearchResult[] {
  return searchPattern(
    /console\.(log|warn|error|debug|info)\s*\(/g
  );
}

function findDeprecatedCode(): SearchResult[] {
  return searchPattern(
    /@deprecated|DEPRECATED|deprecated/gi
  );
}

function findSecurityIssues(): SearchResult[] {
  const patterns = [
    /eval\s*\(/g,
    /innerHTML\s*=/g,
    /dangerouslySetInnerHTML/g,
    /password\s*=\s*['"][^'"]+['"]/gi,
    /api[_-]?key\s*=\s*['"][^'"]+['"]/gi,
    /secret\s*=\s*['"][^'"]+['"]/gi,
  ];
  
  return searchPatterns(patterns);
}

function findErrorHandling(): SearchResult[] {
  const patterns = [
    /try\s*\{/g,
    /catch\s*\(/g,
    /\.catch\s*\(/g,
    /throw\s+new\s+\w+Error/g,
  ];
  
  return searchPatterns(patterns);
}
```

### 4. 依赖分析

```typescript
interface DependencyNode {
  name: string;
  path: string;
  imports: string[];
  importedBy: string[];
}

function analyzeDependencies(entryFile: string): Map<string, DependencyNode> {
  const graph = new Map<string, DependencyNode>();
  
  function traverse(filePath: string) {
    if (graph.has(filePath)) return;
    
    const imports = extractImports(filePath);
    const node: DependencyNode = {
      name: path.basename(filePath),
      path: filePath,
      imports: [],
      importedBy: []
    };
    
    for (const importPath of imports) {
      const resolved = resolveImportPath(filePath, importPath);
      if (resolved) {
        node.imports.push(resolved);
        traverse(resolved);
        
        const depNode = graph.get(resolved);
        if (depNode) {
          depNode.importedBy.push(filePath);
        }
      }
    }
    
    graph.set(filePath, node);
  }
  
  traverse(entryFile);
  return graph;
}

function findCircularDependencies(graph: Map<string, DependencyNode>): string[][] {
  const cycles: string[][] = [];
  const visited = new Set<string>();
  const recursionStack = new Set<string>();
  
  function dfs(node: string, path: string[]) {
    if (recursionStack.has(node)) {
      const cycleStart = path.indexOf(node);
      cycles.push(path.slice(cycleStart));
      return;
    }
    
    if (visited.has(node)) return;
    
    visited.add(node);
    recursionStack.add(node);
    path.push(node);
    
    const deps = graph.get(node);
    if (deps) {
      for (const dep of deps.imports) {
        dfs(dep, [...path]);
      }
    }
    
    recursionStack.delete(node);
  }
  
  for (const [node] of graph) {
    dfs(node, []);
  }
  
  return cycles;
}

function findUnusedFiles(graph: Map<string, DependencyNode>): string[] {
  const unused: string[] = [];
  
  for (const [path, node] of graph) {
    if (node.importedBy.length === 0 && !isEntryPoint(path)) {
      unused.push(path);
    }
  }
  
  return unused;
}
```

### 5. 重构支持

```typescript
interface RefactoringImpact {
  filesAffected: number;
  linesAffected: number;
  usages: SearchResult[];
  risks: string[];
}

function analyzeRenameImpact(
  oldName: string,
  newName: string,
  scope?: string
): RefactoringImpact {
  const usages = findUsages(oldName, { path: scope });
  const definition = findDefinition(oldName)[0];
  
  const risks: string[] = [];
  
  if (usages.length > 50) {
    risks.push('High number of usages - consider gradual migration');
  }
  
  const externalUsages = usages.filter(u => 
    !u.file.startsWith(scope || '')
  );
  if (externalUsages.length > 0) {
    risks.push('External usages found - may break public API');
  }
  
  if (isExported(definition)) {
    risks.push('Symbol is exported - breaking change possible');
  }
  
  return {
    filesAffected: new Set(usages.map(u => u.file)).size,
    linesAffected: usages.length,
    usages,
    risks
  };
}

function findSimilarCode(threshold: number = 0.8): SimilarCodeGroup[] {
  const files = getAllSourceFiles();
  const groups: SimilarCodeGroup[] = [];
  
  for (let i = 0; i < files.length; i++) {
    for (let j = i + 1; j < files.length; j++) {
      const similarity = calculateSimilarity(
        readFile(files[i]),
        readFile(files[j])
      );
      
      if (similarity >= threshold) {
        groups.push({
          files: [files[i], files[j]],
          similarity,
          duplicateLines: findDuplicateLines(files[i], files[j])
        });
      }
    }
  }
  
  return groups;
}
```

## 搜索命令示例

### Grep模式

```bash
# 查找函数定义
grep -rn "function functionName" --include="*.ts" --include="*.js"

# 查找类定义
grep -rn "class ClassName" --include="*.ts"

# 查找TODO
grep -rn "TODO\|FIXME" --include="*.ts"

# 查找console.log
grep -rn "console\.log" --include="*.ts" --include="*.js"

# 排除目录
grep -rn "pattern" --exclude-dir=node_modules --exclude-dir=dist

# 正则搜索
grep -rnE "import.*from.*['\"]\." --include="*.ts"
```

### Ripgrep模式

```bash
# 智能搜索
rg "pattern" -t ts -t js

# 显示上下文
rg "pattern" -C 3

# 只显示文件名
rg "pattern" -l

# 统计匹配数
rg "pattern" -c

# 正则搜索
rg "function\s+\w+" -t ts

# 搜索并替换预览
rg "oldName" -r "newName"
```

## 最佳实践

1. **精确模式**: 使用具体的搜索模式减少噪音
2. **排除目录**: 排除node_modules、dist等
3. **文件类型**: 指定文件类型提高效率
4. **上下文**: 显示上下文理解匹配
5. **结果限制**: 限制结果数量避免过载
6. **缓存**: 对大型项目使用搜索缓存

## 相关技能

- [cross-file-refactor](../code/cross-file-refactor) - 跨文件重构
- [code-generator](../code-generator) - 代码生成
- [linting-config](../code/linting-config) - Lint配置
