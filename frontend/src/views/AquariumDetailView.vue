<template>
  <div>
    <div class="page-header">
      <div class="breadcrumb">
        <RouterLink to="/aquariums" class="breadcrumb-link">🐠 Aquariums</RouterLink>
        <span class="breadcrumb-sep">›</span>
        <span>{{ aquarium?.name || 'Detail' }}</span>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading aquarium...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <template v-else>
      <!-- Info card -->
      <div class="info-card">
        <h1 class="info-name">{{ aquarium.name }}</h1>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Type</span>
            <span class="info-value">{{ aquarium.aquarium_type_name || '—' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Volume</span>
            <span class="info-value">{{ aquarium.volume_liters }} L</span>
          </div>
          <div class="info-item">
            <span class="info-label">Setup Date</span>
            <span class="info-value">{{ aquarium.setup_date || '—' }}</span>
          </div>
        </div>
        <div v-if="aquarium.notes" class="info-notes">{{ aquarium.notes }}</div>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button v-for="tab in tabs" :key="tab.key"
          class="tab-btn" :class="{ active: activeTab === tab.key }"
          @click="activeTab = tab.key">
          {{ tab.label }}
        </button>
      </div>

      <!-- Fish Tab -->
      <div v-if="activeTab === 'fish'">
        <div class="tab-header">
          <span class="tab-count">{{ fishList.length }} fish</span>
          <button class="btn btn-primary btn-sm" @click="openAddModal('fish')">+ Add Fish</button>
        </div>
        <div v-if="fishList.length === 0" class="empty-state">No fish added yet.</div>
        <table v-else class="table">
          <thead><tr><th>Species</th><th>Common Name</th><th>Qty</th><th>Added</th><th class="col-actions">Actions</th></tr></thead>
          <tbody>
            <tr v-for="f in fishList" :key="f.id">
              <td><em>{{ f.species }}</em></td>
              <td>{{ f.common_name || '—' }}</td>
              <td>{{ f.quantity }}</td>
              <td>{{ f.added_date || '—' }}</td>
              <td class="col-actions">
                <button class="btn btn-sm btn-danger" @click="confirmDeleteItem('fish', f)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Plants Tab -->
      <div v-if="activeTab === 'plants'">
        <div class="tab-header">
          <span class="tab-count">{{ plantList.length }} plants</span>
          <button class="btn btn-primary btn-sm" @click="openAddModal('plants')">+ Add Plant</button>
        </div>
        <div v-if="plantList.length === 0" class="empty-state">No plants added yet.</div>
        <table v-else class="table">
          <thead><tr><th>Species</th><th>Common Name</th><th>Qty</th><th>Added</th><th class="col-actions">Actions</th></tr></thead>
          <tbody>
            <tr v-for="p in plantList" :key="p.id">
              <td><em>{{ p.species }}</em></td>
              <td>{{ p.common_name || '—' }}</td>
              <td>{{ p.quantity }}</td>
              <td>{{ p.added_date || '—' }}</td>
              <td class="col-actions">
                <button class="btn btn-sm btn-danger" @click="confirmDeleteItem('plants', p)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Lighting Tab -->
      <div v-if="activeTab === 'lighting'">
        <div class="tab-header">
          <span class="tab-count">{{ lightList.length }} schedules</span>
          <button class="btn btn-primary btn-sm" @click="openAddModal('lighting')">+ Add Schedule</button>
        </div>
        <div v-if="lightList.length === 0" class="empty-state">No lighting schedules yet.</div>
        <table v-else class="table">
          <thead><tr><th>Type</th><th>On</th><th>Off</th><th>Intensity %</th><th class="col-actions">Actions</th></tr></thead>
          <tbody>
            <tr v-for="l in lightList" :key="l.id">
              <td>{{ l.light_type }}</td>
              <td>{{ l.on_time }}</td>
              <td>{{ l.off_time }}</td>
              <td>{{ l.intensity_percent ?? '—' }}</td>
              <td class="col-actions">
                <button class="btn btn-sm btn-danger" @click="confirmDeleteItem('lighting', l)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Maintenance Tab -->
      <div v-if="activeTab === 'maintenance'">
        <div class="tab-header">
          <span class="tab-count">{{ taskList.length }} tasks</span>
          <button class="btn btn-primary btn-sm" @click="openAddModal('maintenance')">+ Add Task</button>
        </div>
        <div v-if="taskList.length === 0" class="empty-state">No maintenance tasks yet.</div>
        <table v-else class="table">
          <thead><tr><th>Task Type</th><th>Scheduled</th><th>Status</th><th class="col-actions">Actions</th></tr></thead>
          <tbody>
            <tr v-for="t in taskList" :key="t.id">
              <td>{{ t.task_type }}</td>
              <td>{{ t.scheduled_date }}</td>
              <td><span class="badge" :class="t.is_completed ? 'badge-success' : 'badge-warning'">
                {{ t.is_completed ? 'Completed' : 'Pending' }}
              </span></td>
              <td class="col-actions">
                <button v-if="!t.is_completed" class="btn btn-sm btn-success" @click="completeTask(t)">✓ Done</button>
                <button class="btn btn-sm btn-danger" @click="confirmDeleteItem('maintenance', t)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- Add modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2 class="modal-title">{{ modalTitle }}</h2>
        <form @submit.prevent="saveModal">
          <template v-if="modalType === 'fish' || modalType === 'plants'">
            <div class="form-group">
              <label>Species <span class="required">*</span></label>
              <input v-model="modalForm.species" type="text" class="input" required />
            </div>
            <div class="form-group">
              <label>Common Name</label>
              <input v-model="modalForm.common_name" type="text" class="input" />
            </div>
            <div class="form-group">
              <label>Quantity <span class="required">*</span></label>
              <input v-model.number="modalForm.quantity" type="number" min="1" class="input" required />
            </div>
            <div class="form-group">
              <label>Added Date</label>
              <input v-model="modalForm.added_date" type="date" class="input" />
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="modalForm.notes" class="input" rows="2"></textarea>
            </div>
          </template>

          <template v-if="modalType === 'lighting'">
            <div class="form-group">
              <label>Light Type <span class="required">*</span></label>
              <input v-model="modalForm.light_type" type="text" class="input" required placeholder="e.g. LED, Fluorescent" />
            </div>
            <div class="form-group">
              <label>On Time <span class="required">*</span></label>
              <input v-model="modalForm.on_time" type="time" class="input" required />
            </div>
            <div class="form-group">
              <label>Off Time <span class="required">*</span></label>
              <input v-model="modalForm.off_time" type="time" class="input" required />
            </div>
            <div class="form-group">
              <label>Intensity % (0–100)</label>
              <input v-model.number="modalForm.intensity_percent" type="number" min="0" max="100" class="input" />
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="modalForm.notes" class="input" rows="2"></textarea>
            </div>
          </template>

          <template v-if="modalType === 'maintenance'">
            <div class="form-group">
              <label>Task Type <span class="required">*</span></label>
              <input v-model="modalForm.task_type" type="text" class="input" required placeholder="e.g. Water Change" />
            </div>
            <div class="form-group">
              <label>Scheduled Date <span class="required">*</span></label>
              <input v-model="modalForm.scheduled_date" type="date" class="input" required />
            </div>
            <div class="form-group">
              <label>Notes</label>
              <textarea v-model="modalForm.notes" class="input" rows="2"></textarea>
            </div>
          </template>

          <div v-if="formError" class="error-msg">{{ formError }}</div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">{{ saving ? 'Saving…' : 'Add' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete confirm -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal modal-sm">
        <h2 class="modal-title">Confirm Delete</h2>
        <p>Delete this item? This cannot be undone.</p>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="deleteTarget = null">Cancel</button>
          <button class="btn btn-danger" @click="doDelete" :disabled="saving">
            {{ saving ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { aquariums, fish as fishApi, plants as plantsApi, lighting as lightingApi, maintenanceTasks } from '../api/index.js'

const route = useRoute()
const id = route.params.id

const aquarium = ref(null)
const fishList = ref([])
const plantList = ref([])
const lightList = ref([])
const taskList = ref([])
const loading = ref(true)
const error = ref(null)
const activeTab = ref('fish')

const tabs = [
  { key: 'fish', label: '🐟 Fish' },
  { key: 'plants', label: '🌿 Plants' },
  { key: 'lighting', label: '💡 Lighting' },
  { key: 'maintenance', label: '🔧 Maintenance' }
]

const showModal = ref(false)
const modalType = ref('')
const modalForm = ref({})
const formError = ref(null)
const saving = ref(false)
const deleteTarget = ref(null)

const modalTitle = computed(() => {
  const map = { fish: 'Add Fish', plants: 'Add Plant', lighting: 'Add Lighting Schedule', maintenance: 'Add Maintenance Task' }
  return map[modalType.value] || 'Add'
})

async function load() {
  loading.value = true
  error.value = null
  try {
    const [aqRes, fiRes, plRes, liRes, mtRes] = await Promise.all([
      aquariums.getOne(id),
      fishApi.getAll(id),
      plantsApi.getAll(id),
      lightingApi.getAll(id),
      maintenanceTasks.getAll(id)
    ])
    aquarium.value = aqRes.data
    fishList.value = fiRes.data.results ?? fiRes.data
    plantList.value = plRes.data.results ?? plRes.data
    lightList.value = liRes.data.results ?? liRes.data
    taskList.value = mtRes.data.results ?? mtRes.data
  } catch {
    error.value = 'Failed to load aquarium details.'
  } finally {
    loading.value = false
  }
}

function openAddModal(type) {
  modalType.value = type
  modalForm.value = { aquarium: id, species: '', common_name: '', quantity: 1, added_date: '',
    notes: '', light_type: '', on_time: '', off_time: '', intensity_percent: null,
    task_type: '', scheduled_date: '' }
  formError.value = null
  showModal.value = true
}

function closeModal() { showModal.value = false }

async function saveModal() {
  saving.value = true
  formError.value = null
  const payload = { ...modalForm.value }
  Object.keys(payload).forEach(k => { if (payload[k] === '' || payload[k] === null) delete payload[k] })
  payload.aquarium = Number(id)
  try {
    if (modalType.value === 'fish') await fishApi.create(payload)
    else if (modalType.value === 'plants') await plantsApi.create(payload)
    else if (modalType.value === 'lighting') await lightingApi.create(payload)
    else if (modalType.value === 'maintenance') await maintenanceTasks.create(payload)
    closeModal()
    await load()
  } catch (e) {
    formError.value = e.response?.data ? JSON.stringify(e.response.data) : 'Save failed.'
  } finally {
    saving.value = false
  }
}

function confirmDeleteItem(type, item) {
  deleteTarget.value = { type, item }
}

async function doDelete() {
  saving.value = true
  const { type, item } = deleteTarget.value
  try {
    if (type === 'fish') await fishApi.remove(item.id)
    else if (type === 'plants') await plantsApi.remove(item.id)
    else if (type === 'lighting') await lightingApi.remove(item.id)
    else if (type === 'maintenance') await maintenanceTasks.remove(item.id)
    deleteTarget.value = null
    await load()
  } catch {
    error.value = 'Delete failed.'
    deleteTarget.value = null
  } finally {
    saving.value = false
  }
}

async function completeTask(task) {
  try {
    await maintenanceTasks.complete(task.id)
    await load()
  } catch {
    error.value = 'Could not complete task.'
  }
}

onMounted(load)
</script>

<style scoped>
@import '../shared.css';

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.95rem;
  color: #718096;
}

.breadcrumb-link {
  color: #2b6cb0;
  text-decoration: none;
  font-weight: 600;
}
.breadcrumb-link:hover { text-decoration: underline; }
.breadcrumb-sep { color: #cbd5e0; }

.info-card {
  background: #fff;
  border-radius: 14px;
  padding: 24px 28px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  margin-bottom: 28px;
}

.info-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a365d;
  margin-bottom: 14px;
}

.info-grid {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.info-item { display: flex; flex-direction: column; gap: 3px; }
.info-label { font-size: 0.78rem; font-weight: 700; color: #718096; text-transform: uppercase; letter-spacing: 0.05em; }
.info-value { font-size: 1rem; color: #2d3748; font-weight: 500; }

.info-notes {
  margin-top: 10px;
  padding: 10px 14px;
  background: #f7fafc;
  border-radius: 7px;
  font-size: 0.9rem;
  color: #4a5568;
}

.tab-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.tab-count { font-size: 0.9rem; color: #718096; font-weight: 500; }
</style>
