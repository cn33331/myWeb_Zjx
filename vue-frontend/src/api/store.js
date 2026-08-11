import api from './index'

export const getToolList = () => api.get('/store/tools/')
export const getToolDetail = (id) => api.get(`/store/tools/${id}/`)
export const uploadTool = (data) => api.post('/store/tools/', data, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const deleteTool = (id) => api.delete(`/store/tools/${id}/`)
export const downloadTool = (id) => {
  const baseURL = import.meta.env.VITE_API_BASE_URL
  const url = `${baseURL}/store/tools/${id}/download/`
  const a = document.createElement('a')
  a.href = url
  a.download = ''
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
