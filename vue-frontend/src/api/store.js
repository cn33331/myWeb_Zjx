import api from './index'

export const getToolList = () => api.get('/store/tools/')
export const getToolDetail = (id) => api.get(`/store/tools/${id}/`)
export const uploadTool = (data) => api.post('/store/tools/', data, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const deleteTool = (id) => api.delete(`/store/tools/${id}/`)
export const downloadTool = (id) => api.get(`/store/tools/${id}/download/`, {
  responseType: 'blob'
})
