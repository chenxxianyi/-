<template>
  <main class="auth-page">
    <section class="auth-brand">
      <div class="brand-mark">KR</div>
      <h1>阅读工作台</h1>
      <p>创建账号后开始管理你的文档、批注和笔记。</p>
    </section>
    <section class="auth-panel">
      <h2>注册</h2>
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
      <RouterLink class="text-button" to="/login">返回登录</RouterLink>
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
