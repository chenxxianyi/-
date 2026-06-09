import type { DocumentType } from '@/types/document'

const supportedTypes: DocumentType[] = ['pdf', 'md', 'txt', 'docx', 'png', 'jpg', 'jpeg']

export function isSupportedDocumentType(type: string): type is DocumentType {
  return supportedTypes.includes(type.toLowerCase() as DocumentType)
}
