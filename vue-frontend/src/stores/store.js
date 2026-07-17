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
    const res = await downloadTool(id)
    const contentDisposition = res.headers['content-disposition']
    let filename = `tool_${id}.zip`
    if (contentDisposition) {
      const match = contentDisposition.match(/filename=(.+)/)
      if (match) filename = match[1]
    }
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)
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
