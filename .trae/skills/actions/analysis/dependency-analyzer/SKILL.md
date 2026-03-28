---
name: dependency-analyzer
description: "Analyze project dependencies for security, updates, and optimization. Keywords: dependency, npm, pip, maven, gradle, 依赖分析, 包管理"
layer: action
role: executor
version: 2.0.0
invoked_by:
  - debugging-workflow
  - security-auditor
  - aggregation-processor
capabilities:
  - dependency_scanning
  - vulnerability_detection
  - update_checking
  - optimization_suggestions
triggers:
  keywords:
    - dependency
    - dependencies
    - npm
    - pip
    - package
    - vulnerability
    - outdated
    - 依赖
    - 包管理
metrics:
  avg_execution_time: 5s
  success_rate: 0.95
  token_efficiency: 0.90
  vulnerability_detection_rate: 0.92
---

# Dependency Analyzer

分析项目依赖的安全性、更新状态和优化机会。

## 目的

为项目依赖提供全面分析：
- 扫描依赖树
- 检测安全漏洞
- 检查更新状态
- 提供优化建议

## 能力

- **依赖扫描**: 扫描项目所有依赖
- **漏洞检测**: 识别已知安全漏洞
- **更新检查**: 检查过时依赖
- **优化建议**: 提供依赖优化建议

## 支持的包管理器

| 语言 | 包管理器 | 锁文件 |
|------|----------|--------|
| JavaScript | npm, yarn, pnpm | package-lock.json, yarn.lock, pnpm-lock.yaml |
| Python | pip, poetry, pipenv | requirements.txt, poetry.lock, Pipfile.lock |
| Java | maven, gradle | pom.xml, build.gradle |
| Go | go modules | go.mod, go.sum |
| Rust | cargo | Cargo.toml, Cargo.lock |
| Ruby | bundler | Gemfile, Gemfile.lock |

## 分析流程

```
输入: 项目路径
输出: 依赖分析报告

步骤:
1. 检测包管理器
2. 解析依赖文件
3. 构建依赖树
4. 检查安全漏洞
5. 检查更新状态
6. 生成报告
```

## 分析维度

### 1. 安全漏洞

```markdown
## 漏洞等级

| 等级 | CVSS分数 | 描述 |
|------|----------|------|
| Critical | 9.0-10.0 | 立即修复 |
| High | 7.0-8.9 | 尽快修复 |
| Medium | 4.0-6.9 | 计划修复 |
| Low | 0.1-3.9 | 可选修复 |

## 常见漏洞类型
- 原型污染
- 路径遍历
- ReDoS (正则表达式拒绝服务)
- 命令注入
- SSRF (服务器端请求伪造)
```

### 2. 版本状态

```markdown
## 版本状态分类

| 状态 | 描述 | 建议 |
|------|------|------|
| Latest | 最新版本 | 无需操作 |
| Outdated | 有新版本 | 考虑更新 |
| Deprecated | 已废弃 | 必须替换 |
| Unmaintained | 不再维护 | 建议替换 |
```

### 3. 许可证合规

```markdown
## 许可证检查

| 类型 | 示例 | 商业使用 |
|------|------|----------|
| Permissive | MIT, Apache-2.0 | ✅ 允许 |
| Weak Copyleft | LGPL, MPL | ⚠️ 条件允许 |
| Strong Copyleft | GPL, AGPL | ❌ 需评估 |
| Proprietary | 自定义 | ❌ 需授权 |
```

## 报告模板

```markdown
# 依赖分析报告

## 概述
- 总依赖数: X
- 直接依赖: X
- 间接依赖: X
- 安全问题: X
- 过时依赖: X

## 安全问题

### Critical
| 包名 | 当前版本 | 漏洞ID | 描述 | 修复版本 |
|------|----------|--------|------|----------|
| lodash | 4.17.15 | CVE-2020-8203 | 原型污染 | 4.17.19 |

### High
| 包名 | 当前版本 | 漏洞ID | 描述 | 修复版本 |
|------|----------|--------|------|----------|

## 过时依赖

| 包名 | 当前版本 | 最新版本 | 变更类型 |
|------|----------|----------|----------|
| react | 18.0.0 | 18.2.0 | minor |

## 建议
1. [立即修复的安全问题]
2. [建议更新的依赖]
3. [可移除的未使用依赖]
```

## 使用示例

### 示例: npm项目分析

```
用户: "分析这个项目的依赖"

执行:
1. 检测到 package-lock.json
2. 解析依赖树
3. 运行 npm audit
4. 检查过时包
5. 生成报告

输出:
# 依赖分析报告

## 概述
- 总依赖数: 156
- 直接依赖: 24
- 间接依赖: 132
- 安全问题: 2
- 过时依赖: 8

## 安全问题

### High
| 包名 | 当前版本 | 漏洞 | 修复版本 |
|------|----------|------|----------|
| axios | 0.21.1 | SSRF | 0.21.2 |

## 建议
1. 立即更新 axios 到 0.21.2+
2. 考虑更新 react 到 18.2.0
```

## 常用命令

```bash
# npm
npm audit
npm outdated
npm ls --depth=0

# yarn
yarn audit
yarn outdated
yarn list --depth=0

# pip
pip-audit
pip list --outdated
pipdeptree

# poetry
poetry show --outdated
poetry show --tree
```

## 最佳实践

1. **定期检查**: 至少每周检查依赖更新
2. **锁定版本**: 使用锁文件确保一致性
3. **最小依赖**: 只安装必需的依赖
4. **安全更新**: 优先处理安全漏洞
5. **版本范围**: 使用合理的版本范围

## 相关技能

- [security-auditor](../../domains/security/security-auditor) - 安全审计
- [ci-cd-pipeline](../../domains/devops/ci-cd-pipeline) - CI/CD流水线
- [code-review](../code-review) - 代码审查
