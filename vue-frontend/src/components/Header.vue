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
            <button @click="logout" class="btn btn-outline">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-primary">登录</router-link>
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
  background: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  padding: 16px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  text-decoration: none;
}

.nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: #666666;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: #1a1a1a;
}

.auth {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-size: 14px;
  color: #444444;
}

.btn {
  padding: 8px 18px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #1a1a1a;
  color: #ffffff;
}

.btn-primary:hover {
  background: #333333;
}

.btn-secondary {
  background: #f5f5f5;
  color: #1a1a1a;
}

.btn-secondary:hover {
  background: #e8e8e8;
}

.btn-outline {
  background: transparent;
  color: #666666;
  border: 1px solid #e0e0e0;
}

.btn-outline:hover {
  border-color: #1a1a1a;
  color: #1a1a1a;
}
</style>