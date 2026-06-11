<template>
  <main class="auth-page auth-page-register">
    <section class="auth-brand">
      <div class="auth-brand-top">
        <div class="auth-brand-mark">阅</div>
        <span>知阅工作台</span>
      </div>
      <div class="auth-hero-copy">
        <p class="auth-eyebrow">Start reading better</p>
        <h1>给你的资料库一个稳定入口</h1>
        <p>创建账号后，文档、批注、笔记和阅读进度都会归档到同一个工作台。</p>
      </div>
      <div class="auth-preview" aria-hidden="true">
        <div class="auth-preview-paper main">
          <span></span>
          <strong>我的阅读项目</strong>
          <i></i>
          <i></i>
          <em></em>
          <i></i>
        </div>
        <div class="auth-preview-paper note">
          <span>+</span>
          <strong>新建知识库</strong>
          <i></i>
          <i></i>
        </div>
      </div>
    </section>
    <section class="auth-panel">
      <div class="auth-panel-head">
        <p class="auth-eyebrow">Create account</p>
        <h2>注册账号</h2>
        <p>开启你的个人阅读工作台。</p>
      </div>
      <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
      <label>
        <span>用户名</span>
        <input v-model="username" placeholder="researcher" />
      </label>
      <label>
        <span>邮箱</span>
        <input v-model="email" type="email" placeholder="reader@example.com" />
      </label>
      <label>
        <span>密码</span>
        <input v-model="password" type="password" placeholder="请输入密码" />
      </label>
      <label>
        <span>确认密码</span>
        <input v-model="confirmPassword" type="password" placeholder="再次输入密码" />
      </label>
      <button class="button primary full" :disabled="authStore.loading" @click="register">
        {{ authStore.loading ? '注册中…' : '注册' }}
      </button>
      <p class="auth-switch">
        已有账号？
        <RouterLink class="text-button" to="/login">返回登录</RouterLink>
      </p>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

async function register() {
  if (!username.value || !email.value || !password.value) return
  if (password.value !== confirmPassword.value) {
    authStore.error = '两次输入的密码不一致'
    return
  }
  try {
    await authStore.register(username.value, email.value, password.value)
    router.push('/dashboard')
  } catch {
    // 错误信息已在 store 中
  }
}
</script>
