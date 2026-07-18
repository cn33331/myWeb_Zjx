<template>
  <div class="tool-detail-page">
    <div class="container" v-if="storeStore.currentTool">
      <button @click="$router.back()" class="back-btn">返回列表</button>
      
      <div class="tool-detail">
        <div class="tool-header">
          <div class="tool-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
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
            <button v-if="authStore.isStaff" @click="handleDelete" class="btn btn-outline">删除工具</button>
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
  background: #f5f5f5;
  padding: 48px 0;
}

.container {
  max-width: 700px;
  margin: 0 auto;
  padding: 0 24px;
}

.back-btn {
  padding: 8px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background: #ffffff;
  color: #444444;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 24px;
  transition: all 0.2s;
}

.back-btn:hover {
  border-color: #1a1a1a;
  color: #1a1a1a;
}

.tool-detail {
  background: #ffffff;
  border-radius: 4px;
  padding: 40px;
  border: 1px solid #e0e0e0;
}

.tool-header {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  margin-bottom: 32px;
}

.tool-icon {
  width: 72px;
  height: 72px;
  background: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666666;
  flex-shrink: 0;
}

.tool-icon svg {
  width: 32px;
  height: 32px;
}

.tool-info h1 {
  font-size: 26px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}

.tool-meta {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: #666666;
  flex-wrap: wrap;
}

.tool-content {
  border-top: 1px solid #e0e0e0;
  padding-top: 32px;
}

.description h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 16px 0;
}

.description p {
  font-size: 15px;
  color: #444444;
  line-height: 1.8;
  margin: 0;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.btn {
  padding: 12px 32px;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #1a1a1a;
  color: #ffffff;
}

.btn-primary:hover {
  background: #333333;
}

.btn-outline {
  background: transparent;
  color: #666666;
  border: 1px solid #e0e0e0;
}

.btn-outline:hover {
  border-color: #d44;
  color: #d44;
}
</style>