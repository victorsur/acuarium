<script setup>
import EntityManager from '@/components/EntityManager.vue'
import { acuarioApi } from '@/api/acuario'

const fields = [
  { key: 'name',   label: 'Nombre',       type: 'text',   required: true,  min: 2, max: 50,    placeholder: 'Acuario tropical' },
  { key: 'volume', label: 'Volumen (L)',   type: 'number', required: true,  min: 1, max: 10000, placeholder: '200' },
]
</script>

<template>
  <EntityManager title="Acuarios" icon="🏊" :fields="fields" :api="acuarioApi" />
</template>

