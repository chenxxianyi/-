import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchDocumentsApi,
  fetchDocumentDetailApi,
  uploadDocumentApi,
  updateDocumentApi,
  deleteDocumentApi,
  saveReadPositionApi,
} from '@/api/document'
import type { DocumentItem, DocumentType } from '@/types/document'

export const useDocumentStore = defineStore('documents', () => {
  const documents = ref<DocumentItem[]>([])
  const currentDocument = ref<DocumentItem | null>(null)
  const loading = ref(false)
  const uploading = ref(false)
  const uploadProgress = ref(0)
  const error = ref('')
  const filters = ref<{ keyword: string; type: DocumentType | 'all' }>({
    keyword: '',
    type: 'all',
  })

  const filteredDocuments = computed(() => {
    const keyword = filters.value.keyword.trim().toLowerCase()
    return documents.value.filter((item) => {
      const matchType = filters.value.type === 'all' || item.fileType === filters.value.type
      const matchKeyword =
        !keyword ||
        item.fileName.toLowerCase().includes(keyword) ||
        item.fileType.toLowerCase().includes(keyword)
      return matchType && matchKeyword
    })
  })

  async function fetchDocuments() {
    loading.value = true
    error.value = ''
    try {
      documents.value = (await fetchDocumentsApi()) as DocumentItem[]
    } catch (e: any) {
      error.value = e.message || '获取文档列表失败'
    } finally {
      loading.value = false
    }
  }

  async function fetchDocumentDetail(id: number) {
    loading.value = true
    error.value = ''
    try {
      currentDocument.value = (await fetchDocumentDetailApi(id)) as DocumentItem
    } catch (e: any) {
      error.value = e.message || '获取文档详情失败'
    } finally {
      loading.value = false
    }
    return currentDocument.value
  }

  async function uploadDocument(file: File) {
    if (uploading.value) return
    uploading.value = true
    uploadProgress.value = 0
    error.value = ''
    try {
      // 模拟上传进度
      const timer = window.setInterval(() => {
        uploadProgress.value = Math.min(uploadProgress.value + 20, 80)
      }, 150)

      const doc = (await uploadDocumentApi(file)) as DocumentItem
      window.clearInterval(timer)
      uploadProgress.value = 100
      documents.value.unshift(doc)
      return doc
    } catch (e: any) {
      error.value = e.message || '上传失败'
      throw e
    } finally {
      setTimeout(() => {
        uploading.value = false
        uploadProgress.value = 0
      }, 500)
    }
  }

  async function renameDocument(id: number) {
    const item = documents.value.find((doc) => doc.id === id)
    if (!item) return
    error.value = ''
    try {
      const newName = item.fileName.replace(/\.(pdf|md|docx|txt)$/i, '（已重命名）.$1')
      const updated = (await updateDocumentApi(id, { title: newName })) as DocumentItem
      Object.assign(item, updated)
      if (currentDocument.value?.id === id) {
        currentDocument.value = { ...item }
      }
    } catch (e: any) {
      error.value = e.message || '重命名失败'
    }
  }

  async function deleteDocument(id: number) {
    error.value = ''
    try {
      await deleteDocumentApi(id)
      documents.value = documents.value.filter((item) => item.id !== id)
      if (currentDocument.value?.id === id) {
        currentDocument.value = documents.value[0] ?? null
      }
    } catch (e: any) {
      error.value = e.message || '删除失败'
    }
  }

  async function saveReadPosition(id: number, position?: Record<string, unknown>, progress?: number) {
    try {
      await saveReadPositionApi(id, { position, progress })
    } catch {
      // 静默处理阅读进度保存失败
    }
  }

  function setKeyword(keyword: string) {
    filters.value.keyword = keyword
  }

  function setType(type: DocumentType | 'all') {
    filters.value.type = type
  }

  return {
    documents,
    currentDocument,
    loading,
    uploading,
    uploadProgress,
    error,
    filters,
    filteredDocuments,
    fetchDocuments,
    fetchDocumentDetail,
    setKeyword,
    setType,
    uploadDocument,
    renameDocument,
    deleteDocument,
    saveReadPosition,
  }
})
