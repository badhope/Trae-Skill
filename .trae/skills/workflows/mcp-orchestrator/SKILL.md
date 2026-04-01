---
name: mcp-orchestrator
description: "Tier 2: MCP (Model Context Protocol) tool orchestration. Auto-discover, install, configure, and use MCP tools. Keywords: MCP orchestrator, MCP tools, tool chain, MCP工具编排"
layer: workflow
role: mcp-manager
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - tool-use
  - research-workflow
  - human-in-the-loop
tags:
  - mcp
  - tools
  - orchestration
  - automation
---

# MCP Orchestrator

## Overview

MCP (Model Context Protocol) tool discovery, installation, and orchestration.

## Key Capabilities

- MCP tool discovery (3000+ tools)
- Auto installation and configuration
- Tool chain orchestration
- Multi-tool workflow coordination
- API key management
- Dependency resolution
- Health monitoring

## MCP Tool Categories

- Design: Figma, Sketch, Adobe XD
- Media: Image generation, video, audio
- Productivity: Calendar, email, docs
- Development: Git, Docker, CI/CD
- Data: Database, analytics, visualization
- AI: LLM APIs, embeddings, vector DBs

## Process Flow

1. **Discover** - Find relevant MCP tools
2. **Install** - Auto-install and configure
3. **Orchestrate** - Chain tools together
4. **Execute** - Run multi-tool workflow
5. **Monitor** - Track execution and health

## Example Usage

```
"Use Figma + MiniMax to convert this design to a website with voice narration"
"Install and use MCP tools for database migration"
"Create a workflow that uses 5 different MCP tools"
"Manage my MCP tool configurations"
```

## Features

- Smart tool recommendation
- Auto API key setup
- Dependency conflict resolution
- Workflow templates
- Execution history
- Performance monitoring
