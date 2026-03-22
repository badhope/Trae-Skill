import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  metadataBase: new URL('https://badhope.github.io/skill'),
  title: {
    default: 'AI Skill Repository | 专业的 Prompt 工具箱',
    template: '%s | AI Skill Repository',
  },
  description: '132+ 高质量提示词，27+ 技能定义，10+ 工作流。涵盖编程开发、调试修复、学习支持、日常生活的一站式 AI 辅助解决方案。支持 GPT-4、Claude 等主流模型。',
  keywords: [
    'AI提示词',
    'ChatGPT提示词',
    'GPT提示词',
    'AI技能',
    '提示词工程',
    'Prompt模板',
    '代码生成',
    '代码调试',
    'AI工作流',
    '机器学习提示词',
    'AI助手',
    '效率工具',
    '强化学习',
    '上下文记忆',
    'MCP工具',
    '学术写作AI',
    '创意写作AI',
    'ai skills',
    'chatgpt prompts',
    'gpt prompts',
    'prompt engineering',
    'code generation',
  ],
  authors: [{ name: 'badhope', url: 'https://github.com/badhope' }],
  creator: 'badhope',
  publisher: 'badhope',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'zh_CN',
    alternateLocale: 'en_US',
    url: 'https://badhope.github.io/skill',
    siteName: 'AI Skill Repository',
    title: 'AI Skill Repository | 专业的 Prompt 工具箱',
    description: '132+ 高质量提示词，27+ 技能定义，10+ 工作流。编程、调试、学习、日常全覆盖。',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'AI Skill Repository',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Skill Repository | AI提示词工具箱',
    description: '132+ 高质量提示词，27+ 技能定义，10+ 工作流。编程、调试、学习全覆盖。',
    creator: '@badhope',
    images: ['/og-image.png'],
  },
  alternates: {
    canonical: 'https://badhope.github.io/skill',
    languages: {
      'en-US': 'https://badhope.github.io/skill',
      'zh-CN': 'https://badhope.github.io/skill',
    },
  },
  category: 'Developer Tools',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet" />
        <script type="application/ld+json" dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "AI Skill & Prompt Repository",
            "alternateName": "AI提示词仓库",
            "description": "模块化 AI Skill/Prompt/Workflow 仓库，具备高级技术能力，用于代码生成、调试和创意任务",
            "url": "https://badhope.github.io/skill",
            "applicationCategory": "DeveloperApplication",
            "operatingSystem": "Any",
            "offers": {
              "@type": "Offer",
              "price": "0.00",
              "priceCurrency": "USD"
            },
            "author": {
              "@type": "Person",
              "name": "badhope",
              "url": "https://github.com/badhope"
            },
            "keywords": "AI, 提示词, 技能, 工作流, 编程, 调试, 强化学习, MCP工具",
            "softwareVersion": "2.0.0",
            "aggregateRating": {
              "@type": "AggregateRating",
              "ratingValue": "4.9",
              "ratingCount": "100",
              "bestRating": "5"
            }
          })
        }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Collection",
            "name": "AI提示词集合",
            "alternateName": "AI Prompts Collection",
            "description": "132+ 精选AI提示词，涵盖编程、调试、学习和创意任务",
            "numberOfItems": "132",
            "keywords": ["AI提示词", "ChatGPT提示词", "GPT提示词", "提示词工程"],
            "about": [
              {"@type": "Thing", "name": "代码生成"},
              {"@type": "Thing", "name": "代码调试"},
              {"@type": "Thing", "name": "学习支持"},
              {"@type": "Thing", "name": "创意写作"}
            ]
          })
        }} />
      </head>
      <body className="bg-neutral-900 text-white antialiased">
        <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4 bg-neutral-900/80 backdrop-blur-lg border-b border-neutral-800/50">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <a href="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-lg group-hover:scale-110 transition-transform">
                AI
              </div>
              <span className="font-bold text-xl hidden sm:block">Skill Repo</span>
            </a>

            <div className="flex items-center gap-8">
              <NavLink href="/features">功能</NavLink>
              <NavLink href="/docs">文档</NavLink>
              <NavLink href="/about">关于</NavLink>
              <a
                href="https://github.com/badhope/skill"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-lg hover:bg-neutral-800 transition-colors"
                aria-label="GitHub"
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
        </nav>

        <div className="pt-16">
          {children}
        </div>

        <footer className="py-12 px-6 border-t border-neutral-800/50">
          <div className="max-w-6xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-center gap-6">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold text-sm">
                  AI
                </div>
                <span className="font-semibold">AI Skill Repository</span>
              </div>

              <div className="flex flex-wrap justify-center gap-6 text-sm text-neutral-400">
                <a href="/features" className="hover:text-white transition-colors">功能</a>
                <a href="/docs" className="hover:text-white transition-colors">文档</a>
                <a href="/about" className="hover:text-white transition-colors">关于</a>
                <a href="https://github.com/badhope/skill" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">GitHub</a>
              </div>

              <p className="text-sm text-neutral-500">
                Built with ❤️ by <a href="https://github.com/badhope" target="_blank" rel="noopener noreferrer" className="text-primary-400 hover:underline">badhope</a>
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <a
      href={href}
      className="text-sm font-medium text-neutral-400 hover:text-white transition-colors relative group"
    >
      {children}
      <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-primary-500 to-accent-500 group-hover:w-full transition-all duration-300" />
    </a>
  );
}
