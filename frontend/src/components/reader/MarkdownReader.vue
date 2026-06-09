<template>
  <div class="reader-page markdown-document" :style="{ transform: `scale(${zoom / 100})` }">
    <article class="reader-page-content" v-html="html" @mouseup="$emit('selection', $event)" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps<{
  zoom: number
}>()

defineEmits<{
  selection: [event: MouseEvent]
}>()

const md = new MarkdownIt({ html: false, linkify: true, breaks: true })
const source = `## 产品调研摘录

阅读工作台的核心不是管理文件本身，而是帮助用户把阅读过程中的判断、疑问和摘录沉淀下来。

> 当用户离开文档再回来时，系统应该让他快速恢复上下文。

- 文件列表保持高信息密度。
- 阅读器避免过度装饰。
- AI 助手只在需要时出现。`

const html = computed(() => md.render(source))
void props.zoom
</script>
