import api from './index'

export const getTopicList = () => api.get('/forum/topics/')
export const getTopicDetail = (id) => api.get(`/forum/topics/${id}/`)
export const createTopic = (data) => api.post('/forum/topics/', data)
export const getPosts = (topicId) => api.get(`/forum/topics/${topicId}/posts/`)
export const createPost = (topicId, data) => api.post(`/forum/topics/${topicId}/posts/`, data)
