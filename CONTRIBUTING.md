# Contributing to AI Skill & Prompt Repository

Thank you for your interest in contributing to this repository. This document provides guidelines and instructions for contributing.

---

## Ways to Contribute

### Report Issues
- Report broken prompts or incorrect outputs
- Report missing functionality
- Report registry inconsistencies
- Suggest new assets or improvements

### Contribute Content
- Add new prompts following the template
- Add new skills following the skill template
- Add new workflows for common task patterns
- Improve existing asset documentation

### Improve Documentation
- Fix typos or unclear explanations
- Improve selection_hints and when_to_use descriptions
- Add usage examples
- Translate documentation

---

## Contribution Guidelines

### Prompt Contribution Standards

1. **Follow the Template**
   - Use `docs/guides/prompt-template.md` as reference
   - Include all required metadata fields
   - Use consistent naming conventions

2. **Naming Convention**
   - File name: `prompt-<task>-<action>.md`
   - ID: `prompt-<category>-<specific-action>`

3. **Required Fields**
   ```yaml
   ---
   id: prompt-xxx-v1
   name: Clear Name
   summary: Brief description
   type: routing|system|task|workflow|tool-use|output|meta
   category: primary category
   sub_category: specific category
   when_to_use:
     - Specific use case 1
     - Specific use case 2
   when_not_to_use:
     - Specific non-use case 1
   input_requirements:
     - Required input 1
   output_shape:
     - Expected output 1
   tags: [tag1, tag2]
   status: active
   ---
   ```

4. **Quality Standards**
   - Prompts must be actionable and specific
   - Avoid vague or generic instructions
   - Include clear input/output specifications
   - Provide meaningful selection_hints

### Skill Contribution Standards

1. **Follow the Skill Template**
   - Use `docs/guides/skill-template.md` as reference
   - Include use cases and input/output definitions

2. **Naming Convention**
   - Directory: `skills/<category>/`
   - File: `skill-<name>.md`

### Registry Updates

When adding new assets, you must also update the appropriate registry:

1. **New Prompt** → Add entry to `registry/prompts-registry.yaml`
2. **New Skill** → Add entry to `registry/skills-registry.yaml`
3. **New Tag** → Add entry to `registry/tags-registry.yaml`
4. **New Relationship** → Add entry to `registry/relations-registry.yaml`

### Workflow Contribution

1. **Follow the Workflow Template**
   - Use `docs/guides/workflow-template.md` as reference
   - Define clear steps and dependencies

2. **Documentation**
   - List all required prompts
   - Specify execution order
   - Include fallback strategies

---

## Process

### For Minor Changes
1. Fork the repository
2. Make your changes
3. Test locally if possible
4. Submit a pull request with clear description

### For Major Changes
1. Open an issue first to discuss
2. Get approval before implementing
3. Follow the full contribution workflow
4. Include tests and documentation

### Pull Request Guidelines
- Use clear, descriptive titles
- Reference related issues
- Describe what changed and why
- Include before/after if applicable

---

## Quality Checklist

Before submitting, verify:

- [ ] Prompt follows template structure
- [ ] All required fields are present
- [ ] Registry entry matches actual file
- [ ] No broken links or references
- [ ] Selection hints are helpful and specific
- [ ] when_to_use / when_not_to_use are not vague

---

## License

By contributing, you agree that your contributions will be licensed under:
- **CC BY 4.0** for content (prompts, skills, workflows, documentation)

---

## Questions?

If you have questions, please open an issue or contact the maintainers.

---

## Recognition

Contributors will be recognized in the README and CHANGELOG.

---

*Thank you for helping improve this repository!*
