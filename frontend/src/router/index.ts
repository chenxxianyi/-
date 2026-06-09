import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import DashboardView from '@/views/DashboardView.vue'
import DocumentsView from '@/views/DocumentsView.vue'
import ReaderView from '@/views/ReaderView.vue'
import NotesView from '@/views/NotesView.vue'
import SettingsView from '@/views/SettingsView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/',
      component: AppLayout,
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
        { path: 'documents', name: 'documents', component: DocumentsView, meta: { requiresAuth: true } },
        { path: 'reader/:documentId?', name: 'reader', component: ReaderView, meta: { requiresAuth: true } },
        { path: 'notes', name: 'notes', component: NotesView, meta: { requiresAuth: true } },
        { path: 'settings', name: 'settings', component: SettingsView, meta: { requiresAuth: true } },
      ],
    },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  const isAuthPage = to.name === 'login' || to.name === 'register'

  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.meta.requiresAuth && authStore.token && !authStore.currentUser) {
    await authStore.fetchProfile()
    if (!authStore.token) {
      return { name: 'login', query: { redirect: to.fullPath } }
    }
  }

  if (isAuthPage && authStore.token) {
    return { name: 'dashboard' }
  }
})

export default router
