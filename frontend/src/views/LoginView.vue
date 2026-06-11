<template>
  <main class="auth-page auth-page-login">
    <section class="auth-brand">
      <div class="auth-brand-top">
        <div class="auth-brand-mark">阅</div>
        <span>知阅工作台</span>
      </div>
      <div class="auth-hero-copy">
        <p class="auth-eyebrow">Knowledge Reader</p>
        <h1>把阅读沉淀成可复用的知识</h1>
        <p>继续整理文档、批注和笔记，让每一次阅读都有清晰去处。</p>
      </div>
      <div class="auth-preview" aria-hidden="true">
        <div class="auth-preview-paper main">
          <span></span>
          <strong>年度研究材料.pdf</strong>
          <i></i>
          <i></i>
          <em></em>
          <i></i>
        </div>
        <div class="auth-preview-paper note">
          <span>AI</span>
          <strong>3 条可追踪摘要</strong>
          <i></i>
          <i></i>
        </div>
      </div>
    </section>
    <section class="auth-panel">
      <div class="auth-panel-head">
        <p class="auth-eyebrow">Welcome back</p>
        <h2>登录账号</h2>
        <p>回到你的阅读空间。</p>
      </div>
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
      <p class="auth-switch">
        没有账号？
        <RouterLink class="text-button" to="/register">立即注册</RouterLink>
      </p>
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
