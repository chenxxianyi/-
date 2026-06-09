import { request } from '@/utils/request'
import type { AnnotationColor, AnnotationType } from '@/types/annotation'

export function fetchAnnotationsApi(documentId: number) {
  return request.get(`/documents/${documentId}/annotations`)
}

export function fetchAllAnnotationsApi(limit = 20) {
  return request.get(`/annotations?limit=${limit}`)
}

export function createAnnotationApi(
  documentId: number,
  payload: {
    selectedText?: string
    color?: AnnotationColor
    annotationType?: AnnotationType
    note?: string
    pageNumber?: number
    positionData?: Record<string, unknown>
    rangeData?: Record<string, unknown>
    tags?: string[]
  },
) {
  return request.post(`/documents/${documentId}/annotations`, {
    documentId,
    ...payload,
  })
}

export function updateAnnotationApi(
  annotationId: number,
  payload: {
    color?: string
    note?: string
    selectedText?: string
    annotationType?: string
    tags?: string[]
  },
) {
  return request.put(`/annotations/${annotationId}`, payload)
}

export function deleteAnnotationApi(annotationId: number) {
  return request.delete(`/annotations/${annotationId}`)
}
