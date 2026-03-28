---
name: css-tailwind
description: "Tailwind CSS expert for utility-first styling, responsive design, and component patterns. Keywords: tailwind, css, responsive, utility, styling"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
invoked_by:
  - coding-workflow
  - frontend-react
  - frontend-vue
capabilities:
  - tailwind_setup
  - responsive_design
  - component_styling
  - dark_mode
  - custom_theme
---

# CSS Tailwind

Tailwind CSS样式专家。

## 适用场景

- 设置Tailwind CSS
- 创建响应式布局
- 构建组件库
- 自定义Tailwind主题
- 暗黑模式实现

## 配置

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { /* ... */ }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
};
```

## 组件模式

### Button

```tsx
const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-primary-600 text-white hover:bg-primary-700',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base'
      }
    }
  }
);
```

### 响应式布局

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {/* 响应式网格 */}
</div>
```

### 暗黑模式

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  {/* 自动适配暗黑模式 */}
</div>
```

## 工具函数

```typescript
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
```

## 相关技能

- [frontend-react](../react) - React开发
- [frontend-vue](../vue) - Vue开发
