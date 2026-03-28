---
name: i18n
description: "Internationalization (i18n) and localization (l10n) for multi-language applications. Keywords: i18n, l10n, internationalization, localization, translation, 国际化, 本地化"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
languages:
  - typescript
  - javascript
frameworks:
  - i18next
  - react-intl
  - next-intl
invoked_by:
  - frontend-react
  - frontend-vue
  - nextjs
capabilities:
  - i18n_architecture
  - translation_management
  - locale_handling
  - formatting
triggers:
  keywords:
    - i18n
    - l10n
    - internationalization
    - localization
    - translation
    - multi-language
    - 国际化
    - 本地化
    - 多语言
metrics:
  avg_execution_time: 2s
  success_rate: 0.96
  coverage_rate: 0.95
---

# Internationalization (i18n)

国际化和本地化，用于多语言应用开发。

## 目的

提供国际化开发的最佳实践：
- i18n架构设计
- 翻译管理
- 区域设置处理
- 格式化处理

## 能力

- **i18n架构**: 设计国际化架构
- **翻译管理**: 管理翻译资源
- **区域处理**: 处理区域设置
- **格式化**: 处理日期、数字、货币格式

## 核心概念

### 国际化 vs 本地化

| 概念 | 描述 | 示例 |
|------|------|------|
| i18n | 国际化 | 设计支持多语言的架构 |
| l10n | 本地化 | 翻译和区域适配 |

### 区域标识

```
语言代码: zh, en, ja, ko
区域代码: CN, US, JP, KR
完整标识: zh-CN, en-US, ja-JP
```

## React实现

### react-i18next

```tsx
// i18n配置
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          welcome: "Welcome",
          greeting: "Hello, {{name}}!"
        }
      },
      zh: {
        translation: {
          welcome: "欢迎",
          greeting: "你好，{{name}}！"
        }
      }
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

// 使用
import { useTranslation } from 'react-i18next';

function App() {
  const { t, i18n } = useTranslation();
  
  return (
    <div>
      <h1>{t('welcome')}</h1>
      <p>{t('greeting', { name: 'User' })}</p>
      <button onClick={() => i18n.changeLanguage('zh')}>
        切换中文
      </button>
    </div>
  );
}
```

### next-intl (Next.js)

```tsx
// middleware.ts
import createMiddleware from 'next-intl/middleware';

export default createMiddleware({
  locales: ['en', 'zh', 'ja'],
  defaultLocale: 'en'
});

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)']
};

// 使用
import { useTranslations } from 'next-intl';

function Page() {
  const t = useTranslations('common');
  return <h1>{t('welcome')}</h1>;
}
```

## Vue实现

### vue-i18n

```vue
<!-- i18n配置 -->
<script setup>
import { createI18n } from 'vue-i18n';

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: {
      welcome: 'Welcome',
      greeting: 'Hello, {name}!'
    },
    zh: {
      welcome: '欢迎',
      greeting: '你好，{name}！'
    }
  }
});
</script>

<!-- 使用 -->
<template>
  <div>
    <h1>{{ $t('welcome') }}</h1>
    <p>{{ $t('greeting', { name: 'User' }) }}</p>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';

const { t, locale } = useI18n();

const switchLanguage = () => {
  locale.value = locale.value === 'en' ? 'zh' : 'en';
};
</script>
```

## 格式化

### 日期格式化

```typescript
// 使用Intl.DateTimeFormat
const formatDate = (date: Date, locale: string) => {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};

// en-US: "March 28, 2026"
// zh-CN: "2026年3月28日"
// ja-JP: "2026年3月28日"
```

### 数字格式化

```typescript
// 使用Intl.NumberFormat
const formatNumber = (number: number, locale: string) => {
  return new Intl.NumberFormat(locale).format(number);
};

// en-US: "1,234,567.89"
// de-DE: "1.234.567,89"
// fr-FR: "1 234 567,89"
```

### 货币格式化

```typescript
const formatCurrency = (amount: number, locale: string, currency: string) => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency
  }).format(amount);
};

// en-US, USD: "$1,234.56"
// zh-CN, CNY: "¥1,234.56"
// ja-JP, JPY: "￥1,235"
```

### 复数处理

```typescript
// i18next复数
const messages = {
  en: {
    item_one: "{{count}} item",
    item_other: "{{count}} items"
  },
  zh: {
    item: "{{count}} 个项目"
  },
  ru: {
    item_one: "{{count}} элемент",
    item_few: "{{count}} элемента",
    item_many: "{{count}} элементов"
  }
};

// 使用
t('item', { count: 5 });
```

## 翻译管理

### 翻译文件结构

```
locales/
├── en/
│   ├── common.json
│   ├── auth.json
│   └── dashboard.json
├── zh/
│   ├── common.json
│   ├── auth.json
│   └── dashboard.json
└── ja/
    ├── common.json
    ├── auth.json
    └── dashboard.json
```

### 翻译文件示例

```json
// locales/en/common.json
{
  "welcome": "Welcome",
  "greeting": "Hello, {{name}}!",
  "navigation": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "errors": {
    "required": "This field is required",
    "invalid_email": "Please enter a valid email"
  }
}
```

### 命名空间

```tsx
// 按功能模块划分命名空间
i18n.init({
  ns: ['common', 'auth', 'dashboard'],
  defaultNS: 'common'
});

// 使用
const { t } = useTranslation('auth');
t('login.title');
```

## RTL支持

### RTL布局

```css
/* 自动RTL */
[dir="rtl"] {
  text-align: right;
}

/* 使用逻辑属性 */
.element {
  margin-inline-start: 1rem;
  padding-inline-end: 1rem;
  border-inline-start: 1px solid;
}

/* 替代 */
.element {
  /* 不要用 margin-left */
  margin-inline-start: 1rem;
}
```

### React RTL

```tsx
import { I18nextProvider } from 'react-i18next';

function App() {
  const { i18n } = useTranslation();
  const isRTL = ['ar', 'he', 'fa'].includes(i18n.language);
  
  return (
    <div dir={isRTL ? 'rtl' : 'ltr'}>
      {/* 应用内容 */}
    </div>
  );
}
```

## 最佳实践

### 1. 文本提取

```typescript
// 不要硬编码文本
<button>Submit</button>  // ❌

// 使用翻译键
<button>{t('submit')}</button>  // ✅
```

### 2. 避免字符串拼接

```typescript
// 不要拼接
const message = t('hello') + ' ' + name;  // ❌

// 使用插值
const message = t('greeting', { name });  // ✅
```

### 3. 上下文翻译

```json
{
  "save": "Save",
  "save_changes": "Save Changes",
  "save_draft": "Save Draft"
}
```

### 4. 翻译质量

- 保持翻译键简洁有意义
- 提供翻译上下文注释
- 使用专业翻译服务
- 定期审查翻译质量

## 工具推荐

| 工具 | 描述 | 用途 |
|------|------|------|
| i18next | JavaScript国际化框架 | 翻译管理 |
| Crowdin | 翻译管理平台 | 协作翻译 |
| Lokalise | 本地化平台 | 翻译工作流 |
| Phrase | 本地化平台 | 翻译管理 |
| formatjs | ICU消息格式 | 复杂格式化 |

## 相关技能

- [frontend-react](../react) - React开发
- [frontend-vue](../vue) - Vue开发
- [nextjs](../nextjs) - Next.js全栈
- [accessibility](../accessibility) - 无障碍访问
