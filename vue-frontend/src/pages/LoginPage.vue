<template>
  <div class="login-page">
    <div class="container">
      <div class="login-form">
        <h1>登录</h1>
        <form @submit.prevent="handleLogin" class="form">
          <div class="form-group">
            <label>用户名</label>
            <input type="text" v-model="formData.username" required class="form-input" placeholder="输入用户名" />
          </div>
          
          <div class="form-group">
            <label>密码</label>
            <input type="password" v-model="formData.password" required class="form-input" placeholder="输入密码" />
          </div>
          
          <div v-if="error" class="error-message">{{ error }}</div>
          
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? '登录中...' : '登录' }}
          </button>
          
          <div class="register-link">
            <span>还没有账号？</span>
            <router-link to="/register">立即注册</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const loading = ref(false)
const error = ref('')

const formData = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    await authStore.handleLogin(formData)
    window.location.href = '/'
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 80px);
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.container {
  width: 100%;
  max-width: 400px;
  padding: 0 20px;
}

.login-form {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.login-form h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 32px 0;
  text-align: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #3b82f6;
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  padding: 12px;
  background: #fee2e2;
  border-radius: 6px;
}

.btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 14px;
  color: #6b7280;
}

.register-link a {
  color: #3b82f6;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
