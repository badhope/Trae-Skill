---
name: accessibility
description: "Web accessibility (a11y) implementation for WCAG compliance and inclusive design. Keywords: accessibility, a11y, wcag, aria, inclusive, 无障碍, 可访问性"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
languages:
  - html
  - typescript
frameworks:
  - axe-core
  - react-aria
invoked_by:
  - frontend-react
  - frontend-vue
  - code-review
capabilities:
  - wcag_compliance
  - aria_implementation
  - accessibility_testing
  - inclusive_design
triggers:
  keywords:
    - accessibility
    - a11y
    - wcag
    - aria
    - inclusive
    - screen reader
    - 无障碍
    - 可访问性
metrics:
  avg_execution_time: 3s
  success_rate: 0.94
  wcag_compliance_rate: 0.92
---

# Accessibility

Web无障碍(a11y)实现，用于WCAG合规和包容性设计。

## 目的

提供Web无障碍开发的最佳实践：
- WCAG合规指南
- ARIA实现技术
- 无障碍测试方法
- 包容性设计原则

## 能力

- **WCAG合规**: 确保符合WCAG标准
- **ARIA实现**: 实现ARIA属性
- **无障碍测试**: 测试无障碍功能
- **包容性设计**: 设计包容性用户体验

## WCAG原则

### 四大原则 (POUR)

| 原则 | 描述 | 示例 |
|------|------|------|
| Perceivable | 可感知 | 替代文本、字幕 |
| Operable | 可操作 | 键盘导航、焦点管理 |
| Understandable | 可理解 | 清晰语言、一致性 |
| Robust | 健壮 | 语义化HTML、兼容性 |

### 合规级别

| 级别 | 描述 | 要求 |
|------|------|------|
| A | 最低级别 | 必须满足 |
| AA | 推荐级别 | 大多数法规要求 |
| AAA | 最高级别 | 增强体验 |

## 常见实现

### 1. 替代文本

```html
<!-- 图片 -->
<img src="chart.png" alt="2024年销售增长图表：Q1增长15%，Q2增长20%">

<!-- 装饰性图片 -->
<img src="decoration.png" alt="" role="presentation">

<!-- 复杂图片 -->
<figure>
  <img src="diagram.png" aria-describedby="diagram-desc">
  <figcaption id="diagram-desc">
    详细描述图表内容和数据...
  </figcaption>
</figure>
```

### 2. 键盘导航

```html
<!-- 可聚焦元素 -->
<button tabindex="0">点击我</button>

<!-- 跳过导航链接 -->
<a href="#main-content" class="skip-link">跳到主要内容</a>
<main id="main-content">
  <!-- 主要内容 -->
</main>

<!-- 焦点管理 -->
<div role="dialog" aria-modal="true">
  <!-- 打开时聚焦到对话框 -->
  <!-- 关闭时恢复焦点 -->
</div>
```

### 3. ARIA属性

```html
<!-- 角色 -->
<nav role="navigation">
<main role="main">
<aside role="complementary">

<!-- 状态 -->
<button aria-pressed="true">已选中</button>
<input aria-invalid="true" aria-describedby="error-msg">

<!-- 标签 -->
<button aria-label="关闭菜单">×</button>
<nav aria-label="主导航">

<!-- 描述 -->
<input aria-describedby="password-hint">
<span id="password-hint">至少8个字符</span>

<!-- 实时区域 -->
<div aria-live="polite" aria-atomic="true">
  <!-- 动态内容更新 -->
</div>
```

### 4. 表单无障碍

```html
<form>
  <!-- 标签关联 -->
  <label for="email">邮箱地址</label>
  <input type="email" id="email" name="email" required>
  
  <!-- 错误提示 -->
  <div role="alert" id="email-error">
    请输入有效的邮箱地址
  </div>
  
  <!-- 字段集 -->
  <fieldset>
    <legend>联系方式</legend>
    <!-- 相关字段 -->
  </fieldset>
  
  <!-- 必填标识 -->
  <label for="name">
    姓名 <span aria-hidden="true">*</span>
    <span class="sr-only">（必填）</span>
  </label>
</form>
```

## React实现

### 无障碍组件

```tsx
import { useRef, useEffect } from 'react';

// 模态框焦点管理
function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef(null);
  const previousFocus = useRef(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      {children}
    </div>
  );
}

// 跳过链接
function SkipLink() {
  return (
    <a href="#main-content" className="skip-link">
      跳到主要内容
    </a>
  );
}

// 无障碍按钮
function IconButton({ icon, label, onClick }) {
  return (
    <button
      aria-label={label}
      onClick={onClick}
    >
      {icon}
    </button>
  );
}
```

## 测试工具

### 自动化测试

```javascript
// Jest + jest-axe
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

test('Button should have no accessibility violations', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});

// Playwright
test('Page accessibility', async ({ page }) => {
  await page.goto('/');
  const accessibilitySnapshot = await page.accessibility.snapshot();
  // 验证快照
});
```

### 手动测试清单

```markdown
## 键盘测试
- [ ] Tab键可以导航所有交互元素
- [ ] Enter/Space可以激活按钮
- [ ] Escape可以关闭模态框
- [ ] 焦点顺序符合视觉顺序
- [ ] 焦点可见

## 屏幕阅读器测试
- [ ] 所有图片有替代文本
- [ ] 表单标签正确关联
- [ ] 标题层级正确
- [ ] 动态内容有通知

## 视觉测试
- [ ] 对比度足够 (4.5:1)
- [ ] 文字可缩放至200%
- [ ] 不只依赖颜色传达信息
- [ ] 焦点可见
```

## 常见问题修复

### 问题1: 缺少替代文本

```html
<!-- 问题 -->
<img src="logo.png">

<!-- 修复 -->
<img src="logo.png" alt="公司Logo">
```

### 问题2: 键盘无法操作

```html
<!-- 问题 -->
<div onclick="handleClick()">点击</div>

<!-- 修复 -->
<button onclick="handleClick()">点击</button>
<!-- 或 -->
<div 
  onclick="handleClick()"
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  tabIndex={0}
  role="button"
>
  点击
</div>
```

### 问题3: 对比度不足

```css
/* 问题 */
.text {
  color: #999;
  background: #fff;
  /* 对比度: 2.8:1 - 不合格 */
}

/* 修复 */
.text {
  color: #595959;
  background: #fff;
  /* 对比度: 7:1 - 合格 */
}
```

## 最佳实践

1. **语义化HTML**: 使用正确的HTML元素
2. **渐进增强**: 确保基础功能可用
3. **持续测试**: 集成无障碍测试到CI/CD
4. **用户测试**: 包含残障用户测试
5. **文档化**: 记录无障碍决策

## 相关技能

- [frontend-react](../frontend/react) - React开发
- [frontend-vue](../frontend/vue) - Vue开发
- [css-tailwind](../frontend/css-tailwind) - Tailwind CSS
- [e2e-test](../testing/e2e-test) - E2E测试
