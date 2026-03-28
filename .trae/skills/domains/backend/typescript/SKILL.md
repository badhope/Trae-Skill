---
name: typescript
description: "TypeScript development with advanced types, generics, and patterns. Keywords: typescript, types, generics, interface, 类型"
layer: domain
role: specialist
version: 2.0.0
domain: backend
languages:
  - typescript
frameworks:
  - typescript
invoked_by:
  - coding-workflow
  - code-generator
capabilities:
  - type_design
  - generic_programming
  - pattern_implementation
  - type_safety
  - code_organization
---

# TypeScript

TypeScript开发专家，专注于类型设计、泛型编程和最佳实践。

## 适用场景

- 类型安全开发
- 复杂类型设计
- 代码重构
- API类型定义
- 库开发

## 核心类型模式

### 1. 高级类型

```typescript
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

type DeepRequired<T> = {
  [P in keyof T]-?: T[P] extends object ? DeepRequired<T[P]> : T[P];
};

type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

type PickByType<T, U> = {
  [P in keyof T as T[P] extends U ? P : never]: T[P];
};

type OmitByType<T, U> = {
  [P in keyof T as T[P] extends U ? never : P]: T[P];
};

type RequiredKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? never : K;
}[keyof T];

type OptionalKeys<T> = {
  [K in keyof T]-?: {} extends Pick<T, K> ? K : never;
}[keyof T];

type UnionToIntersection<U> = 
  (U extends any ? (k: U) => void : never) extends ((k: infer I) => void) ? I : never;

type UnionToTuple<T> = UnionToIntersection<
  T extends any ? (t: T) => T : never
> extends (_: any) => infer W ? [...UnionToTuple<Exclude<T, W>>, W] : [];
```

### 2. 泛型工具

```typescript
interface Result<T, E = Error> {
  ok: boolean;
  value?: T;
  error?: E;
}

function Ok<T>(value: T): Result<T> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

interface AsyncResult<T, E = Error> extends Promise<Result<T, E>> {}

async function tryAsync<T, E = Error>(
  fn: () => Promise<T>
): AsyncResult<T, E> {
  try {
    const value = await fn();
    return Ok(value);
  } catch (error) {
    return Err(error as E);
  }
}

interface Option<T> {
  isSome(): boolean;
  isNone(): boolean;
  unwrap(): T;
  unwrapOr(defaultValue: T): T;
  map<U>(fn: (value: T) => U): Option<U>;
  flatMap<U>(fn: (value: T) => Option<U>): Option<U>;
}

class Some<T> implements Option<T> {
  constructor(private value: T) {}
  
  isSome(): boolean { return true; }
  isNone(): boolean { return false; }
  unwrap(): T { return this.value; }
  unwrapOr(): T { return this.value; }
  
  map<U>(fn: (value: T) => U): Option<U> {
    return new Some(fn(this.value));
  }
  
  flatMap<U>(fn: (value: T) => Option<U>): Option<U> {
    return fn(this.value);
  }
}

class None<T> implements Option<T> {
  isSome(): boolean { return false; }
  isNone(): boolean { return true; }
  unwrap(): T { throw new Error('Called unwrap on None'); }
  unwrapOr(defaultValue: T): T { return defaultValue; }
  
  map<U>(): Option<U> { return new None<U>(); }
  flatMap<U>(): Option<U> { return new None<U>(); }
}

function Some<T>(value: T): Option<T> {
  return new SomeImpl(value);
}

function None<T>(): Option<T> {
  return new NoneImpl<T>();
}
```

### 3. 类型安全API

```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

type RouteConfig<T extends Record<string, any>> = {
  [K in keyof T]: {
    method: HttpMethod;
    path: string;
    request: T[K]['request'];
    response: T[K]['response'];
  };
};

type ApiClient<T extends RouteConfig<any>> = {
  [K in keyof T]: (
    params: T[K]['request']
  ) => Promise<T[K]['response']>;
};

function createApiClient<T extends RouteConfig<any>>(
  baseUrl: string,
  config: T
): ApiClient<T> {
  return new Proxy({} as ApiClient<T>, {
    get: (_, key: string) => {
      const route = config[key];
      if (!route) throw new Error(`Unknown route: ${key}`);
      
      return async (params: any) => {
        const url = `${baseUrl}${route.path}`;
        const response = await fetch(url, {
          method: route.method,
          headers: { 'Content-Type': 'application/json' },
          body: route.method !== 'GET' ? JSON.stringify(params) : undefined
        });
        
        return response.json();
      };
    }
  });
}

interface UserApiRoutes {
  getUser: {
    request: { id: string };
    response: { id: string; name: string; email: string };
  };
  createUser: {
    request: { name: string; email: string; password: string };
    response: { id: string; name: string; email: string };
  };
}

const userApi = createApiClient<UserApiRoutes>('https://api.example.com', {
  getUser: { method: 'GET', path: '/users/:id' },
  createUser: { method: 'POST', path: '/users' }
});

const user = await userApi.getUser({ id: '123' });
```

### 4. 类型推断

```typescript
type ExtractParams<T extends string> = T extends `${string}:${infer Param}/${infer Rest}`
  ? Param | ExtractParams<Rest>
  : T extends `${string}:${infer Param}`
  ? Param
  : never;

type RouteParams<T extends string> = {
  [K in ExtractParams<T>]: string;
};

function createRoute<T extends string>(
  path: T,
  handler: (params: RouteParams<T>) => Response
) {
  return { path, handler };
}

const userRoute = createRoute('/users/:userId/posts/:postId', (params) => {
  return new Response(`User ${params.userId}, Post ${params.postId}`);
});

type InferEventHandlers<T> = T extends {
  on: (event: infer E, handler: infer H) => void;
}
  ? { [K in E extends string ? E : never]: H }
  : never;

type ExtractPromiseType<T> = T extends Promise<infer U> ? U : T;

type AsyncReturnType<T extends (...args: any) => Promise<any>> = T extends (
  ...args: any
) => Promise<infer R>
  ? R
  : never;
```

### 5. 类型守卫

```typescript
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isNumber(value: unknown): value is number {
  return typeof value === 'number';
}

function isArray<T>(value: unknown, guard: (v: unknown) => v is T): value is T[] {
  return Array.isArray(value) && value.every(guard);
}

function hasProperty<K extends string>(
  obj: unknown,
  key: K
): obj is Record<K, unknown> {
  return typeof obj === 'object' && obj !== null && key in obj;
}

interface User {
  id: string;
  name: string;
  email: string;
}

function isUser(value: unknown): value is User {
  return (
    hasProperty(value, 'id') &&
    hasProperty(value, 'name') &&
    hasProperty(value, 'email') &&
    isString(value.id) &&
    isString(value.name) &&
    isString(value.email)
  );
}

function assertIsUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new TypeError('Value is not a valid User');
  }
}

function parseUser(data: unknown): Result<User, TypeError> {
  if (isUser(data)) {
    return Ok(data);
  }
  return Err(new TypeError('Invalid user data'));
}
```

### 6. 装饰器模式

```typescript
function Log(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const original = descriptor.value;
  
  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with args:`, args);
    const result = original.apply(this, args);
    console.log(`Result:`, result);
    return result;
  };
  
  return descriptor;
}

function Memoize(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const original = descriptor.value;
  const cache = new Map<string, any>();
  
  descriptor.value = function (...args: any[]) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    
    const result = original.apply(this, args);
    cache.set(key, result);
    return result;
  };
  
  return descriptor;
}

function Validate(
  schema: z.ZodSchema
): MethodDecorator {
  return function (
    target: any,
    propertyKey: string | symbol,
    descriptor: PropertyDescriptor
  ) {
    const original = descriptor.value;
    
    descriptor.value = function (...args: any[]) {
      const result = schema.safeParse(args[0]);
      if (!result.success) {
        throw new ValidationError(result.error);
      }
      return original.apply(this, [result.data, ...args.slice(1)]);
    };
    
    return descriptor;
  };
}

class UserService {
  @Log
  @Memoize
  async getUser(id: string): Promise<User> {
    return fetch(`/api/users/${id}`).then(r => r.json());
  }
  
  @Validate(UserSchema)
  async createUser(data: CreateUserInput): Promise<User> {
    return fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(data)
    }).then(r => r.json());
  }
}
```

## 最佳实践

1. **严格模式**: 启用strict模式
2. **类型推断**: 让TypeScript推断类型
3. **避免any**: 使用unknown替代any
4. **类型复用**: 使用泛型和工具类型
5. **命名规范**: 类型用PascalCase
6. **文档注释**: 使用JSDoc注释类型

## 相关技能

- [backend-nodejs](../nodejs) - Node.js后端
- [frontend-react](../../frontend/react) - React开发
- [api-design](../../actions/code/api-design) - API设计
