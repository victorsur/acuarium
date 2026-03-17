<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-brand">
        <span class="brand-icon">🐠</span>
        <span class="brand-name">Acuarium</span>
      </div>
      <nav class="sidebar-nav">
        <RouterLink to="/" class="nav-item" exact-active-class="active">
          <span class="nav-icon">🏠</span>
          <span>Home</span>
        </RouterLink>
        <RouterLink to="/aquariums" class="nav-item" active-class="active">
          <span class="nav-icon">🐠</span>
          <span>Aquariums</span>
        </RouterLink>
        <RouterLink to="/fish" class="nav-item" active-class="active">
          <span class="nav-icon">🐟</span>
          <span>Fish</span>
        </RouterLink>
        <RouterLink to="/plants" class="nav-item" active-class="active">
          <span class="nav-icon">🌿</span>
          <span>Plants</span>
        </RouterLink>
        <RouterLink to="/lighting" class="nav-item" active-class="active">
          <span class="nav-icon">💡</span>
          <span>Lighting</span>
        </RouterLink>
        <RouterLink to="/maintenance-tasks" class="nav-item" active-class="active">
          <span class="nav-icon">🔧</span>
          <span>Maintenance</span>
        </RouterLink>
        <RouterLink to="/aquarium-types" class="nav-item" active-class="active">
          <span class="nav-icon">📋</span>
          <span>Aquarium Types</span>
        </RouterLink>
      </nav>
    </aside>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f4f8;
  color: #1a202c;
  min-height: 100vh;
}

.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  min-height: 100vh;
  background: linear-gradient(180deg, #1a365d 0%, #2a4a7f 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100;
  box-shadow: 2px 0 12px rgba(0,0,0,0.15);
}

.sidebar-brand {
  padding: 24px 20px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.12);
}

.brand-icon { font-size: 1.7rem; }
.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.sidebar-nav {
  padding: 16px 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 20px;
  color: rgba(255,255,255,0.75);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 0;
  transition: background 0.15s, color 0.15s;
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: #fff;
}

.nav-item.active {
  background: rgba(255,255,255,0.18);
  color: #fff;
  border-left: 3px solid #63b3ed;
}

.nav-icon { font-size: 1.1rem; width: 22px; text-align: center; }

.main-content {
  margin-left: 220px;
  flex: 1;
  padding: 32px;
  min-height: 100vh;
}
</style>
