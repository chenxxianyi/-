<template>
  <div class="reader-shell">
    <aside class="reader-left-panel">
      <div class="panel-section">
        <h3>目录</h3>
        <button class="outline-item active">摘要与问题定义</button>
        <button class="outline-item">相关研究</button>
        <button class="outline-item">方法与实验</button>
        <button class="outline-item">结论与限制</button>
      </div>
      <div class="panel-section">
        <h3>页面</h3>
        <div class="thumb-list">
          <button class="page-thumb active">12</button>
          <button class="page-thumb">13</button>
          <button class="page-thumb">14</button>
        </div>
      </div>
      <div class="panel-section muted-box">
        <h3>文件信息</h3>
        <p>{{ document?.pageCount ?? 0 }} 页 · {{ document?.wordCount ?? 0 }} 字 · {{ document?.annotationCount ?? 0 }} 条批注</p>
      </div>
    </aside>

    <section class="reader-stage" ref="stageRef">
      <PdfReader
        v-if="document?.fileType === 'pdf'"
        :zoom="zoom"
        :annotations="annotations"
        :active-annotation-id="activeAnnotationId"
        @selection="handleSelection"
      />
      <MarkdownReader v-else-if="document?.fileType === 'md'" :zoom="zoom" @selection="handleSelection" />
      <TxtReader v-else-if="document?.fileType === 'txt'" :zoom="zoom" @selection="handleSelection" />
      <DocxReader v-else :zoom="zoom" @selection="handleSelection" />
      <SelectionToolbar
        :visible="toolbar.visible"
        :x="toolbar.x"
        :y="toolbar.y"
        @highlight="(color) => $emit('annotate', color)"
        @underline="$emit('underline')"
        @note="$emit('note')"
        @excerpt="$emit('excerpt')"
        @explain="$emit('explain')"
      />
    </section>

    <AnnotationSidebar
      :annotations="annotations"
      :notes="notes"
      :active-annotation-id="activeAnnotationId"
      :ai-answer="aiAnswer"
      @activate="$emit('activateAnnotation', $event)"
      @delete="$emit('deleteAnnotation', $event)"
      @ai="$emit('ai', $event)"
      @ask="$emit('ask', $event)"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { AnnotationColor, AnnotationItem } from '@/types/annotation'
import type { DocumentItem } from '@/types/document'
import type { NoteItem } from '@/types/note'
import AnnotationSidebar from './AnnotationSidebar.vue'
import DocxReader from './DocxReader.vue'
import MarkdownReader from './MarkdownReader.vue'
import PdfReader from './PdfReader.vue'
import SelectionToolbar from './SelectionToolbar.vue'
import TxtReader from './TxtReader.vue'

defineProps<{
  document: DocumentItem | null
  zoom: number
  annotations: AnnotationItem[]
  notes: NoteItem[]
  activeAnnotationId: number | null
  aiAnswer: { title: string; text: string }
}>()

const emit = defineEmits<{
  selectText: [text: string]
  annotate: [color: Exclude<AnnotationColor, 'red'>]
  underline: []
  note: []
  excerpt: []
  explain: []
  activateAnnotation: [id: number]
  deleteAnnotation: [id: number]
  ai: [action: 'summary' | 'explain' | 'translate']
  ask: [question: string]
}>()

const toolbar = reactive({
  visible: false,
  x: 0,
  y: 0,
})

function handleSelection() {
  const selection = window.getSelection()
  const text = selection?.toString().trim() ?? ''
  if (!selection || selection.isCollapsed || !text) {
    toolbar.visible = false
    return
  }
  const rect = selection.getRangeAt(0).getBoundingClientRect()
  toolbar.x = Math.min(rect.left, window.innerWidth - 360)
  toolbar.y = Math.max(rect.top - 46, 64)
  toolbar.visible = true
  emit('selectText', text)
}
</script>
