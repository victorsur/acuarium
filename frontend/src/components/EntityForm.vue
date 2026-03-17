<script setup>
/**
 * EntityForm — formulario genérico con validación.
 *
 * Props:
 *   fields  Array<FieldConfig>  — configuración de campos
 *   initial Object|null         — datos del item a editar (null = crear)
 *   saving  Boolean             — bloquea el botón mientras guarda
 *
 * FieldConfig:
 *   key           String   — nombre del campo (coincide con la API)
 *   label         String   — etiqueta visible
 *   type          String   — text | number | checkbox | select | time | datetime-local | url | textarea
 *   required      Boolean
 *   min / max     Number   — para number (valor) y text (longitud)
 *   pattern       String   — regex de validación (string)
 *   patternHint   String   — mensaje de ayuda del patrón
 *   options       Array    — [{ value, label }] para type='select'
 *   tableHide     Boolean  — no mostrar en tabla (ignorado aquí)
 *   default       *        — valor por defecto
 *   checkboxLabel String   — texto junto al checkbox
 */
import { ref, watch } from 'vue'

const props = defineProps({
  fields:  { type: Array,  required: true },
  initial: { type: Object, default: null },
  saving:  { type: Boolean, default: false },
})
const emit = defineEmits(['submit', 'cancel'])

const form   = ref({})
const errors = ref({})

// ── Inicializar formulario ────────────────────────
function initForm() {
  form.value   = {}
  errors.value = {}
  for (const f of props.fields) {
    if (props.initial?.[f.key] !== undefined) {
      // datetime-local: recortar a YYYY-MM-DDTHH:mm
      if (f.type === 'datetime-local' && props.initial[f.key]) {
        form.value[f.key] = String(props.initial[f.key]).slice(0, 16)
      } else {
        form.value[f.key] = props.initial[f.key]
      }
    } else {
      form.value[f.key] = f.default ?? (f.type === 'checkbox' ? false : '')
    }
  }
}
watch(() => props.initial, initForm, { immediate: true })

// ── Validación ────────────────────────────────────
function validate() {
  errors.value = {}
  for (const f of props.fields) {
    const val = form.value[f.key]
    const empty = val === '' || val === null || val === undefined

    if (f.required && empty && f.type !== 'checkbox') {
      errors.value[f.key] = `${f.label} es obligatorio`
      continue
    }
    if (!empty) {
      if ((f.type === 'text' || f.type === 'textarea' || f.type === 'url') && typeof val === 'string') {
        if (f.min && val.length < f.min) { errors.value[f.key] = `Mínimo ${f.min} caracteres`; continue }
        if (f.max && val.length > f.max) { errors.value[f.key] = `Máximo ${f.max} caracteres`; continue }
      }
      if (f.type === 'number') {
        const n = Number(val)
        if (isNaN(n))            { errors.value[f.key] = 'Debe ser un número'; continue }
        if (f.min !== undefined && n < f.min) { errors.value[f.key] = `Mínimo ${f.min}`; continue }
        if (f.max !== undefined && n > f.max) { errors.value[f.key] = `Máximo ${f.max}`; continue }
      }
      if (f.pattern && typeof val === 'string') {
        if (!new RegExp(f.pattern).test(val)) {
          errors.value[f.key] = `Formato inválido${f.patternHint ? ' (' + f.patternHint + ')' : ''}`
        }
      }
    }
  }
  return Object.keys(errors.value).length === 0
}

// ── Submit ────────────────────────────────────────
function submit() {
  if (!validate()) return
  const data = {}
  for (const f of props.fields) {
    let val = form.value[f.key]
    if (f.type === 'number')          val = val !== '' && val !== null ? Number(val) : null
    if (f.type === 'checkbox')        val = Boolean(val)
    if (f.type === 'datetime-local' && val) val = val.length === 16 ? val + ':00' : val
    if (!f.required && val === '')    val = null
    if (f.type === 'select')          val = val !== '' ? Number(val) : null
    data[f.key] = val
  }
  emit('submit', data)
}
</script>

<template>
  <form @submit.prevent="submit" novalidate>
    <div v-for="field in fields" :key="field.key" class="form-group">
      <label :for="field.key" class="form-label">
        {{ field.label }}<span v-if="field.required" class="req"> *</span>
      </label>

      <!-- Checkbox -->
      <label v-if="field.type === 'checkbox'" class="checkbox-wrap">
        <input :id="field.key" v-model="form[field.key]" type="checkbox" class="checkbox-input" />
        <span class="checkbox-label">{{ field.checkboxLabel || 'Activado' }}</span>
      </label>

      <!-- Select -->
      <select
        v-else-if="field.type === 'select'"
        :id="field.key"
        v-model="form[field.key]"
        :class="['form-input', { 'is-error': errors[field.key] }]"
      >
        <option value="">— Selecciona —</option>
        <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Textarea -->
      <textarea
        v-else-if="field.type === 'textarea'"
        :id="field.key"
        v-model="form[field.key]"
        rows="3"
        :class="['form-input', { 'is-error': errors[field.key] }]"
        :placeholder="field.placeholder || ''"
      />

      <!-- Todos los demás inputs -->
      <input
        v-else
        :id="field.key"
        v-model="form[field.key]"
        :type="field.type || 'text'"
        :placeholder="field.placeholder || ''"
        :class="['form-input', { 'is-error': errors[field.key] }]"
      />

      <span v-if="errors[field.key]" class="form-error">{{ errors[field.key] }}</span>
    </div>

    <div class="form-actions">
      <button type="button" class="btn btn-ghost" @click="$emit('cancel')">Cancelar</button>
      <button type="submit" class="btn btn-primary" :disabled="saving">
        {{ saving ? 'Guardando…' : (initial?.id ? 'Actualizar' : 'Crear') }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.req { color: var(--primary); }
.checkbox-wrap  { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.checkbox-input { width: 16px; height: 16px; accent-color: var(--primary); cursor: pointer; }
.checkbox-label { font-size: 14px; color: var(--text-muted); }
.form-actions   { display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px; }
</style>

