export type DocumentType = 'pdf' | 'md' | 'txt' | 'docx' | 'png' | 'jpg' | 'jpeg'

export interface DocumentItem {
  id: number
  title: string
  fileName: string
  fileType: DocumentType
  mimeType: string
  fileSize: number
  displaySize: string
  parsedStatus: 'pending' | 'success' | 'failed'
  pageCount: number
  wordCount: number
  annotationCount: number
  progress: number
  lastReadAt: string
  uploadedAt: string
  lastReadPosition?: Record<string, unknown>
  createdAt: string
  updatedAt: string
}
