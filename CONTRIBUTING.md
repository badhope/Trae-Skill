# Contributing to DevFlow Agent

**English** | [简体中文](#简体中文)

---

## 🎯 How to Contribute

We welcome contributions! Here are the ways you can help:

### Report Bugs
- Search existing issues first
- Create a detailed issue with:
  - Clear title and description
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, Node version, etc.)

### Suggest Features
- Search existing issues first
- Create an issue with:
  - Clear use case
  - Expected behavior
  - Alternative solutions considered

### Pull Requests

#### Process
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

#### Guidelines
- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic
- Write clear commit messages

#### Branch Naming
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Adding tests

---

## 🏗️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/devflow-agent.git
cd devflow-agent

# Install dependencies
npm install

# Run tests
npm test

# Type check
npm run typecheck

# Lint
npm run lint
```

---

## 📝 Style Guide

### Code
- Use TypeScript
- Follow ESLint rules
- Add JSDoc comments for public APIs
- Write meaningful variable names

### Documentation
- Use clear, concise language
- Add examples where appropriate
- Keep docs up to date

### Git Commits
Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance

---

## 🧪 Testing

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

---

# 简体中文

## 🎯 如何贡献

我们欢迎各种形式的贡献！以下是您可以参与的方式：

### 报告问题
- 先搜索现有问题
- 创建详细的问题报告，包括：
  - 清晰的标题和描述
  - 复现步骤
  - 预期与实际行为
  - 环境详情（操作系统、Node版本等）

### 建议功能
- 先搜索现有问题
- 创建问题报告，包括：
  - 清晰的使用场景
  - 预期行为
  - 已考虑的替代方案

### 提交 Pull Request

#### 流程
1. Fork 项目仓库
2. 创建功能分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'feat: 添加新功能'`
4. 推送到分支: `git push origin feature/amazing-feature`
5. 打开 Pull Request

#### 规范
- 遵循现有代码风格
- 为新功能添加测试
- 更新相关文档
- 保持提交原子性
- 编写清晰的提交信息

#### 分支命名
- `feature/` - 新功能
- `fix/` - Bug修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 添加测试

---

## 🏗️ 开发环境设置

```bash
# 克隆你的 fork
git clone https://github.com/YOUR_USERNAME/devflow-agent.git
cd devflow-agent

# 安装依赖
npm install

# 运行测试
npm test

# 类型检查
npm run typecheck

# 代码检查
npm run lint
```

---

## 📝 代码规范

### 代码
- 使用 TypeScript
- 遵循 ESLint 规则
- 为公共 API 添加 JSDoc 注释
- 使用有意义的变量名

### 文档
- 使用清晰简洁的语言
- 适当添加示例
- 保持文档更新

### Git 提交
遵循 [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` - 新功能
- `fix:` - Bug 修复
- `docs:` - 文档更新
- `style:` - 格式调整
- `refactor:` - 代码重构
- `test:` - 添加测试
- `chore:` - 维护工作

---

## 🧪 测试

```bash
# 运行所有测试
npm test

# 运行并查看覆盖率
npm run test:coverage

# 监视模式
npm run test:watch
```

---

## 📄 许可证

贡献代码即表示您同意您的贡献将遵循 MIT 许可证。
