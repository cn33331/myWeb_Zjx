import api from './index'

export const notesApi = {
  quickSync(repoUrl, localPath) {
    return api.post('/notes/sync/', {
      repo_url: repoUrl,
      local_path: localPath
    })
  },

  syncRepository(repositoryId) {
    return api.post(`/notes/repositories/${repositoryId}/sync/`)
  },

  getRepositories() {
    return api.get('/notes/repositories/')
  },

  getRepositoryDetail(repositoryId) {
    return api.get(`/notes/repositories/${repositoryId}/`)
  },

  createRepository(data) {
    return api.post('/notes/repositories/', data)
  },

  updateRepository(repositoryId, data) {
    return api.put(`/notes/repositories/${repositoryId}/`, data)
  },

  deleteRepository(repositoryId) {
    return api.delete(`/notes/repositories/${repositoryId}/`)
  },

  getNotes(repositoryId, search = '') {
    const params = search ? { search } : {}
    return api.get(`/notes/repositories/${repositoryId}/notes/`, { params })
  },

  getNoteContent(repositoryId, filePath) {
    return api.get(`/notes/repositories/${repositoryId}/notes/${filePath}/`)
  }
}
