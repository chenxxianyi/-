<template>
  <section class="view active" aria-labelledby="settingsTitle">
    <div class="page-heading compact">
      <div>
        <p class="eyebrow">Settings</p>
        <h1 id="settingsTitle">设置</h1>
      </div>
      <div class="view-actions">
        <button v-if="authStore.isAuthenticated" class="button secondary" @click="logout">退出登录</button>
        <RouterLink v-else class="button primary" to="/login">去登录</RouterLink>
      </div>
    </div>

    <div class="settings-layout">
      <aside class="settings-nav">
        <button
          v-for="item in sections"
          :key="item.key"
          :class="{ active: activeSection === item.key }"
          @click="activeSection = item.key"
        >
          {{ item.label }}
        </button>
      </aside>

      <section class="settings-form">
        <div v-if="!authStore.isAuthenticated" class="settings-empty">
          <h2>需要登录后才能管理设置</h2>
          <p>文档、批注、笔记和 AI 配置都绑定到当前账号。登录后页面会自动恢复你的个人资料。</p>
          <div class="view-actions left">
            <RouterLink class="button primary" to="/login">登录</RouterLink>
            <RouterLink class="button secondary" to="/register">注册账号</RouterLink>
          </div>
        </div>

        <template v-else>
          <div v-show="activeSection === 'profile'" class="form-section">
            <div class="settings-section-head">
              <div>
                <h2>用户资料</h2>
                <p>{{ profileHint }}</p>
              </div>
              <span class="soft-badge">{{ authStore.currentUser ? '已登录' : '同步中' }}</span>
            </div>
            <label>
              <span>用户名</span>
              <input v-model="profile.username" autocomplete="username" />
            </label>
            <label>
              <span>邮箱</span>
              <input v-model="profile.email" type="email" autocomplete="email" />
            </label>
            <button class="button primary" @click="saveProfile">保存资料</button>
            <p v-if="saveMessage" class="settings-message">{{ saveMessage }}</p>
          </div>

          <div v-show="activeSection === 'theme'" class="form-section">
            <h2>主题设置</h2>
            <p class="settings-copy">当前版本先保留浅色工作台，后续可以在这里接入深色模式和跟随系统。</p>
            <div class="segmented" role="group" aria-label="主题模式">
              <button class="active">浅色</button>
              <button>深色预留</button>
              <button>跟随系统</button>
            </div>
          </div>

          <div v-show="activeSection === 'storage'" class="form-section">
            <h2>存储空间</h2>
            <p class="settings-copy">本地开发环境默认使用 MinIO 存储上传文件。上传失败时请先确认后端和 MinIO 已启动。</p>
            <div class="settings-meter">
              <div class="storage-row">
                <span>已用空间</span>
                <span>2.4 / 10 GB</span>
              </div>
              <div class="storage-track"><span style="width: 24%" /></div>
            </div>
          </div>

          <div v-show="activeSection === 'ai'" class="form-section">
            <h2>AI 配置预留</h2>
            <label>
              <span>Provider</span>
              <select v-model="aiProvider">
                <option>Mock Provider</option>
                <option>OpenAI</option>
                <option>Claude</option>
                <option>Ollama</option>
              </select>
            </label>
            <label>
              <span>API Key</span>
              <input type="password" placeholder="后续接入真实模型时填写" />
            </label>
            <button class="button secondary" @click="saveMessage = 'AI 配置入口已保留，当前未写入后端。'">保存配置</button>
          </div>
        </template>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

type SectionKey = 'profile' | 'theme' | 'storage' | 'ai'

const router = useRouter()
const authStore = useAuthStore()
const activeSection = ref<SectionKey>('profile')
const aiProvider = ref('Mock Provider')
const saveMessage = ref('')

const profile = reactive({
  username: '',
  email: '',
})

const sections: Array<{ key: SectionKey; label: string }> = [
  { key: 'profile', label: '用户资料' },
  { key: 'theme', label: '主题' },
  { key: 'storage', label: '存储空间' },
  { key: 'ai', label: 'AI 配置' },
]

const profileHint = computed(() => {
  return authStore.currentUser
    ? `当前账号 ID：${authStore.currentUser.id}`
    : '正在同步当前账号资料，请稍候。'
})

watch(
  () => authStore.currentUser,
  (user) => {
    profile.username = user?.username ?? ''
    profile.email = user?.email ?? ''
  },
  { immediate: true },
)

function saveProfile() {
  saveMessage.value = '资料保存入口已就绪，当前后端暂未提供更新接口。'
}

function logout() {
  authStore.logout()
  router.push('/login')
}
</script>
