<script setup>
import { computed, ref, onMounted } from 'vue'
import EntityManager  from '@/components/EntityManager.vue'
import { lightingApi } from '@/api/lighting'
import { acuarioApi }  from '@/api/acuario'

const acuarioOptions = ref([])
onMounted(async () => {
  try {
    const list = await acuarioApi.list({ limit: 100 })
    acuarioOptions.value = list.map(a => ({ value: a.id, label: `#${a.id} – ${a.name}` }))
  } catch { /* silencioso */ }
})

const TIME_PATTERN = '^([01]\\d|2[0-3]):[0-5]\\d$'

const fields = computed(() => [
  { key: 'light_type', label: 'Tipo de luz',    type: 'text',     required: true,  min: 2, max: 30, placeholder: 'LED' },
  { key: 'watts',      label: 'Potencia (W)',   type: 'number',   required: true,  min: 1, max: 1000 },
  { key: 'wifi',       label: 'WiFi',           type: 'checkbox', required: false, default: false, checkboxLabel: 'Conectividad WiFi' },
  { key: 'start_time', label: 'Hora encendido', type: 'time',     required: true,  pattern: TIME_PATTERN, patternHint: 'HH:mm' },
  { key: 'end_time',   label: 'Hora apagado',   type: 'time',     required: true,  pattern: TIME_PATTERN, patternHint: 'HH:mm' },
  { key: 'aquariumId', label: 'Acuario',        type: 'select',   required: true,  options: acuarioOptions.value },
])
</script>

<template>
  <EntityManager title="Iluminación" icon="💡" :fields="fields" :api="lightingApi" />
</template>

