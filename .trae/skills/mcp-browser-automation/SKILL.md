# MCP Browser Automation

## Description
MCP 浏览器自动化专家。帮助实现基于 MCP 的浏览器自动化，包括网页抓取、自动化测试、性能分析等功能。

## Details

### 功能特性
- 网页导航与交互
- 元素查找与操作
- 截图与 PDF 生成
- 性能分析
- 网络请求监控
- 多浏览器支持

### Chrome DevTools MCP

#### 配置
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-chrome"]
    }
  }
}
```

#### 可用工具
- `navigate` - 导航到 URL
- `screenshot` - 截取页面截图
- `click` - 点击元素
- `type` - 输入文本
- `evaluate` - 执行 JavaScript
- `get_console_logs` - 获取控制台日志
- `get_network_logs` - 获取网络日志

### Puppeteer 集成

```typescript
import puppeteer, { Browser, Page } from "puppeteer";

class BrowserManager {
  private browser: Browser | null = null;
  private pages: Map<string, Page> = new Map();
  
  async launch(options: puppeteer.LaunchOptions = {}) {
    this.browser = await puppeteer.launch({
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage"
      ],
      ...options
    });
    return this.browser;
  }
  
  async newPage(id: string): Promise<Page> {
    if (!this.browser) {
      await this.launch();
    }
    
    const page = await this.browser!.newPage();
    
    // 设置视口
    await page.setViewport({ width: 1920, height: 1080 });
    
    // 设置用户代理
    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    );
    
    this.pages.set(id, page);
    return page;
  }
  
  async getPage(id: string): Promise<Page | undefined> {
    return this.pages.get(id);
  }
  
  async closePage(id: string) {
    const page = this.pages.get(id);
    if (page) {
      await page.close();
      this.pages.delete(id);
    }
  }
  
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.pages.clear();
    }
  }
}

const browserManager = new BrowserManager();
```

### 工具实现

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "browser_navigate",
      description: "Navigate to a URL",
      inputSchema: {
        type: "object",
        properties: {
          pageId: { type: "string", description: "Page identifier" },
          url: { type: "string", description: "URL to navigate to" },
          waitUntil: {
            type: "string",
            enum: ["load", "domcontentloaded", "networkidle0", "networkidle2"],
            default: "networkidle2"
          }
        },
        required: ["pageId", "url"]
      }
    },
    {
      name: "browser_screenshot",
      description: "Take a screenshot of the page",
      inputSchema: {
        type: "object",
        properties: {
          pageId: { type: "string" },
          fullPage: { type: "boolean", default: false },
          selector: { type: "string", description: "CSS selector for element" }
        },
        required: ["pageId"]
      }
    },
    {
      name: "browser_click",
      description: "Click an element",
      inputSchema: {
        type: "object",
        properties: {
          pageId: { type: "string" },
          selector: { type: "string", description: "CSS selector" },
          waitForNavigation: { type: "boolean", default: true }
        },
        required: ["pageId", "selector"]
      }
    },
    {
      name: "browser_type",
      description: "Type text into an element",
      inputSchema: {
        type: "object",
        properties: {
          pageId: { type: "string" },
          selector: { type: "string" },
          text: { type: "string" },
          delay: { type: "integer", default: 50 }
        },
        required: ["pageId", "selector", "text"]
      }
    },
    {
      name: "browser_evaluate",
      description: "Execute JavaScript on the page",
      inputSchema: {
        type: "object",
        properties: {
          pageId: { type: "string" },
          script: { type: "string", description: "JavaScript code" }
        },
        required: ["pageId", "script"]
      }
    },
    {
      name: "browser_get_content",
      description: "Get page content",
      inputSchema: {
        type: "object",
        properties: {
          pageId: { type: "string" },
          selector: { type: "string", description: "CSS selector (optional)" }
        },
        required: ["pageId"]
      }
    }
  ]
}));
```

### 工具执行

```typescript
// 导航
async function navigate(pageId: string, url: string, waitUntil: string = "networkidle2") {
  const page = await browserManager.getPage(pageId);
  if (!page) {
    throw new Error(`Page ${pageId} not found`);
  }
  
  // URL 验证
  const parsedUrl = new URL(url);
  const allowedProtocols = ["http:", "https:"];
  if (!allowedProtocols.includes(parsedUrl.protocol)) {
    throw new Error(`Protocol ${parsedUrl.protocol} is not allowed`);
  }
  
  await page.goto(url, { waitUntil: waitUntil as any, timeout: 30000 });
  
  return {
    url: page.url(),
    title: await page.title()
  };
}

// 截图
async function screenshot(
  pageId: string,
  options: { fullPage?: boolean; selector?: string } = {}
): Promise<string> {
  const page = await browserManager.getPage(pageId);
  if (!page) {
    throw new Error(`Page ${pageId} not found`);
  }
  
  let screenshot: Buffer;
  
  if (options.selector) {
    const element = await page.$(options.selector);
    if (!element) {
      throw new Error(`Element not found: ${options.selector}`);
    }
    screenshot = await element.screenshot();
  } else {
    screenshot = await page.screenshot({ fullPage: options.fullPage });
  }
  
  return screenshot.toString("base64");
}

// 点击
async function click(
  pageId: string,
  selector: string,
  waitForNavigation: boolean = true
) {
  const page = await browserManager.getPage(pageId);
  if (!page) {
    throw new Error(`Page ${pageId} not found`);
  }
  
  await page.waitForSelector(selector, { timeout: 10000 });
  
  if (waitForNavigation) {
    await Promise.all([
      page.waitForNavigation({ waitUntil: "networkidle2" }),
      page.click(selector)
    ]);
  } else {
    await page.click(selector);
  }
  
  return { success: true, url: page.url() };
}

// 执行脚本
async function evaluate(pageId: string, script: string) {
  const page = await browserManager.getPage(pageId);
  if (!page) {
    throw new Error(`Page ${pageId} not found`);
  }
  
  // 安全检查
  const forbiddenPatterns = [
    /eval\s*\(/,
    /Function\s*\(/,
    /document\.cookie/,
    /localStorage/,
    /sessionStorage/
  ];
  
  for (const pattern of forbiddenPatterns) {
    if (pattern.test(script)) {
      throw new Error("Script contains forbidden patterns");
    }
  }
  
  const result = await page.evaluate(script);
  return result;
}

// 获取内容
async function getContent(pageId: string, selector?: string) {
  const page = await browserManager.getPage(pageId);
  if (!page) {
    throw new Error(`Page ${pageId} not found`);
  }
  
  if (selector) {
    const element = await page.$(selector);
    if (!element) {
      throw new Error(`Element not found: ${selector}`);
    }
    return await element.evaluate(el => el.textContent);
  }
  
  return await page.content();
}
```

### 网络监控

```typescript
async function setupNetworkMonitoring(pageId: string) {
  const page = await browserManager.getPage(pageId);
  if (!page) return;
  
  const requests: any[] = [];
  const responses: any[] = [];
  
  page.on("request", (request) => {
    requests.push({
      url: request.url(),
      method: request.method(),
      headers: request.headers(),
      timestamp: Date.now()
    });
  });
  
  page.on("response", async (response) => {
    responses.push({
      url: response.url(),
      status: response.status(),
      headers: response.headers(),
      timestamp: Date.now()
    });
  });
  
  return { requests, responses };
}
```

### 性能分析

```typescript
async function analyzePerformance(pageId: string) {
  const page = await browserManager.getPage(pageId);
  if (!page) {
    throw new Error(`Page ${pageId} not found`);
  }
  
  // 获取性能指标
  const metrics = await page.metrics();
  
  // 获取性能时间线
  const performanceTiming = await page.evaluate(() => {
    const timing = performance.timing;
    return {
      dns: timing.domainLookupEnd - timing.domainLookupStart,
      tcp: timing.connectEnd - timing.connectStart,
      request: timing.responseStart - timing.requestStart,
      response: timing.responseEnd - timing.responseStart,
      domProcessing: timing.domComplete - timing.domInteractive,
      totalLoad: timing.loadEventEnd - timing.navigationStart
    };
  });
  
  // 获取 Core Web Vitals
  const webVitals = await page.evaluate(() => {
    return new Promise((resolve) => {
      const vitals: any = {};
      
      // LCP
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        vitals.lcp = entries[entries.length - 1].startTime;
      }).observe({ type: "largest-contentful-paint", buffered: true });
      
      // FID
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        vitals.fid = entries[0].processingStart - entries[0].startTime;
      }).observe({ type: "first-input", buffered: true });
      
      // CLS
      let clsValue = 0;
      new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!(entry as any).hadRecentInput) {
            clsValue += (entry as any).value;
          }
        }
        vitals.cls = clsValue;
      }).observe({ type: "layout-shift", buffered: true });
      
      setTimeout(() => resolve(vitals), 1000);
    });
  });
  
  return {
    metrics,
    timing: performanceTiming,
    webVitals
  };
}
```

### Playwright 集成

```typescript
import { chromium, Browser, Page, BrowserContext } from "playwright";

class PlaywrightManager {
  private browser: Browser | null = null;
  private contexts: Map<string, BrowserContext> = new Map();
  
  async launch() {
    this.browser = await chromium.launch({
      headless: true
    });
  }
  
  async newContext(id: string, options: any = {}) {
    if (!this.browser) await this.launch();
    
    const context = await this.browser!.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      ...options
    });
    
    this.contexts.set(id, context);
    return context;
  }
  
  async newPage(contextId: string): Promise<Page> {
    const context = this.contexts.get(contextId);
    if (!context) {
      throw new Error(`Context ${contextId} not found`);
    }
    return await context.newPage();
  }
}
```

### 安全考虑

1. **URL 验证**: 只允许 HTTP/HTTPS 协议
2. **脚本限制**: 禁止执行危险 JavaScript
3. **资源限制**: 限制页面数量和内存使用
4. **超时设置**: 设置合理的操作超时
5. **沙箱模式**: 在沙箱环境中运行浏览器

## Related Skills
- `mcp-server-development` - MCP 服务器开发
- `web-scraping` - 网页抓取
- `e2e-testing` - 端到端测试
- `performance-optimizer` - 性能优化
