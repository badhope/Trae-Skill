---
name: design-to-code
description: "Tier 2: Convert design mockups to production code. Figma, Sketch, images to HTML/CSS/React. Keywords: design to code, figma to code, mockup to code, 设计稿转代码"
layer: workflow
role: design-engineer
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - research-workflow
  - coding-workflow
  - code-review
tags:
  - design
  - figma
  - code-generation
  - frontend
---

# Design to Code

## Overview

Convert design mockups to production-ready code.

## Key Capabilities

- Figma design import
- Image/Sketch upload
- Layout understanding
- Component extraction
- Responsive code generation
- Pixel-perfect replication
- Interactive component support

## Supported Input Formats

- Figma files/links
- Sketch files
- PNG/JPG images
- Adobe XD
- Wireframe tools

## Output Formats

- HTML/CSS
- React components
- Vue components
- Tailwind CSS
- Next.js
- Svelte

## Process Flow

1. **Import** - Load design file
2. **Analyze** - Understand layout and components
3. **Extract** - Extract components and styles
4. **Generate** - Generate clean code
5. **Optimize** - Refine and optimize
6. **Validate** - Pixel-perfect check

## Example Usage

```
"Convert this Figma design to React + Tailwind"
"Turn this mockup into a responsive website"
"Extract components from this design file"
"Make this design interactive with animations"
```

## Quality Features

- Semantic HTML
- Accessibility (WCAG)
- Performance optimized
- Clean, maintainable code
- Design system integration
