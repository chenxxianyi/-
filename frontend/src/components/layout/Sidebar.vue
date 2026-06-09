<template>
  <aside class="sidebar" aria-label="主导航">
    <div class="brand">
      <div class="brand-mark">KR</div>
      <div>
        <div class="brand-name">阅读工作台</div>
        <div class="brand-subtitle">Knowledge Reader</div>
      </div>
    </div>

    <nav class="nav-list">
      <RouterLink v-for="item in navItems" :key="item.name" class="nav-item" :to="item.to" :class="{ active: route.name === item.name }">
        <span class="nav-icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="sidebar-footer">
      <div class="storage-row">
        <span>存储空间</span>
        <span>2.4 / 10 GB</span>
      </div>
      <div class="storage-track">
        <span style="width: 24%" />
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { name: 'dashboard', to: '/dashboard', label: '工作台', icon: 'D' },
  { name: 'documents', to: '/documents', label: '文件库', icon: 'F' },
  { name: 'reader', to: '/reader/1', label: '阅读器', icon: 'R' },
  { name: 'notes', to: '/notes', label: '笔记', icon: 'N' },
  { name: 'settings', to: '/settings', label: '设置', icon: 'S' },
]
</script>
