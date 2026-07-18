import api from './index'

export const getTransferRecords = () => api.get('/transfer/records/')
export const createTransferRecord = (data) => api.post('/transfer/records/', data)
export const updateTransferRecord = (id, data) => api.put(`/transfer/records/${id}/`, data)
export const deleteTransferRecord = (id) => api.delete(`/transfer/records/${id}/`)
