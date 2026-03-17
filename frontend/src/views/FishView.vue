<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">🐟 Fish</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Fish</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <div v-else>
      <div v-if="items.length === 0" class="empty-state">No fish recorded yet.</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>Aquarium</th>
            <th>Species</th>
            <th>Common Name</th>
            <th>Qty</th>
            <th>Added Date</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ aquariumName(item.aquarium) }}</td>
            <td><em>{{ item.species }}</em></td>
            <td>{{ item.common_name || '—' }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.added_date || '—' }}</td>
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
        <h2 class="modal-title">{{ editing ? 'Edit Fish' : 'Add Fish' }}</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label>Aquarium <span class="required">*</span></label>
            <select v-model="form.aquarium" class="input" required>
              <option :value="null">— Select —</option>
              <option v-for="a in aquariumList" :key="a.id" :value="a.id">{{ a.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Species <span class="required">*</span></label>
            <input v-model="form.species" type="text" class="input" required placeholder="e.g. Danio rerio" />
          </div>
          <div class="form-group">
            <label>Common Name</label>
            <input v-model="form.common_name" type="text" class="input" placeholder="e.g. Zebra Danio" />
          </div>
          <div class="form-group">
            <label>Quantity <span class="required">*</span></label>
            <input v-model.number="form.quantity" type="number" min="1" class="input" required />
          </div>
          <div class="form-group">
            <label>Added Date</label>
            <input v-model="form.added_date" type="date" class="input" />
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
        <h2 class="modal-title">Delete Fish</h2>
        <p>Delete <strong>{{ deleteTarget.species }}</strong>? This cannot be undone.</p>
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
import { fish as fishApi, aquariums } from '../api/index.js'

const items = ref([])
const aquariumList = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editing = ref(null)
const form = ref({ aquarium: null, species: '', common_name: '', quantity: 1, added_date: '', notes: '' })
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
    const [fiRes, aqRes] = await Promise.all([fishApi.getAll(), aquariums.getAll()])
    items.value = fiRes.data.results ?? fiRes.data
    aquariumList.value = aqRes.data.results ?? aqRes.data
  } catch {
    error.value = 'Failed to load fish.'
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editing.value = null
  form.value = { aquarium: null, species: '', common_name: '', quantity: 1, added_date: '', notes: '' }
  formError.value = null
  showModal.value = true
}

function openEdit(item) {
  editing.value = item
  form.value = { aquarium: item.aquarium, species: item.species, common_name: item.common_name || '',
    quantity: item.quantity, added_date: item.added_date || '', notes: item.notes || '' }
  formError.value = null
  showModal.value = true
}

function closeModal() { showModal.value = false; editing.value = null }

async function save() {
  saving.value = true
  formError.value = null
  const payload = { ...form.value }
  if (!payload.added_date) delete payload.added_date
  try {
    if (editing.value) await fishApi.update(editing.value.id, payload)
    else await fishApi.create(payload)
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
    await fishApi.remove(deleteTarget.value.id)
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
</style>
