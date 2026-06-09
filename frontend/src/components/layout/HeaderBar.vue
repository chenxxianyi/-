<template>
  <header class="header-bar">
    <button class="mobile-menu" aria-label="打开导航">Menu</button>
    <div>
      <div class="header-title">{{ meta.title }}</div>
      <div class="header-subtitle">{{ meta.subtitle }}</div>
    </div>
    <div class="header-actions">
      <label class="search-field">
        <span>Search</span>
        <input v-model="globalSearch" type="search" placeholder="搜索文档、批注、笔记" />
      </label>
      <button class="button secondary" @click="emit('sync')">同步</button>
      <RouterLink class="button primary" to="/documents">上传文件</RouterLink>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const emit = defineEmits<{
  sync: []
}>()

const route = useRoute()
const globalSearch = ref('')

const metas: Record<string, { title: string; subtitle: string }> = {
  dashboard: { title: '工作台', subtitle: '继续阅读、整理批注和笔记' },
  documents: { title: '文件库', subtitle: '上传、搜索和管理所有阅读资料' },
  reader: { title: '阅读器', subtitle: '阅读、划线、批注和 AI 辅助理解' },
  notes: { title: '笔记', subtitle: '整理摘录和自己的思考' },
  settings: { title: '设置', subtitle: '用户资料、主题和 AI 配置预留' },
}

const meta = computed(() => metas[String(route.name)] ?? metas.dashboard)
</script>
