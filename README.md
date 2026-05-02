# 🚀 MCP Mega-Agent Platform / MCP Super Agent Platform

[![CI Status](https://github.com/badhope/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/badhope/skills/actions)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Standard-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌐 Language / 语言

- [English](#english-documentation)
- [中文](#chinese-documentation)

---

# English Documentation

## 🎯 Overview

**MCP Mega-Agent Platform** is the world's first MCP-based Mega-Agent Platform with **96+ professional tools** and **13 expert engines**. Build once, run on **every LLM platform** that supports the MCP standard.

> One architecture to rule them all.

## ⚡️ Quick Start (Just 3 Steps!)

### Step 1: Clone the Project
```bash
git clone https://github.com/badhope/skills.git
cd skills
```

### Step 2: Give It to Your LLM
Simply drag and drop the `skills` folder into your AI interface, or configure it as a workspace:

**For Claude Desktop:**
- Open Settings → Plugins → Add the `skills` folder path
- Or drag the folder directly into Claude's file panel

**For Cursor:**
- Use `@load ./skills` command
- Or add as workspace in Settings → Workspaces

**For Windsurf:**
- Add `skills` directory to your workspace
- Or use the Cascade commands to load the folder

**For Cline / Roo Code:**
- Configure MCP servers to point to `skills/mcp`

### Step 3: Just Tell It What You Want!
Once the skills folder is loaded, simply describe your request in natural language:

```
"Build a React todo app"
"I need to build a React login page with JWT authentication"
"My API is returning errors, help me debug"
"Deploy my Node.js app to AWS"
"Crawl product data from this e-commerce website"
```

The system will automatically:
1. Analyze your intent
2. Select appropriate expert engines
3. Discover and invoke relevant tools
4. Execute the task
5. Return the complete result

**That's it!** No complex configuration, no setup needed. Just clone, give it to your AI, and start building!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Intent                            │
│            (Natural Language Input)                       │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    Intent Analyzer                         │
│              (clarify module)                              │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Expert Engines (13)                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   AI Agent  │ │  Full-Stack │ │  DevOps     │            │
│  │  Architect  │ │  Engineer   │ │  Engineer   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │  Security   │ │  Database  │ │  Testing    │            │
│  │  Auditor    │ │  Specialist │ │  Master     │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   Platform Services                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Tool     │ │   Message  │ │   Auth      │            │
│  │  Registry   │ │    Bus      │ │  Manager    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │  Protocol   │ │  Monitoring │                            │
│  │  Standard   │ │   System    │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Tools (96+)                                │
│  filesystem │ terminal │ search │ code-generator │ ...     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Available Modules (96+ Tools)

### 🤖 AI Agent Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `agent-autonomous` | Autonomous task execution | 6 tools |
| `agent-multi` | Multi-agent collaboration | 6 tools |
| `agent-reflection` | Self-reflection system | 5 tools |
| `agent-devkit` | AI agent development kit | 5 tools |
| `agent-coordinator` | Agent coordination hub | 11 expert roles |
| `agent-unified-toolkit` | Unified tool calling | 5 tools |
| `agent-persistence` | Persistent storage | 8 tools |

### 🔧 Development Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `core-dev-kit` | Core development toolkit | 8 tools |
| `frontend-dev-kit` | Frontend development | 10 tools |
| `backend-dev-kit` | Backend development | 12 tools |
| `api-dev` | API development | 8 tools |
| `code-generator` | Code generation | 6 tools |
| `code-review` | Code review | 5 tools |
| `refactoring-workflow` | Code refactoring | 6 tools |
| `debugging-workflow` | Debugging tools | 7 tools |

### 🎨 Frontend Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `react` | React development | 8 tools |
| `typescript` | TypeScript support | 6 tools |
| `ui-design-kit` | UI design | 7 tools |
| `colors` | Color utilities | 5 tools |

### 🗄️ Database Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `database` | Database operations | 9 tools |
| `mongodb` | MongoDB support | 7 tools |
| `redis` | Redis support | 6 tools |

### ☁️ DevOps Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `docker` | Docker management | 8 tools |
| `kubernetes` | K8s management | 9 tools |
| `git` | Git operations | 7 tools |
| `github` | GitHub integration | 6 tools |
| `gitlab` | GitLab integration | 5 tools |
| `aws` | AWS services | 10 tools |
| `aliyun` | Aliyun services | 8 tools |
| `cloudflare` | Cloudflare CDN | 6 tools |
| `vercel` | Vercel deployment | 5 tools |
| `ssh` | SSH management | 6 tools |
| `terminal` | Terminal operations | 7 tools |
| `network` | Network tools | 8 tools |
| `system-admin` | System administration | 9 tools |

### 🔒 Security Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `security-auditor` | Security auditing | 8 tools |
| `secrets` | API key management | 5 tools |
| `auth` | RBAC access control | 9 tools |

### 🧪 Testing Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `qa-dev-kit` | QA toolkit | 7 tools |
| `testing-toolkit` | Testing utilities | 6 tools |
| `test-generator` | Test generation | 5 tools |
| `performance-optimizer` | Performance optimization | 8 tools |

### 📊 Data Engineering
| Module | Description | Tools |
|--------|-------------|-------|
| `data-crawler` | Web crawling & data processing | 4 tools |
| `csv` | CSV operations | 5 tools |
| `spreadsheet` | Spreadsheet operations | 6 tools |
| `json` | JSON utilities | 5 tools |
| `yaml` | YAML utilities | 4 tools |

### 🌐 Platform Services
| Module | Description | Tools |
|--------|-------------|-------|
| `tool-registry` | Dynamic tool discovery & registration | 6 tools |
| `protocol` | Standardized calling protocol | 7 tools |
| `message-bus` | Pub/sub messaging & state sync | 9 tools |
| `monitoring` | Logging, metrics & error tracking | 11 tools |
| `clarify` | Intent analysis & requirement clarification | 5 tools |
| `libraries` | Library recommendations | 4 tools |
| `proxy` | Proxy configuration | 4 tools |

### 📚 Documentation Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `documentation` | Technical documentation | 6 tools |
| `markdown` | Markdown processing | 5 tools |
| `pdf` | PDF operations | 4 tools |
| `academic-writing` | Academic writing | 7 tools |

### 🔍 Search & Utility
| Module | Description | Tools |
|--------|-------------|-------|
| `search` | Search operations | 5 tools |
| `web-search` | Web search | 4 tools |
| `search-tools` | Advanced search | 6 tools |
| `filesystem` | File operations | 8 tools |
| `datetime` | Date/time utilities | 5 tools |
| `math` | Math operations | 6 tools |
| `regex` | Regex utilities | 4 tools |
| `compression` | Compression tools | 5 tools |
| `encoding` | Encoding utilities | 4 tools |
| `env` | Environment variables | 5 tools |

### 🌐 Integrations
| Module | Description | Tools |
|--------|-------------|-------|
| `browser-automation` | Puppeteer automation | 8 tools |
| `web-crawler` | Web crawling | 6 tools |
| `site-generator` | Site generation | 7 tools |
| `website-builder` | Website builder | 9 tools |
| `game-dev-toolkit` | Game development | 8 tools |
| `puppeteer` | Browser automation | 7 tools |
| `jira` | Jira integration | 5 tools |
| `fun` | Entertainment tools | 6 tools |

---

## 💡 Usage Examples

### Example 1: Build a React App
```
User: "Create a React todo app with local storage"
System automatically:
- Selects frontend-dev-kit + react
- Invokes code-generator
- Creates component structure
- Implements local storage
- Returns complete code
```

### Example 2: Debug an Issue
```
User: "My API returns 500 error, help me debug"
System automatically:
- Selects debugging-workflow
- Invokes error analysis
- Checks API endpoints
- Reviews error logs
- Provides solution
```

### Example 3: Deploy to Cloud
```
User: "Deploy my Node.js app to AWS"
System automatically:
- Selects aws + docker
- Creates Dockerfile
- Sets up CI/CD
- Configures infrastructure
- Deploys application
```

### Example 4: Data Crawling
```
User: "Crawl product data from an e-commerce site"
System automatically:
- Selects data-crawler + web-crawler
- Analyzes page structure
- Extracts data
- Processes and cleans
- Exports to CSV/JSON
```

### Example 5: Security Audit
```
User: "Run a security audit on my code"
System automatically:
- Selects security-auditor
- Scans for vulnerabilities
- Checks dependencies
- Reviews authentication
- Generates report
```

### Example 6: Multi-Agent Collaboration
```
User: "Design and implement a new feature with team collaboration"
System automatically:
- Creates agent team (PM + Tech Lead + Dev + QA)
- Coordinates discussions
- Synthesizes decisions
- Implements code
- Runs tests
```

### Example 7: Database Operations
```
User: "Create a user table with pagination"
System automatically:
- Selects database + mongodb/redis
- Creates schema
- Implements CRUD
- Adds pagination
- Returns queries
```

### Example 8: Requirement Clarification
```
User: "I want to make something AI-related"
System automatically:
- Invokes clarify module
- Analyzes vague intent
- Generates clarifying questions
- Helps refine requirements
- Suggests appropriate tools
```

---

## 🔧 API Reference

### Core Functions

```typescript
import {
  processUserRequest,
  discoverTools,
  initializePlatform,
  getSystemInfo,
  listAllTools
} from 'skills'

// Initialize the platform
await initializePlatform()

// Process user intent (main entry point)
const result = await processUserRequest("your task description")

// Discover relevant tools
const tools = discoverTools("react development")

// Get system information
const info = await getSystemInfo()
```

### Tool Registry

```typescript
import { toolRegistry } from 'skills/mcp/tool-registry'

// Register a new tool
await toolRegistry.registerTool(serverId, toolId, metadata, handler)

// Discover tools
const tools = await toolRegistry.discoverTools({ category: 'frontend' })

// Invoke a tool
const result = await toolRegistry.invokeTool(toolId, params)
```

### Message Bus

```typescript
import { messageBus } from 'skills/mcp/message-bus'

// Subscribe to messages
const subscriptionId = messageBus.subscribe('topic', handler)

// Publish a message
messageBus.publish({ topic: 'agent.task', payload: {...}, priority: 'high' })

// State synchronization
stateSyncManager.updateState(agentId, state)
```

---

## 📋 Protocol Standard

### Tool Call Format

```json
{
  "tool_name": "module_name/tool_name",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  },
  "timeout": 30000,
  "retries": 3
}
```

### Response Format

```json
{
  "success": true,
  "data": {...},
  "metadata": {
    "toolId": "module/tool",
    "version": "1.0.0",
    "executionTime": 123
  }
}
```

### Error Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameters",
    "details": {...},
    "retryable": true
  }
}
```

---

## 🏷️ Tags & Categories

### Module Categories
- `ai-agent` - AI agent development
- `frontend` - Frontend development
- `backend` - Backend development
- `database` - Database operations
- `devops` - DevOps & infrastructure
- `security` - Security & secrets
- `testing` - Testing & QA
- `data` - Data engineering
- `documentation` - Documentation
- `utility` - Utilities
- `integration` - Third-party integrations
- `platform` - Platform services

### Tool Tags
- `code-generation` - Code generation
- `analysis` - Analysis tools
- `automation` - Automation
- `monitoring` - Monitoring
- `optimization` - Optimization
- `collaboration` - Collaboration
- `discovery` - Discovery
- `management` - Management

---

## 🔌 MCP Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Desktop | ✅ Native | Official MCP support |
| Cursor Composer | ✅ Native | Full MCP integration |
| Windsurf Cascade | ✅ Native | Built for agentic workflows |
| Cline / Roo Code | ✅ Compatible | MCP tool protocol |
| Any MCP Client | ✅ Standard | Model Context Protocol |

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Expert Engines** | 13 |
| **MCP Tools** | 96+ |
| **AI Agents** | 7 dedicated modules |
| **Platform Services** | 5 core services |
| **TypeScript Coverage** | 100% |
| **Architecture Version** | 3.1 |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Contribution Guidelines

1. **Report Issues**: Create an Issue describing the problem
2. **Submit Fixes**: Fork the repository and submit a Pull Request
3. **Add New Features**: Create an Issue first to discuss the design
4. **Code Standards**: Follow TypeScript best practices

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

# Chinese Documentation

## 🎯 Overview

**MCP Mega-Agent Platform** is the world's first MCP-based Mega-Agent Platform with **96+ professional tools** and **13 expert engines**. Build once, run on **every LLM platform** that supports the MCP standard.

> One architecture to rule them all.

## ⚡️ Quick Start (Just 3 Steps!)

### Step 1: Clone the Project
```bash
git clone https://github.com/badhope/skills.git
cd skills
```

### Step 2: Give It to Your LLM
Simply drag and drop the `skills` folder into your AI interface, or configure it as a workspace:

**For Claude Desktop:**
- Open Settings → Plugins → Add the `skills` folder path
- Or drag the folder directly into Claude's file panel

**For Cursor:**
- Use `@load ./skills` command
- Or add as workspace in Settings → Workspaces

**For Windsurf:**
- Add `skills` directory to your workspace
- Or use the Cascade commands to load the folder

**For Cline / Roo Code:**
- Configure MCP servers to point to `skills/mcp`

### Step 3: Just Tell It What You Want!
Once the skills folder is loaded, simply describe your request in natural language:

```
"帮我创建一个React待办应用"
"I need to build a React login page with JWT authentication"
"我的API报错了，帮我调试"
"Deploy my Node.js app to AWS"
"爬取这个电商网站的产品数据"
```

The system will automatically:
1. Analyze your intent
2. Select appropriate expert engines
3. Discover and invoke relevant tools
4. Execute the task
5. Return the complete result

**That's it!** No complex configuration, no setup needed. Just clone, give it to your AI, and start building!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Intent                            │
│            (Natural Language Input)                       │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    Intent Analyzer                         │
│              (clarify module)                              │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Expert Engines (13)                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   AI Agent  │ │  Full-Stack │ │  DevOps     │            │
│  │  Architect  │ │  Engineer   │ │  Engineer   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │  Security   │ │  Database  │ │  Testing    │            │
│  │  Auditor    │ │  Specialist │ │  Master     │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   Platform Services                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Tool     │ │   Message  │ │   Auth      │            │
│  │  Registry   │ │    Bus      │ │  Manager    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │  Protocol   │ │  Monitoring │                            │
│  │  Standard   │ │   System    │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────┬─────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Tools (96+)                                │
│  filesystem │ terminal │ search │ code-generator │ ...     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Available Modules (96+ Tools)

### 🤖 AI Agent Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `agent-autonomous` | Autonomous task execution | 6 tools |
| `agent-multi` | Multi-agent collaboration | 6 tools |
| `agent-reflection` | Self-reflection system | 5 tools |
| `agent-devkit` | AI agent development kit | 5 tools |
| `agent-coordinator` | Agent coordination hub | 11 expert roles |
| `agent-unified-toolkit` | Unified tool calling | 5 tools |
| `agent-persistence` | Persistent storage | 8 tools |

### 🔧 Development Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `core-dev-kit` | Core development toolkit | 8 tools |
| `frontend-dev-kit` | Frontend development | 10 tools |
| `backend-dev-kit` | Backend development | 12 tools |
| `api-dev` | API development | 8 tools |
| `code-generator` | Code generation | 6 tools |
| `code-review` | Code review | 5 tools |
| `refactoring-workflow` | Code refactoring | 6 tools |
| `debugging-workflow` | Debugging tools | 7 tools |

### 🎨 Frontend Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `react` | React development | 8 tools |
| `typescript` | TypeScript support | 6 tools |
| `ui-design-kit` | UI design | 7 tools |
| `colors` | Color utilities | 5 tools |

### 🗄️ Database Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `database` | Database operations | 9 tools |
| `mongodb` | MongoDB support | 7 tools |
| `redis` | Redis support | 6 tools |

### ☁️ DevOps Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `docker` | Docker management | 8 tools |
| `kubernetes` | K8s management | 9 tools |
| `git` | Git operations | 7 tools |
| `github` | GitHub integration | 6 tools |
| `gitlab` | GitLab integration | 5 tools |
| `aws` | AWS services | 10 tools |
| `aliyun` | Aliyun services | 8 tools |
| `cloudflare` | Cloudflare CDN | 6 tools |
| `vercel` | Vercel deployment | 5 tools |
| `ssh` | SSH management | 6 tools |
| `terminal` | Terminal operations | 7 tools |
| `network` | Network tools | 8 tools |
| `system-admin` | System administration | 9 tools |

### 🔒 Security Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `security-auditor` | Security auditing | 8 tools |
| `secrets` | API key management | 5 tools |
| `auth` | RBAC access control | 9 tools |

### 🧪 Testing Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `qa-dev-kit` | QA toolkit | 7 tools |
| `testing-toolkit` | Testing utilities | 6 tools |
| `test-generator` | Test generation | 5 tools |
| `performance-optimizer` | Performance optimization | 8 tools |

### 📊 Data Engineering
| Module | Description | Tools |
|--------|-------------|-------|
| `data-crawler` | Web crawling & data processing | 4 tools |
| `csv` | CSV operations | 5 tools |
| `spreadsheet` | Spreadsheet operations | 6 tools |
| `json` | JSON utilities | 5 tools |
| `yaml` | YAML utilities | 4 tools |

### 🌐 Platform Services
| Module | Description | Tools |
|--------|-------------|-------|
| `tool-registry` | Dynamic tool discovery & registration | 6 tools |
| `protocol` | Standardized calling protocol | 7 tools |
| `message-bus` | Pub/sub messaging & state sync | 9 tools |
| `monitoring` | Logging, metrics & error tracking | 11 tools |
| `clarify` | Intent analysis & requirement clarification | 5 tools |
| `libraries` | Library recommendations | 4 tools |
| `proxy` | Proxy configuration | 4 tools |

### 📚 Documentation Modules
| Module | Description | Tools |
|--------|-------------|-------|
| `documentation` | Technical documentation | 6 tools |
| `markdown` | Markdown processing | 5 tools |
| `pdf` | PDF operations | 4 tools |
| `academic-writing` | Academic writing | 7 tools |

### 🔍 Search & Utility
| Module | Description | Tools |
|--------|-------------|-------|
| `search` | Search operations | 5 tools |
| `web-search` | Web search | 4 tools |
| `search-tools` | Advanced search | 6 tools |
| `filesystem` | File operations | 8 tools |
| `datetime` | Date/time utilities | 5 tools |
| `math` | Math operations | 6 tools |
| `regex` | Regex utilities | 4 tools |
| `compression` | Compression tools | 5 tools |
| `encoding` | Encoding utilities | 4 tools |
| `env` | Environment variables | 5 tools |

### 🌐 Integrations
| Module | Description | Tools |
|--------|-------------|-------|
| `browser-automation` | Puppeteer automation | 8 tools |
| `web-crawler` | Web crawling | 6 tools |
| `site-generator` | Site generation | 7 tools |
| `website-builder` | Website builder | 9 tools |
| `game-dev-toolkit` | Game development | 8 tools |
| `puppeteer` | Browser automation | 7 tools |
| `jira` | Jira integration | 5 tools |
| `fun` | Entertainment tools | 6 tools |

---

## 💡 Usage Examples

### Example 1: Build a React App
```
User: "Create a React todo app with local storage"
System automatically:
- Selects frontend-dev-kit + react
- Invokes code-generator
- Creates component structure
- Implements local storage
- Returns complete code
```

### Example 2: Debug an Issue
```
User: "My API returns 500 error, help me debug"
System automatically:
- Selects debugging-workflow
- Invokes error analysis
- Checks API endpoints
- Reviews error logs
- Provides solution
```

### Example 3: Deploy to Cloud
```
User: "Deploy my Node.js app to AWS"
System automatically:
- Selects aws + docker
- Creates Dockerfile
- Sets up CI/CD
- Configures infrastructure
- Deploys application
```

### Example 4: Data Crawling
```
User: "Crawl product data from an e-commerce site"
System automatically:
- Selects data-crawler + web-crawler
- Analyzes page structure
- Extracts data
- Processes and cleans
- Exports to CSV/JSON
```

### Example 5: Security Audit
```
User: "Run a security audit on my code"
System automatically:
- Selects security-auditor
- Scans for vulnerabilities
- Checks dependencies
- Reviews authentication
- Generates report
```

### Example 6: Multi-Agent Collaboration
```
User: "Design and implement a new feature with team collaboration"
System automatically:
- Creates agent team (PM + Tech Lead + Dev + QA)
- Coordinates discussions
- Synthesizes decisions
- Implements code
- Runs tests
```

### Example 7: Database Operations
```
User: "Create a user table with pagination"
System automatically:
- Selects database + mongodb/redis
- Creates schema
- Implements CRUD
- Adds pagination
- Returns queries
```

### Example 8: Requirement Clarification
```
User: "I want to make something AI-related"
System automatically:
- Invokes clarify module
- Analyzes vague intent
- Generates clarifying questions
- Helps refine requirements
- Suggests appropriate tools
```

---

## 🔧 API Reference

### Core Functions

```typescript
import {
  processUserRequest,
  discoverTools,
  initializePlatform,
  getSystemInfo,
  listAllTools
} from 'skills'

// Initialize the platform
await initializePlatform()

// Process user intent (main entry point)
const result = await processUserRequest("your task description")

// Discover relevant tools
const tools = discoverTools("react development")

// Get system information
const info = await getSystemInfo()
```

### Tool Registry

```typescript
import { toolRegistry } from 'skills/mcp/tool-registry'

// Register a new tool
await toolRegistry.registerTool(serverId, toolId, metadata, handler)

// Discover tools
const tools = await toolRegistry.discoverTools({ category: 'frontend' })

// Invoke a tool
const result = await toolRegistry.invokeTool(toolId, params)
```

### Message Bus

```typescript
import { messageBus } from 'skills/mcp/message-bus'

// Subscribe to messages
const subscriptionId = messageBus.subscribe('topic', handler)

// Publish a message
messageBus.publish({ topic: 'agent.task', payload: {...}, priority: 'high' })

// State synchronization
stateSyncManager.updateState(agentId, state)
```

---

## 📋 Protocol Standard

### Tool Call Format

```json
{
  "tool_name": "module_name/tool_name",
  "parameters": {
    "param1": "value1",
    "param2": "value2"
  },
  "timeout": 30000,
  "retries": 3
}
```

### Response Format

```json
{
  "success": true,
  "data": {...},
  "metadata": {
    "toolId": "module/tool",
    "version": "1.0.0",
    "executionTime": 123
  }
}
```

### Error Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameters",
    "details": {...},
    "retryable": true
  }
}
```

---

## 🏷️ Tags & Categories

### Module Categories
- `ai-agent` - AI agent development
- `frontend` - Frontend development
- `backend` - Backend development
- `database` - Database operations
- `devops` - DevOps & infrastructure
- `security` - Security & secrets
- `testing` - Testing & QA
- `data` - Data engineering
- `documentation` - Documentation
- `utility` - Utilities
- `integration` - Third-party integrations
- `platform` - Platform services

### Tool Tags
- `code-generation` - Code generation
- `analysis` - Analysis tools
- `automation` - Automation
- `monitoring` - Monitoring
- `optimization` - Optimization
- `collaboration` - Collaboration
- `discovery` - Discovery
- `management` - Management

---

## 🔌 MCP Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Desktop | ✅ Native | Official MCP support |
| Cursor Composer | ✅ Native | Full MCP integration |
| Windsurf Cascade | ✅ Native | Built for agentic workflows |
| Cline / Roo Code | ✅ Compatible | MCP tool protocol |
| Any MCP Client | ✅ Standard | Model Context Protocol |

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Expert Engines** | 13 |
| **MCP Tools** | 96+ |
| **AI Agents** | 7 dedicated modules |
| **Platform Services** | 5 core services |
| **TypeScript Coverage** | 100% |
| **Architecture Version** | 3.1 |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Contribution Guidelines

1. **Report Issues**: Create an Issue describing the problem
2. **Submit Fixes**: Fork the repository and submit a Pull Request
3. **Add New Features**: Create an Issue first to discuss the design
4. **Code Standards**: Follow TypeScript best practices

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

> **The future is multi-platform.**
>
> Don't build for one LLM. Build for **all** LLMs. 🚀