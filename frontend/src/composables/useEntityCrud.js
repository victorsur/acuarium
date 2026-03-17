// useEntityCrud.js — composable genérico para operaciones CRUD
import { ref, onMounted } from 'vue'
import { useNotification } from './useNotification'

export function useEntityCrud(api) {
  const items     = ref([])
  const loading   = ref(false)
  const saving    = ref(false)
  const showModal = ref(false)
  const editing   = ref(null)       // null = crear, objeto = editar
  const { notify } = useNotification()

  // ── Helpers ──────────────────────────────────────
  function getErrorMsg(err) {
    const d = err.response?.data?.detail
    if (Array.isArray(d)) return d.map(e => e.msg).join(' · ')
    return d || err.message || 'Error desconocido'
  }

  // ── Carga ─────────────────────────────────────────
  async function load() {
    loading.value = true
    try {
      items.value = await api.list({ limit: 100 })
    } catch (err) {
      notify('Error al cargar datos: ' + getErrorMsg(err), 'error')
    } finally {
      loading.value = false
    }
  }

  // ── Modal ─────────────────────────────────────────
  function openCreate() { editing.value = null;        showModal.value = true }
  function openEdit(item) { editing.value = { ...item }; showModal.value = true }
  function closeModal() { showModal.value = false;    editing.value = null }

  // ── Guardar (crear o actualizar) ──────────────────
  async function save(formData) {
    saving.value = true
    try {
      if (editing.value?.id) {
        await api.update(editing.value.id, formData)
        notify('✓ Actualizado correctamente', 'success')
      } else {
        await api.create(formData)
        notify('✓ Creado correctamente', 'success')
      }
      await load()
      closeModal()
    } catch (err) {
      const status = err.response?.status
      if (status === 403) notify('Sin permisos para esta acción', 'error')
      else                notify('Error: ' + getErrorMsg(err), 'error')
    } finally {
      saving.value = false
    }
  }

  // ── Eliminar ──────────────────────────────────────
  async function remove(id) {
    if (!window.confirm('¿Eliminar este elemento? Esta acción no se puede deshacer.')) return
    try {
      await api.remove(id)
      notify('✓ Eliminado correctamente', 'success')
      await load()
    } catch (err) {
      const status = err.response?.status
      if (status === 403) notify('Sin permisos para eliminar', 'error')
      else                notify('Error al eliminar: ' + getErrorMsg(err), 'error')
    }
  }

  onMounted(load)

  return { items, loading, saving, showModal, editing, load, openCreate, openEdit, closeModal, save, remove }
}

