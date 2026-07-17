<template>
  <div class="topic-card" @click="$router.push(`/forum/${topic.id}`)">
    <div class="topic-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="16" x2="12" y2="12" />
        <line x1="12" y1="8" x2="12.01" y2="8" />
      </svg>
    </div>
    <div class="topic-info">
      <h3 class="topic-title">{{ topic.title }}</h3>
      <p class="topic-content">{{ topic.content }}</p>
      <div class="topic-meta">
        <span class="author">作者: {{ topic.author_username }}</span>
        <span class="views">{{ topic.views }} 浏览</span>
        <span class="posts">{{ topic.post_count }} 回复</span>
        <span class="date">{{ formatDate(topic.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  topic: {
    type: Object,
    required: true
  }
})

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}
</script>

<style scoped>
.topic-card {
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

.topic-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.topic-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.topic-icon svg {
  width: 24px;
  height: 24px;
}

.topic-info {
  flex: 1;
  min-width: 0;
}

.topic-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.topic-content {
  font-size: 14px;
  color: #6b7280;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.topic-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #9ca3af;
}
</style>
