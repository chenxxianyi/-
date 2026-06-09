<template>
  <div class="reader-page docx-document" :style="{ transform: `scale(${zoom / 100})` }">
    <article class="reader-page-content" @mouseup="$emit('selection', $event)">
      <h2>行业分析报告</h2>
      <p>这里展示后端转换后的 DOCX 文本占位。真实版本中，后端会把 DOCX 转为结构化 HTML，前端在阅读态渲染并挂载批注层。</p>
      <p><mark class="highlight-blue">转换失败时需要提供基础文本或错误状态，不能让用户面对空白页面。</mark></p>
      <p>当前 Vue3 demo 保留与 PDF 阅读器一致的排版、选区捕获和 AI 辅助入口。</p>
    </article>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  zoom: number
}>()

defineEmits<{
  selection: [event: MouseEvent]
}>()
</script>
