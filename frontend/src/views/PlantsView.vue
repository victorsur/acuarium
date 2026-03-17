<script setup>
import { computed, ref, onMounted } from 'vue'
import EntityManager from '@/components/EntityManager.vue'
import { plantsApi }  from '@/api/plants'
import { acuarioApi } from '@/api/acuario'

const acuarioOptions = ref([])
onMounted(async () => {
  try {
    const list = await acuarioApi.list({ limit: 100 })
    acuarioOptions.value = list.map(a => ({ value: a.id, label: `#${a.id} – ${a.name}` }))
  } catch { /* silencioso */ }
})

const fields = computed(() => [
  { key: 'name',        label: 'Nombre',       type: 'text',     required: true,  min: 2, max: 50 },
  { key: 'species',     label: 'Especie',       type: 'text',     required: true,  min: 2, max: 50 },
  { key: 'age',         label: 'Edad (años)',   type: 'number',   required: true,  min: 0, max: 10 },
  { key: 'description', label: 'Descripción',   type: 'textarea', required: false, max: 200, tableHide: true },
  { key: 'picture',     label: 'Imagen (URL)',   type: 'url',      required: false, isImage: true },
  { key: 'acuarioId',   label: 'Acuario',       type: 'select',   required: true,  options: acuarioOptions.value },
])
</script>

<template>
  <EntityManager title="Plantas" icon="🌿" :fields="fields" :api="plantsApi" />
</template>

