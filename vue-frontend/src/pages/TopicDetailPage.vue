<template>
  <div class="topic-detail-page">
    <div class="container" v-if="forumStore.currentTopic">
      <button @click="$router.back()" class="back-btn">返回论坛</button>
      
      <div class="topic-detail">
        <div class="topic-header">
          <h1>{{ forumStore.currentTopic.title }}</h1>
          <div class="topic-meta">
            <span class="author">作者: {{ forumStore.currentTopic.author_username }}</span>
            <span class="views">{{ forumStore.currentTopic.views }} 浏览</span>
            <span class="date">{{ formatDate(forumStore.currentTopic.created_at) }}</span>
          </div>
          <p class="topic-content">{{ forumStore.currentTopic.content }}</p>
        </div>
        
        <div class="posts-section">
          <h2>回复 ({{ forumStore.posts.length }})</h2>
          
          <div class="posts-list">
            <div v-for="post in forumStore.posts" :key="post.id" class="post-card">
              <div class="post-author">{{ post.author_username }}</div>
              <div class="post-content">{{ post.content }}</div>
              <div class="post-date">{{ formatDate(post.created_at) }}</div>
            </div>
            <div v-if="forumStore.posts.length === 0" class="empty-posts">
              <p>暂无回复，快来抢沙发吧！</p>
            </div>
          </div>
          
          <div v-if="authStore.isAuthenticated" class="reply-form">
            <textarea v-model="replyContent" placeholder="写下你的回复..." rows="3" class="reply-input"></textarea>
            <button @click="handleReply" class="btn btn-primary" :disabled="!replyContent.trim() || forumStore.loading">
              {{ forumStore.loading ? '发送中...' : '回复' }}
            </button>
          </div>
          <div v-else class="login-prompt">
            <router-link to="/login">登录后可以回复</router-link>
          </div>
        </div>
      </div>
    </div>
    
    <Loading :loading="forumStore.loading" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useForumStore } from '@/stores/forum'
import { useAuthStore } from '@/stores/auth'
import Loading from '@/components/Loading.vue'

const route = useRoute()
const forumStore = useForumStore()
const authStore = useAuthStore()
const replyContent = ref('')

const handleReply = async () => {
  if (!replyContent.value.trim()) return
  await forumStore.handleCreatePost(route.params.id, { content: replyContent.value })
  replyContent.value = ''
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  forumStore.fetchTopicDetail(route.params.id)
  forumStore.fetchPosts(route.params.id)
})
</script>

<style scoped>
.topic-detail-page {
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

.topic-detail {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.topic-header {
  margin-bottom: 32px;
}

.topic-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 16px 0;
}

.topic-meta {
  display: flex;
  gap: 24px;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 16px;
}

.topic-content {
  font-size: 16px;
  color: #4b5563;
  line-height: 1.8;
  margin: 0;
}

.posts-section {
  border-top: 1px solid #e5e7eb;
  padding-top: 32px;
}

.posts-section h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 24px 0;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.post-card {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
}

.post-author {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.post-content {
  font-size: 15px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 8px;
}

.post-date {
  font-size: 12px;
  color: #9ca3af;
}

.empty-posts {
  text-align: center;
  padding: 32px;
  color: #9ca3af;
}

.empty-posts p {
  margin: 0;
}

.reply-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.reply-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  resize: vertical;
  box-sizing: border-box;
}

.reply-input:focus {
  border-color: #3b82f6;
}

.btn {
  align-self: flex-end;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-prompt {
  text-align: center;
  padding: 24px;
  background: #eff6ff;
  border-radius: 8px;
}

.login-prompt a {
  color: #3b82f6;
  text-decoration: none;
}

.login-prompt a:hover {
  text-decoration: underline;
}
</style>
