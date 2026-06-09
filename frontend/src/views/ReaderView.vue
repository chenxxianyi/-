<template>
  <section class="view active reader-view" aria-labelledby="readerTitle">
    <ReaderTopBar
      :document="currentDocument"
      :zoom="zoom"
      @zoom-in="zoom = Math.min(130, zoom + 10)"
      @zoom-out="zoom = Math.max(80, zoom - 10)"
      @summary="handleSummary"
    />
    <ReaderShell
      :document="currentDocument"
      :zoom="zoom"
      :annotations="documentAnnotations"
      :notes="notes"
      :active-annotation-id="activeAnnotationId"
      :ai-answer="aiAnswer"
      @select-text="selectedText = $event"
      @annotate="createHighlight"
      @underline="createUnderline"
      @note="createNoteAnnotation"
      @excerpt="createExcerpt"
      @explain="handleExplain"
      @translate="handleTranslate"
      @activate-annotation="annotationStore.setActiveAnnotation"
      @delete-annotation="annotationStore.deleteAnnotation"
      @ai="handleAiAction"
      @ask="askAi"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useRoute } from 'vue-router'
import ReaderShell from '@/components/reader/ReaderShell.vue'
import ReaderTopBar from '@/components/reader/ReaderTopBar.vue'
import { askDocumentAiApi, aiSummaryApi, aiExplainApi, aiTranslateApi } from '@/api/ai'
import { useAnnotationStore } from '@/stores/annotationStore'
import { useDocumentStore } from '@/stores/documentStore'
import { useNoteStore } from '@/stores/noteStore'
import type { AnnotationColor } from '@/types/annotation'

const route = useRoute()
const documentStore = useDocumentStore()
const annotationStore = useAnnotationStore()
const noteStore = useNoteStore()
const { currentDocument } = storeToRefs(documentStore)
const { activeAnnotationId } = storeToRefs(annotationStore)
const { notes } = storeToRefs(noteStore)

const zoom = ref(100)
const selectedText = ref('')
const aiAnswer = ref<{ title: string; text: string }>({
  title: 'AI 阅读助手',
  text: '选择一段文字，或点击上方按钮获取当前文档的总结。',
})

const documentAnnotations = computed(() => {
  const id = currentDocument.value?.id ?? 1
  return annotationStore.byDocument(id)
})

async function loadDocument() {
  const id = Number(route.params.documentId || 1)
  await documentStore.fetchDocumentDetail(id)
  await annotationStore.fetchAnnotations(id)
  await noteStore.fetchNotes()
}

function createHighlight(color: Exclude<AnnotationColor, 'red'>) {
  if (!selectedText.value || !currentDocument.value) return
  annotationStore.createAnnotation({
    documentId: currentDocument.value.id,
    selectedText: selectedText.value,
    color,
  })
}

function createUnderline() {
  if (!selectedText.value || !currentDocument.value) return
  annotationStore.createAnnotation({
    documentId: currentDocument.value.id,
    selectedText: selectedText.value,
    color: 'yellow',
    annotationType: 'underline',
  })
}

function createNoteAnnotation() {
  if (!selectedText.value || !currentDocument.value) return
  annotationStore.createAnnotation({
    documentId: currentDocument.value.id,
    selectedText: selectedText.value,
    color: 'yellow',
    annotationType: 'note',
    note: '',
  })
}

function createExcerpt() {
  if (!selectedText.value || !currentDocument.value) return
  noteStore.createFromAnnotation(selectedText.value, currentDocument.value.id)
}

/* ---- AI 操作 ---- */

async function handleSummary() {
  const docId = currentDocument.value?.id
  if (!docId) return
  try {
    const data = await aiSummaryApi(docId) as { answer: string }
    aiAnswer.value = { title: '文档总结', text: data.answer }
  } catch {
    aiAnswer.value = { title: '文档总结', text: 'AI 服务暂不可用，请稍后重试。' }
  }
}

async function handleExplain() {
  if (!selectedText.value) {
    aiAnswer.value = { title: 'AI 解释', text: '请先在阅读区选中文本，再请求解释。' }
    return
  }
  const docId = currentDocument.value?.id
  if (!docId) return
  try {
    const data = await aiExplainApi(docId, selectedText.value) as { answer: string }
    aiAnswer.value = { title: 'AI 解释', text: data.answer }
  } catch {
    aiAnswer.value = { title: 'AI 解释', text: 'AI 服务暂不可用，请稍后重试。' }
  }
}

async function handleTranslate() {
  if (!selectedText.value) {
    aiAnswer.value = { title: '翻译结果', text: '请先在阅读区选中文本，再请求翻译。' }
    return
  }
  const docId = currentDocument.value?.id
  if (!docId) return
  try {
    const data = await aiTranslateApi(docId, selectedText.value) as { answer: string }
    aiAnswer.value = { title: '翻译结果', text: data.answer }
  } catch {
    aiAnswer.value = { title: '翻译结果', text: 'AI 服务暂不可用，请稍后重试。' }
  }
}

async function askAi(question: string) {
  const docId = currentDocument.value?.id
  if (!docId || !question.trim()) return
  try {
    const data = await askDocumentAiApi(docId, question) as { answer: string }
    aiAnswer.value = { title: '文档问答', text: data.answer }
  } catch {
    aiAnswer.value = { title: '文档问答', text: 'AI 服务暂不可用，请稍后重试。' }
  }
}

function handleAiAction(action: string) {
  if (action === 'summary' || action === '文档总结') {
    handleSummary()
  } else if (action === 'translate') {
    handleTranslate()
  } else {
    handleExplain()
  }
}

onMounted(loadDocument)
watch(() => route.params.documentId, loadDocument)
</script>
