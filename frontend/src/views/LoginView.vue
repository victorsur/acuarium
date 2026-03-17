<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router    = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error    = ref('')
const loading  = ref(false)

async function submit() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = 'Introduce usuario y contraseña.'
    return
  }
  loading.value = true
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    if (err.response?.status === 401) error.value = 'Usuario o contraseña incorrectos.'
    else                              error.value = 'No se puede conectar con el servidor.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-logo">🐠</div>
      <h1 class="login-title">Acuarium Manager</h1>
      <p class="login-sub">Inicia sesión para continuar</p>

      <form @submit.prevent="submit" novalidate>
        <div class="form-group">
          <label class="form-label" for="user">Usuario</label>
          <input id="user" v-model="username" type="text"
            class="form-input" placeholder="admin" autocomplete="username" />
        </div>
        <div class="form-group">
          <label class="form-label" for="pass">Contraseña</label>
          <input id="pass" v-model="password" type="password"
            class="form-input" placeholder="••••••••" autocomplete="current-password" />
        </div>

        <div v-if="error" class="login-error">⚠ {{ error }}</div>

        <button type="submit" class="btn btn-primary login-btn" :disabled="loading">
          {{ loading ? 'Iniciando sesión…' : '→ Entrar' }}
        </button>
      </form>

      <p class="login-hint">
        Usuario por defecto: <code>admin</code> / <code>Admin1234!</code>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 50% -20%, #2d1b6933 0%, var(--bg) 65%);
}
.login-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 44px 40px;
  width: 100%; max-width: 380px;
  box-shadow: 0 24px 48px #00000055, 0 0 0 1px #9b6dff11;
}
.login-logo  { font-size: 52px; text-align: center; margin-bottom: 10px; }
.login-title { font-size: 24px; font-weight: 700; text-align: center; margin-bottom: 4px; }
.login-sub   { font-size: 13px; color: var(--text-muted); text-align: center; margin-bottom: 30px; }
.login-btn   { width: 100%; justify-content: center; margin-top: 6px; padding: 11px; font-size: 14px; }
.login-error {
  background: var(--danger-glow); border: 1px solid #f8717144;
  color: var(--danger); border-radius: 8px;
  padding: 10px 14px; font-size: 13px; margin-bottom: 12px;
}
.login-hint {
  margin-top: 20px; text-align: center;
  font-size: 12px; color: var(--text-dim);
}
.login-hint code {
  background: var(--surface-3); color: var(--primary);
  padding: 1px 5px; border-radius: 4px;
}
</style>

