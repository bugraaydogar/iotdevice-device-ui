import { createRouter, createWebHistory } from 'vue-router'
import OtaView from '../views/OtaView.vue'
import AutoView from '../views/AutoView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: AutoView
    },
    {
      path: '/ota',
      name: 'ota',
      component: OtaView
    },
    { 
      path: '/:pathMatch(.*)*',
      name: 'NotFound', 
      component: () => import('../views/NotFoundView.vue')
    },
  ]
})

export default router