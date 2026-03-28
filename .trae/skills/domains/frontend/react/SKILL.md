---
name: frontend-react
description: "React and Next.js development expert with hooks, state management, server components, and performance optimization. Keywords: react, nextjs, hooks, redux, typescript, frontend"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
language: typescript
frameworks:
  - react
  - nextjs
invoked_by:
  - coding-workflow
capabilities:
  - component_development
  - state_management
  - server_components
  - performance_optimization
  - testing
---

# Frontend React

React和Next.js开发专家，精通Hooks、状态管理、服务端组件和性能优化。

## 适用场景

- 构建React应用
- 实现React Hooks
- Redux/Zustand状态管理
- Next.js App Router
- 性能优化
- 组件测试

## 核心概念

### 函数组件

```tsx
import { useState, useEffect } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

export function UserProfile({ id }: { id: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    let mounted = true;
    
    async function fetchUser() {
      const response = await fetch(`/api/users/${id}`);
      const data = await response.json();
      if (mounted) {
        setUser(data);
        setLoading(false);
      }
    }
    
    fetchUser();
    return () => { mounted = false; };
  }, [id]);
  
  if (loading) return <div>Loading...</div>;
  if (!user) return null;
  
  return (
    <div className="user-profile">
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### 自定义Hooks

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);
  
  return { data, loading, error };
}

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return debouncedValue;
}
```

### Context和Provider

```tsx
import { createContext, useContext, useReducer } from 'react';

interface State {
  user: User | null;
  theme: 'light' | 'dark';
}

type Action = 
  | { type: 'SET_USER'; payload: User }
  | { type: 'LOGOUT' };

const AppContext = createContext<{
  state: State;
  dispatch: React.Dispatch<Action>;
} | null>(null);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, initialState);
  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  return useContext(AppContext)!;
}
```

## Next.js App Router

### 服务端组件

```tsx
async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetch(`/api/users/${params.id}`).then(r => r.json());
  
  return (
    <div>
      <h1>{user.name}</h1>
      <Suspense fallback={<div>Loading posts...</div>}>
        <UserPosts userId={user.id} />
      </Suspense>
    </div>
  );
}
```

### Server Actions

```tsx
'use server';

import { revalidatePath } from 'next/cache';

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  await fetch('/api/users', {
    method: 'POST',
    body: JSON.stringify({ name }),
  });
  revalidatePath('/users');
}
```

## 性能优化

```tsx
import { memo, useMemo, useCallback } from 'react';

const ExpensiveList = memo(function ExpensiveList({ items, filter }: Props) {
  const filteredItems = useMemo(
    () => items.filter(item => item.name.includes(filter)),
    [items, filter]
  );
  
  return (
    <ul>
      {filteredItems.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
});

// 代码分割
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

## 表单处理

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  });
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}
      <input {...register('password')} type="password" />
      <button type="submit">Submit</button>
    </form>
  );
}
```

## 最佳实践

1. **TypeScript**: 类型安全
2. **组件设计**: 单一职责
3. **状态管理**: 合理选择本地/全局状态
4. **性能**: memo、useMemo、useCallback
5. **可访问性**: 语义化HTML
6. **测试**: Jest + React Testing Library

## 相关技能

- [frontend-vue](../vue) - Vue开发
- [backend-nodejs](../../backend/nodejs) - Node.js后端
- [css-tailwind](../../styles/tailwind) - Tailwind CSS
