import { request } from '@/utils/request'

export function fetchNotesApi() {
  return request.get('/notes')
}

export function createNoteApi(payload: {
  documentId?: number
  sourceAnnotationId?: number
  title?: string
  content?: string
  excerpt?: string
  source?: string
  contentType?: string
  tags?: string[]
}) {
  return request.post('/notes', payload)
}

export function updateNoteApi(
  noteId: number,
  payload: {
    title?: string
    content?: string
    excerpt?: string
    source?: string
    contentType?: string
    tags?: string[]
  },
) {
  return request.put(`/notes/${noteId}`, payload)
}

export function deleteNoteApi(noteId: number) {
  return request.delete(`/notes/${noteId}`)
}

export function createNoteFromAnnotationApi(payload: {
  documentId: number
  sourceAnnotationId: number
  title?: string
}) {
  return request.post('/notes/from-annotation', payload)
}
