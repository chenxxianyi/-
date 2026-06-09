<template>
  <div class="reader-page txt-document" :style="{ transform: `scale(${zoom / 100})` }">
    <article class="reader-page-content" @mouseup="$emit('selection', $event)">
      <h2>会议纪要</h2>
      <p>本次讨论聚焦阅读器 MVP：文件库、阅读区、批注列表、笔记编辑和 AI 辅助面板先打通一条完整流程。</p>
      <p>移动端优先保证阅读正文可用，复杂列表转换为紧凑信息块，避免把桌面表格直接缩小。</p>
      <p>后续对接真实 API 时，前端 store 保持同一状态模型，替换 mock 数据即可。</p>
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
