export function toPercentPosition(rect: DOMRect, containerRect: DOMRect) {
  return {
    xPercent: (rect.left - containerRect.left) / containerRect.width,
    yPercent: (rect.top - containerRect.top) / containerRect.height,
    widthPercent: rect.width / containerRect.width,
    heightPercent: rect.height / containerRect.height,
  }
}
