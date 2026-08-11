import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getToolList, getToolDetail, uploadTool, deleteTool, downloadTool } from '@/api/store'

export const useStoreStore = defineStore('store', () => {
  const tools = ref([])
  const currentTool = ref(null)
  const loading = ref(false)

  const fetchTools = async () => {
    loading.value = true
    try {
      const res = await getToolList()
      tools.value = res.data.results || res.data
    } finally {
      loading.value = false
    }
  }

  const fetchToolDetail = async (id) => {
    loading.value = true
    try {
      const res = await getToolDetail(id)
      currentTool.value = res.data
    } finally {
      loading.value = false
    }
  }

  const handleUpload = async (data) => {
    const res = await uploadTool(data)
    await fetchTools()
    return res.data
  }

  const handleDelete = async (id) => {
    await deleteTool(id)
    await fetchTools()
  }

  const handleDownload = async (id) => {
    downloadTool(id)
    await fetchTools()
  }

  return {
    tools,
    currentTool,
    loading,
    fetchTools,
    fetchToolDetail,
    handleUpload,
    handleDelete,
    handleDownload
  }
})
