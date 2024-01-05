import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    }
  ],
  history: createWebHistory(import.meta.env.BASE_URL)
})

export default router
