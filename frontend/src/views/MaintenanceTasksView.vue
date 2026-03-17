<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">🔧 Maintenance Tasks</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Task</button>
    </div>

    <div class="filter-bar">
      <button class="tab-btn" :class="{ active: filter === 'all' }" @click="filter = 'all'">All</button>
      <button class="tab-btn" :class="{ active: filter === 'pending' }" @click="filter = 'pending'">Pending</button>
      <button class="tab-btn" :class="{ active: filter === 'completed' }" @click="filter = 'completed'">Completed</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <div v-else>
      <div v-if="filteredItems.length === 0" class="empty-state">No tasks found.</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>Aquarium</th>
            <th>Task Type</th>
            <th>Scheduled Date</th>
            <th>Status</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id">
            <td>{{ aquariumName(item.aquarium) }}</td>
            <td>{{ item.task_type }}</td>
            <td>{{ item.scheduled_date }}</td>
            <td>
              <span class="badge" :class="item.is_completed ? 'badge-success' : 'badge-warning'">
                {{ item.is_completed ? 'Completed' : 'Pending' }}
              </span>
            </td>
            <td class="col-actions">
              <button v-if="!item.is_completed" class="btn btn-sm btn-success" @click="markComplete(item)">✓ Done</button>
              <button class="btn btn-sm btn-secondary" @click="openEdit(item)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="confirmDelete(item)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2 class="modal-title">{{ editing ? 'Edit Task' : 'Add Task' }}</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label>Aquarium <span class="required">*</span></label>
            <select v-model="form.aquarium" class="input" required>
              <option :value="null">— Select —</option>
              <option v-for="a in aquariumList" :key="a.id" :value="a.id">{{ a.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Task Type <span class="required">*</span></label>
            <input v-model="form.task_type" type="text" class="input" required placeholder="e.g. Water Change, Filter Clean" />
          </div>
          <div class="form-group">
            <label>Scheduled Date <span class="required">*</span></label>
            <input v-model="form.scheduled_date" type="date" class="input" required />
          </div>
          <div class="form-group">
            <label>Notes</label>
            <textarea v-model="form.notes" class="input" rows="2"></textarea>
          </div>
          <div v-if="formError" class="error-msg">{{ formError }}</div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? 'Saving…' : (editing ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal modal-sm">
        <h2 class="modal-title">Delete Task</h2>
        <p>Delete task <strong>{{ deleteTarget.task_type }}</strong>? This cannot be undone.</p>
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
import { ref, computed, onMounted } from 'vue'
import { maintenanceTasks, aquariums } from '../api/index.js'

const items = ref([])
const aquariumList = ref([])
const loading = ref(true)
const error = ref(null)
const filter = ref('all')
const showModal = ref(false)
const editing = ref(null)
const form = ref({ aquarium: null, task_type: '', scheduled_date: '', notes: '' })
const formError = ref(null)
const saving = ref(false)
const deleteTarget = ref(null)

function aquariumName(id) {
  const a = aquariumList.value.find(x => x.id === id)
  return a ? a.name : '—'
}

const filteredItems = computed(() => {
  if (filter.value === 'pending') return items.value.filter(x => !x.is_completed)
  if (filter.value === 'completed') return items.value.filter(x => x.is_completed)
  return items.value
})

async function load() {
  loading.value = true
  error.value = null
  try {
    const [mtRes, aqRes] = await Promise.all([maintenanceTasks.getAll(), aquariums.getAll()])
    items.value = mtRes.data.results ?? mtRes.data
    aquariumList.value = aqRes.data.results ?? aqRes.data
  } catch {
    error.value = 'Failed to load tasks.'
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editing.value = null
  form.value = { aquarium: null, task_type: '', scheduled_date: '', notes: '' }
  formError.value = null
  showModal.value = true
}

function openEdit(item) {
  editing.value = item
  form.value = { aquarium: item.aquarium, task_type: item.task_type,
    scheduled_date: item.scheduled_date, notes: item.notes || '' }
  formError.value = null
  showModal.value = true
}

function closeModal() { showModal.value = false; editing.value = null }

async function save() {
  saving.value = true
  formError.value = null
  const payload = { ...form.value }
  try {
    if (editing.value) await maintenanceTasks.update(editing.value.id, payload)
    else await maintenanceTasks.create(payload)
    closeModal()
    await load()
  } catch (e) {
    formError.value = e.response?.data ? JSON.stringify(e.response.data) : 'Save failed.'
  } finally {
    saving.value = false
  }
}

async function markComplete(item) {
  try {
    await maintenanceTasks.complete(item.id)
    await load()
  } catch {
    error.value = 'Could not mark task as complete.'
  }
}

function confirmDelete(item) { deleteTarget.value = item }

async function doDelete() {
  saving.value = true
  try {
    await maintenanceTasks.remove(deleteTarget.value.id)
    deleteTarget.value = null
    await load()
  } catch {
    error.value = 'Delete failed.'
    deleteTarget.value = null
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
@import '../shared.css';

.filter-bar {
  display: flex;
  gap: 0;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 9px 20px;
  background: none;
  border: none;
  font-size: 0.93rem;
  font-weight: 600;
  color: #718096;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: color 0.15s, border-color 0.15s;
}

.tab-btn.active { color: #2b6cb0; border-bottom-color: #2b6cb0; }
.tab-btn:hover:not(.active) { color: #4a5568; }
</style>
