import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchAnnotationsApi,
  fetchAllAnnotationsApi,
  createAnnotationApi,
  updateAnnotationApi,
  deleteAnnotationApi,
} from '@/api/annotation'
import type { AnnotationColor, AnnotationItem, AnnotationType } from '@/types/annotation'

export const useAnnotationStore = defineStore('annotations', () => {
  const annotations = ref<AnnotationItem[]>([])
  const activeAnnotationId = ref<number | null>(null)
  const loading = ref(false)
  const error = ref('')

  const recentAnnotations = computed(() => annotations.value.slice(0, 4))

  function byDocument(documentId: number) {
    return annotations.value.filter((item) => item.documentId === documentId)
  }

  async function fetchRecentAnnotations() {
    loading.value = true
    error.value = ''
    try {
      annotations.value = (await fetchAllAnnotationsApi(10)) as AnnotationItem[]
    } catch (e: any) {
      error.value = e.message || '获取最近批注失败'
    } finally {
      loading.value = false
    }
  }

  async function fetchAnnotations(documentId: number) {
    loading.value = true
    error.value = ''
    try {
      annotations.value = (await fetchAnnotationsApi(documentId)) as AnnotationItem[]
    } catch (e: any) {
      error.value = e.message || '获取批注失败'
    } finally {
      loading.value = false
    }
  }

  async function createAnnotation(payload: {
    documentId: number
    selectedText: string
    color: AnnotationColor
    annotationType?: AnnotationType
    note?: string
    pageNumber?: number
  }) {
    error.value = ''
    try {
      const annotation = (await createAnnotationApi(payload.documentId, payload)) as AnnotationItem
      annotations.value.unshift(annotation)
      activeAnnotationId.value = annotation.id
      return annotation
    } catch (e: any) {
      error.value = e.message || '创建批注失败'
      throw e
    }
  }

  async function updateAnnotation(id: number, payload: {
    color?: string
    note?: string
    selectedText?: string
    annotationType?: string
    tags?: string[]
  }) {
    error.value = ''
    try {
      const updated = (await updateAnnotationApi(id, payload)) as AnnotationItem
      const idx = annotations.value.findIndex((a) => a.id === id)
      if (idx !== -1) annotations.value[idx] = updated
      return updated
    } catch (e: any) {
      error.value = e.message || '更新批注失败'
      throw e
    }
  }

  async function deleteAnnotation(id: number) {
    error.value = ''
    try {
      await deleteAnnotationApi(id)
      annotations.value = annotations.value.filter((item) => item.id !== id)
      if (activeAnnotationId.value === id) {
        activeAnnotationId.value = annotations.value[0]?.id ?? null
      }
    } catch (e: any) {
      error.value = e.message || '删除批注失败'
      throw e
    }
  }

  function setActiveAnnotation(id: number) {
    activeAnnotationId.value = id
  }

  return {
    annotations,
    activeAnnotationId,
    loading,
    error,
    recentAnnotations,
    byDocument,
    fetchRecentAnnotations,
    fetchAnnotations,
    createAnnotation,
    updateAnnotation,
    deleteAnnotation,
    setActiveAnnotation,
  }
})
