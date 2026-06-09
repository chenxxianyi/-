<template>
  <main class="auth-page">
    <section class="auth-brand">
      <div class="brand-mark">KR</div>
      <h1>阅读工作台</h1>
      <p>专注阅读、划线批注与知识整理。</p>
    </section>
    <section class="auth-panel">
      <h2>登录</h2>
      <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
      <label>
        <span>邮箱</span>
        <input v-model="email" type="email" placeholder="reader@example.com" />
      </label>
      <label>
        <span>密码</span>
        <input v-model="password" type="password" placeholder="请输入密码" @keyup.enter="login" />
      </label>
      <button class="button primary full" :disabled="authStore.loading" @click="login">
        {{ authStore.loading ? '登录中…' : '登录' }}
      </button>
      <RouterLink class="text-button" to="/register">没有账号？注册</RouterLink>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')

async function login() {
  if (!email.value || !password.value) return
  try {
    await authStore.login(email.value, password.value)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/dashboard'
    router.push(redirect)
  } catch {
    // 错误信息已在 store 中
  }
}
</script>
