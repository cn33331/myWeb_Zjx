<template>
  <div class="tool-card" @click="$router.push(`/store/${tool.id}`)">
    <div class="tool-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.2s;
  cursor: pointer;
}

.tool-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.tool-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.tool-icon svg {
  width: 28px;
  height: 28px;
}

.tool-info {
  flex: 1;
  min-width: 0;
}

.tool-name {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.tool-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.tool-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #9ca3af;
}

.tool-actions {
  flex-shrink: 0;
}

.download-btn {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
  color: #3b82f6;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.download-btn:hover {
  background: #eff6ff;
  border-color: #3b82f6;
}

.download-btn svg {
  width: 18px;
  height: 18px;
}
</style>
