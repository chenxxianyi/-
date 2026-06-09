<template>
  <section class="view active" aria-labelledby="notesTitle">
    <div class="page-heading compact">
      <div>
        <p class="eyebrow">Notes</p>
        <h1 id="notesTitle">笔记</h1>
      </div>
      <button class="button primary" @click="noteStore.createNote()">新建笔记</button>
    </div>

    <div class="notes-layout">
      <NoteList :notes="filteredNotes" :current-id="currentNote?.id" :keyword="keyword" @search="noteStore.setKeyword" @select="noteStore.selectNote" />
      <NoteEditor :note="currentNote" :saving-status="savingStatus" @update="noteStore.updateCurrentNote" />
      <aside class="source-panel">
        <h3>来源</h3>
        <p class="source-title">{{ currentNote?.source ?? '暂无来源' }}</p>
        <blockquote>{{ currentNote?.excerpt ?? '从原文摘录的内容会显示在这里。' }}</blockquote>
        <RouterLink class="button secondary full" :to="`/reader/${currentNote?.documentId ?? 1}`">回到原文</RouterLink>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { RouterLink } from 'vue-router'
import NoteEditor from '@/components/notes/NoteEditor.vue'
import NoteList from '@/components/notes/NoteList.vue'
import { useNoteStore } from '@/stores/noteStore'

const noteStore = useNoteStore()
const { currentNote, filteredNotes, keyword, savingStatus } = storeToRefs(noteStore)

onMounted(() => {
  noteStore.fetchNotes()
})
</script>
