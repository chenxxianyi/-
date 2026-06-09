import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchNotesApi,
  createNoteApi,
  updateNoteApi,
  deleteNoteApi,
} from '@/api/note'
import type { NoteItem } from '@/types/note'

export const useNoteStore = defineStore('notes', () => {
  const notes = ref<NoteItem[]>([])
  const currentNote = ref<NoteItem | null>(null)
  const savingStatus = ref<'saved' | 'saving' | 'failed'>('saved')
  const loading = ref(false)
  const error = ref('')
  const keyword = ref('')
  let saveTimer = 0

  const filteredNotes = computed(() => {
    const value = keyword.value.trim().toLowerCase()
    return notes.value.filter(
      (item) =>
        !value ||
        item.title.toLowerCase().includes(value) ||
        (item.excerpt && item.excerpt.toLowerCase().includes(value)) ||
        (item.source && item.source.toLowerCase().includes(value)),
    )
  })

  function setKeyword(value: string) {
    keyword.value = value
  }

  function selectNote(id: number) {
    currentNote.value = notes.value.find((item) => item.id === id) ?? currentNote.value
  }

  async function fetchNotes() {
    loading.value = true
    error.value = ''
    try {
      notes.value = (await fetchNotesApi()) as NoteItem[]
    } catch (e: any) {
      error.value = e.message || '获取笔记列表失败'
    } finally {
      loading.value = false
    }
  }

  async function createNote() {
    error.value = ''
    try {
      const note = (await createNoteApi({
        title: '未命名笔记',
        content: '<p>新的阅读笔记内容。</p>',
        contentType: 'richtext',
        excerpt: '新的阅读笔记内容。',
        source: '手动创建',
      })) as NoteItem
      notes.value.unshift(note)
      currentNote.value = note
      return note
    } catch (e: any) {
      error.value = e.message || '创建笔记失败'
      throw e
    }
  }

  async function createFromAnnotation(selectedText: string, documentId: number, sourceAnnotationId?: number) {
    error.value = ''
    try {
      const payload: any = {
        title: selectedText.slice(0, 18) || '新摘录',
        content: `<p>${selectedText}</p>`,
        excerpt: selectedText,
        source: '',
        contentType: 'richtext',
        tags: ['摘录'],
        documentId,
      }
      if (sourceAnnotationId) {
        payload.sourceAnnotationId = sourceAnnotationId
      }
      const note = (await createNoteApi(payload)) as NoteItem
      notes.value.unshift(note)
      currentNote.value = note
      return note
    } catch (e: any) {
      error.value = e.message || '创建摘录失败'
      throw e
    }
  }

  async function updateCurrentNote(content: string, title?: string) {
    if (!currentNote.value) return
    savingStatus.value = 'saving'
    error.value = ''

    // 乐观更新本地状态
    currentNote.value.content = content
    if (title !== undefined) {
      currentNote.value.title = title
    }

    window.clearTimeout(saveTimer)
    saveTimer = window.setTimeout(async () => {
      try {
        const updated = (await updateNoteApi(currentNote.value!.id, {
          content,
          title: currentNote.value!.title,
        })) as NoteItem
        Object.assign(currentNote.value!, updated)
        savingStatus.value = 'saved'
      } catch {
        savingStatus.value = 'failed'
        error.value = '保存失败'
      }
    }, 800)
  }

  async function deleteNote(id: number) {
    error.value = ''
    try {
      await deleteNoteApi(id)
      notes.value = notes.value.filter((item) => item.id !== id)
      if (currentNote.value?.id === id) {
        currentNote.value = notes.value[0] ?? null
      }
    } catch (e: any) {
      error.value = e.message || '删除笔记失败'
      throw e
    }
  }

  return {
    notes,
    currentNote,
    savingStatus,
    loading,
    error,
    keyword,
    filteredNotes,
    setKeyword,
    selectNote,
    fetchNotes,
    createNote,
    createFromAnnotation,
    updateCurrentNote,
    deleteNote,
  }
})
