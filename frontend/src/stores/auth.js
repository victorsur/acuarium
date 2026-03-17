// stores/auth.js — estado global de autenticación (Pinia)
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const user        = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin         = computed(() => user.value?.role === 'ROLE_ADMIN')

  // ── Login: obtiene tokens y perfil ───────────────
  async function login(username, password) {
    const tokenData = await authApi.login(username, password)
    accessToken.value = tokenData.access_token
    localStorage.setItem('access_token',  tokenData.access_token)
    localStorage.setItem('refresh_token', tokenData.refresh_token)

    const profile = await authApi.me()
    user.value = profile
    localStorage.setItem('user', JSON.stringify(profile))
  }

  // ── Logout: limpia todo ───────────────────────────
  function logout() {
    accessToken.value = null
    user.value        = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  // ── Restaura el usuario desde localStorage ────────
  function restore() {
    const raw = localStorage.getItem('user')
    if (raw) user.value = JSON.parse(raw)
  }

  return { accessToken, user, isAuthenticated, isAdmin, login, logout, restore }
})

