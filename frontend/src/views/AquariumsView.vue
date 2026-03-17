<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">🐠 Aquariums</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Aquarium</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <div v-else>
      <div v-if="items.length === 0" class="empty-state">No aquariums yet. Add one!</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Volume (L)</th>
            <th>Type</th>
            <th>Setup Date</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td><strong>{{ item.name }}</strong></td>
            <td>{{ item.volume_liters }}</td>
            <td>{{ typeName(item.aquarium_type) }}</td>
            <td>{{ item.setup_date || '—' }}</td>
            <td class="col-actions">
              <RouterLink :to="`/aquariums/${item.id}`" class="btn btn-sm btn-info">View</RouterLink>
              <button class="btn btn-sm btn-secondary" @click="openEdit(item)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="confirmDelete(item)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2 class="modal-title">{{ editing ? 'Edit Aquarium' : 'Add Aquarium' }}</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label>Name <span class="required">*</span></label>
            <input v-model="form.name" type="text" class="input" required placeholder="My Aquarium" />
          </div>
          <div class="form-group">
            <label>Volume (Liters) <span class="required">*</span></label>
            <input v-model.number="form.volume_liters" type="number" step="0.1" min="0" class="input" required placeholder="100" />
          </div>
          <div class="form-group">
            <label>Aquarium Type</label>
            <select v-model="form.aquarium_type_id" class="input">
              <option :value="null">— None —</option>
              <option v-for="t in types" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Setup Date</label>
            <input v-model="form.setup_date" type="date" class="input" />
          </div>
          <div class="form-group">
            <label>Notes</label>
            <textarea v-model="form.notes" class="input" rows="3" placeholder="Optional notes"></textarea>
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

    <!-- Delete confirm -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal modal-sm">
        <h2 class="modal-title">Delete Aquarium</h2>
        <p>Delete <strong>{{ deleteTarget.name }}</strong>? All related data will be removed.</p>
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
import { RouterLink } from 'vue-router'
import { aquariums, aquariumTypes } from '../api/index.js'

const items = ref([])
const types = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editing = ref(null)
const form = ref({ name: '', volume_liters: '', aquarium_type_id: null, setup_date: '', notes: '' })
const formError = ref(null)
const saving = ref(false)
const deleteTarget = ref(null)

function typeName(typeId) {
  const t = types.value.find(x => x.id === typeId)
  return t ? t.name : '—'
}

async function load() {
  loading.value = true
  error.value = null
  try {
    const [aqRes, typRes] = await Promise.all([aquariums.getAll(), aquariumTypes.getAll()])
    items.value = aqRes.data.results ?? aqRes.data
    types.value = typRes.data.results ?? typRes.data
  } catch {
    error.value = 'Failed to load aquariums.'
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editing.value = null
  form.value = { name: '', volume_liters: '', aquarium_type_id: null, setup_date: '', notes: '' }
  formError.value = null
  showModal.value = true
}

function openEdit(item) {
  editing.value = item
  form.value = {
    name: item.name,
    volume_liters: item.volume_liters,
    aquarium_type_id: item.aquarium_type ?? null,
    setup_date: item.setup_date || '',
    notes: item.notes || ''
  }
  formError.value = null
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editing.value = null
}

async function save() {
  saving.value = true
  formError.value = null
  const payload = { ...form.value }
  if (!payload.aquarium_type_id) delete payload.aquarium_type_id
  if (!payload.setup_date) delete payload.setup_date
  try {
    if (editing.value) {
      await aquariums.update(editing.value.id, payload)
    } else {
      await aquariums.create(payload)
    }
    closeModal()
    await load()
  } catch (e) {
    formError.value = e.response?.data ? JSON.stringify(e.response.data) : 'Save failed.'
  } finally {
    saving.value = false
  }
}

function confirmDelete(item) {
  deleteTarget.value = item
}

async function doDelete() {
  saving.value = true
  try {
    await aquariums.remove(deleteTarget.value.id)
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
.btn-info { background: #3182ce; color: #fff; }
.btn-info:hover:not(:disabled) { background: #2b6cb0; }
</style>
