<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <router-link to="/" class="logo">
          <span>Hub</span>
        </router-link>
        <nav class="nav">
          <router-link to="/store" class="nav-link" :class="{ active: $route.name === 'Store' }">商店</router-link>
        </nav>
        <div class="auth">
          <template v-if="authStore.isAuthenticated">
            <span class="username">{{ authStore.username }}</span>
            <button v-if="authStore.isStaff" @click="$router.push('/store/upload')" class="btn btn-secondary">上传</button>
            <button @click="logout" class="btn btn-danger">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-secondary">登录</router-link>
            <router-link to="/register" class="btn btn-primary">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const logout = () => {
  authStore.clearTokens()
  window.location.href = '/login'
}
</script>

<style scoped>
.header {
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: white;
  padding: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 24px;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-size: 16px;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: white;
}

.auth {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-size: 14px;
  font-weight: 500;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: white;
  color: #3b82f6;
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.9);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-danger {
  background: rgba(239, 68, 68, 0.8);
  color: white;
}

.btn-danger:hover {
  background: rgba(239, 68, 68, 1);
}
</style>
