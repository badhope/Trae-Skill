import { createMCPServer } from '../../packages/core/mcp/builder'
import fs from 'fs/promises'
import path from 'path'

const TEMPLATES = {
  'landing-page': {
    name: '🚀 Landing Page',
    description: 'High-converting marketing landing page with Tailwind CSS',
    tech: ['HTML5', 'Tailwind CSS 3', 'Font Awesome'],
    features: ['Hero section', 'Features', 'Testimonials', 'Pricing', 'CTA', 'Footer']
  },
  'portfolio': {
    name: '💼 Portfolio Site',
    description: 'Developer/designer portfolio with project gallery',
    tech: ['HTML5', 'Tailwind CSS 3', 'JavaScript'],
    features: ['About', 'Projects grid', 'Skills', 'Contact form', 'Dark mode']
  },
  'blog': {
    name: '📝 Blog Layout',
    description: 'Clean blog template with article cards',
    tech: ['HTML5', 'Tailwind CSS 3', 'Font Awesome'],
    features: ['Featured post', 'Article grid', 'Sidebar', 'Categories', 'Newsletter']
  },
  'ecommerce': {
    name: '🛒 E-commerce Store',
    description: 'Product showcase with shopping cart UI',
    tech: ['HTML5', 'Tailwind CSS 3', 'JavaScript'],
    features: ['Product grid', 'Filters', 'Cart', 'Product detail', 'Checkout form']
  },
  'saas-dashboard': {
    name: '📊 SaaS Dashboard',
    description: 'Admin dashboard with charts and data tables',
    tech: ['HTML5', 'Tailwind CSS 3', 'Chart.js'],
    features: ['Sidebar nav', 'Charts', 'Data tables', 'Stats cards', 'Dark mode']
  },
  'nextjs-starter': {
    name: '⚡ Next.js Starter',
    description: 'Full Next.js 14 app with App Router',
    tech: ['Next.js 14', 'TypeScript', 'Tailwind CSS', 'shadcn/ui'],
    features: ['App Router', 'Server Components', 'Route handlers', 'Layouts']
  }
}

export default createMCPServer({
  name: 'website-builder',
  version: '1.0.0',
  description: 'One-Click Website Generation - Production-ready websites instantly',
  author: 'Trae Professional',
  icon: '🌐'
})
  .addTool({
    name: 'list_templates',
    description: 'List all available website templates',
    parameters: {},
    execute: async () => {
      return {
        success: true,
        templates: Object.entries(TEMPLATES).map(([id, t]) => ({
          id,
          name: t.name,
          description: t.description,
          techStack: t.tech,
          features: t.features
        }))
      }
    }
  })
  .addTool({
    name: 'generate_landing_page',
    description: 'ONE CLICK - Generate complete landing page HTML with Tailwind CSS',
    parameters: {
      brandName: { type: 'string', description: 'Your brand name', required: true },
      primaryColor: { type: 'string', description: 'Primary color hex default #3b82f6', required: false },
      industry: { type: 'string', description: 'Industry: saas, ecomm, agency, personal', required: true },
      outputPath: { type: 'string', description: 'Output file path', required: false }
    },
    execute: async (params: Record<string, any>) => {
      const primary = params.primaryColor || '#3b82f6'
      const outputFile = params.outputPath || 'index.html'
      const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${params.brandName}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '${primary}',
          },
        }
      }
    }
  </script>
  <style type="text/tailwindcss">
    @layer utilities {
      .content-auto {
        content-visibility: auto;
      }
      .text-shadow {
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
      }
    }
  </style>
</head>
<body class="font-sans antialiased">
  <nav class="fixed w-full bg-white/90 backdrop-blur-sm z-50 border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16 items-center">
        <div class="flex items-center">
          <span class="text-2xl font-bold text-primary">${params.brandName}</span>
        </div>
        <div class="hidden md:flex items-center space-x-8">
          <a href="#features" class="text-gray-600 hover:text-primary transition">Features</a>
          <a href="#pricing" class="text-gray-600 hover:text-primary transition">Pricing</a>
          <a href="#about" class="text-gray-600 hover:text-primary transition">About</a>
          <button class="bg-primary text-white px-6 py-2 rounded-full hover:bg-primary/90 transition transform hover:scale-105">
            Get Started
          </button>
        </div>
        <button class="md:hidden text-gray-600">
          <i class="fa fa-bars text-xl"></i>
        </button>
      </div>
    </div>
  </nav>

  <section class="pt-32 pb-20 bg-gradient-to-br from-primary/5 to-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-4xl mx-auto">
        <div class="inline-flex items-center px-4 py-2 bg-primary/10 rounded-full text-primary text-sm font-medium mb-6">
          <i class="fa fa-star mr-2"></i> Launching Soon
        </div>
        <h1 class="text-[clamp(2.5rem,5vw,4rem)] font-bold text-gray-900 leading-tight text-shadow mb-6">
          Transform the way you <span class="text-primary">build products</span>
        </h1>
        <p class="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          The all-in-one platform that helps ${params.industry} teams build, launch, and scale faster than ever before.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="bg-primary text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-primary/90 transition transform hover:scale-105 shadow-lg shadow-primary/25">
            Start Free Trial
          </button>
          <button class="bg-white text-gray-700 px-8 py-4 rounded-full text-lg font-semibold border border-gray-200 hover:border-gray-300 transition flex items-center justify-center gap-2">
            <i class="fa fa-play-circle text-primary"></i> Watch Demo
          </button>
        </div>
      </div>
      <div class="mt-16 relative">
        <div class="bg-gradient-to-t from-white/50 absolute inset-x-0 bottom-0 h-1/3"></div>
        <div class="rounded-2xl shadow-2xl overflow-hidden border border-gray-100">
          <div class="bg-gray-900 px-4 py-3 flex items-center gap-2">
            <div class="w-3 h-3 rounded-full bg-red-500"></div>
            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div class="w-3 h-3 rounded-full bg-green-500"></div>
            <span class="text-gray-400 text-sm ml-4">${params.brandName} Dashboard</span>
          </div>
          <div class="bg-gray-100 aspect-video flex items-center justify-center">
            <div class="text-center text-gray-400">
              <i class="fa fa-desktop text-5xl mb-4 text-primary/50"></i>
              <p class="text-lg">Your Product Preview</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="py-12 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <p class="text-center text-gray-500 text-sm mb-8">TRUSTED BY LEADING COMPANIES</p>
      <div class="flex flex-wrap justify-center items-center gap-12 opacity-60">
        <i class="fa fa-google text-3xl text-gray-400"></i>
        <i class="fa fa-microsoft text-3xl text-gray-400"></i>
        <i class="fa fa-amazon text-3xl text-gray-400"></i>
        <i class="fa fa-apple text-3xl text-gray-400"></i>
        <i class="fa fa-slack text-3xl text-gray-400"></i>
      </div>
    </div>
  </section>

  <section id="features" class="py-20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Everything you need</h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">Powerful features to supercharge your workflow</p>
      </div>
      <div class="grid md:grid-cols-3 gap-8">
        ${[
          { icon: 'bolt', title: 'Lightning Fast', desc: 'Blazing fast performance optimized for speed and efficiency' },
          { icon: 'shield', title: 'Secure by Default', desc: 'Enterprise-grade security built into every layer' },
          { icon: 'cogs', title: 'Easy Integration', desc: 'Connect with your favorite tools in minutes' },
          { icon: 'line-chart', title: 'Analytics', desc: 'Deep insights and real-time reporting dashboards' },
          { icon: 'users', title: 'Team Collaboration', desc: 'Work together seamlessly with built-in collaboration' },
          { icon: 'headphones', title: '24/7 Support', desc: 'Expert support available around the clock' }
        ].map(f => `
        <div class="bg-white p-8 rounded-2xl border border-gray-100 hover:shadow-xl hover:border-primary/20 transition group">
          <div class="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-primary group-hover:text-white transition">
            <i class="fa fa-${f.icon} text-2xl text-primary group-hover:text-white transition"></i>
          </div>
          <h3 class="text-xl font-semibold mb-3">${f.title}</h3>
          <p class="text-gray-600">${f.desc}</p>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <section id="pricing" class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Simple, transparent pricing</h2>
        <p class="text-xl text-gray-600">No hidden fees. No surprises.</p>
      </div>
      <div class="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <div class="bg-white p-8 rounded-2xl border border-gray-100">
          <h3 class="text-xl font-semibold mb-2">Starter</h3>
          <div class="mb-6">
            <span class="text-5xl font-bold">$29</span>
            <span class="text-gray-500">/month</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> 5 Team members</li>
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> 10GB Storage</li>
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> Basic analytics</li>
            <li class="flex items-center text-gray-400"><i class="fa fa-times text-gray-300 mr-3"></i> Advanced integrations</li>
          </ul>
          <button class="w-full py-3 border-2 border-gray-200 rounded-xl font-semibold hover:border-gray-300 transition">
            Get Started
          </button>
        </div>
        <div class="bg-primary text-white p-8 rounded-2xl shadow-xl shadow-primary/25 transform scale-105 relative">
          <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-yellow-400 text-gray-900 px-4 py-1 rounded-full text-sm font-semibold">
            Most Popular
          </div>
          <h3 class="text-xl font-semibold mb-2">Professional</h3>
          <div class="mb-6">
            <span class="text-5xl font-bold">$79</span>
            <span class="text-white/70">/month</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center"><i class="fa fa-check mr-3"></i> 25 Team members</li>
            <li class="flex items-center"><i class="fa fa-check mr-3"></i> 100GB Storage</li>
            <li class="flex items-center"><i class="fa fa-check mr-3"></i> Advanced analytics</li>
            <li class="flex items-center"><i class="fa fa-check mr-3"></i> All integrations</li>
            <li class="flex items-center"><i class="fa fa-check mr-3"></i> Priority support</li>
          </ul>
          <button class="w-full py-3 bg-white text-primary rounded-xl font-semibold hover:bg-gray-100 transition">
            Get Started
          </button>
        </div>
        <div class="bg-white p-8 rounded-2xl border border-gray-100">
          <h3 class="text-xl font-semibold mb-2">Enterprise</h3>
          <div class="mb-6">
            <span class="text-5xl font-bold">$199</span>
            <span class="text-gray-500">/month</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> Unlimited members</li>
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> Unlimited storage</li>
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> Custom analytics</li>
            <li class="flex items-center"><i class="fa fa-check text-green-500 mr-3"></i> Dedicated support</li>
          </ul>
          <button class="w-full py-3 border-2 border-gray-200 rounded-xl font-semibold hover:border-gray-300 transition">
            Contact Sales
          </button>
        </div>
      </div>
    </div>
  </section>

  <section class="py-20">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <div class="bg-gradient-to-r from-primary to-primary/80 rounded-3xl p-12 text-white">
        <h2 class="text-4xl font-bold mb-4">Ready to get started?</h2>
        <p class="text-xl mb-8 opacity-90 max-w-2xl mx-auto">Join thousands of teams already using ${params.brandName} to build better products.</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="bg-white text-primary px-8 py-4 rounded-full text-lg font-semibold hover:bg-gray-100 transition">
            Start Your Free Trial
          </button>
          <button class="bg-transparent border-2 border-white/50 text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/10 transition">
            Talk to Sales
          </button>
        </div>
      </div>
    </div>
  </section>

  <footer class="bg-gray-900 text-gray-400 py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid md:grid-cols-4 gap-8">
        <div>
          <span class="text-2xl font-bold text-white">${params.brandName}</span>
          <p class="mt-4">Building the future of ${params.industry} tools.</p>
          <div class="flex gap-4 mt-6">
            <a href="#" class="hover:text-white transition"><i class="fa fa-twitter text-xl"></i></a>
            <a href="#" class="hover:text-white transition"><i class="fa fa-github text-xl"></i></a>
            <a href="#" class="hover:text-white transition"><i class="fa fa-linkedin text-xl"></i></a>
          </div>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Product</h4>
          <ul class="space-y-2">
            <li><a href="#" class="hover:text-white transition">Features</a></li>
            <li><a href="#" class="hover:text-white transition">Pricing</a></li>
            <li><a href="#" class="hover:text-white transition">Integrations</a></li>
            <li><a href="#" class="hover:text-white transition">Changelog</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Resources</h4>
          <ul class="space-y-2">
            <li><a href="#" class="hover:text-white transition">Documentation</a></li>
            <li><a href="#" class="hover:text-white transition">Blog</a></li>
            <li><a href="#" class="hover:text-white transition">Community</a></li>
            <li><a href="#" class="hover:text-white transition">Support</a></li>
          </ul>
        </div>
        <div>
          <h4 class="text-white font-semibold mb-4">Company</h4>
          <ul class="space-y-2">
            <li><a href="#" class="hover:text-white transition">About</a></li>
            <li><a href="#" class="hover:text-white transition">Careers</a></li>
            <li><a href="#" class="hover:text-white transition">Privacy</a></li>
            <li><a href="#" class="hover:text-white transition">Terms</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-800 mt-12 pt-8 text-center">
        <p>&copy; ${new Date().getFullYear()} ${params.brandName}. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script>
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault()
        document.querySelector(this.getAttribute('href')).scrollIntoView({ behavior: 'smooth' })
      })
    })
    window.addEventListener('scroll', () => {
      const nav = document.querySelector('nav')
      if (window.scrollY > 10) nav.classList.add('shadow-sm')
      else nav.classList.remove('shadow-sm')
    })
  </script>
</body>
</html>`
      
      try {
        await fs.mkdir(path.dirname(outputFile), { recursive: true })
      } catch {}
      await fs.writeFile(outputFile, html, 'utf-8')
      
      return {
        success: true,
        websiteGenerated: true,
        file: outputFile,
        size: html.length + ' bytes',
        previewInstructions: `Open ${outputFile} in your browser.`
      }
    }
  })
  .build()
