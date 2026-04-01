---
name: ai-research-assistant
description: "Tier 2: AI research assistant - literature review, paper analysis, experiment design. Keywords: AI research, literature review, paper analysis, AI研究助手"
layer: workflow
role: research-assistant
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - research-workflow
  - documentation
  - problem-decomposer
tags:
  - research
  - ai
  - papers
  - literature
---

# AI Research Assistant

## Overview

AI research assistant for literature review, paper analysis, and experiment design.

## Key Capabilities

- Literature search and discovery
- Paper summarization and analysis
- Research gap identification
- Experiment design and planning
- Methodology comparison
- Citation management
- Research roadmap creation

## Research Workflows

### Literature Review
1. Search across arXiv, PubMed, IEEE, etc.
2. Filter by relevance, citations, date
3. Summarize key findings
4. Extract methodology and results
5. Create literature matrix

### Paper Analysis
- Abstract and introduction analysis
- Methodology breakdown
- Results and discussion
- Limitations and future work
- Code and data availability

### Experiment Design
- Hypothesis formulation
- Experimental setup
- Metric selection
- Baseline comparison
- Statistical analysis plan

## Process Flow

1. **Define** - Research topic and questions
2. **Search** - Discover relevant literature
3. **Analyze** - Summarize and synthesize
4. **Identify** - Find research gaps
5. **Design** - Plan experiments
6. **Report** - Generate research report

## Example Usage

```
"Do a literature review on transformer architectures"
"Analyze this paper and extract key findings"
"Help me design an experiment for my research"
"Find research gaps in this field"
"Create a research roadmap for the next 6 months"
```

## Output Artifacts

- Literature review report
- Paper summaries
- Research gap analysis
- Experiment design document
- Research roadmap
- Citation list
