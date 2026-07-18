<template>
  <div class="upload-page">
    <div class="container">
      <button @click="$router.back()" class="back-btn">返回商店</button>
      
      <div class="upload-form">
        <h1>上传工具</h1>
        <form @submit.prevent="handleSubmit" class="form">
          <div class="form-group">
            <label>工具名称</label>
            <input type="text" v-model="formData.name" required class="form-input" placeholder="输入工具名称" />
          </div>
          
          <div class="form-group">
            <label>版本号</label>
            <input type="text" v-model="formData.version" required class="form-input" placeholder="例如：1.0.0" />
          </div>
          
          <div class="form-group">
            <label>工具描述</label>
            <textarea v-model="formData.description" required class="form-textarea" placeholder="描述您的工具功能..." rows="4"></textarea>
          </div>
          
          <div class="form-group">
            <label>工具文件</label>
            <input type="file" @change="handleFileSelect" required class="form-file" accept=".zip,.tar,.tar.gz" />
            <span v-if="selectedFile" class="file-name">{{ selectedFile.name }}</span>
          </div>
          
          <button type="submit" class="btn btn-primary" :disabled="storeStore.loading">
            {{ storeStore.loading ? '上传中...' : '上传工具' }}
          </button>
        </form>
      </div>
    </div>
    <Loading :loading="storeStore.loading" />
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useStoreStore } from '@/stores/store'
import Loading from '@/components/Loading.vue'

const storeStore = useStoreStore()
const selectedFile = ref(null)

const formData = reactive({
  name: '',
  version: '',
  description: ''
})

const handleFileSelect = (event) => {
  selectedFile.value = event.target.files[0]
}

const handleSubmit = async () => {
  const data = new FormData()
  data.append('name', formData.name)
  data.append('version', formData.version)
  data.append('description', formData.description)
  data.append('file', selectedFile.value)
  
  await storeStore.handleUpload(data)
  window.location.href = '/store'
}
</script>

<style scoped>
.upload-page {
  min-height: calc(100vh - 80px);
  background: #f5f5f5;
  padding: 48px 0;
}

.container {
  max-width: 550px;
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

.upload-form {
  background: #ffffff;
  border-radius: 4px;
  padding: 40px 32px;
  border: 1px solid #e0e0e0;
}

.upload-form h1 {
  font-size: 24px;
  font-weight: 600;
  color: #1a1a1a;
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
  color: #444444;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
  background: #ffffff;
}

.form-input:focus {
  border-color: #1a1a1a;
}

.form-input::placeholder {
  color: #999999;
}

.form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
  resize: vertical;
  background: #ffffff;
}

.form-textarea:focus {
  border-color: #1a1a1a;
}

.form-textarea::placeholder {
  color: #999999;
}

.form-file {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  background: #ffffff;
}

.form-file:focus {
  border-color: #1a1a1a;
}

.file-name {
  display: block;
  font-size: 14px;
  color: #444444;
  margin-top: 8px;
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

.btn-primary:hover:not(:disabled) {
  background: #333333;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>