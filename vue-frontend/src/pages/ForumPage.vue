<template>
  <div class="forum-page">
    <div class="container">
      <div class="page-header">
        <h1>社区论坛</h1>
        <router-link to="/forum/new" class="btn btn-primary">发布话题</router-link>
      </div>
      
      <div class="topics-list">
        <TopicCard 
          v-for="topic in forumStore.topics" 
          :key="topic.id" 
          :topic="topic" 
        />
        <div v-if="forumStore.topics.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </svg>
          <p>暂无话题，快来发布第一个吧！</p>
        </div>
      </div>
    </div>
    <Loading :loading="forumStore.loading" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForumStore } from '@/stores/forum'
import TopicCard from '@/components/TopicCard.vue'
import Loading from '@/components/Loading.vue'

const forumStore = useForumStore()

onMounted(() => {
  forumStore.fetchTopics()
})
</script>

<style scoped>
.forum-page {
  min-height: calc(100vh - 80px);
  background: #f3f4f6;
  padding: 40px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
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

.topics-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  background: white;
  border-radius: 12px;
  padding: 60px;
  text-align: center;
  color: #9ca3af;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
}
</style>
