<template>
  <section class="note-editor-panel">
    <div class="editor-toolbar">
      <button :class="{ active: editor?.isActive('bold') }" @click="editor?.chain().focus().toggleBold().run()">B</button>
      <button :class="{ active: editor?.isActive('italic') }" @click="editor?.chain().focus().toggleItalic().run()">I</button>
      <button :class="{ active: editor?.isActive('heading', { level: 1 }) }" @click="editor?.chain().focus().toggleHeading({ level: 1 }).run()">H1</button>
      <button :class="{ active: editor?.isActive('blockquote') }" @click="editor?.chain().focus().toggleBlockquote().run()">Quote</button>
      <span>{{ statusText }}</span>
    </div>
    <input class="note-title-input" :value="note?.title" @input="handleTitleInput" />
    <EditorContent v-if="editor" class="note-editor" :editor="editor" />
  </section>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { EditorContent, useEditor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import type { NoteItem } from '@/types/note'

const props = defineProps<{
  note: NoteItem | null
  savingStatus: 'saved' | 'saving' | 'failed'
}>()

const emit = defineEmits<{
  update: [content: string, title?: string]
}>()

const editor = useEditor({
  content: props.note?.content ?? '',
  extensions: [
    StarterKit,
    Placeholder.configure({
      placeholder: '记录你的阅读想法...',
    }),
  ],
  editorProps: {
    attributes: {
      class: 'tiptap-content',
    },
  },
  onUpdate({ editor }) {
    emit('update', editor.getHTML())
  },
})

watch(
  () => props.note?.id,
  () => {
    if (editor.value && props.note) {
      editor.value.commands.setContent(props.note.content)
    }
  },
)

const statusText = computed(() => {
  if (props.savingStatus === 'saving') return '保存中...'
  if (props.savingStatus === 'failed') return '保存失败'
  return '已保存'
})

function handleTitleInput(event: Event) {
  emit('update', editor.value?.getHTML() ?? '', (event.target as HTMLInputElement).value)
}
</script>
