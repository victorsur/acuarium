<script setup>
/**
 * EntityManager — tabla + modal genérico.
 * Props: title, icon, fields (Array<FieldConfig>), api { list, create, update, remove }
 * Campos con isImage:true se muestran como miniatura clicable en la primera columna.
 */
import { computed, ref } from 'vue'
import EntityForm from './EntityForm.vue'
import { useEntityCrud } from '@/composables/useEntityCrud'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  title:  { type: String, required: true },
  icon:   { type: String, default: '📋' },
  fields: { type: Array,  required: true },
  api:    { type: Object, required: true },
})

const auth = useAuthStore()
const crud = useEntityCrud(props.api)

// Campos de imagen (miniatura clicable, siempre van primeros)
const imageFields  = computed(() => props.fields.filter(f => f.isImage))
// Campos normales visibles en tabla (sin tableHide ni isImage)
const tableFields  = computed(() => props.fields.filter(f => !f.tableHide && !f.isImage))
// ¿Hay alguna columna de imagen que mostrar?
const hasImageCol  = computed(() => imageFields.value.length > 0)

// Modal de imagen ampliada
const imgModal = ref(null)   // null = cerrado, string URL = abierto
function openImg(url) { if (url) imgModal.value = url }
function closeImg()   { imgModal.value = null }

// Formatea un valor para mostrarlo en la tabla
function fmt(item, field) {
  const v = item[field.key]
  if (v === null || v === undefined || v === '') return '—'
  if (field.type === 'checkbox') return v ? '✓ Sí' : '✗ No'
  if (field.type === 'datetime-local' || field.key === 'date') {
    return new Date(v).toLocaleString('es-ES', { dateStyle: 'short', timeStyle: 'short' })
  }
  if (field.type === 'select') {
    const opt = field.options?.find(o => o.value === v)
    return opt ? opt.label : v
  }
  if (typeof v === 'string' && v.startsWith('http')) return '🔗 URL'
  return v
}
</script>

<template>
  <div class="card">
    <!-- Cabecera -->
    <div class="card-header">
      <h2 class="card-title">{{ icon }} {{ title }}</h2>
      <button class="btn btn-primary" @click="crud.openCreate">
        + Añadir {{ title }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="crud.loading.value" class="spinner" />

    <!-- Tabla -->
    <template v-else>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <!-- Columna imagen (primera de datos) -->
              <th v-if="hasImageCol" class="img-col">Imagen</th>
              <th v-for="f in tableFields" :key="f.key">{{ f.label }}</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!crud.items.value.length">
              <td :colspan="tableFields.length + (hasImageCol ? 3 : 2)">
                <div class="empty-state">
                  <div class="empty-icon">{{ icon }}</div>
                  Sin {{ title.toLowerCase() }}. ¡Crea el primero!
                </div>
              </td>
            </tr>
            <tr v-for="item in crud.items.value" :key="item.id">
              <td class="id-cell">{{ item.id }}</td>

              <!-- Miniatura clicable (primera imagen que encuentre) -->
              <td v-if="hasImageCol" class="img-col">
                <template v-for="f in imageFields" :key="f.key">
                  <img
                    v-if="item[f.key]"
                    :src="item[f.key]"
                    :alt="item.name || 'imagen'"
                    class="thumb"
                    @click="openImg(item[f.key])"
                  />
                  <span v-else class="thumb-empty">—</span>
                </template>
              </td>

              <td v-for="f in tableFields" :key="f.key">{{ fmt(item, f) }}</td>
              <td>
                <div class="actions">
                  <button class="btn btn-ghost btn-sm" @click="crud.openEdit(item)">✏️ Editar</button>
                  <button
                    v-if="auth.isAdmin"
                    class="btn btn-danger btn-sm"
                    @click="crud.remove(item.id)"
                  >🗑️ Eliminar</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>

  <!-- Modal formulario -->
  <Teleport to="body">
    <div v-if="crud.showModal.value" class="modal-backdrop" @click.self="crud.closeModal">
      <div class="modal">
        <div class="modal-header">
          <span class="modal-title">
            {{ crud.editing.value?.id ? '✏️ Editar' : '✨ Nuevo' }}
            {{ title.endsWith('s') ? title.slice(0, -1) : title }}
          </span>
          <button class="btn btn-ghost btn-sm" @click="crud.closeModal">✕</button>
        </div>
        <div class="modal-body">
          <EntityForm
            :fields="fields"
            :initial="crud.editing.value"
            :saving="crud.saving.value"
            @submit="crud.save"
            @cancel="crud.closeModal"
          />
        </div>
      </div>
    </div>
  </Teleport>

  <!-- Modal imagen ampliada -->
  <Teleport to="body">
    <div v-if="imgModal" class="modal-backdrop img-backdrop" @click.self="closeImg">
      <div class="img-modal">
        <button class="img-modal-close" @click="closeImg" aria-label="Cerrar">✕</button>
        <img :src="imgModal" alt="Vista ampliada" class="img-modal-img" />
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.id-cell { color: var(--text-dim); font-size: 11px; font-family: monospace; }

/* ── Miniatura en tabla ── */
.img-col { width: 64px; text-align: center; padding: 6px; }

.thumb {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 8px;
  cursor: zoom-in;
  border: 2px solid transparent;
  transition: border-color 0.15s, transform 0.15s;
  display: block;
  margin: 0 auto;
}
.thumb:hover {
  border-color: var(--primary);
  transform: scale(1.08);
}

.thumb-empty {
  color: var(--text-dim);
  font-size: 13px;
}

/* ── Modal imagen ampliada ── */
.img-backdrop {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.75);
}

.img-modal {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.img-modal-img {
  max-width: 90vw;
  max-height: 85vh;
  border-radius: 12px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
  display: block;
}

.img-modal-close {
  position: absolute;
  top: -16px;
  right: -16px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--surface, #1e2635);
  color: var(--text, #e0e6f0);
  border: 2px solid var(--border, #2e3a4e);
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s, transform 0.15s;
  z-index: 10;
}
.img-modal-close:hover {
  background: var(--primary, #4a9eff);
  transform: scale(1.1);
}
</style>

