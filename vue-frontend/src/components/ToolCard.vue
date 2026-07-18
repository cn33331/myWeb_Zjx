<template>
  <div class="tool-card" @click="$router.push(`/store/${tool.id}`)">
    <div class="tool-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M4 7h16M4 17h16M10 12h4M4 12h2M18 12h2" />
      </svg>
    </div>
    <div class="tool-info">
      <h3 class="tool-name">{{ tool.name }}</h3>
      <p class="tool-description">{{ tool.description }}</p>
      <div class="tool-meta">
        <span class="version">v{{ tool.version }}</span>
        <span class="downloads">{{ tool.downloads }} 下载</span>
        <span class="date">{{ formatDate(tool.upload_date) }}</span>
      </div>
    </div>
    <div class="tool-actions">
      <button @click.stop="handleDownload" class="download-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useStoreStore } from '@/stores/store'

const props = defineProps({
  tool: {
    type: Object,
    required: true
  }
})

const storeStore = useStoreStore()

const handleDownload = () => {
  storeStore.handleDownload(props.tool.id)
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.tool-card {
  background: #ffffff;
  border-radius: 4px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  border: 1px solid #e0e0e0;
  transition: all 0.2s;
  cursor: pointer;
}

.tool-card:hover {
  border-color: #1a1a1a;
  background: #fafafa;
}

.tool-icon {
  width: 48px;
  height: 48px;
  background: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666666;
  flex-shrink: 0;
}

.tool-icon svg {
  width: 22px;
  height: 22px;
}

.tool-info {
  flex: 1;
  min-width: 0;
}

.tool-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 6px 0;
}

.tool-description {
  font-size: 13px;
  color: #666666;
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

.tool-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #999999;
}

.tool-actions {
  flex-shrink: 0;
}

.download-btn {
  width: 36px;
  height: 36px;
  border-radius: 4px;
  border: 1px solid #e0e0e0;
  background: #ffffff;
  color: #666666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.download-btn:hover {
  border-color: #1a1a1a;
  color: #1a1a1a;
}

.download-btn svg {
  width: 16px;
  height: 16px;
}
</style>