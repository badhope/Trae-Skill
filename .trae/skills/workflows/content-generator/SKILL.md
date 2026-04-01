---
name: content-generator
description: "Tier 2: Generate content - blog articles, product descriptions, documentation, marketing copy. Keywords: content generation, blog writing, article generator, 内容生成, 博客写作"
layer: workflow
role: content-specialist
tier: 2
version: 5.0.0
architecture: handoff-chain
invokes:
  - research-workflow
  - documentation
  - prompt-engineering
invoked_by:
  - full-stack-development
  - lead-agent
capabilities:
  - blog_article_generation
  - product_description_writing
  - technical_documentation
  - marketing_copy
triggers:
  keywords:
    - content generation
    - blog writing
    - article generator
    - write content
    - 内容生成
    - 博客写作
    - 写文章
  conditions:
    - "need blog articles"
    - "need product descriptions"
    - "need documentation"
metrics:
  avg_article_length: 800-1500 words
  articles_per_hour: 4
  quality_score: 0.82
---

# Content Generator - Tier 2

> **Tier 2 Skill**: Generate content - blogs, product descriptions, docs, marketing copy

## What is Content Generation?

Generate high-quality content for blogs, products, documentation, and more.

```
CONTENT TYPES:
  ├─ Blog Articles
  │  ├─ Tutorials
  │  ├─ How-to guides
  │  ├─ Opinion pieces
  │  └─ News & updates
  │
  ├─ Product Content
  │  ├─ Product descriptions
  │  ├─ Marketing copy
  │  └─ Landing pages
  │
  ├─ Documentation
  │  ├─ Technical docs
  │  ├─ API docs
  │  └─ User manuals
  │
  └─ Social Media
     ├─ Twitter/X threads
     ├─ LinkedIn posts
     └─ Blog snippets
```

## Content Types

| Type | Use Case | Output |
|------|----------|--------|
| **Blog Article** | Personal/company blog | 800-1500 word article |
| **Product Description** | E-commerce product page | 100-300 words |
| **Technical Doc** | Software documentation | 500-2000 words |
| **Marketing Copy** | Landing page/ads | 50-200 words |

## Handoff Chain

```
Topic Research ━━(handoff)━━► Outline Creation ━━(handoff)━━► Draft Writing ━━(handoff)━━► Editing & SEO ━━(handoff)━━► Final Review
     │                      │                     │                    │                   │
  ├─ Research topic    ├─ Create outline    ├─ Write draft      ├─ Edit & polish    ├─ Final check
  └─ Gather sources    └─ Structure        └─ Add examples      └─ SEO optimize     └─ Publish ready
```

## Phase 1: Topic Research

```yaml
purpose: "Research the topic"
state: researching
inputs:
  topic: "What is AI Agent?"
  target_audience: "developers"
  content_type: "blog_article"

actions:
  - skill: research-workflow
    task: "Research topic, gather sources"
    output: ResearchReport

output: TopicBrief
```

## Phase 2: Outline Creation

```yaml
purpose: "Create content outline"
state: outlining
inputs:
  topic_brief: {...}
  content_type: "blog_article"

structure:
  blog_article:
    - Title (H1)
    - Introduction
    - Section 1 (H2)
    - Section 2 (H2)
    - ...
    - Conclusion
    - Call to Action

output: ContentOutline
```

## Phase 3: Draft Writing

```yaml
purpose: "Write the first draft"
state: writing_draft
inputs:
  outline: {...}
  tone: "professional but friendly"
  length: "1000-1200 words"

actions:
  - Write each section
  - Add examples
  - Add code snippets (if technical)
  - Add images/placeholders

output: ContentDraft
```

## Phase 4: Editing & SEO

```yaml
purpose: "Edit, polish, and optimize"
state: editing
checks:
  - Grammar & spelling
  - Clarity & flow
  - Tone consistency
  - SEO keywords
  - Readability

optimizations:
  - Add meta description
  - Add headings (H2/H3)
  - Add internal links
  - Add alt text for images

output: PolishedContent
```

## Phase 5: Final Review

```yaml
purpose: "Final quality check"
state: final_review
quality_gate:
  checks:
    - "No grammar errors"
    - "Clear and readable"
    - "Meets length requirement"
    - "SEO optimized"
    - "Factually accurate"

output: FinalContent (ready to publish)
```

## Example: Blog Article Generation

```
REQUEST: "Write a blog article: 'What is an AI Agent?'"

PHASE 1: Research
  ✓ Research AI Agents
  ✓ Gather sources (OpenAI, Anthropic, etc.)
  ✓ Identify key points

PHASE 2: Outline
  ✓ Title: "What is an AI Agent? A Complete Guide for Developers"
  ✓ Introduction
  ✓ Section 1: What is an AI Agent?
  ✓ Section 2: Key Components
  ✓ Section 3: How Agents Work
  ✓ Section 4: Examples
  ✓ Conclusion

PHASE 3: Draft Writing
  ✓ Write 1,100 words
  ✓ Add code examples
  ✓ Add diagrams

PHASE 4: Editing & SEO
  ✓ Edit for clarity
  ✓ Add keywords: "AI Agent", "LLM Agent", "Autonomous Agent"
  ✓ Add meta description

PHASE 5: Final Review
  ✓ All checks pass
  ✓ Ready to publish!

RESULT: 1,100-word blog article, SEO optimized!
```

## Related Skills

- **research-workflow** - Research
- **documentation** - Documentation
- **prompt-engineering** - Prompt optimization
