# Trae Skills - Official MCP Skill Marketplace

> 🔌 **Model Context Protocol Skills for Trae IDE by ByteDance**
> 
> Industry-standard skill collection built on the MCP protocol, providing production-grade tools for AI-assisted development.

---

## ✨ Quick Overview

| Metric | Status |
|--------|--------|
| 📦 **MCP Servers** | 16 Production-Grade |
| 🔧 **AI Tools** | 52 |
| ⚡ **User Prompts** | 21 |
| 📄 **Context Resources** | 6 |
| ✅ **TypeScript Validated** | 0 Errors |
| 🎯 **Trae Optimized** | 100% Ready |

---

## 🚀 Installation for Trae IDE

This skill collection is **natively optimized** for Trae IDE. The MCP protocol allows the Trae Agent system to automatically discover and utilize all available tools.

### One-Click Activation

1. Open **Trae IDE**
2. Navigate to **Skills Marketplace**
3. Search for **Trae Official Skills**
4. Click **Install**

### Manual Setup

Add to your Trae configuration:

```json
{
  "mcpServers": {
    "trae-skills": {
      "command": "node",
      "args": ["./packages/cli/index.js", "mcp"]
    }
  }
}
```

---

## 📦 Skill Catalog

### 🧱 Core Foundation

| Server | Icon | Categories | Rating | Key Features |
|--------|------|------------|--------|--------------|
| **git** | 📦 | Version Control | Beginner | Branch management, diff, conventional commits |
| **terminal** | 💻 | System | Advanced | Sandboxed command execution, npm, shell |
| **code-review** | 🔍 | Code Quality | Intermediate | Static analysis, bug detection, code scan |

### 🔧 Development Actions

| Server | Icon | Categories | Rating | Key Features |
|--------|------|------------|--------|--------------|
| **test-generator** | 🧪 | Testing | Intermediate | Unit tests, coverage reports, TDD workflow |
| **documentation** | 📚 | Docs | Beginner | JSDoc generation, README, API documentation |
| **search** | 🔍 | Code Analysis | Intermediate | Regex search, symbol lookup, reference tracking |
| **code-generator** | ⚡ | Generation | Intermediate | CRUD APIs, component templates, project detection |
| **dependency-analyzer** | 📦 | Security | Intermediate | NPM audit, unused packages, version checks |

### ⚛️ Technology Stack

| Server | Icon | Categories | Rating | Key Features |
|--------|------|------------|--------|--------------|
| **react** | ⚛️ | Frontend | Intermediate | Hooks, component patterns, memo optimization |
| **typescript** | 📘 | Types | Advanced | Type safety, generics, type best practices |
| **docker** | 🐳 | DevOps | Intermediate | Dockerfile, multi-stage build, compose |

### 🛡️ Quality & Security

| Server | Icon | Categories | Rating | Key Features |
|--------|------|------------|--------|--------------|
| **security-auditor** | 🔒 | Security | Advanced | Secret scanning, OWASP top 10, vulnerability scan |
| **performance-optimizer** | ⚡ | Performance | Advanced | Build speed, bundle analysis, dead code detection |

### 🔄 Standard Workflows

| Server | Icon | Categories | Rating | Key Features |
|--------|------|------------|--------|--------------|
| **coding-workflow** | 🚀 | Workflow | Intermediate | Feature branches, TDD cycle, PR preparation |
| **debugging-workflow** | 🔧 | Troubleshooting | Advanced | System info, log analysis, root cause verification |
| **refactoring-workflow** | ♻️ | Refactoring | Advanced | Safety checks, incremental refactoring, validation |

---

## 🎯 Why This is Built for Trae IDE

### Native MCP Integration

We follow the **official Model Context Protocol** specification used by Anthropic and Trae IDE:

- ✅ **Standard Tool Primitives** - AI agent automatically knows how to call every tool
- ✅ **Rich Context Resources** - Automatic context injection for the LLM
- ✅ **User Prompt Templates** - One-click standardized workflows
- ✅ **Fully Typed Interfaces** - No more implicit "any" types

### Trae Platform Optimizations

Every skill includes platform-specific metadata:

```typescript
.forTrae({
  categories: ['Version Control', 'Core'],
  rating: 'beginner',
  features: ['Git Operations', 'Code Review']
})
```

This powers Trae's marketplace features:
- 📂 Skill categorization and filtering
- ⭐ Difficulty rating for appropriate suggestions
- 🔍 Search and discovery optimization
- 🎯 Context-aware skill recommendations

---

## 💻 Developer CLI

### List All MCP Servers

```bash
node packages/cli/index.js mcp
```

```
🔌 Trae MCP - Model Context Protocol Servers

Found 16 MCP Servers:

  📦  git@1.0.0 by Trae Official
      Git version control toolkit
      Tools: 4 | Prompts: 1 | Resources: 1

  💻  terminal@1.0.0 by Trae Official
      Secure sandboxed terminal execution
      Tools: 4 | Prompts: 1 | Resources: 1

  ... 14 more
```

### Browse All AI Tools

```bash
node packages/cli/index.js mcp-tools
```

This shows every tool that the Trae Agent can invoke automatically.

---

## 🏗️ Architecture

### The MCP Three Primitive Model

```
┌─────────────────────────────────────────┐
│          Model Context Protocol         │
├─────────────────────────────────────────┤
│                                         │
│  🔧 TOOLS                               │
│     • AI-executable functions           │
│     • Strongly typed parameters         │
│     • Pure async execution              │
│                                         │
│  ⚡ PROMPTS                             │
│     • User-facing workflow templates    │
│     • Argument validation               │
│     • Standardized LLM instructions     │
│                                         │
│  📄 RESOURCES                           │
│     • Automatic context injection       │
│     • URI-addressable content           │
│     • Live, up-to-date data             │
│                                         │
└─────────────────────────────────────────┘
```

### Directory Structure

```
trae-skill/
├── mcp/                          # All MCP Skill Servers
│   ├── git/
│   ├── terminal/
│   ├── code-review/
│   └── ... 13 more skills
│
├── packages/
│   ├── core/                     # MCP Core Framework
│   │   ├── mcp/types.ts          # Type definitions
│   │   ├── mcp/builder.ts        # Fluent builder API
│   │   └── mcp/registry.ts       # Server registry
│   │
│   └── cli/                      # Command line interface
│
├── tsconfig.json
├── package.json
└── README.md
```

---

## 🔨 Building Your Own Trae Skill

### Quick Template

```typescript
import { createMCPServer } from '@trae/skills'

export default createMCPServer({
  name: 'my-awesome-skill',
  version: '1.0.0',
  description: 'What your skill does',
  icon: '✨'
})
  .forTrae({
    categories: ['Your Category'],
    rating: 'intermediate',
    features: ['Feature 1', 'Feature 2']
  })
  .addTool({
    name: 'tool_name',
    description: 'Clear description for AI agent',
    parameters: {
      param1: {
        type: 'string',
        description: 'What this parameter means',
        required: true
      }
    },
    execute: async (params) => {
      return { result: 'your implementation' }
    }
  })
  .addPrompt({
    name: 'my-workflow',
    description: 'For users to click and run',
    generate: async (args) => `
      Your LLM prompt template here
    `
  })
  .build()
```

See `mcp/template/index.ts` for a complete starter.

---

## 📋 Changelog

### v1.0.0 - Official Marketplace Release

- ✅ **16 Production MCP Servers** ready for Trae IDE
- ✅ **52 Tools** with complete type definitions
- ✅ **21 Prompt Templates** for standardized workflows
- ✅ **6 Context Resources** for automatic injection
- ✅ **Platform Metadata** for marketplace discovery
- ✅ **TypeScript 0 Errors** validation
- ✅ **MCP Protocol 100% compatible** with Trae/Anthropic standard

---

## 🤝 Contributing

We welcome contributions to grow the Trae Skill Marketplace!

1. **Fork** the repository
2. Create your feature: `git checkout -b feature/amazing-skill`
3. Build following the MCP standard template
4. Add `forTrae()` platform metadata
5. Validate: `npx tsc --noEmit`
6. Open a **Pull Request**

---

## 📄 License

MIT © Trae Official

---

> Built with ❤️ for the **Trae IDE Developer Community**
> 
> *This is the official skill collection maintained by Trae Team*
