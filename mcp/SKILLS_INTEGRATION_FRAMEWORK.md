# 技能模块统一集成框架

## 概述

本文档描述了三大专业技能模块的统一集成架构、API接口规范和使用指南。

## 模块列表

| 模块名称 | 版本 | 等级 | 核心工具数量 | 主要功能 |
|---------|------|------|-------------|---------|
| **site-generator** | 2.0.0 | intermediate | 8 | 网站与小程序快速创建、模板管理、一键部署 |
| **browser-automation** | 2.0.0 | advanced | 12 | 浏览器自动化、隐身模式、人类行为模拟 |
| **web-crawler** | 2.0.0 | advanced | 7 | 多数据源爬取、反爬处理、数据格式化 |

---

## 一、网站与小程序快速创建工具 (site-generator)

### 技术架构

- **模板引擎**: 基于Node.js生态的官方脚手架集成
- **框架支持**: Astro, Next.js, Vite, Nuxt, SvelteKit, UniApp, Taro 等
- **部署能力**: Vercel, Netlify, Cloudflare Pages, 微信开发者工具

### 核心工具 API

#### 1. `site_list_templates` - 列出可用模板

**参数:**
```typescript
{
  category?: string    // 可选: blog, ecommerce, portfolio, docs, miniprogram
  framework?: string   // 可选: astro, next, vite, react, vue
}
```

**返回示例:**
```json
{
  "total": 18,
  "categories": ["博客", "电商", "文档", "作品集", "小程序"],
  "templates": [
    {
      "id": "astro-minimal",
      "name": "Astro 极简博客",
      "framework": "astro",
      "features": ["博客", "极简设计", "SEO优化"],
      "deployTarget": ["vercel", "netlify", "cloudflare"]
    }
  ]
}
```

#### 2. `site_create` - 创建新项目

**参数:**
```typescript
{
  template: string,        // 模板ID，必填
  projectName: string,     // 项目名称
  outputDir: string,       // 输出目录
  installDeps: boolean,    // 是否自动安装依赖
  config?: object          // 自定义配置
}
```

#### 3. `site_config` - 配置项目

**参数:**
```typescript
{
  projectDir: string,
  title?: string,
  description?: string,
  theme?: string,
  colors?: object,
  navigation?: array,
  socialLinks?: object
}
```

#### 4. `site_deploy` - 一键部署

**参数:**
```typescript
{
  projectDir: string,
  target: "vercel" | "netlify" | "cloudflare" | "wx",
  token?: string,
  projectName?: string,
  domain?: string
}
```

---

## 二、浏览器自动化操作技能 (browser-automation)

### 技术架构

- **核心引擎**: Puppeteer Core + Chrome DevTools Protocol
- **反爬技术**: 隐身脚本(Stealth Scripts) + 指纹随机化
- **行为模拟**: 贝塞尔曲线鼠标移动、人类打字模式、自然滚动

### 核心工具 API

#### 1. `browser_screenshot` - 高级截图

**参数:**
```typescript
{
  url: string,              // 必填
  outputFile: string,
  preset: "chrome" | "chromeMac" | "mobile" | "firefox" | "edge",
  stealthMode: boolean,     // 启用反检测
  fullPage: boolean,
  delaySeconds: number,     // 加载后等待
  emulateHuman: boolean,    // 模拟人类滚动
  proxy: string             // 代理服务器
}
```

**反检测特性:**
- 移除 `navigator.webdriver` 标识
- 修复 `window.chrome` 运行时
- Canvas 指纹噪声注入
- 插件数组模拟
- 语言和平台指纹模拟

#### 2. `browser_fill_form` - 自动填表

**参数:**
```typescript
{
  url: string,
  formData: object,         // {字段选择器: 值}
  submit: boolean,
  humanTyping: boolean,     // 模拟打字速度
  randomDelay: boolean      // 字段间随机延迟
}
```

#### 3. `browser_click_elements` - 批量点击

**参数:**
```typescript
{
  url: string,
  selectors: string[],      // CSS选择器数组
  waitForNavigation: boolean,
  humanMove: boolean        // 模拟鼠标移动
}
```

#### 4. `browser_export_cookies` - 导出会话

**参数:**
```typescript
{
  url: string,
  outputFile: string,
  format: "json" | "netscape" | "string"
}
```

#### 5. `browser_test_stealth` - 反爬检测

**参数:**
```typescript
{
  url: string,
  tests: ["bot" | "fingerprint" | "cloudflare" | "captcha"]
}
```

---

## 三、网络爬虫专业版 (web-crawler)

### 技术架构

- **多模式爬取**: 静态HTTP / JS渲染 / API接口
- **数据提取**: Cheerio + CSS选择器 / XPath / 正则
- **反爬绕过**: UA轮换 / 代理池 / 请求延迟 / 重试机制

### 核心工具 API

#### 1. `crawl_single_page` - 单页智能爬取

**参数:**
```typescript
{
  url: string,              // 必填
  mode: "auto" | "static" | "js" | "api",
  userAgent: string,        // 自定义UA，默认随机
  headers: object,
  cookies: string,
  proxy: string,
  delaySeconds: number,
  outputFormat: "raw" | "markdown" | "json" | "text",
  extractLinks: boolean,
  extractImages: boolean
}
```

**爬取模式说明:**

| 模式 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| `static` | 纯静态页面, 博客, 文档 | 速度快, 资源占用低 | 无法获取JS渲染内容 |
| `js` | SPA应用, 动态内容, 反爬站 | 内容完整, 模拟真实浏览器 | 速度慢, 资源消耗大 |
| `api` | 后端API接口 | 数据结构化, 高效 | 需要分析接口 |
| `auto` | 通用场景 | 自动降级处理 | 略慢 |

#### 2. `crawler_extract_data` - 结构化数据提取

**参数:**
```typescript
{
  html?: string,
  url?: string,
  selectors: object,        // {key: CSS选择器}
  useXPath: boolean,
  regexPatterns: object,    // {key: 正则表达式}
  extractTables: boolean,   // 自动提取所有表格
  cleanWhitespace: boolean
}
```

**示例 - 爬取新闻列表:**
```json
{
  "url": "https://news.example.com",
  "selectors": {
    "articles": ".article-item",
    "titles": ".article-title"
  },
  "extractTables": true
}
```

#### 3. `crawler_batch` - 批量深度爬虫

**参数:**
```typescript
{
  startUrls: string[],      // 起始URL列表
  maxDepth: number,         // 递归深度，默认1
  maxPages: number,         // 最大页面数，默认20
  concurrency: number,      // 并发数 1-5，默认2
  sameDomain: boolean,      // 仅同域名
  includePattern: string,   // URL必须包含
  excludePattern: string,   // URL排除规则
  rateLimit: number,        // 请求间隔毫秒
  outputFile: string
}
```

#### 4. `crawler_api_fetch` - API接口爬取

**参数:**
```typescript
{
  url: string,
  method: "GET" | "POST" | "PUT" | "DELETE",
  headers: object,
  body: string,
  authType: "none" | "bearer" | "basic" | "apikey",
  authToken: string,
  pagination: "none" | "offset" | "cursor" | "page",
  maxPages: number,
  outputFile: string
}
```

#### 5. `crawler_export` - 数据导出

**参数:**
```typescript
{
  data: string,             // JSON字符串数据
  outputFile: string,       // 必填
  format: "json" | "csv" | "xlsx" | "md",
  fields: string[],         // CSV字段
  sheetName: string,        // Excel表名
  prettyPrint: boolean
}
```

#### 6. `crawler_anti_detect` - 反爬检测与绕过

**参数:**
```typescript
{
  url: string,
  runTests: boolean,
  generateBypass: boolean
}
```

**检测指标:**
- User-Agent 拦截检测
- Cloudflare 保护检测
- reCAPTCHA / hCaptcha 检测
- 速率限制检测
- JS 指纹校验检测

---

## 统一集成规范

### 1. 统一中间件架构

所有技能模块共享以下中间件能力:

```typescript
// 缓存中间件
.withCache(ttlSeconds)

// 速率限制
.withRateLimit(maxRequests, windowMinutes)

// 认证中间件
.withAuth(type, envKey)

// 自定义中间件
.use({
  priority: 50,
  before: async (params, tool) => params,
  after: async (result, params, tool) => result,
  onError: async (error, params, tool) => fallback
})
```

### 2. 统一错误处理

所有工具返回标准化错误格式:

```typescript
{
  success: boolean,
  error?: string,
  errorCode?: string,
  message?: string,
  fallback?: any
}
```

### 3. 统一日志规范

```typescript
{
  level: "debug" | "info" | "warn" | "error",
  module: "site-generator" | "browser-automation" | "web-crawler",
  tool: string,
  durationMs: number,
  timestamp: string,
  message: string
}
```

### 4. Prompt 模板规范

```typescript
{
  name: string,
  description: string,
  arguments: [{ name, description, required }],
  generate: async (args) => promptString
}
```

---

## 使用场景示例

### 场景 A: 完整文章采集工作流

```
1. crawler_anti_detect(url) → 检测反爬级别
2. crawl_single_page(url, mode="js", stealthMode=true)
3. crawler_extract_data(selectors={标题, 正文, 作者, 日期})
4. crawler_export(format="markdown", outputFile="article.md")
```

### 场景 B: 产品网站快速上线

```
1. site_list_templates(category="ecommerce")
2. site_create(template="next-ecommerce", installDeps=true)
3. site_config(title="我的店铺", colors={primary: "#..."})
4. site_deploy(target="vercel")
```

### 场景 C: 批量表单提交

```
1. browser_export_cookies(loginUrl) → 保存会话
2. browser_fill_form(importCookies, humanTyping=true)
3. browser_screenshot(验证提交结果)
```

---

## 性能优化建议

### web-crawler 优化

1. **静态优先**: 能用 static 模式不用 js 模式
2. **并发控制**: 建议 concurrency=2-3，配合 rateLimit=1000
3. **选择器精准**: 使用 ID 和类选择器，避免通用选择器
4. **结果缓存**: 重复爬取启用 `.withCache(3600)`

### browser-automation 优化

1. **隐身模式**: 反爬网站强制启用 stealthMode
2. **行为模拟**: 高反爬启用 emulateHuman
3. **会话复用**: 登录后导出 Cookie 复用
4. **预设匹配**: 目标网站用什么浏览器就用什么 preset

### site-generator 优化

1. **预安装依赖**: CI环境缓存 node_modules
2. **模板缓存**: 常用模板创建本地脚手架
3. **并行构建**: 多项目部署并行执行

---

## 安全与合规注意事项

1. **robots.txt**: 遵守目标网站爬虫协议
2. **速率控制**: 避免对目标服务器造成压力
3. **数据版权**: 爬取数据注意版权问题
4. **隐私保护**: 不要爬取和存储个人敏感信息
5. **代理合规**: 使用合规代理服务，避免法律风险

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 2.0.0 | 2026-04-11 | 三大模块首次发布，完整实现所有功能 |
