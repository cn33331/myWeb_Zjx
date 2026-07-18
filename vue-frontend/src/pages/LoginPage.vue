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
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.container {
  width: 100%;
  max-width: 420px;
  padding: 0 24px;
}

.login-form {
  background: #ffffff;
  border-radius: 4px;
  padding: 40px 32px;
  border: 1px solid #e0e0e0;
}

.login-form h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
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
  color: #444444;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
  background: #ffffff;
}

.form-input:focus {
  border-color: #1a1a1a;
}

.form-input::placeholder {
  color: #999999;
}

.error-message {
  color: #d44;
  font-size: 13px;
  padding: 10px 12px;
  background: #faf0f0;
  border-radius: 4px;
  border: 1px solid #f0d0d0;
}

.btn {
  padding: 12px 32px;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #1a1a1a;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #333333;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>