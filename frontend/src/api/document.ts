import { request } from '@/utils/request'

export function fetchDocumentsApi() {
  return request.get('/documents')
}

export function fetchDocumentDetailApi(id: number) {
  return request.get(`/documents/${id}`)
}

export function uploadDocumentApi(file: File) {
  const form = new FormData()
  form.append('file', file)
  return request.post('/documents/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export function updateDocumentApi(id: number, payload: { title?: string }) {
  return request.put(`/documents/${id}`, payload)
}

export function deleteDocumentApi(id: number) {
  return request.delete(`/documents/${id}`)
}

export function getDocumentContentApi(id: number) {
  return request.get(`/documents/${id}/content`)
}

export function saveReadPositionApi(id: number, payload: { position?: Record<string, unknown>; progress?: number }) {
  return request.put(`/documents/${id}/read-position`, payload)
}
