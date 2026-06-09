export interface NoteItem {
  id: number
  documentId?: number
  sourceAnnotationId?: number
  title: string
  content: string
  excerpt: string
  source: string
  contentType: 'markdown' | 'richtext'
  tags: string[]
  createdAt: string
  updatedAt: string
}
