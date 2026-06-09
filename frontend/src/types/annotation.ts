export type AnnotationType = 'highlight' | 'underline' | 'note'
export type AnnotationColor = 'yellow' | 'blue' | 'green' | 'red'

export interface AnnotationItem {
  id: number
  documentId: number
  pageNumber?: number
  annotationType: AnnotationType
  color: AnnotationColor
  selectedText: string
  note?: string
  positionData?: Record<string, unknown>
  rangeData?: Record<string, unknown>
  tags: string[]
  createdAt: string
  updatedAt: string
}
