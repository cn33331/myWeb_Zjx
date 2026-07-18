<template>
  <div class="transfer-page">
    <div class="container">
      <div class="page-header">
        <h1>临时中转站</h1>
        <p class="page-subtitle">文件传输导航与记录管理</p>
      </div>

      <section class="platform-links">
        <h2>快速导航</h2>
        <div class="platform-grid">
          <a href="https://www.airportal.cn/" target="_blank" class="platform-card airportal">
            <div class="platform-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2v20M2 12h20" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </div>
            <div class="platform-info">
              <h3>AirPortal 空投</h3>
              <p>免登录临时文件传输</p>
            </div>
            <div class="platform-arrow">→</div>
          </a>

          <a href="https://www.wenshushu.cn/" target="_blank" class="platform-card wenshushu">
            <div class="platform-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <polyline points="10 9 9 9 8 9" />
              </svg>
            </div>
            <div class="platform-info">
              <h3>文叔叔</h3>
              <p>大文件临时传输服务</p>
            </div>
            <div class="platform-arrow">→</div>
          </a>
        </div>
      </section>

      <section class="records-section">
        <div class="section-header">
          <h2>传输记录</h2>
          <button @click="showForm = !showForm" class="btn btn-primary">
            {{ showForm ? '取消' : '添加记录' }}
          </button>
        </div>

        <div v-if="showForm" class="record-form">
          <form @submit.prevent="addRecord">
            <div class="form-row">
              <div class="form-group">
                <label>平台</label>
                <select v-model="newRecord.platform" required class="form-select">
                  <option value="airportal">AirPortal 空投</option>
                  <option value="wenshushu">文叔叔</option>
                </select>
              </div>
              <div class="form-group">
                <label>取件码</label>
                <input type="text" v-model="newRecord.code" placeholder="输入取件码" class="form-input" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>取件链接</label>
                <input type="text" v-model="newRecord.link" placeholder="输入取件链接" class="form-input" />
              </div>
              <div class="form-group">
                <label>文件名</label>
                <input type="text" v-model="newRecord.file_name" placeholder="文件名" class="form-input" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>文件大小</label>
                <input type="text" v-model="newRecord.file_size" placeholder="如: 100MB" class="form-input" />
              </div>
            </div>
            <div class="form-group">
              <label>备注</label>
              <textarea v-model="newRecord.notes" placeholder="添加备注信息..." class="form-textarea"></textarea>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn btn-primary">保存记录</button>
              <button type="button" @click="showForm = false" class="btn btn-outline">取消</button>
            </div>
          </form>
        </div>

        <div class="records-list">
          <div v-for="record in records" :key="record.id" class="record-card">
            <div class="record-header">
              <div class="record-platform" :class="record.platform">
                {{ record.platform_name }}
              </div>
              <div class="record-actions">
                <button @click="deleteRecord(record.id)" class="action-btn delete-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="record-content">
              <div v-if="record.code" class="record-item">
                <span class="label">取件码</span>
                <span class="value">{{ record.code }}</span>
              </div>
              <div v-if="record.link" class="record-item">
                <span class="label">链接</span>
                <a :href="record.link" target="_blank" class="value link">{{ record.link }}</a>
              </div>
              <div v-if="record.file_name" class="record-item">
                <span class="label">文件名</span>
                <span class="value">{{ record.file_name }}</span>
              </div>
              <div v-if="record.file_size" class="record-item">
                <span class="label">大小</span>
                <span class="value">{{ record.file_size }}</span>
              </div>
              <div v-if="record.notes" class="record-item">
                <span class="label">备注</span>
                <span class="value">{{ record.notes }}</span>
              </div>
            </div>
            <div class="record-time">
              {{ formatDate(record.created_at) }}
            </div>
          </div>

          <div v-if="records.length === 0" class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2v20M2 12h20" />
              <circle cx="12" cy="12" r="3" />
            </svg>
            <p>暂无传输记录</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTransferRecords, createTransferRecord, deleteTransferRecord } from '@/api/transfer'

const records = ref([])
const showForm = ref(false)
const newRecord = ref({
  platform: 'airportal',
  code: '',
  link: '',
  file_name: '',
  file_size: '',
  notes: ''
})

const fetchRecords = async () => {
  try {
    const response = await getTransferRecords()
    records.value = response.data.results || response.data
  } catch (error) {
    console.error('获取记录失败:', error)
  }
}

const addRecord = async () => {
  try {
    await createTransferRecord(newRecord.value)
    showForm.value = false
    newRecord.value = {
      platform: 'airportal',
      code: '',
      link: '',
      file_name: '',
      file_size: '',
      notes: ''
    }
    fetchRecords()
  } catch (error) {
    console.error('添加记录失败:', error)
  }
}

const deleteRecord = async (id) => {
  if (confirm('确定要删除这条记录吗？')) {
    try {
      await deleteTransferRecord(id)
      fetchRecords()
    } catch (error) {
      console.error('删除记录失败:', error)
    }
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.transfer-page {
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
  text-align: center;
  margin-bottom: 48px;
}

.page-header h1 {
  font-size: 32px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #666666;
  margin: 0;
}

.platform-links {
  margin-bottom: 48px;
}

.platform-links h2 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 20px 0;
}

.platform-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.platform-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  text-decoration: none;
  color: #1a1a1a;
  border: 1px solid #e0e0e0;
  transition: all 0.2s;
}

.platform-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.platform-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.platform-card.airportal .platform-icon {
  background: #e3f2fd;
  color: #1976d2;
}

.platform-card.wenshushu .platform-icon {
  background: #fce4ec;
  color: #c2185b;
}

.platform-icon svg {
  width: 24px;
  height: 24px;
}

.platform-info {
  flex: 1;
}

.platform-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.platform-info p {
  font-size: 13px;
  color: #666666;
  margin: 0;
}

.platform-arrow {
  font-size: 20px;
  color: #999999;
}

.records-section {
  background: #ffffff;
  border-radius: 8px;
  padding: 24px;
  border: 1px solid #e0e0e0;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.section-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0;
}

.btn {
  padding: 8px 18px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
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
  border-color: #1a1a1a;
  color: #1a1a1a;
}

.record-form {
  background: #fafafa;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #444444;
  margin-bottom: 6px;
}

.form-input,
.form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  background: #ffffff;
}

.form-input:focus,
.form-select:focus {
  border-color: #1a1a1a;
}

.form-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  background: #ffffff;
  resize: vertical;
  min-height: 80px;
}

.form-textarea:focus {
  border-color: #1a1a1a;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 20px;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.record-card {
  background: #fafafa;
  border-radius: 4px;
  padding: 16px;
  border: 1px solid #e0e0e0;
}

.record-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.record-platform {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.record-platform.airportal {
  background: #e3f2fd;
  color: #1976d2;
}

.record-platform.wenshushu {
  background: #fce4ec;
  color: #c2185b;
}

.record-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.delete-btn {
  color: #e53935;
}

.delete-btn:hover {
  background: #ffebee;
}

.record-content {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 12px;
}

.record-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.record-item .label {
  font-size: 12px;
  color: #999999;
}

.record-item .value {
  font-size: 14px;
  color: #1a1a1a;
  font-weight: 500;
}

.record-item .value.link {
  color: #1976d2;
  text-decoration: none;
}

.record-item .value.link:hover {
  text-decoration: underline;
}

.record-time {
  font-size: 12px;
  color: #999999;
}

.empty-state {
  background: #fafafa;
  border-radius: 4px;
  padding: 40px;
  text-align: center;
  color: #999999;
}

.empty-state svg {
  width: 40px;
  height: 40px;
  margin-bottom: 12px;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}
</style>
