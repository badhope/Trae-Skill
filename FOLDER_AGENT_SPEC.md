# Folder as Agent Specification

## Overview

This specification defines a standard format for creating self-contained agent definitions that can be packaged as folders and uploaded to any AI platform (such as Doubao, Claude, Cursor, etc.). The "Folder as Agent" concept provides a convenient way to define agent behavior through structured configuration files.

## Core Concept

An agent folder contains all necessary configuration, instructions, and knowledge for an AI to execute specific tasks. When uploaded to an AI platform, the AI reads the folder contents and executes according to the defined workflows.

## Folder Structure

```
agent-folder/
├── agent.yaml          # Required - Agent metadata and capabilities
├── system-prompt.md    # Required - Agent instructions and guidelines
├── workflow/           # Required - Workflow definitions
│   ├── intent.yaml     # Intent recognition rules
│   ├── stages.yaml     # Workflow stages and outputs
│   └── tools.yaml      # Available tools and parameters
├── knowledge/          # Optional - Domain knowledge base
├── tests/              # Optional - Test cases for validation
└── outputs/            # Auto-created - Generated outputs
```

## File Specifications

### 1. agent.yaml (Required)

Defines the agent's identity, capabilities, and execution parameters.

```yaml
version: "1.0.0"
id: "agent-unique-id"
name: "Agent Display Name"
description: "Brief description of what this agent does"
author: "Author Name"
tags:
  - "tag1"
  - "tag2"

capabilities:
  - id: "capability-id"
    name: "Capability Name"
    description: "What this capability enables"
    keywords:
      - "keyword1"
      - "keyword2"

tools:
  - id: "tool-id"
    name: "Tool Name"
    required: true
    fallback: "What to do if tool is unavailable"

execution:
  maxIterations: 50
  defaultTimeout: 60000
  enableReflection: true
  requireConfirmation: false

output:
  format: "markdown"
  includeSteps: true
  includeConfidence: true
  includeRecommendations: true
```

### 2. system-prompt.md (Required)

Defines the agent's role, responsibilities, and operational guidelines. This is read by the AI as its primary instruction set.

**Content Guidelines:**
- Define the agent's identity and role
- Specify core responsibilities
- Establish operational guidelines and constraints
- Define output standards and formats
- Include error handling protocols

### 3. workflow/intent.yaml (Required)

Defines how user input maps to workflows through keyword-based intent matching.

```yaml
version: "1.0.0"
intents:
  - id: "intent-id"
    name: "Intent Name"
    description: "Description of this intent"
    keywords:
      - "trigger phrase 1"
      - "trigger phrase 2"
    requiredTools:
      - "tool-id"
    workflow: "workflow-id-to-execute"
```

### 4. workflow/stages.yaml (Required)

Defines the sequential stages for each workflow.

```yaml
version: "1.0.0"
workflows:
  - id: "workflow-id"
    name: "Workflow Name"
    description: "Purpose and scope of this workflow"
    stages:
      - id: "stage-id"
        name: "Stage Name"
        description: "What happens in this stage"
        required: true
        timeout: 30000
        outputs:
          - "output-file-name.md"
```

### 5. workflow/tools.yaml (Required)

Documents available tools and their parameters for reference.

```yaml
version: "1.0.0"
tools:
  - id: "tool-id"
    name: "Tool Display Name"
    description: "What this tool does"
    category: "tool-category"
    parameters:
      - name: "parameter-name"
        type: "string|number|boolean"
        required: true|false
        description: "Parameter description"
```

### 6. knowledge/ (Optional)

Contains domain-specific knowledge files in Markdown format.

### 7. tests/ (Optional)

Contains test cases for validation.

## Execution Flow

1. **Intent Recognition**: AI reads `workflow/intent.yaml` and matches user input to an intent
2. **Workflow Selection**: Selects the corresponding workflow from `workflow/stages.yaml`
3. **Stage Execution**: Executes each stage sequentially:
   - Read stage definition
   - Execute tasks with available tools
   - Validate outputs
   - Record confidence score
4. **Result Compilation**: Collects outputs from all stages
5. **Reflection**: Generates summary and recommendations

## Platform Compatibility

The agent folder format is designed to work with:

| Platform | Status | Notes |
|----------|--------|-------|
| Doubao | Full Support | Native folder upload |
| Claude Desktop | Full Support | Folder context |
| Cursor | Full Support | Project context |
| Windsurf | Full Support | File operations |
| Generic MCP | Full Support | Standardized tools |

## Best Practices

1. **Keep it Simple**: Start with minimal configuration
2. **Use Clear Names**: Use descriptive IDs and names
3. **Define Outputs**: Specify expected outputs for each stage
4. **Include Fallbacks**: Provide fallback strategies for unavailable tools
5. **Test Thoroughly**: Create test cases to validate behavior
6. **Document Everything**: Maintain clear documentation

## Versioning

- Use semantic versioning in `agent.yaml`
- Maintain backward compatibility when updating

## Example Usage

**User**: Uploads the folder to Doubao
**AI**: Reads `system-prompt.md`, `agent.yaml`, and workflow files
**User**: "Create a React todo app"
**AI**: 
  1. Matches to "new-project" intent
  2. Executes "full-project-workflow"
  3. Runs through all stages sequentially
  4. Produces complete project structure

## Conclusion

The Folder as Agent specification provides a simple, portable way to define agent behavior using standard file formats. It enables users to create reusable agent definitions that work across multiple AI platforms without modification.
