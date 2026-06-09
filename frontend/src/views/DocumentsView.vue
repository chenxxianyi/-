<template>
  <section class="view active" aria-labelledby="documentsTitle">
    <div class="page-heading compact">
      <div>
        <p class="eyebrow">Library</p>
        <h1 id="documentsTitle">文件库</h1>
      </div>
      <div class="view-actions">
        <button class="button secondary" @click="renameSelected">重命名</button>
        <button class="button primary" @click="triggerUpload">上传文件</button>
        <input ref="headerFileInput" type="file" accept=".pdf,.md,.txt,.docx,.png,.jpg,.jpeg,.gif" hidden @change="onHeaderFileSelected" />
      </div>
    </div>

    <div class="documents-layout">
      <aside class="filter-panel">
        <div class="filter-group">
          <h3>文件类型</h3>
          <button v-for="item in filters" :key="item.value" class="filter-item" :class="{ active: documentStore.filters.type === item.value }" @click="documentStore.setType(item.value)">
            {{ item.label }} <span v-if="item.value === 'all'">{{ documents.length }}</span>
          </button>
        </div>
        <div class="filter-group">
          <h3>标签</h3>
          <button class="filter-item subtle">论文</button>
          <button class="filter-item subtle">产品研究</button>
          <button class="filter-item subtle">会议资料</button>
        </div>
      </aside>

      <section class="document-panel">
        <div class="document-toolbar">
          <label class="search-field wide">
            <span>Search</span>
            <input :value="documentStore.filters.keyword" type="search" placeholder="搜索文件名、类型或标签" @input="documentStore.setKeyword(($event.target as HTMLInputElement).value)" />
          </label>
          <select class="select-field" aria-label="排序">
            <option value="recent">最近阅读</option>
            <option value="upload">上传时间</option>
            <option value="name">文件名</option>
          </select>
        </div>

        <FileUploader :uploading="uploading" :progress="uploadProgress" @upload="handleUpload" />

        <div v-if="filteredDocuments.length" class="table-wrap">
          <table class="data-table document-table">
            <thead>
              <tr>
                <th>文件名</th>
                <th>类型</th>
                <th>大小</th>
                <th>上传时间</th>
                <th>最近阅读</th>
                <th>批注</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doc in filteredDocuments" :key="doc.id">
                <td>
                  <button class="plain-row-link file-cell" @click="openDocument(doc.id)">
                    <FileTypeIcon :type="doc.fileType" />
                    <span>{{ doc.fileName }}</span>
                  </button>
                </td>
                <td>{{ doc.fileType.toUpperCase() }}</td>
                <td>{{ doc.displaySize }}</td>
                <td>{{ doc.uploadedAt }}</td>
                <td>{{ doc.lastReadAt }}</td>
                <td><TextBadge>{{ doc.annotationCount }}</TextBadge></td>
                <td>
                  <div class="row-actions">
                    <button class="text-button" @click="openDocument(doc.id)">打开</button>
                    <button class="text-button" @click="documentStore.renameDocument(doc.id)">重命名</button>
                    <button class="delete-link" @click="documentStore.deleteDocument(doc.id)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <EmptyState v-else title="暂无匹配文件" description="换一个关键词，或上传第一份文档开始阅读。" />
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import EmptyState from '@/components/common/EmptyState.vue'
import FileTypeIcon from '@/components/common/FileTypeIcon.vue'
import TextBadge from '@/components/common/TextBadge.vue'
import FileUploader from '@/components/upload/FileUploader.vue'
import { useDocumentStore } from '@/stores/documentStore'
import type { DocumentType } from '@/types/document'

const router = useRouter()
const documentStore = useDocumentStore()
const { documents, filteredDocuments, uploading, uploadProgress } = storeToRefs(documentStore)

const headerFileInput = ref<HTMLInputElement | null>(null)

const filters: Array<{ value: DocumentType | 'all'; label: string }> = [
  { value: 'all', label: '全部文件' },
  { value: 'pdf', label: 'PDF' },
  { value: 'md', label: 'Markdown' },
  { value: 'txt', label: 'TXT' },
  { value: 'docx', label: 'DOCX' },
]

onMounted(() => {
  documentStore.fetchDocuments()
})

function openDocument(id: number) {
  router.push(`/reader/${id}`)
}

function renameSelected() {
  documentStore.renameDocument(documents.value[0]?.id ?? 0)
}

function triggerUpload() {
  headerFileInput.value?.click()
}

function onHeaderFileSelected() {
  const files = headerFileInput.value?.files
  if (files && files.length > 0) {
    handleUpload(files[0])
    headerFileInput.value!.value = ''
  }
}

function handleUpload(file: File) {
  documentStore.uploadDocument(file)
}
</script>
