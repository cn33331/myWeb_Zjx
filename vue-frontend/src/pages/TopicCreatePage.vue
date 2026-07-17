<template>
  <div class="create-page">
    <div class="container">
      <button @click="$router.back()" class="back-btn">返回论坛</button>
      
      <div class="create-form">
        <h1>发布话题</h1>
        <form @submit.prevent="handleSubmit" class="form">
          <div class="form-group">
            <label>话题标题</label>
            <input type="text" v-model="formData.title" required class="form-input" placeholder="输入话题标题" />
          </div>
          
          <div class="form-group">
            <label>话题内容</label>
            <textarea v-model="formData.content" required class="form-textarea" placeholder="描述您的话题..." rows="6"></textarea>
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="forumStore.loading">
            {{ forumStore.loading ? '发布中...' : '发布话题' }}
          </button>
        </form>
      </div>
    </div>
    <Loading :loading="forumStore.loading" />
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useForumStore } from '@/stores/forum'
import Loading from '@/components/Loading.vue'

const forumStore = useForumStore()

const formData = reactive({
  title: '',
  content: ''
})

const handleSubmit = async () => {
  await forumStore.handleCreateTopic(formData)
  window.location.href = '/forum'
}
</script>

<style scoped>
.create-page {
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

.create-form {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.create-form h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 32px 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #3b82f6;
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
  resize: vertical;
}

.form-textarea:focus {
  border-color: #3b82f6;
}

.btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-end;
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
</style>
