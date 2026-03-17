<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">💡 Lighting Schedules</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Schedule</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <div v-else>
      <div v-if="items.length === 0" class="empty-state">No lighting schedules yet.</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>Aquarium</th>
            <th>Light Type</th>
            <th>On Time</th>
            <th>Off Time</th>
            <th>Intensity %</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ aquariumName(item.aquarium) }}</td>
            <td>{{ item.light_type }}</td>
            <td>{{ item.on_time }}</td>
            <td>{{ item.off_time }}</td>
            <td>{{ item.intensity_percent ?? '—' }}</td>
            <td class="col-actions">
              <button class="btn btn-sm btn-secondary" @click="openEdit(item)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="confirmDelete(item)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2 class="modal-title">{{ editing ? 'Edit Lighting' : 'Add Lighting' }}</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label>Aquarium <span class="required">*</span></label>
            <select v-model="form.aquarium" class="input" required>
              <option :value="null">— Select —</option>
              <option v-for="a in aquariumList" :key="a.id" :value="a.id">{{ a.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Light Type <span class="required">*</span></label>
            <input v-model="form.light_type" type="text" class="input" required placeholder="e.g. LED, Fluorescent" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>On Time <span class="required">*</span></label>
              <input v-model="form.on_time" type="time" class="input" required />
            </div>
            <div class="form-group">
              <label>Off Time <span class="required">*</span></label>
              <input v-model="form.off_time" type="time" class="input" required />
            </div>
          </div>
          <div class="form-group">
            <label>Intensity % <span class="hint">(0–100)</span></label>
            <input v-model.number="form.intensity_percent" type="number" min="0" max="100" class="input" placeholder="e.g. 80" />
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
        <h2 class="modal-title">Delete Schedule</h2>
        <p>Delete lighting schedule for <strong>{{ aquariumName(deleteTarget.aquarium) }}</strong>?</p>
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
import { ref, onMounted } from 'vue'
import { lighting as lightingApi, aquariums } from '../api/index.js'

const items = ref([])
const aquariumList = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editing = ref(null)
const form = ref({ aquarium: null, light_type: '', on_time: '', off_time: '', intensity_percent: null, notes: '' })
const formError = ref(null)
const saving = ref(false)
const deleteTarget = ref(null)

function aquariumName(id) {
  const a = aquariumList.value.find(x => x.id === id)
  return a ? a.name : '—'
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const [liRes, aqRes] = await Promise.all([lightingApi.getAll(), aquariums.getAll()])
    items.value = liRes.data.results ?? liRes.data
    aquariumList.value = aqRes.data.results ?? aqRes.data
  } catch {
    error.value = 'Failed to load lighting schedules.'
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editing.value = null
  form.value = { aquarium: null, light_type: '', on_time: '', off_time: '', intensity_percent: null, notes: '' }
  formError.value = null
  showModal.value = true
}

function openEdit(item) {
  editing.value = item
  form.value = { aquarium: item.aquarium, light_type: item.light_type, on_time: item.on_time,
    off_time: item.off_time, intensity_percent: item.intensity_percent ?? null, notes: item.notes || '' }
  formError.value = null
  showModal.value = true
}

function closeModal() { showModal.value = false; editing.value = null }

async function save() {
  saving.value = true
  formError.value = null
  const payload = { ...form.value }
  if (payload.intensity_percent === '' || payload.intensity_percent === null) delete payload.intensity_percent
  try {
    if (editing.value) await lightingApi.update(editing.value.id, payload)
    else await lightingApi.create(payload)
    closeModal()
    await load()
  } catch (e) {
    formError.value = e.response?.data ? JSON.stringify(e.response.data) : 'Save failed.'
  } finally {
    saving.value = false
  }
}

function confirmDelete(item) { deleteTarget.value = item }

async function doDelete() {
  saving.value = true
  try {
    await lightingApi.remove(deleteTarget.value.id)
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.hint { color: #a0aec0; font-weight: 400; font-size: 0.8rem; }
</style>
