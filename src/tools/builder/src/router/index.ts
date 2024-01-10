import { builderRoutes } from '@/views/builder/routes'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  routes: [
    ...builderRoutes
  ],
  history: createWebHistory(import.meta.env.BASE_URL)
})

export default router
