<template>
  <div class="reader-topbar">
    <RouterLink class="icon-button" to="/documents" aria-label="返回文件库">←</RouterLink>
    <div class="reader-file-title">
      <strong>{{ document?.fileName ?? '未选择文档' }}</strong>
      <span>{{ document ? `${document.fileType.toUpperCase()} · 已保存到第 12 页` : '请选择文档' }}</span>
    </div>
    <div class="reader-tools">
      <button class="tool-button">搜索</button>
      <button class="tool-button" @click="$emit('zoomOut')">−</button>
      <span class="zoom-value">{{ zoom }}%</span>
      <button class="tool-button" @click="$emit('zoomIn')">+</button>
      <button class="tool-button">专注</button>
      <button class="button primary small" @click="$emit('summary')">AI 总结</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { DocumentItem } from '@/types/document'

defineProps<{
  document: DocumentItem | null
  zoom: number
}>()

defineEmits<{
  zoomIn: []
  zoomOut: []
  summary: []
}>()
</script>
