<template>
  <div class="upload-zone" :class="{ 'drag-over': isDragOver }" @click="openFileDialog" @dragover.prevent="isDragOver = true" @dragleave="isDragOver = false" @drop.prevent="handleDrop">
    <div>
      <strong>拖拽文件到这里上传</strong>
      <span>支持 PDF、Markdown、TXT、DOCX 和图片，单文件最大 50MB</span>
    </div>
    <button class="button secondary" :disabled="uploading">{{ uploading ? '上传中' : '选择文件' }}</button>
    <input ref="fileInput" type="file" accept=".pdf,.md,.txt,.docx,.png,.jpg,.jpeg,.gif" hidden @change="onFileSelected" />
  </div>
  <div v-if="uploading" class="upload-progress">
    <span>正在上传，请稍候…</span>
    <div><span :style="{ width: `${progress}%` }" /></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  uploading: boolean
  progress: number
}>()

const emit = defineEmits<{
  (e: 'upload', file: File): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const isDragOver = ref(false)

function openFileDialog() {
  fileInput.value?.click()
}

function onFileSelected() {
  const files = fileInput.value?.files
  if (files && files.length > 0) {
    emit('upload', files[0])
    // 清空 input 以便重复选择同一文件
    fileInput.value!.value = ''
  }
}

function handleDrop(e: DragEvent) {
  isDragOver.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    emit('upload', files[0])
  }
}
</script>
