<template>
  <div>
    <h1 class="page-title">Welcome to Acuarium 🐠</h1>
    <p class="page-subtitle">Your aquarium management dashboard</p>

    <div v-if="loading" class="loading">Loading dashboard...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>

    <div class="cards" v-else>
      <div class="card">
        <div class="card-icon">🐠</div>
        <div class="card-value">{{ counts.aquariums }}</div>
        <div class="card-label">Aquariums</div>
      </div>
      <div class="card">
        <div class="card-icon">🐟</div>
        <div class="card-value">{{ counts.fish }}</div>
        <div class="card-label">Fish</div>
      </div>
      <div class="card">
        <div class="card-icon">🌿</div>
        <div class="card-value">{{ counts.plants }}</div>
        <div class="card-label">Plants</div>
      </div>
      <div class="card card-warning">
        <div class="card-icon">🔧</div>
        <div class="card-value">{{ counts.pendingTasks }}</div>
        <div class="card-label">Pending Tasks</div>
      </div>
    </div>

    <div class="quick-links">
      <h2 class="section-title">Quick Actions</h2>
      <div class="link-grid">
        <RouterLink to="/aquariums" class="quick-link">➕ Add Aquarium</RouterLink>
        <RouterLink to="/fish" class="quick-link">➕ Add Fish</RouterLink>
        <RouterLink to="/plants" class="quick-link">➕ Add Plant</RouterLink>
        <RouterLink to="/maintenance-tasks" class="quick-link">➕ Add Task</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { aquariums, fish, plants, maintenanceTasks } from '../api/index.js'

const loading = ref(true)
const error = ref(null)
const counts = ref({ aquariums: 0, fish: 0, plants: 0, pendingTasks: 0 })

onMounted(async () => {
  try {
    const [aq, fi, pl, mt] = await Promise.all([
      aquariums.getAll(),
      fish.getAll(),
      plants.getAll(),
      maintenanceTasks.getAll(null, false)
    ])
    counts.value = {
      aquariums: (aq.data.results ?? aq.data).length,
      fish: (fi.data.results ?? fi.data).length,
      plants: (pl.data.results ?? pl.data).length,
      pendingTasks: (mt.data.results ?? mt.data).length
    }
  } catch (e) {
    error.value = 'Could not load dashboard data.'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-title { font-size: 2rem; font-weight: 700; color: #1a365d; margin-bottom: 6px; }
.page-subtitle { color: #718096; margin-bottom: 32px; font-size: 1.05rem; }

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 36px;
}

.card {
  background: #fff;
  border-radius: 14px;
  padding: 28px 24px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  transition: transform 0.15s, box-shadow 0.15s;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.11);
}

.card-warning { border-top: 4px solid #ed8936; }

.card-icon { font-size: 2.2rem; margin-bottom: 10px; }
.card-value { font-size: 2.4rem; font-weight: 800; color: #2b6cb0; line-height: 1; margin-bottom: 6px; }
.card-label { font-size: 0.9rem; color: #718096; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

.section-title { font-size: 1.2rem; font-weight: 600; color: #2d3748; margin-bottom: 14px; }

.link-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.quick-link {
  display: inline-block;
  padding: 10px 20px;
  background: #2b6cb0;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: background 0.15s;
}

.quick-link:hover { background: #2c5282; }

.loading { color: #718096; padding: 20px 0; }
.error-msg { color: #e53e3e; background: #fff5f5; padding: 14px 18px; border-radius: 8px; margin-bottom: 20px; }
</style>
