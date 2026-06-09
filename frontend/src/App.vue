<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <router-view />
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import type { GlobalThemeOverrides } from 'naive-ui'
import { useAuthStore } from '@/stores/authStore'

const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#2563EB',
    primaryColorHover: '#1D4ED8',
    borderRadius: '8px',
    fontFamily:
      'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif',
  },
}

const authStore = useAuthStore()

onMounted(() => {
  // 如果已有 token，尝试获取用户信息
  if (authStore.token) {
    authStore.fetchProfile()
  }
})
</script>
