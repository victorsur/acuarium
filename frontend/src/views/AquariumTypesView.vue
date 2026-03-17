<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">📋 Aquarium Types</h1>
      <button class="btn btn-primary" @click="openAdd">+ Add Type</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <div v-else>
      <div v-if="items.length === 0" class="empty-state">No aquarium types yet. Add one!</div>
      <table v-else class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th class="col-actions">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td><strong>{{ item.name }}</strong></td>
            <td>{{ item.description || '—' }}</td>
            <td class="col-actions">
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
        <h2 class="modal-title">{{ editing ? 'Edit Type' : 'Add Type' }}</h2>
        <form @submit.prevent="save">
          <div class="form-group">
            <label>Name <span class="required">*</span></label>
            <input v-model="form.name" type="text" class="input" required placeholder="e.g. Freshwater" />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="form.description" class="input" rows="3" placeholder="Optional description"></textarea>
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
        <h2 class="modal-title">Delete Type</h2>
        <p>Delete <strong>{{ deleteTarget.name }}</strong>? This cannot be undone.</p>
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
import { aquariumTypes } from '../api/index.js'

const items = ref([])
const loading = ref(true)
const error = ref(null)
const showModal = ref(false)
const editing = ref(null)
const form = ref({ name: '', description: '' })
const formError = ref(null)
const saving = ref(false)
const deleteTarget = ref(null)

async function load() {
  loading.value = true
  error.value = null
  try {
    const res = await aquariumTypes.getAll()
    items.value = res.data.results ?? res.data
  } catch {
    error.value = 'Failed to load aquarium types.'
  } finally {
    loading.value = false
  }
}

function openAdd() {
  editing.value = null
  form.value = { name: '', description: '' }
  formError.value = null
  showModal.value = true
}

function openEdit(item) {
  editing.value = item
  form.value = { name: item.name, description: item.description || '' }
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
  try {
    if (editing.value) {
      await aquariumTypes.update(editing.value.id, form.value)
    } else {
      await aquariumTypes.create(form.value)
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
    await aquariumTypes.remove(deleteTarget.value.id)
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
