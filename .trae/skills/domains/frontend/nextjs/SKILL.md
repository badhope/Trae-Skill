---
name: nextjs
description: "Next.js full-stack framework for React applications with SSR, SSG, and API routes. Keywords: nextjs, next, ssr, ssg, react, 全栈"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
languages:
  - typescript
  - javascript
frameworks:
  - next.js
  - react
invoked_by:
  - coding-workflow
  - code-generator
capabilities:
  - server_rendering
  - static_generation
  - api_routes
  - app_router
  - middleware
---

# Next.js

Next.js全栈框架专家，专注于服务端渲染、静态生成和API路由开发。

## 适用场景

- SEO友好的Web应用
- 企业级网站
- 电商应用
- 博客和内容站点
- 全栈React应用

## 核心架构

### 1. App Router (Next.js 14+)

```typescript
// app/layout.tsx
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'My App',
  description: 'A Next.js application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Header />
          <main>{children}</main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}

// app/page.tsx
import { Suspense } from 'react';

async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }
  });
  return res.json();
}

export default async function HomePage() {
  return (
    <div>
      <h1>Welcome</h1>
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
    </div>
  );
}

async function Posts() {
  const posts = await getPosts();
  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}

// app/posts/[id]/page.tsx
interface PageProps {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(r => r.json());
  
  return posts.map((post: any) => ({
    id: post.id.toString(),
  }));
}

export async function generateMetadata({ params }: PageProps) {
  const post = await fetch(`https://api.example.com/posts/${params.id}`).then(r => r.json());
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.image],
    },
  };
}

export default async function PostPage({ params }: PageProps) {
  const post = await fetch(`https://api.example.com/posts/${params.id}`, {
    cache: 'no-store'
  }).then(r => r.json());
  
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// app/posts/[id]/edit/page.tsx
import { notFound } from 'next/navigation';

export default async function EditPostPage({ params }: PageProps) {
  const post = await getPost(params.id);
  
  if (!post) {
    notFound();
  }
  
  return <EditPostForm post={post} />;
}
```

### 2. API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
});

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = parseInt(searchParams.get('page') || '1');
  const limit = parseInt(searchParams.get('limit') || '20');
  
  const users = await getUsers({ page, limit });
  
  return NextResponse.json({
    data: users,
    pagination: { page, limit }
  });
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validated = CreateUserSchema.parse(body);
    
    const user = await createUser(validated);
    
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await getUser(params.id);
  
  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }
  
  return NextResponse.json(user);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();
  const user = await updateUser(params.id, body);
  
  return NextResponse.json(user);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await deleteUser(params.id);
  
  return new NextResponse(null, { status: 204 });
}
```

### 3. Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  const isAuthenticated = !!token;
  
  const protectedPaths = ['/dashboard', '/profile', '/settings'];
  const isProtectedPath = protectedPaths.some(path => 
    request.nextUrl.pathname.startsWith(path)
  );
  
  if (isProtectedPath && !isAuthenticated) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }
  
  const authPages = ['/login', '/register'];
  const isAuthPage = authPages.some(path => 
    request.nextUrl.pathname.startsWith(path)
  );
  
  if (isAuthPage && isAuthenticated) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  
  const response = NextResponse.next();
  
  response.headers.set('x-request-id', crypto.randomUUID());
  
  return response;
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/profile/:path*',
    '/settings/:path*',
    '/login',
    '/register'
  ]
};
```

### 4. Server Actions

```typescript
// app/actions/user.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const UpdateUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

export async function updateUser(formData: FormData) {
  const validated = UpdateUserSchema.parse({
    name: formData.get('name'),
    email: formData.get('email'),
  });
  
  await fetch('https://api.example.com/users/me', {
    method: 'PUT',
    body: JSON.stringify(validated),
  });
  
  revalidatePath('/profile');
  revalidateTag('user');
}

export async function deleteUser() {
  await fetch('https://api.example.com/users/me', {
    method: 'DELETE',
  });
  
  redirect('/login');
}

// app/components/EditProfileForm.tsx
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { updateUser } from '@/app/actions/user';

function SubmitButton() {
  const { pending } = useFormStatus();
  
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Saving...' : 'Save Changes'}
    </button>
  );
}

export function EditProfileForm({ user }: { user: User }) {
  const [state, formAction] = useFormState(updateUser, null);
  
  return (
    <form action={formAction}>
      <input name="name" defaultValue={user.name} />
      <input name="email" defaultValue={user.email} type="email" />
      <SubmitButton />
      {state?.error && <p className="error">{state.error}</p>}
    </form>
  );
}
```

### 5. 数据获取策略

```typescript
// lib/api.ts
export const fetchData = async <T>(
  url: string,
  options: {
    cache?: 'force-cache' | 'no-store';
    revalidate?: number | false;
    tags?: string[];
  } = {}
): Promise<T> => {
  const { cache = 'no-store', revalidate, tags } = options;
  
  const res = await fetch(url, {
    cache,
    next: revalidate !== undefined ? { revalidate, tags } : undefined,
  });
  
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  
  return res.json();
};

export const fetchWithAuth = async <T>(
  url: string,
  token: string,
  options: RequestInit = {}
): Promise<T> => {
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
    },
  }).then(r => r.json());
};

// Static Generation
export const getStaticData = async <T>(url: string): Promise<T> => {
  return fetchData(url, { cache: 'force-cache' });
};

// ISR (Incremental Static Regeneration)
export const getISRData = async <T>(
  url: string,
  revalidateSeconds: number = 60
): Promise<T> => {
  return fetchData(url, { revalidate: revalidateSeconds });
};

// Server-Side Rendering
export const getSSRData = async <T>(url: string): Promise<T> => {
  return fetchData(url, { cache: 'no-store' });
};
```

## 最佳实践

1. **App Router优先**: 使用新的App Router
2. **Server Components**: 默认使用Server Components
3. **流式渲染**: 使用Suspense实现流式渲染
4. **缓存策略**: 合理配置缓存和重新验证
5. **SEO优化**: 使用Metadata API
6. **错误处理**: 使用error.tsx和not-found.tsx

## 相关技能

- [frontend-react](../react) - React开发
- [backend-nodejs](../../backend/nodejs) - Node.js后端
- [api-design](../../actions/code/api-design) - API设计
- [unit-test](../../testing/unit-test) - 单元测试
