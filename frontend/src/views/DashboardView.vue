<script setup>
import { useRouter, RouterView, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth   = useAuthStore()

const nav = [
  { to: '/acuario',     label: 'Acuarios',      icon: '🏊' },
  { to: '/fish',        label: 'Peces',          icon: '🐟' },
  { to: '/plants',      label: 'Plantas',        icon: '🌿' },
  { to: '/lighting',    label: 'Iluminación',    icon: '💡' },
  { to: '/maintenance', label: 'Mantenimiento',  icon: '🔧' },
]

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-brand">
        <span class="brand-icon">🐠</span>
        <span class="brand-name">Acuarium</span>
      </div>

      <nav class="sidebar-nav">
        <RouterLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          active-class="nav-link--active"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="sidebar-footer">
        <div class="user-card">
          <div class="user-avatar">{{ auth.user?.username?.[0]?.toUpperCase() ?? '?' }}</div>
          <div class="user-info">
            <div class="user-name">{{ auth.user?.username }}</div>
            <span :class="['badge', auth.isAdmin ? 'badge-admin' : 'badge-user']">
              {{ auth.isAdmin ? '⚡ Admin' : '👤 Usuario' }}
            </span>
          </div>
        </div>
        <button class="btn btn-ghost logout-btn" @click="logout">↩ Cerrar sesión</button>
      </div>
    </aside>

    <!-- Contenido principal -->
    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: 230px; min-width: 230px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  padding: 20px 14px;
  position: sticky; top: 0; height: 100vh;
  overflow-y: auto;
}
.sidebar-brand {
  display: flex; align-items: center; gap: 10px;
  padding: 6px 8px 22px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 14px;
}
.brand-icon { font-size: 30px; }
.brand-name {
  font-size: 18px; font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--success));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* ── Nav ── */
.sidebar-nav { flex: 1; display: flex; flex-direction: column; gap: 3px; }
.nav-link {
  display: flex; align-items: center; gap: 11px;
  padding: 10px 12px; border-radius: 8px;
  font-size: 14px; font-weight: 500;
  color: var(--text-muted);
  text-decoration: none;
  transition: background var(--transition), color var(--transition);
}
.nav-link:hover        { background: var(--surface-2); color: var(--text); }
.nav-link--active      { background: var(--primary-glow); color: var(--primary); font-weight: 600; }
.nav-link--active .nav-icon { filter: drop-shadow(0 0 4px var(--primary)); }
.nav-icon { font-size: 18px; }

/* ── Footer ── */
.sidebar-footer  { border-top: 1px solid var(--border); padding-top: 16px; margin-top: 8px; }
.user-card       { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.user-avatar     {
  width: 36px; height: 36px; border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-dark), #4a1a8a);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 15px; color: #fff;
  flex-shrink: 0;
}
.user-info  { min-width: 0; }
.user-name  { font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.logout-btn { width: 100%; justify-content: center; font-size: 13px; }

/* ── Main ── */
.main { flex: 1; padding: 28px; overflow-y: auto; }
</style>

