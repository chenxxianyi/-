import { request } from '@/utils/request'

export function askDocumentAiApi(documentId: number, question: string) {
  return request.post(`/documents/${documentId}/ai/ask`, { question })
}

export function aiSummaryApi(documentId: number) {
  return request.post('/ai/summary', { documentId })
}

export function aiExplainApi(documentId: number, text: string) {
  return request.post('/ai/explain', { documentId, text })
}

export function aiTranslateApi(documentId: number, text: string, targetLanguage = '中文') {
  return request.post('/ai/translate', { documentId, text, targetLanguage })
}

export function aiChatApi(documentId: number, message: string) {
  return request.post('/ai/chat', { documentId, message })
}
