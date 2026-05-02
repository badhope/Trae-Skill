# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this repository, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Instead, please send a private disclosure to the maintainers
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Any suggested fixes (optional)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will assess the severity and impact of the vulnerability
- **Status Updates**: We will provide updates on the progress every 3-5 business days
- **Resolution**: Once fixed, we will credit your contribution (if desired) in the release notes

### Scope

This security policy applies to:

- Prompt injection vulnerabilities
- Sensitive data exposure in prompts or documentation
- Malicious code in example scripts or configurations
- Dependency vulnerabilities (if applicable)

### Out of Scope

- Social engineering attacks
- Physical security issues
- Denial of service attacks on external services
- Issues caused by misuse of prompts

---

## Security Best Practices for Users

### Prompt Usage

1. **Validate AI Outputs**: Always validate outputs from AI systems, especially for code generation
2. **Sanitize Inputs**: Do not blindly trust user inputs processed through AI prompts
3. **Review Generated Code**: Generated code should be reviewed before production use
4. **Protect Secrets**: Never include sensitive information (API keys, passwords) in prompt inputs

### Repository Security

1. **Check Origins**: Only use prompts from trusted sources
2. **Review Changes**: Review all changes before incorporating them
3. **Backup**: Maintain backups of working prompts before major changes

---

## Content Licenses and Security

- **Apache-2.0** (code/scripts): Use freely with standard attribution
- **CC BY 4.0** (prompts/content): Share with attribution as specified in LICENSE-CONTENT

---

## Updates to This Policy

This security policy may be updated periodically. The latest version will always be available in this repository.

---

*Thank you for helping keep this community and repository secure.*
