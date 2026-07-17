import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const username = ref('')
  const isStaff = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)

  const setTokens = (access, refresh) => {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('username', username.value)
    localStorage.setItem('is_staff', String(isStaff.value))
  }

  const clearTokens = () => {
    accessToken.value = ''
    refreshToken.value = ''
    username.value = ''
    isStaff.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    localStorage.removeItem('is_staff')
  }

  const handleLogin = async (data) => {
    const res = await login(data)
    setTokens(res.data.access, res.data.refresh)
    username.value = res.data.username
    isStaff.value = res.data.is_staff || false
    return res.data
  }

  const handleRegister = async (data) => {
    const res = await register(data)
    setTokens(res.data.access, res.data.refresh)
    username.value = res.data.username
    return res.data
  }

  const initFromStorage = () => {
    const storedToken = localStorage.getItem('access_token')
    if (storedToken) {
      accessToken.value = storedToken
      refreshToken.value = localStorage.getItem('refresh_token') || ''
      username.value = localStorage.getItem('username') || ''
      isStaff.value = localStorage.getItem('is_staff') === 'true'
    }
  }

  return {
    accessToken,
    refreshToken,
    username,
    isStaff,
    isAuthenticated,
    setTokens,
    clearTokens,
    handleLogin,
    handleRegister,
    initFromStorage
  }
})
