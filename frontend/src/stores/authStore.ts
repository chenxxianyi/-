import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { loginApi, registerApi, getMeApi } from '@/api/auth'
import type { UserProfile } from '@/types/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(window.localStorage.getItem('kr_token') ?? '')
  const currentUser = ref<UserProfile | null>(null)
  const loading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => Boolean(token.value))

  function setToken(value: string) {
    token.value = value
    window.localStorage.setItem('kr_token', value)
  }

  function clearToken() {
    token.value = ''
    window.localStorage.removeItem('kr_token')
  }

  async function login(email: string, password: string) {
    loading.value = true
    error.value = ''
    try {
      const data = await loginApi({ email, password }) as { accessToken: string }
      setToken(data.accessToken)
      await fetchProfile()
    } catch (e: any) {
      error.value = e.message || '登录失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function register(username: string, email: string, password: string) {
    loading.value = true
    error.value = ''
    try {
      const data = await registerApi({ username, email, password }) as { accessToken: string }
      setToken(data.accessToken)
      await fetchProfile()
    } catch (e: any) {
      error.value = e.message || '注册失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function fetchProfile() {
    if (!token.value) return
    try {
      currentUser.value = await getMeApi() as UserProfile
    } catch {
      // token invalid, clear it
      clearToken()
      currentUser.value = null
    }
  }

  function logout() {
    clearToken()
    currentUser.value = null
    error.value = ''
  }

  return { token, currentUser, loading, error, isAuthenticated, login, register, logout, fetchProfile }
})
