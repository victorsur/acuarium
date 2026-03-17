<script setup>
import { computed, ref, onMounted } from 'vue'
import EntityManager     from '@/components/EntityManager.vue'
import { maintenanceApi } from '@/api/maintenance'
import { acuarioApi }     from '@/api/acuario'

const acuarioOptions = ref([])
onMounted(async () => {
  try {
    const list = await acuarioApi.list({ limit: 100 })
    acuarioOptions.value = list.map(a => ({ value: a.id, label: `#${a.id} – ${a.name}` }))
  } catch { /* silencioso */ }
})

const fields = computed(() => [
  { key: 'task',      label: 'Tarea',    type: 'text',           required: true, min: 3, max: 100, placeholder: 'Cambio de agua 30%' },
  { key: 'date',      label: 'Fecha',    type: 'datetime-local', required: true },
  { key: 'acuarioId', label: 'Acuario',  type: 'select',         required: true, options: acuarioOptions.value },
])
</script>

<template>
  <EntityManager title="Mantenimiento" icon="🔧" :fields="fields" :api="maintenanceApi" />
</template>

