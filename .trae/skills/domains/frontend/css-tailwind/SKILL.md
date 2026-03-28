---
name: css-tailwind
description: "Tailwind CSS utility-first styling for rapid UI development. Keywords: tailwind, css, styling, utility-first, tailwind css, 样式"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
languages:
  - css
  - typescript
frameworks:
  - tailwindcss
  - postcss
invoked_by:
  - coding-workflow
  - frontend-react
  - frontend-vue
capabilities:
  - utility_styling
  - responsive_design
  - component_styling
  - theme_customization
triggers:
  keywords:
    - tailwind
    - css
    - styling
    - utility-first
    - tailwind css
    - 样式
metrics:
  avg_execution_time: 2s
  success_rate: 0.98
  styling_quality: 0.92
---

# Tailwind CSS

Tailwind CSS实用优先样式框架，用于快速UI开发。

## 目的

提供Tailwind CSS的最佳实践：
- 实用类样式
- 响应式设计
- 组件样式
- 主题定制

## 能力

- **实用样式**: 使用实用类快速样式
- **响应式设计**: 响应式布局实现
- **组件样式**: 组件级样式封装
- **主题定制**: 自定义主题配置

## 核心概念

### 实用优先

```html
<!-- 传统CSS -->
<button class="btn-primary">Click</button>

<!-- Tailwind -->
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
  Click
</button>
```

### 响应式前缀

| 前缀 | 断点 |
|------|------|
| sm | 640px |
| md | 768px |
| lg | 1024px |
| xl | 1280px |
| 2xl | 1536px |

```html
<div class="text-sm md:text-base lg:text-lg">
  响应式文字
</div>
```

## 配置

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

## 常用布局

### Flexbox

```html
<div class="flex items-center justify-between">
  <span>Left</span>
  <span>Right</span>
</div>

<div class="flex flex-col gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

### Grid

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-white p-4 rounded shadow">Card 1</div>
  <div class="bg-white p-4 rounded shadow">Card 2</div>
  <div class="bg-white p-4 rounded shadow">Card 3</div>
</div>
```

## 组件示例

### 按钮

```html
<!-- Primary Button -->
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded transition-colors">
  Primary
</button>

<!-- Secondary Button -->
<button class="border border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white font-bold py-2 px-4 rounded transition-colors">
  Secondary
</button>

<!-- Disabled Button -->
<button class="bg-gray-300 text-gray-500 font-bold py-2 px-4 rounded cursor-not-allowed" disabled>
  Disabled
</button>
```

### 卡片

```html
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <img class="w-full h-48 object-cover" src="image.jpg" alt="Card image">
  <div class="p-6">
    <h3 class="text-xl font-semibold mb-2">Card Title</h3>
    <p class="text-gray-600">Card description text here.</p>
    <button class="mt-4 bg-blue-500 text-white py-2 px-4 rounded">
      Action
    </button>
  </div>
</div>
```

### 表单

```html
<form class="space-y-4">
  <div>
    <label class="block text-sm font-medium text-gray-700">Email</label>
    <input type="email" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
  </div>
  
  <div>
    <label class="block text-sm font-medium text-gray-700">Password</label>
    <input type="password" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
  </div>
  
  <button type="submit" class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
    Submit
  </button>
</form>
```

## 暗色模式

```html
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  自动适配暗色模式
</div>
```

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // 或 'media'
}
```

## 最佳实践

1. **组件抽象**: 提取重复的类组合
2. **@apply**: 谨慎使用@apply指令
3. **一致性**: 遵循设计系统
4. **性能**: 启用JIT模式
5. **可维护性**: 使用语义化类名

## 相关技能

- [react](../react) - React开发
- [vue](../vue) - Vue开发
- [nextjs](../nextjs) - Next.js框架
- [accessibility](../accessibility) - 无障碍访问
