import api from './index'

export const login = (data) => api.post('/auth/login/', data)
export const refreshToken = (data) => api.post('/auth/refresh/', data)
