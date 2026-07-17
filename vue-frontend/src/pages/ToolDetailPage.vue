<template>
  <div class="tool-detail-page">
    <div class="container" v-if="storeStore.currentTool">
      <button @click="$router.back()" class="back-btn">返回列表</button>
      
      <div class="tool-detail">
        <div class="tool-header">
          <div class="tool-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 7h16M4 17h16M10 12h4M4 12h2M18 12h2" />
            </svg>
          </div>
          <div class="tool-info">
            <h1>{{ storeStore.currentTool.name }}</h1>
            <div class="tool-meta">
              <span class="version">版本: v{{ storeStore.currentTool.version }}</span>
              <span class="downloads">{{ storeStore.currentTool.downloads }} 下载</span>
              <span class="date">上传于 {{ formatDate(storeStore.currentTool.upload_date) }}</span>
            </div>
          </div>
        </div>
        
        <div class="tool-content">
          <div class="description">
            <h2>描述</h2>
            <p>{{ storeStore.currentTool.description }}</p>
          </div>
          
          <div class="actions">
            <button @click="handleDownload" class="btn btn-primary">下载工具</button>
            <button v-if="authStore.isStaff" @click="handleDelete" class="btn btn-danger">删除工具</button>
          </div>
        </div>
      </div>
    </div>
    
    <Loading :loading="storeStore.loading" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStoreStore } from '@/stores/store'
import { useAuthStore } from '@/stores/auth'
import Loading from '@/components/Loading.vue'

const route = useRoute()
const storeStore = useStoreStore()
const authStore = useAuthStore()

const handleDownload = () => {
  storeStore.handleDownload(route.params.id)
}

const handleDelete = () => {
  if (confirm('确定要删除这个工具吗？')) {
    storeStore.handleDelete(route.params.id)
    window.location.href = '/store'
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  storeStore.fetchToolDetail(route.params.id)
})
</script>

<style scoped>
.tool-detail-page {
  min-height: calc(100vh - 80px);
  background: #f3f4f6;
  padding: 40px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-btn {
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 24px;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #f9fafb;
}

.tool-detail {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.tool-header {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 32px;
}

.tool-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.tool-icon svg {
  width: 40px;
  height: 40px;
}

.tool-info h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.tool-meta {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: #6b7280;
}

.tool-content {
  border-top: 1px solid #e5e7eb;
  padding-top: 32px;
}

.description h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.description p {
  font-size: 16px;
  color: #4b5563;
  line-height: 1.8;
  margin: 0;
}

.actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}
</style>
