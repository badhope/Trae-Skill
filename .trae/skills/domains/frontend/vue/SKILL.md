---
name: vue
description: "Vue.js development for progressive web applications with Composition API. Keywords: vue, vue3, composition api, pinia, vuex, vite, vue开发"
layer: domain
role: specialist
version: 2.0.0
domain: frontend
language: typescript
frameworks:
  - vue3
  - pinia
  - vite
invoked_by:
  - coding-workflow
  - frontend-react
capabilities:
  - component_development
  - state_management
  - routing
  - composition_api
triggers:
  keywords:
    - vue
    - vue3
    - vue.js
    - composition api
    - pinia
    - vuex
    - vite
metrics:
  avg_execution_time: 3s
  success_rate: 0.95
  component_quality: 0.90
---

# Vue.js

Vue.js开发，用于渐进式Web应用开发。

## 目的

提供Vue.js开发的最佳实践：
- 组件开发
- 状态管理
- 路由配置
- Composition API

## 能力

- **组件开发**: Vue组件设计和实现
- **状态管理**: Pinia/Vuex状态管理
- **路由**: Vue Router配置
- **Composition API**: 组合式API使用

## Vue 3特性

### Composition API vs Options API

| 特性 | Composition API | Options API |
|------|----------------|-------------|
| 代码组织 | 按功能组织 | 按选项组织 |
| 逻辑复用 | Composables | Mixins |
| TypeScript | 更好支持 | 一般支持 |
| 适用场景 | 大型项目 | 小型项目 |

## 组件开发

### 基本组件

```vue
<template>
  <div class="counter">
    <p>Count: {{ count }}</p>
    <button @click="increment">+1</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  initialValue: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['change'])

const count = ref(props.initialValue)

const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
  emit('change', count.value)
}
</script>

<style scoped>
.counter {
  padding: 1rem;
}
</style>
```

### Props和Emits

```vue
<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update', 'delete'])

function handleUpdate(item) {
  emit('update', item)
}
</script>
```

### 插槽

```vue
<template>
  <div class="card">
    <header>
      <slot name="header">
        Default Header
      </slot>
    </header>
    <main>
      <slot></slot>
    </main>
    <footer>
      <slot name="footer" :data="footerData">
        Default Footer
      </slot>
    </footer>
  </div>
</template>
```

## Composition API

### 响应式

```typescript
import { ref, reactive, computed, watch, watchEffect } from 'vue'

// ref - 基本类型
const count = ref(0)
count.value++

// reactive - 对象
const state = reactive({
  name: 'Vue',
  version: 3
})

// computed
const doubled = computed(() => count.value * 2)

// watch
watch(count, (newVal, oldVal) => {
  console.log(`Count changed: ${oldVal} -> ${newVal}`)
})

// watchEffect
watchEffect(() => {
  console.log(`Count is: ${count.value}`)
})
```

### Composables

```typescript
// composables/useCounter.ts
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  
  const doubled = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }
  
  function decrement() {
    count.value--
  }
  
  function reset() {
    count.value = initialValue
  }
  
  return {
    count,
    doubled,
    increment,
    decrement,
    reset
  }
}

// 使用
<script setup>
import { useCounter } from './composables/useCounter'

const { count, increment } = useCounter(10)
</script>
```

### 生命周期

```typescript
import {
  onMounted,
  onUpdated,
  onUnmounted,
  onBeforeMount,
  onBeforeUpdate,
  onBeforeUnmount
} from 'vue'

onMounted(() => {
  console.log('Component mounted')
})

onUnmounted(() => {
  // 清理
})
```

## 状态管理

### Pinia

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const isLoggedIn = computed(() => !!user.value)
  
  async function login(credentials) {
    const response = await api.login(credentials)
    user.value = response.user
  }
  
  function logout() {
    user.value = null
  }
  
  return {
    user,
    isLoggedIn,
    login,
    logout
  }
})

// 使用
<script setup>
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const { user, isLoggedIn } = storeToRefs(userStore)
const { login, logout } = userStore
</script>
```

## 路由

### Vue Router

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/users/:id',
    name: 'User',
    component: () => import('@/views/User.vue'),
    props: true,
    children: [
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('@/views/UserProfile.vue')
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫
router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }
})

export default router
```

### 组合式路由

```vue
<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const userId = computed(() => route.params.id)

function navigateToUser(id) {
  router.push({ name: 'User', params: { id } })
}
</script>
```

## 最佳实践

### 1. 组件命名

```
组件文件: PascalCase (UserProfile.vue)
组件注册: PascalCase (<UserProfile />)
Props: camelCase (userName)
Events: kebab-case (user-updated)
```

### 2. 目录结构

```
src/
├── components/
│   ├── common/
│   └── features/
├── composables/
├── stores/
├── views/
├── router/
└── main.ts
```

### 3. 性能优化

```typescript
// 异步组件
const AsyncComponent = defineAsyncComponent(() =>
  import('./components/Heavy.vue')
)

// v-memo
<div v-memo="[item.id]">
  {{ item.name }}
</div>

// 懒加载路由
{
  path: '/heavy',
  component: () => import('@/views/Heavy.vue')
}
```

## 相关技能

- [react](../react) - React开发
- [nextjs](../nextjs) - Next.js框架
- [typescript](../../backend/typescript) - TypeScript
- [css-tailwind](../css-tailwind) - Tailwind CSS
