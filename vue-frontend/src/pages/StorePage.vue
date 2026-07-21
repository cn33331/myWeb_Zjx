<template>
  <div class="store-page">
    <div class="container">
      <div class="page-header">
        <h1>工具仓库</h1>
        <div class="search-bar">
          <input type="text" v-model="searchQuery" placeholder="搜索工具..." class="search-input" />
        </div>
      </div>
      
      <div class="tools-list">
        <ToolCard 
          v-for="tool in filteredTools" 
          :key="tool.id" 
          :tool="tool" 
        />
        <div v-if="filteredTools.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          <p>暂无工具，快来上传第一个吧！</p>
        </div>
      </div>
    </div>
    <Loading :loading="storeStore.loading" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useStoreStore } from '@/stores/store'
import ToolCard from '@/components/ToolCard.vue'
import Loading from '@/components/Loading.vue'

const storeStore = useStoreStore()
const searchQuery = ref('')

const filteredTools = computed(() => {
  if (!searchQuery.value) return storeStore.tools
  const query = searchQuery.value.toLowerCase()
  return storeStore.tools.filter(tool => 
    tool.name.toLowerCase().includes(query) ||
    tool.description.toLowerCase().includes(query)
  )
})

onMounted(() => {
  storeStore.fetchTools()
})
</script>

<style scoped>
.store-page {
  min-height: calc(100vh - 80px);
  background: #f5f5f5;
  padding: 48px 0;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 24px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.search-bar {
  flex: 0 0 280px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  background: #ffffff;
}

.search-input:focus {
  border-color: #1a1a1a;
}

.search-input::placeholder {
  color: #999999;
}

.tools-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state {
  background: #ffffff;
  border-radius: 4px;
  padding: 60px;
  text-align: center;
  color: #999999;
  border: 1px solid #e0e0e0;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0;
  font-size: 15px;
}
</style>