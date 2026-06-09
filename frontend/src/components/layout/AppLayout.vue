<template>
  <div class="app-shell">
    <Sidebar />
    <div class="workspace">
      <HeaderBar @sync="showToast('已模拟同步最新阅读数据')" />
      <main class="main-content">
        <RouterView />
      </main>
    </div>
    <div class="toast" :class="{ hidden: !toast }">{{ toast }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import Sidebar from './Sidebar.vue'
import HeaderBar from './HeaderBar.vue'

const toast = ref('')
let toastTimer = 0

function showToast(message: string) {
  toast.value = message
  window.clearTimeout(toastTimer)
  toastTimer = window.setTimeout(() => {
    toast.value = ''
  }, 2200)
}
</script>
