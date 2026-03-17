<script setup>
import { useNotification } from '@/composables/useNotification'
const { state, hide } = useNotification()
</script>

<template>
  <Transition name="notif">
    <div v-if="state.visible" :class="['notif', `notif--${state.type}`]" @click="hide">
      <span class="notif-icon">{{ state.type === 'success' ? '✓' : state.type === 'error' ? '✕' : '⚠' }}</span>
      <span class="notif-msg">{{ state.message }}</span>
    </div>
  </Transition>
</template>

<style scoped>
.notif {
  position: fixed; top: 20px; right: 20px; z-index: 999;
  display: flex; align-items: center; gap: 10px;
  padding: 13px 18px; border-radius: 10px;
  font-size: 14px; font-weight: 500;
  max-width: 400px; cursor: pointer;
  box-shadow: 0 8px 24px #00000055;
  border: 1px solid transparent;
}
.notif--success { background: #0f2b1f; color: #4ade80; border-color: #4ade8044; }
.notif--error   { background: #2b0f0f; color: #f87171; border-color: #f8717144; }
.notif--warning { background: #2b200f; color: #fbbf24; border-color: #fbbf2444; }
.notif-icon { font-size: 16px; font-weight: 700; }
.notif-enter-active, .notif-leave-active { transition: all .3s cubic-bezier(.34,1.56,.64,1); }
.notif-enter-from { opacity: 0; transform: translateX(60px) scale(.9); }
.notif-leave-to   { opacity: 0; transform: translateX(60px) scale(.9); }
</style>

