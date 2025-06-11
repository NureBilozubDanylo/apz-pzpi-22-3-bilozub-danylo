import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Main from '../components/Main.vue'
import Work from '../components/Work.vue'
import Shops from '../components/Shops.vue'
import Shop from '../components/Shop.vue'
import ShopStats from '@/components/ShopStats.vue'
import Sensors from '@/components/Sensors.vue'
import Animals from '@/components/Animals.vue'
import ClimateHistory from '@/components/ClimateHistory.vue'
import AdminPanel from '@/components/AdminPanel.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: Main
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/register',
    name: 'register',
    component: Register
  },
  {
    path: '/shops',
    name: 'shops',
    component: Shops
  },
  {
    path: '/shop/:id',
    name: 'shop',
    component: Shop
  },
  {
    path: '/shop/:id/stats',
    name: 'shopStats',
    component: ShopStats
  },
  {
    path: '/work/:id',
    name: 'work',
    component: Work
  },
  {
    path: '/sensors/:id',
    name: 'sensors',
    component: Sensors
  },
  {
    path: '/animals/:id',
    name: 'animals',
    component: Animals
  },
  {
    path: '/climateHistory/:id',
    name: 'climateHistory',
    component: ClimateHistory
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminPanel
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
