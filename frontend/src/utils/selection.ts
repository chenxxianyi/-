export interface ReaderSelection {
  text: string
  rect: DOMRect
  range: Range
}

export function getSelectionInContainer(container: HTMLElement): ReaderSelection | null {
  const selection = window.getSelection()
  if (!selection || selection.isCollapsed) return null

  const text = selection.toString().trim()
  if (!text) return null

  const range = selection.getRangeAt(0)
  if (!container.contains(range.commonAncestorContainer)) return null

  return {
    text,
    rect: range.getBoundingClientRect(),
    range: range.cloneRange(),
  }
}
