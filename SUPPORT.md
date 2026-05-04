# Support

## Getting Help

If you need help with Thesis Specialist, here are some resources:

### Documentation

- [English README](README.md) - Main documentation in English
- [Chinese README](README_zh.md) - Main documentation in Chinese
- [agent.yaml](agent.yaml) - Platform configuration reference
- [system-prompt.md](system-prompt.md) - System prompt documentation

### GitHub Issues

For bugs and feature requests, please use GitHub Issues:

- [Bug Reports](https://github.com/badhope/Thesis-Specialist-Agent/issues/new?template=bug_report.md)
- [Feature Requests](https://github.com/badhope/Thesis-Specialist-Agent/issues/new?template=feature_request.md)
- [Questions](https://github.com/badhope/Thesis-Specialist-Agent/issues/new?template=question.md)

### Community

- **GitHub Discussions**: [ Discussions](https://github.com/badhope/Thesis-Specialist-Agent/discussions)

## Frequently Asked Questions

### Q: How do I use Thesis Specialist?

A: Simply download the folder and submit it to any LLM (Doubao, Claude, GPT, Gemini). The agent will automatically execute the complete thesis writing workflow.

### Q: Do I need to configure anything?

A: No! Thesis Specialist is designed to be zero-configuration. Just download and use.

### Q: Which LLMs are supported?

A: Any LLM that supports file/context loading, including:
- Doubao (豆包)
- Claude
- GPT-4
- Gemini
- Other MCP-compatible platforms

### Q: How do I report bugs?

A: Please use GitHub Issues with the bug report template. Include as much detail as possible.

### Q: Can I contribute?

A: Yes! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Troubleshooting

### Configuration Validation Fails

Run the validator manually:
```bash
python config-validator.py
```

### Tests Fail

Run tests with verbose output:
```bash
python -m unittest tests.test_agent -v
```

### Memory System Not Working

Check that the memory store files exist:
```bash
ls memory/stores/
```

## Maintenance

Thesis Specialist is actively maintained. Here's the maintenance status:

| Component | Status | Last Updated |
|-----------|--------|--------------|
| Core Platform | :white_check_mark: Active | 2026-05-04 |
| Expert Engines | :white_check_mark: Active | 2026-05-04 |
| Meta Agents | :white_check_mark: Active | 2026-05-04 |
| Tools | :white_check_mark: Active | 2026-05-04 |
| Documentation | :white_check_mark: Active | 2026-05-04 |

## Contact

For other questions or concerns:
- GitHub Issues: [Open an Issue](https://github.com/badhope/Thesis-Specialist-Agent/issues)
