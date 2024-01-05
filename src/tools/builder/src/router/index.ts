import { createRouter, createWebHistory } from 'vue-router'
import { editorRoutes } from '@/views/editor/routes'

const router = createRouter({
  routes: [
    ...editorRoutes
  ],
  history: createWebHistory(import.meta.env.BASE_URL)
})

export default router
