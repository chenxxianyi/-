<template>
  <aside class="notes-list-panel">
    <label class="search-field wide">
      <span>Search</span>
      <input :value="keyword" type="search" placeholder="搜索笔记" @input="$emit('search', ($event.target as HTMLInputElement).value)" />
    </label>
    <div class="note-list">
      <button v-for="note in notes" :key="note.id" class="note-item" :class="{ active: note.id === currentId }" @click="$emit('select', note.id)">
        <strong>{{ note.title }}</strong>
        <span class="note-meta">{{ note.source }} · {{ note.updatedAt }}</span>
        <p>{{ note.excerpt }}</p>
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import type { NoteItem } from '@/types/note'

defineProps<{
  notes: NoteItem[]
  currentId?: number
  keyword: string
}>()

defineEmits<{
  search: [keyword: string]
  select: [id: number]
}>()
</script>
