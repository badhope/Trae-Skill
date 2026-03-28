---
name: frontend-vue
description: "Vue.js and Nuxt.js development expert with Composition API, Pinia state management, and composables. Keywords: vue, nuxt, pinia, composition-api, typescript, frontend"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
language: typescript
frameworks:
  - vue
  - nuxt
invoked_by:
  - coding-workflow
capabilities:
  - component_development
  - state_management
  - composables
  - ssr
  - testing
---

# Frontend Vue

Vue.js和Nuxt.js开发专家，精通Composition API、Pinia状态管理和Composables。

## 适用场景

- 构建Vue应用
- 使用Composition API
- Pinia状态管理
- Nuxt.js SSR
- 组件设计
- 组件测试

## 核心概念

### Composition API

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';

const props = defineProps<{ userId: string }>();
const emit = defineEmits<{ update: [user: User] }>();

interface User {
  id: string;
  name: string;
  email: string;
}

const user = ref<User | null>(null);
const loading = ref(true);

const displayName = computed(() => user.value?.name ?? 'Unknown');

async function fetchUser() {
  loading.value = true;
  const response = await fetch(`/api/users/${props.userId}`);
  user.value = await response.json();
  loading.value = false;
}

watch(() => props.userId, fetchUser, { immediate: true });
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="user" class="user-profile">
    <h1>{{ user.name }}</h1>
    <p>{{ user.email }}</p>
  </div>
</template>

<style scoped>
.user-profile { padding: 1rem; }
</style>
```

### Composables

```typescript
import { ref, watch, type Ref } from 'vue';

export function useFetch<T>(url: Ref<string> | string) {
  const data = ref<T | null>(null) as Ref<T | null>;
  const loading = ref(true);
  const error = ref<Error | null>(null);
  
  async function fetchData() {
    loading.value = true;
    try {
      const response = await fetch(typeof url === 'string' ? url : url.value);
      data.value = await response.json();
    } catch (err) {
      error.value = err as Error;
    } finally {
      loading.value = false;
    }
  }
  
  if (typeof url === 'string') {
    fetchData();
  } else {
    watch(url, fetchData, { immediate: true });
  }
  
  return { data, loading, error, refetch: fetchData };
}

export function useDebounce<T>(value: Ref<T>, delay: number) {
  const debouncedValue = ref(value.value) as Ref<T>;
  
  watch(value, (newValue) => {
    const timer = setTimeout(() => {
      debouncedValue.value = newValue;
    }, delay);
    return () => clearTimeout(timer);
  });
  
  return debouncedValue;
}
```

### Pinia Store

```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  
  const isAuthenticated = computed(() => !!token.value);
  
  async function login(email: string, password: string) {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    user.value = data.user;
    token.value = data.token;
  }
  
  function logout() {
    user.value = null;
    token.value = null;
  }
  
  return { user, token, isAuthenticated, login, logout };
});
```

## Nuxt.js

### 页面和路由

```vue
<script setup lang="ts">
const route = useRoute();
const { data: user, pending } = await useFetch(`/api/users/${route.params.id}`);
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else>
    <h1>{{ user?.name }}</h1>
  </div>
</template>
```

### 服务端路由

```typescript
export default defineEventHandler(async (event) => {
  const method = getMethod(event);
  const id = getRouterParam(event, 'id');
  
  if (method === 'GET') {
    return await getUserById(id);
  }
  
  if (method === 'PUT') {
    const body = await readBody(event);
    return await updateUser(id, body);
  }
  
  throw createError({ statusCode: 405, message: 'Method not allowed' });
});
```

## 组件模式

### Props和Emits

```vue
<script setup lang="ts">
interface Props {
  title: string;
  items: Array<{ id: string; name: string }>;
  maxItems?: number;
}

const props = withDefaults(defineProps<Props>(), {
  maxItems: 10,
});

const emit = defineEmits<{
  select: [item: { id: string; name: string }];
  delete: [id: string];
}>();

const visibleItems = computed(() => props.items.slice(0, props.maxItems));
</script>

<template>
  <div class="list">
    <h2>{{ title }}</h2>
    <ul>
      <li
        v-for="item in visibleItems"
        :key="item.id"
        @click="emit('select', item)"
      >
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>
```

### v-model

```vue
<script setup lang="ts">
const model = defineModel<string>({ default: '' });
</script>

<template>
  <input
    :value="model"
    @input="model = ($event.target as HTMLInputElement).value"
  />
</template>
```

## 最佳实践

1. **TypeScript**: 类型安全
2. **Composition API**: 使用script setup
3. **状态管理**: Pinia
4. **组件设计**: 单一职责
5. **可访问性**: 语义化HTML
6. **测试**: Vitest

## 相关技能

- [frontend-react](../react) - React开发
- [backend-nodejs](../../backend/nodejs) - Node.js后端
