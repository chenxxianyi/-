<template>
  <div class="reader-page" :style="{ transform: `scale(${zoom / 100})` }">
    <div class="pdf-page-label">Page 12</div>
    <AnnotationLayer :annotations="annotations" :active-id="activeAnnotationId" />
    <article ref="contentRef" class="reader-page-content" @mouseup="$emit('selection', $event)">
      <h2>阅读复杂文档时，批注是理解的外部记忆</h2>
      <p>
        在长文档阅读中，用户并不是简单地从第一页顺序读到最后一页。更常见的行为是来回跳转、标记关键段落、记录疑问，并在之后重新组织这些片段。
        因此，一个阅读工作台需要把文档、批注、摘录和笔记放在同一个上下文中，而不是把它们拆散到不同工具里。
      </p>
      <p>
        <mark class="highlight-yellow">稳定的高亮位置需要保存相对坐标，而不是固定像素。</mark>
        当 PDF 缩放或页面重新渲染时，百分比坐标可以让覆盖层跟随页面尺寸变化，减少错位问题。
      </p>
      <p>
        对 Markdown 和 TXT 来说，MVP 阶段可以先保存选中文本和简化 range 信息。后续如果要支持编辑后的重新定位，则需要引入文本锚点系统，例如 quote selector 和 position selector 的组合。
      </p>
      <p>
        AI 阅读助手应该是辅助工具。它可以帮助用户总结文档、解释术语、翻译片段或基于文档提问，但它不应该在界面上喧宾夺主。真正的主角始终是文档内容和用户自己的思考。
      </p>
    </article>
  </div>
</template>

<script setup lang="ts">
import * as pdfjsLib from 'pdfjs-dist'
import type { AnnotationItem } from '@/types/annotation'
import AnnotationLayer from './AnnotationLayer.vue'

defineProps<{
  zoom: number
  annotations: AnnotationItem[]
  activeAnnotationId: number | null
}>()

defineEmits<{
  selection: [event: MouseEvent]
}>()

void pdfjsLib.version
</script>
