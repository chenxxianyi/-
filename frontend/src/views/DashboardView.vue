<template>
  <section class="view active" aria-labelledby="dashboardTitle">
    <div class="page-heading">
      <div>
        <p class="eyebrow">Today</p>
        <h1 id="dashboardTitle">晚上好，继续你的阅读流</h1>
      </div>
      <RouterLink class="button primary" to="/documents">快速上传</RouterLink>
    </div>

    <div class="dashboard-grid">
      <section class="surface-section continue-section">
        <div class="section-head">
          <h2>继续阅读</h2>
          <RouterLink class="text-button" to="/reader/1">打开阅读器</RouterLink>
        </div>
        <div class="reading-list">
          <button v-for="doc in documents.slice(0, 3)" :key="doc.id" class="reading-row" @click="openDocument(doc.id)">
            <FileTypeIcon :type="doc.fileType" />
            <div class="reading-main">
              <strong>{{ doc.fileName }}</strong>
              <span>上次阅读 {{ doc.lastReadAt }}</span>
            </div>
            <div class="progress-meta">
              <span>{{ doc.progress }}%</span>
              <div class="mini-progress"><span :style="{ width: `${doc.progress}%` }" /></div>
            </div>
          </button>
        </div>
      </section>

      <section class="surface-section">
        <div class="section-head">
          <h2>最近批注</h2>
          <RouterLink class="text-button" to="/reader/1">查看全部</RouterLink>
        </div>
        <div class="annotation-feed">
          <button v-for="item in recentAnnotations" :key="item.id" class="annotation-item" @click="router.push(`/reader/${item.documentId}`)">
            <div class="annotation-topline">
              <span class="annotation-color" :class="item.color" />
              <span class="annotation-meta">Page {{ item.pageNumber }} · {{ item.createdAt }}</span>
            </div>
            <p class="annotation-text">{{ item.selectedText }}</p>
            <p class="annotation-note">{{ item.note }}</p>
          </button>
        </div>
      </section>
    </div>

    <section class="surface-section recent-files-section">
      <div class="section-head">
        <h2>最近上传</h2>
        <RouterLink class="text-button" to="/documents">进入文件库</RouterLink>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>文件名</th>
              <th>类型</th>
              <th>大小</th>
              <th>最近阅读</th>
              <th>批注</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in documents" :key="doc.id">
              <td>
                <button class="plain-row-link file-cell" @click="openDocument(doc.id)">
                  <FileTypeIcon :type="doc.fileType" />
                  <span>{{ doc.fileName }}</span>
                </button>
              </td>
              <td>{{ doc.fileType.toUpperCase() }}</td>
              <td>{{ doc.displaySize }}</td>
              <td>{{ doc.lastReadAt }}</td>
              <td>{{ doc.annotationCount }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { RouterLink, useRouter } from 'vue-router'
import FileTypeIcon from '@/components/common/FileTypeIcon.vue'
import { useAnnotationStore } from '@/stores/annotationStore'
import { useDocumentStore } from '@/stores/documentStore'

const router = useRouter()
const documentStore = useDocumentStore()
const annotationStore = useAnnotationStore()
const { documents } = storeToRefs(documentStore)
const { recentAnnotations } = storeToRefs(annotationStore)

onMounted(() => {
  documentStore.fetchDocuments()
  annotationStore.fetchRecentAnnotations()
})

function openDocument(id: number) {
  router.push(`/reader/${id}`)
}
</script>
