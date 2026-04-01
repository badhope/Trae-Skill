---
name: one-click-project
description: "Tier 3: One-click project development from natural language. Build complete websites/apps with a single prompt. Keywords: one-click project, auto development, full stack, 一键开发, 一句话开发"
layer: workflow
role: project-lead
tier: 3
version: 5.0.0
architecture: lead-worker-handoff
invokes:
  - requirements-collector
  - technical-design-doc
  - project-scaffold
  - system-architecture
  - coding-workflow
  - full-stack-development
  - progress-reporter
  - iteration-controller
tags:
  - full-stack
  - auto-dev
  - one-click
  - project
---

# One-Click Project

## Overview

Tier 3: Complete project development from a single natural language prompt.

## Key Capabilities

- One-prompt full-stack development
- Auto requirements gathering and validation
- Auto technical design and architecture
- Auto project scaffolding
- Auto code generation and implementation
- Auto testing and quality checks
- Auto deployment preparation

## Process Flow (Lead-Worker + Handoff)

### Lead Agent
1. **Understand** - Parse user's natural language request
2. **Plan** - Create comprehensive project plan
3. **Assign** - Decompose into worker teams
4. **Monitor** - Track progress and coordinate
5. **Review** - Quality check and final integration

### Worker Teams (Handoff within teams)

**Team 1: Planning**
- requirements-collector → technical-design-doc → system-architecture

**Team 2: Development**
- project-scaffold → coding-workflow → full-stack-development

**Team 3: Quality**
- testing → code-review → security-audit

**Team 4: Deployment**
- docker → ci-cd-pipeline → launch-checklist

## Example Usage

```
"Build me a coffee shop website with:
- Menu display with photos
- Online ordering system
- Table booking
- Customer reviews
- Responsive design"
```

The skill will automatically:
1. ✅ Analyze requirements
2. ✅ Design architecture
3. ✅ Generate complete codebase
4. ✅ Run tests
5. ✅ Prepare for deployment

## Output Artifacts

- Complete working project
- Technical documentation
- Test reports
- Deployment guide
- User manual
