<template>
  <div class="reader-right-panel">
    <div class="panel-tabs">
      <button class="tab-button" :class="{ active: activeTab === 'annotations' }" @click="activeTab = 'annotations'">批注</button>
      <button class="tab-button" :class="{ active: activeTab === 'excerpts' }" @click="activeTab = 'excerpts'">摘录</button>
      <button class="tab-button" :class="{ active: activeTab === 'ai' }" @click="activeTab = 'ai'">AI 助手</button>
    </div>
    <div v-if="activeTab === 'annotations'" class="tab-pane active">
      <div v-if="annotations.length" class="annotation-list">
        <div v-for="item in annotations" :key="item.id" class="annotation-item" :class="{ active: item.id === activeAnnotationId }" @click="$emit('activate', item.id)">
          <div class="annotation-topline">
            <span class="annotation-color" :class="item.color" />
            <span class="annotation-meta">Page {{ item.pageNumber }} · {{ item.createdAt }}</span>
            <button class="delete-link" @click.stop="$emit('delete', item.id)">删除</button>
          </div>
          <p class="annotation-text">{{ item.selectedText }}</p>
          <p class="annotation-note">{{ item.note || '暂无备注' }}</p>
        </div>
      </div>
      <EmptyState v-else title="暂无批注" description="选中文本后可以添加高亮和备注。" />
    </div>
    <div v-if="activeTab === 'excerpts'" class="tab-pane active">
      <div class="note-list compact">
        <button v-for="note in notes" :key="note.id" class="note-item" @click="$router.push('/notes')">
          <strong>{{ note.title }}</strong>
          <span class="note-meta">{{ note.source }} · {{ note.updatedAt }}</span>
          <p>{{ note.excerpt }}</p>
        </button>
      </div>
    </div>
    <AiPanel v-if="activeTab === 'ai'" :answer="aiAnswer" @summary="$emit('ai', 'summary')" @explain="$emit('ai', 'explain')" @translate="$emit('ai', 'translate')" @ask="(question) => $emit('ask', question)" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { AnnotationItem } from '@/types/annotation'
import type { NoteItem } from '@/types/note'
import EmptyState from '@/components/common/EmptyState.vue'
import AiPanel from './AiPanel.vue'

defineProps<{
  annotations: AnnotationItem[]
  notes: NoteItem[]
  activeAnnotationId: number | null
  aiAnswer: { title: string; text: string }
}>()

defineEmits<{
  activate: [id: number]
  delete: [id: number]
  ai: [action: 'summary' | 'explain' | 'translate']
  ask: [question: string]
}>()

const activeTab = ref<'annotations' | 'excerpts' | 'ai'>('annotations')
</script>
