---
name: "repo-analysis"
description: "Analyzes repository structure, locates files, and summarizes architecture. Invoke when working with unfamiliar codebase or need to understand project structure."
---

# Repo Analysis Skill

Tools and methodology for understanding unfamiliar code repositories.

## When to Use

- Working with a new/unfamiliar codebase
- Need to understand project structure
- Need to locate specific files or code
- Need to summarize project architecture
- Onboarding to a new project

## Analysis Workflows

### 1. Analyze Repository Structure

Use `analyze-repository-structure` for comprehensive analysis:

**Information Collected:**
- Project overview (type, tech stack, complexity)
- Directory structure analysis
- Key configuration files
- Module breakdown
- Entry points and dependencies

**Output:**
- Project map
- Technology stack summary
- Module responsibilities
- Key file locations

### 2. Locate Bug-Related Files

Use `locate-bug-related-files` for targeted search:

**Search Strategy:**
1. Extract bug characteristics
2. Analyze error message/stack trace
3. Search by keywords
4. Search by module relevance
5. Narrow down candidates

**Confidence Scoring:**
- High (>70%): Direct evidence from stack trace
- Medium (40-70%): Functional relevance
- Low (<40%): Possible but uncertain

### 3. Summarize Project Architecture

Use `summarize-project-architecture` for high-level overview:

**Summary Includes:**
- Architecture pattern
- Component interaction
- Data flow
- Technology decisions
- Design principles

## Repository Understanding Checklist

When analyzing a new repository:

1. **Read README** - Understand project purpose
2. **Check package.json** - Learn dependencies and scripts
3. **Explore src/** - Understand code organization
4. **Review config files** - Learn build and deployment
5. **Find entry points** - Know where to start

## Common Patterns

### Web Application
```
src/
├── components/    # UI components
├── pages/         # Page components
├── services/      # API calls
├── stores/       # State management
├── utils/        # Helper functions
└── App.tsx        # Root component
```

### Backend API
```
src/
├── controllers/   # Request handlers
├── services/     # Business logic
├── repositories/ # Data access
├── models/       # Data models
├── middleware/   # Express middleware
└── routes/       # Route definitions
```

### Library/SDK
```
src/
├── index.ts       # Main export
├── core/         # Core functionality
├── utils/        # Utilities
└── types/        # Type definitions
```

## Key Files to Identify

| File Type | Purpose | Priority |
|-----------|---------|----------|
| README.md | Project overview | 🔴 Essential |
| package.json | Dependencies | 🔴 Essential |
| tsconfig.json | TypeScript config | 🟡 Important |
| .env.example | Environment vars | 🟡 Important |
| entry files | App start point | 🔴 Essential |
| route files | API/Page routes | 🟡 Important |

## Related Prompts

- `prompt-task-repo-analysis-analyze-repository-structure`
- `prompt-task-repo-analysis-locate-bug-related-files`
- `prompt-task-repo-analysis-summarize-project-architecture`

## Related Skills

- `debugging` - use after understanding structure to fix issues
- `coding` - understand implementation details
