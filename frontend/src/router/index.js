// router/index.js — rutas con guards JWT
import { createRouter, createWebHistory } from 'vue-router'
import LoginView    from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { public: true }
  },
  {
    path: '/',
    component: DashboardView,
    meta: { requiresAuth: true },
    children: [
      { path: '',           redirect: '/acuario' },
      { path: 'acuario',     name: 'acuario',     component: () => import('@/views/AcuarioView.vue') },
      { path: 'fish',        name: 'fish',        component: () => import('@/views/FishView.vue') },
      { path: 'plants',      name: 'plants',      component: () => import('@/views/PlantsView.vue') },
      { path: 'lighting',    name: 'lighting',    component: () => import('@/views/LightingView.vue') },
      { path: 'maintenance', name: 'maintenance', component: () => import('@/views/MaintenanceView.vue') },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard global: redirige a /login si no hay token
router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  if (!to.meta.public && !token) return { name: 'login' }
  if (to.name === 'login' && token) return { path: '/' }
})

export default router

