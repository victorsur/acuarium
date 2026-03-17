import { describe, test, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

// Mocks necesarios para evitar imports de axios y router en el store
vi.mock('@/api/auth', () => ({
  authApi: {
    login: vi.fn(),
    me: vi.fn(),
    register: vi.fn(),
  }
}))

vi.mock('@/router', () => ({
  default: { push: vi.fn() }
}))

import { useAuthStore } from './auth'

beforeEach(() => {
  setActivePinia(createPinia())
  localStorage.clear()
})

describe('useAuthStore', () => {
  test('estado inicial: no autenticado', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
    expect(store.isAdmin).toBe(false)
    expect(store.user).toBeNull()
  })

  test('login y logout actualizan el estado', () => {
    const store = useAuthStore()
    // Simula login seteando el estado directamente
    store.accessToken = 'token'
    store.user = { username: 'admin', role: 'ROLE_ADMIN' }
    expect(store.isAuthenticated).toBe(true)
    expect(store.isAdmin).toBe(true)
    store.logout()
    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBeNull()
  })

  test('isAdmin es false para usuarios sin rol admin', () => {
    const store = useAuthStore()
    store.accessToken = 'token'
    store.user = { username: 'usuario', role: 'ROLE_USER' }
    expect(store.isAuthenticated).toBe(true)
    expect(store.isAdmin).toBe(false)
  })

  test('logout limpia el localStorage', () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'token')
    localStorage.setItem('refresh_token', 'refresh')
    localStorage.setItem('user', JSON.stringify({ username: 'admin' }))
    store.logout()
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
    expect(localStorage.getItem('user')).toBeNull()
  })
})
