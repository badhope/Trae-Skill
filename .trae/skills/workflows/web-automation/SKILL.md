---
name: web-automation
description: "Tier 2: Web automation and browser operations. Click buttons, fill forms, navigate pages via natural language. Keywords: web automation, browser automation, DOM操作, 网页自动化"
layer: workflow
role: web-operator
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - tool-use
  - human-in-the-loop
tags:
  - automation
  - browser
  - web
  - dom
---

# Web Automation

## Overview

Web automation and browser operations via natural language.

## Key Capabilities

- DOM understanding and analysis
- Click buttons and links
- Fill forms and inputs
- Navigate between pages
- Extract data from pages
- Screenshot and capture
- Safe operation with validation

## Safety Features

- Operation whitelist/blacklist
- Data anonymization
- Custom knowledge base injection
- Human-in-the-loop confirmation
- Rollback capability

## Process Flow

1. **Analyze** - Understand DOM structure
2. **Plan** - Plan operation sequence
3. **Execute** - Perform operations safely
4. **Verify** - Confirm operation success
5. **Report** - Report results

## Example Usage

```
"Add a new user configuration to this admin panel"
"Fill out this form with test data"
"Navigate to settings and change the theme"
"Extract all product information from this page"
"Generate a user manual for this website"
```

## Tools & Integration

- DOM manipulation layer
- Event-driven communication
- Pure frontend (no backend required)
- CDN/NPM installation
- Custom LLM endpoint support
