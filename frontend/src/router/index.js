import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AquariumTypesView from '../views/AquariumTypesView.vue'
import AquariumsView from '../views/AquariumsView.vue'
import AquariumDetailView from '../views/AquariumDetailView.vue'
import FishView from '../views/FishView.vue'
import PlantsView from '../views/PlantsView.vue'
import LightingView from '../views/LightingView.vue'
import MaintenanceTasksView from '../views/MaintenanceTasksView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/aquarium-types', component: AquariumTypesView },
  { path: '/aquariums', component: AquariumsView },
  { path: '/aquariums/:id', component: AquariumDetailView },
  { path: '/fish', component: FishView },
  { path: '/plants', component: PlantsView },
  { path: '/lighting', component: LightingView },
  { path: '/maintenance-tasks', component: MaintenanceTasksView }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
