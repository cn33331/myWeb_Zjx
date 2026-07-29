<template>
  <div class="notes-page">
    <div v-if="!selectedRepo" class="repo-select-page">
      <div class="container">
        <h1>笔记管理</h1>
        <p class="subtitle">本地仓库可上传/删除，远程仓库仅支持同步和查看</p>
        
        <div class="repo-section">
          <h2 class="section-title">📁 本地仓库</h2>
          <div class="repo-grid">
            <div 
              v-for="repo in localRepos" 
              :key="repo.id" 
              class="repo-card local"
              @click="selectRepository(repo)"
            >
              <div class="repo-icon">📝</div>
              <div class="repo-info">
                <h3>{{ repo.name }}</h3>
                <p class="repo-type-badge local-badge">本地仓库</p>
                <p class="repo-path">路径: {{ repo.local_path }}</p>
                <p class="repo-status" :class="repo.sync_status">
                  {{ repo.sync_status === 'synced' ? '✓ 已就绪' : '○ 待初始化' }}
                </p>
              </div>
              <div class="repo-actions">
                <button @click.stop="uploadNote(repo.id)" class="action-btn upload" :disabled="!isLoggedIn">
                  {{ isLoggedIn ? '上传' : '登录' }}
                </button>
                <button 
                  @click.stop="downloadRepo(repo)" 
                  class="action-btn download" 
                  :disabled="!isLoggedIn"
                  title="下载整个仓库"
                >
                  📦 下载全部
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="repo-section" v-if="remoteRepos.length > 0">
          <h2 class="section-title">☁️ 远程仓库</h2>
          <div class="repo-grid">
            <div 
              v-for="repo in remoteRepos" 
              :key="repo.id" 
              class="repo-card remote"
              @click="selectRepository(repo)"
            >
              <div class="repo-icon">🔗</div>
              <div class="repo-info">
                <h3>{{ repo.name }}</h3>
                <p class="repo-type-badge remote-badge">远程仓库</p>
                <p class="repo-url">{{ repo.repo_url }}</p>
                <p class="repo-branch">🌿 分支: {{ repo.branch || 'main' }}</p>
                <p class="repo-status" :class="repo.sync_status">
                  <span v-if="syncingRepos.includes(repo.id)" class="spinner"></span>
                  {{ syncingRepos.includes(repo.id) ? '同步中...' : repo.sync_status === 'synced' ? '✓ 已同步' : repo.sync_status === 'failed' ? '✗ 同步失败' : '○ 未同步' }}
                </p>
                <p v-if="repo.last_sync && !syncingRepos.includes(repo.id)" class="repo-time">最后同步: {{ formatTime(repo.last_sync) }}</p>
              </div>
              <div class="repo-actions">
                <button 
                  @click.stop="showBranchSelector(repo)" 
                  class="branch-btn"
                  :disabled="!isLoggedIn || syncingRepos.includes(repo.id)"
                  :title="!isLoggedIn ? '请先登录' : '切换分支'"
                >
                  🌿 {{ repo.branch || 'main' }}
                </button>
                <button 
                  @click.stop="syncRepo(repo.id)" 
                  class="sync-btn"
                  :disabled="syncingRepos.includes(repo.id)"
                >
                  <span v-if="syncingRepos.includes(repo.id)" class="spinner-small"></span>
                  {{ syncingRepos.includes(repo.id) ? '同步中' : '同步' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="remoteRepos.length === 0" class="add-remote-section">
          <button @click="showAddModal = true" class="btn">+ 添加远程仓库</button>
        </div>
      </div>
    </div>

    <div v-else class="vscode-layout">
      <div class="activity-bar">
        <div class="activity-icon active" @click="leftPanelOpen = !leftPanelOpen" title="文件树">📄</div>
        <div 
          v-if="selectedRepo.repo_type === 'remote'" 
          class="activity-icon" 
          :class="{ 'icon-spinning': syncingRepos.includes(selectedRepo.id) }"
          @click="syncRepo(selectedRepo.id)" 
          :title="syncingRepos.includes(selectedRepo.id) ? '同步中...' : '同步'"
        >
          <span v-if="syncingRepos.includes(selectedRepo.id)" class="spinner-small"></span>
          <span v-else>🔄</span>
        </div>
        <div v-if="selectedRepo.repo_type === 'local'" class="activity-icon" @click="uploadNote(selectedRepo.id)" title="上传">📤</div>
        <div class="activity-icon" @click="selectedRepo = null" title="返回">⬅️</div>
      </div>

      <transition name="panel">
        <div v-if="leftPanelOpen" class="sidebar-left">
          <div class="sidebar-header">
            <div class="header-info">
              <span class="header-title">{{ selectedRepo.name }}</span>
              <span class="repo-tag" :class="selectedRepo.repo_type">{{ selectedRepo.repo_type === 'local' ? '本地' : '远程' }}</span>
            </div>
            <span class="close-btn" @click="leftPanelOpen = false">×</span>
          </div>
          
          <div class="search-box">
            <input 
              v-model="searchQuery" 
              placeholder="搜索..." 
              @input="handleSearch"
            />
          </div>

          <div v-if="selectedRepo.repo_type === 'local' && isLoggedIn" class="toolbar">
            <button @click="uploadNote(selectedRepo.id)" class="toolbar-btn">📤 上传文件</button>
          </div>
          
          <div class="file-tree">
            <div 
              v-for="item in fileTree" 
              :key="item.name" 
            >
              <template v-if="item.is_file">
                <div 
                  class="tree-item-file"
                  :class="{ selected: currentNote?.file_path === item.file_path }"
                  @click="openNote(item)"
                >
                  <span class="file-icon">📄</span>
                  <span class="file-name">{{ item.name }}</span>
                  <span 
                    v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                    class="download-icon"
                    @click.stop="downloadFile(item)"
                    title="下载"
                  >⬇</span>
                  <span 
                    v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                    class="delete-icon"
                    @click.stop="deleteNote(item)"
                    title="删除"
                  >×</span>
                </div>
              </template>
              <template v-else>
                <div class="tree-item-dir">
                  <span class="dir-icon" @click="toggleExpand(item)">
                    {{ isExpanded(item) ? '▼' : '▶' }}
                  </span>
                  <span class="dir-icon-folder">{{ isExpanded(item) ? '📂' : '📁' }}</span>
                  <span class="dir-name">{{ item.name }}</span>
                </div>
                <template v-if="isExpanded(item)">
                  <div class="tree-children">
                    <template v-for="child in item.children" :key="child.name">
                      <template v-if="child.is_file">
                        <div 
                          class="tree-item-file"
                          :class="{ selected: currentNote?.file_path === child.file_path }"
                          @click="openNote(child)"
                        >
                          <span class="file-icon">📄</span>
                          <span class="file-name">{{ child.name }}</span>
                          <span 
                            v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                            class="download-icon"
                            @click.stop="downloadFile(child)"
                            title="下载"
                          >⬇</span>
                          <span 
                            v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                            class="delete-icon"
                            @click.stop="deleteNote(child)"
                            title="删除"
                          >×</span>
                        </div>
                      </template>
                      <template v-else>
                        <div class="tree-item-dir">
                          <span class="dir-icon" @click="toggleExpand(child)">
                            {{ isExpanded(child) ? '▼' : '▶' }}
                          </span>
                          <span class="dir-icon-folder">{{ isExpanded(child) ? '📂' : '📁' }}</span>
                          <span class="dir-name">{{ child.name }}</span>
                        </div>
                        <template v-if="isExpanded(child)">
                          <div class="tree-children">
                            <div 
                              v-for="sub in child.children" 
                              :key="sub.name"
                              class="tree-item-file"
                              :class="{ selected: currentNote?.file_path === sub.file_path }"
                              @click="openNote(sub)"
                            >
                              <span class="file-icon">📄</span>
                              <span class="file-name">{{ sub.name }}</span>
                              <span 
                                v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                                class="download-icon"
                                @click.stop="downloadFile(sub)"
                                title="下载"
                              >⬇</span>
                              <span 
                                v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                                class="delete-icon"
                                @click.stop="deleteNote(sub)"
                                title="删除"
                              >×</span>
                            </div>
                          </div>
                        </template>
                      </template>
                    </template>
                  </div>
                </template>
              </template>
            </div>
          </div>
        </div>
      </transition>

      <div class="content-area">
        <div v-if="!currentNote" class="empty-content">
          <div class="empty-icon">📝</div>
          <p>选择一个笔记开始阅读</p>
        </div>
        <div v-else class="note-view">
          <div class="note-header">
            <h1>{{ currentNote.file_name }}</h1>
            <div class="note-meta">
              <span>{{ formatTime(currentNote.last_modified) }}</span>
              <span>{{ formatSize(currentNote.size) }}</span>
              <span v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                    class="download-link" 
                    @click="downloadFile(currentNote)">
                ⬇ 下载
              </span>
              <span v-if="selectedRepo.repo_type === 'local' && isLoggedIn" 
                    class="delete-link" 
                    @click="deleteNote(currentNote)">
                🗑️ 删除
              </span>
            </div>
          </div>
          <div class="note-content markdown-body" v-html="renderedContent"></div>
        </div>
      </div>

      <transition name="panel-right">
        <div v-if="rightPanelOpen" class="sidebar-right">
          <div class="toc-header">
            <span>目录</span>
            <span class="close-btn" @click="rightPanelOpen = false">×</span>
          </div>
          <div v-if="noteToc.length === 0" class="empty-toc">
            <p>暂无目录</p>
          </div>
          <div v-else class="toc-list">
            <div 
              v-for="(item, index) in noteToc" 
              :key="index"
              class="toc-item"
              :class="'level-' + item.level"
              @click="scrollToHeading(item.slug)"
            >
              {{ item.title }}
            </div>
          </div>
        </div>
      </transition>

      <div class="right-toggle" @click="rightPanelOpen = !rightPanelOpen" :title="rightPanelOpen ? '收起目录' : '展开目录'">
        {{ rightPanelOpen ? '›' : '‹' }}
      </div>
    </div>

    <div v-if="showAddModal" class="modal" @click.self="showAddModal = false">
      <div class="modal-content">
        <h3>添加远程仓库</h3>
        <input v-model="repoUrl" placeholder="仓库地址 (如: git@gitee.com:zeng333/note.git)" />
        <input v-model="localPath" placeholder="本地路径 (如: /tmp/my-notes)" />
        <div class="modal-actions">
          <button @click="addRepo" class="btn primary">保存</button>
          <button @click="showAddModal = false" class="btn">取消</button>
        </div>
      </div>
    </div>

    <div v-if="showUploadModal" class="modal" @click.self="showUploadModal = false">
      <div class="modal-content">
        <h3>上传笔记文件</h3>
        <div class="upload-area" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
          <input ref="fileInput" type="file" accept=".md,.markdown,.txt" @change="handleFileSelect" style="display:none" />
          <div v-if="!uploadFile" class="upload-placeholder">
            <p>📄</p>
            <p>点击选择文件或拖拽到此处</p>
            <p class="hint">支持 .md, .markdown, .txt 格式</p>
          </div>
          <div v-else class="upload-preview">
            <p>📄 {{ uploadFile.name }}</p>
            <p class="hint">{{ formatSize(uploadFile.size) }}</p>
          </div>
        </div>
        <input v-model="uploadPath" placeholder="保存路径 (可选，如: work-note/)" class="path-input" />
        <div class="modal-actions">
          <button @click="doUpload" class="btn primary" :disabled="!uploadFile">上传</button>
          <button @click="showUploadModal = false" class="btn">取消</button>
        </div>
      </div>
    </div>

    <div v-if="showBranchModal" class="modal" @click.self="showBranchModal = false">
      <div class="modal-content">
        <h3>选择分支</h3>
        <p v-if="branchLoading">正在获取分支列表...</p>
        <div v-else-if="availableBranches.length > 0" class="branch-list">
          <div 
            v-for="branch in availableBranches" 
            :key="branch" 
            class="branch-item"
            :class="{ active: branch === currentBranch }"
            @click="selectBranch(branch)"
          >
            🌿 {{ branch }}
          </div>
        </div>
        <p v-else class="hint">未找到可用分支</p>
        <div class="modal-actions">
          <button @click="fetchBranches" class="btn">🔄 刷新分支</button>
          <button @click="showBranchModal = false" class="btn">关闭</button>
        </div>
      </div>
    </div>

    <div v-if="syncErrorModal" class="modal" @click.self="syncErrorModal = false">
      <div class="modal-content error-modal">
        <div class="error-icon">⚠️</div>
        <h3>同步失败</h3>
        <p class="error-repo">仓库: {{ syncErrorRepo }}</p>
        <div class="error-message">
          <p>{{ syncErrorMsg }}</p>
        </div>
        <div class="modal-actions">
          <button @click="syncErrorModal = false" class="btn primary">知道了</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted, nextTick } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { renderMarkdown, generateToc, renderAllMermaids } from '@/utils/markdown';
import '@/styles/markdown.css';
import 'katex/dist/katex.min.css';

// 全局 axios 拦截器：若携带的 token 已过期导致 401，则清除失效 token 并重试（作为匿名请求）
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      const originalRequest = error.config;
      // 已经重试过则不再重试
      if (originalRequest._retry) {
        return Promise.reject(error);
      }
      originalRequest._retry = true;
      // 清除本地失效的 token，避免影响后续请求
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        delete axios.defaults.headers.common['Authorization'];
        if (authStore && typeof authStore.clearTokens === 'function') {
          authStore.clearTokens();
        }
      }
      delete originalRequest.headers.Authorization;
      return axios(originalRequest);
    }
    return Promise.reject(error);
  }
);

const authStore = useAuthStore();

const repos = ref([]);
const selectedRepo = ref(null);
const currentNote = ref(null);
const noteContent = ref('');
const noteToc = ref([]);
const fileTree = ref([]);
const searchQuery = ref('');
const showAddModal = ref(false);
const showUploadModal = ref(false);
const showBranchModal = ref(false);
const repoUrl = ref('');
const localPath = ref('');
const uploadFile = ref(null);
const uploadPath = ref('');
const uploadingRepoId = ref(null);
const expandedDirs = ref(new Set());
const leftPanelOpen = ref(true);
const rightPanelOpen = ref(true);
const currentBranch = ref('main');
const availableBranches = ref([]);
const branchLoading = ref(false);
const syncingRepos = ref([]);
const syncErrorModal = ref(false);
const syncErrorMsg = ref('');
const syncErrorRepo = ref('');

const isLoggedIn = computed(() => authStore.isAuthenticated);

const localRepos = computed(() => repos.value.filter(r => r.repo_type === 'local'));
const remoteRepos = computed(() => repos.value.filter(r => r.repo_type === 'remote'));

watch(() => authStore.accessToken, (newToken) => {
  if (newToken) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }
}, { immediate: true });

const handleStorageChange = (e) => {
  if (e.key === 'access_token') {
    authStore.initFromStorage();
  }
};

onMounted(() => {
  window.addEventListener('storage', handleStorageChange);
});

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageChange);
});

const loadRepos = async () => {
  try {
    const res = await axios.get('/api/notes/repositories/');
    repos.value = res.data.results || res.data;
  } catch (e) {
    console.error('加载仓库失败:', e);
  }
};

const selectRepository = async (repo) => {
  selectedRepo.value = repo;
  expandedDirs.value = new Set();
  await loadFileTree(repo.id);
};

const loadFileTree = async (repoId) => {
  try {
    const res = await axios.get(`/api/notes/repositories/${repoId}/file-tree/`);
    fileTree.value = res.data;
    expandedDirs.value = new Set(fileTree.value.map(d => d.name));
  } catch (e) {
    console.error('加载文件树失败:', e);
  }
};

const isExpanded = (item) => {
  return expandedDirs.value.has(item.name);
};

const toggleExpand = (item) => {
  const newSet = new Set(expandedDirs.value);
  if (newSet.has(item.name)) {
    newSet.delete(item.name);
  } else {
    newSet.add(item.name);
  }
  expandedDirs.value = newSet;
};

const syncRepo = async (id) => {
  if (syncingRepos.value.includes(id)) return;
  
  syncingRepos.value = [...syncingRepos.value, id];
  try {
    const res = await axios.post(`/api/notes/repositories/${id}/sync/`);
    
    // 检查后端返回的结果
    if (Array.isArray(res.data)) {
      // 如果是数组格式（sync_notes 返回）
      const firstResult = res.data[0];
      if (firstResult && !firstResult.success) {
        throw new Error(firstResult.message || firstResult.stderr || '同步失败');
      }
    } else if (res.data && !res.data.success && res.data.sync_status === 'failed') {
      throw new Error(res.data.sync_message || '同步失败');
    }
    
    await loadRepos();
    if (selectedRepo.value?.id === id) {
      await loadFileTree(id);
    }
  } catch (e) {
    console.error('同步失败:', e);
    syncErrorRepo.value = repos.value.find(r => r.id === id)?.name || '未知仓库';
    syncErrorMsg.value = e.message || e.response?.data?.error || e.response?.data?.sync_message || '未知错误';
    syncErrorModal.value = true;
  } finally {
    syncingRepos.value = syncingRepos.value.filter(r => r !== id);
  }
};

const addRepo = async () => {
  if (!repoUrl.value || !localPath.value) {
    alert('请填写完整信息');
    return;
  }
  try {
    await axios.post('/api/notes/repositories/', {
      name: repoUrl.value.split('/').pop().replace('.git', ''),
      repo_type: 'remote',
      repo_url: repoUrl.value,
      local_path: localPath.value
    });
    showAddModal.value = false;
    repoUrl.value = '';
    localPath.value = '';
    await loadRepos();
  } catch (e) {
    console.error('添加失败:', e);
    alert('添加失败，请检查仓库地址是否正确');
  }
};

const openNote = async (note) => {
  if (!selectedRepo.value) return;
  currentNote.value = note;
  try {
    const res = await axios.get(`/api/notes/repositories/${selectedRepo.value.id}/note/${encodeURIComponent(note.file_path)}/`);
    noteContent.value = res.data.content || '';
    // 使用前端 generateToc 生成目录（更准确地匹配 marked 生成的 ID）
    noteToc.value = generateToc(noteContent.value);
  } catch (error) {
    console.error('加载笔记内容失败:', error);
    noteContent.value = '加载失败';
    noteToc.value = [];
  }
};

const uploadNote = (repoId) => {
  if (!isLoggedIn.value) {
    alert('请先登录后再上传文件');
    window.location.href = '/login';
    return;
  }
  uploadingRepoId.value = repoId;
  uploadFile.value = null;
  uploadPath.value = '';
  showUploadModal.value = true;
};

const handleFileSelect = (event) => {
  uploadFile.value = event.target.files[0];
};

const handleDrop = (event) => {
  const files = event.dataTransfer.files;
  if (files.length > 0) {
    uploadFile.value = files[0];
  }
};

const doUpload = async () => {
  if (!uploadFile.value) return;
  
  const formData = new FormData();
  formData.append('file', uploadFile.value);
  if (uploadPath.value) {
    const filePath = uploadPath.value.endsWith('/') 
      ? uploadPath.value + uploadFile.value.name 
      : uploadPath.value;
    formData.append('file_path', filePath);
  }
  
  try {
    const repoId = uploadingRepoId.value || selectedRepo.value?.id;
    const res = await axios.post(`/api/notes/repositories/${repoId}/upload/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    if (res.data.success) {
      alert('上传成功！');
      showUploadModal.value = false;
      uploadingRepoId.value = null;
      if (selectedRepo.value) {
        await loadFileTree(selectedRepo.value.id);
      }
    }
  } catch (e) {
    if (e.response?.status === 401) {
      alert('登录已过期，请重新登录！');
      authStore.clearTokens();
      window.location.href = '/login';
    } else {
      console.error('上传失败:', e);
      alert('上传失败: ' + (e.response?.data?.error || e.message));
    }
  }
};

const deleteNote = async (note) => {
  if (!isLoggedIn.value) {
    alert('请先登录后再删除文件');
    window.location.href = '/login';
    return;
  }
  
  if (!confirm(`确定要删除「${note.file_name}」吗？`)) return;
  
  try {
    await axios.post(`/api/notes/repositories/${selectedRepo.value.id}/delete/`, {
      file_path: note.file_path
    });
    
    if (currentNote.value?.file_path === note.file_path) {
      currentNote.value = null;
      noteContent.value = '';
      noteToc.value = [];
    }
    
    await loadFileTree(selectedRepo.value.id);
    alert('删除成功！');
  } catch (e) {
    if (e.response?.status === 401) {
      alert('登录已过期，请重新登录！');
      authStore.clearTokens();
      window.location.href = '/login';
    } else {
      console.error('删除失败:', e);
      alert('删除失败: ' + (e.response?.data?.error || e.message));
    }
  }
};

const downloadFile = async (note) => {
  if (!isLoggedIn.value) {
    alert('请先登录后再下载文件');
    window.location.href = '/login';
    return;
  }
  
  try {
    const repoId = selectedRepo.value?.id;
    const filePath = note.file_path;
    const response = await axios.get(`/api/notes/repositories/${repoId}/download-file/${encodeURIComponent(filePath)}/`, {
      responseType: 'blob'
    });
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.download = note.file_name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    if (e.response?.status === 401) {
      alert('登录已过期，请重新登录！');
      authStore.clearTokens();
      window.location.href = '/login';
    } else {
      console.error('下载失败:', e);
      alert('下载失败: ' + (e.response?.data?.error || e.message));
    }
  }
};

const downloadRepo = async (repo) => {
  if (!isLoggedIn.value) {
    alert('请先登录后再下载');
    window.location.href = '/login';
    return;
  }
  
  try {
    const response = await axios.get(`/api/notes/repositories/${repo.id}/download-repo/`, {
      responseType: 'blob'
    });
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.download = `${repo.name}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    if (e.response?.status === 401) {
      alert('登录已过期，请重新登录！');
      authStore.clearTokens();
      window.location.href = '/login';
    } else {
      console.error('下载失败:', e);
      alert('下载失败: ' + (e.response?.data?.error || e.message));
    }
  }
};

const showBranchSelector = async (repo) => {
  if (!isLoggedIn.value) {
    alert('请先登录后再切换分支！');
    window.location.href = '/login';
    return;
  }
  
  selectedRepo.value = repo;
  currentBranch.value = repo.branch || 'main';
  showBranchModal.value = true;
  await fetchBranches();
};

const fetchBranches = async () => {
  if (!selectedRepo.value) return;
  
  branchLoading.value = true;
  try {
    const res = await axios.get(`/api/notes/repositories/${selectedRepo.value.id}/branches/`);
    if (res.data.success && res.data.branches) {
      availableBranches.value = res.data.branches;
    } else {
      availableBranches.value = ['main', 'master'];
    }
  } catch (e) {
    console.error('获取分支失败:', e);
    availableBranches.value = ['main', 'master'];
  } finally {
    branchLoading.value = false;
  }
};

const selectBranch = async (branch) => {
  if (!selectedRepo.value) return;
  
  try {
    const res = await axios.post(`/api/notes/repositories/${selectedRepo.value.id}/update-branch/`, {
      branch: branch
    });
    
    if (res.data.success) {
      currentBranch.value = branch;
      const repo = selectedRepo.value;
      repo.branch = branch;
      
      const index = repos.value.findIndex(r => r.id === repo.id);
      if (index !== -1) {
        repos.value[index] = { ...repo, branch: branch };
      }
      
      showBranchModal.value = false;
      alert(`分支已切换到: ${branch}\n请点击同步以拉取该分支的内容`);
    }
  } catch (e) {
    console.error('更新分支失败:', e);
    alert('更新分支失败: ' + (e.response?.data?.error || e.message));
  }
};

const handleSearch = () => {
  if (selectedRepo.value) {
    loadFileTree(selectedRepo.value.id);
  }
};

const renderedContent = computed(() => {
  if (!noteContent.value) return '';
  return renderMarkdown(noteContent.value);
});

// 监听内容变化，渲染 Mermaid 图表
watch(renderedContent, async (newContent) => {
  if (newContent && currentNote.value) {
    await nextTick();
    const container = document.querySelector('.note-content');
    if (container) {
      await renderAllMermaids(container);
    }
  }
});

const scrollToHeading = (slug) => {
  const element = document.getElementById(slug);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    element.classList.add('highlighted');
    setTimeout(() => element.classList.remove('highlighted'), 1000);
  }
};

const formatTime = (timeStr) => {
  if (!timeStr) return '';
  const date = new Date(timeStr);
  return date.toLocaleString('zh-CN');
};

const formatSize = (bytes) => {
  if (!bytes || bytes < 0) return '0 B';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

onMounted(() => {
  authStore.initFromStorage();
  loadRepos();
});
</script>

<style scoped>
.notes-page { height: 100vh; display: flex; background: #f0f4fa; color: #1a1a1a; }

.repo-select-page { flex: 1; padding: 24px; overflow-y: auto; background: #f0f4fa; }
.container { max-width: 1200px; margin: 0 auto; }

.subtitle { color: #666666; margin-bottom: 24px; }

.repo-section { margin-bottom: 32px; }
.section-title { 
  font-size: 18px; 
  margin-bottom: 16px; 
  color: #1a1a1a;
  padding-bottom: 8px;
  border-bottom: 1px solid #e0e6ed;
}

.repo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 16px; }

.repo-card { 
  border: 1px solid #e0e6ed; 
  padding: 16px; 
  border-radius: 8px; 
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.repo-card:hover { border-color: #0078d4; box-shadow: 0 2px 8px rgba(0,120,212,0.12); }
.repo-card.local { border-left: 3px solid #107c10; }
.repo-card.remote { border-left: 3px solid #0078d4; }

.repo-icon { font-size: 32px; }
.repo-info { flex: 1; min-width: 0; }
.repo-info h3 { margin: 0 0 4px 0; color: #1a1a1a; font-size: 16px; }

.repo-type-badge {
  display: inline-block;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 10px;
  margin-bottom: 4px;
}
.local-badge { background: #dff6dd; color: #107c10; }
.remote-badge { background: #deecf9; color: #0078d4; }

.repo-url { font-size: 12px; color: #666666; margin: 0 0 4px 0; word-break: break-all; }
.repo-path { font-size: 12px; color: #666666; margin: 0 0 4px 0; word-break: break-all; }
.repo-status { 
  font-size: 12px; 
  padding: 2px 6px; 
  border-radius: 2px;
  display: inline-block;
}
.repo-status.synced { background: #dff6dd; color: #107c10; }
.repo-status.failed { background: #fde7e9; color: #d13438; }
.repo-status.idle { background: #fff4ce; color: #ca5010; }
.repo-time { font-size: 11px; color: #999999; margin: 4px 0 0 0; }

.repo-actions { display: flex; gap: 8px; }
.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}
.action-btn.upload {
  background: #0078d4;
  color: #fff;
}
.action-btn.upload:hover { background: #106ebe; }

.action-btn.download {
  background: #107c10;
  color: #fff;
}
.action-btn.download:hover { background: #0b6b0f; }

.action-btn:disabled {
  background: #e0e6ed;
  color: #999999;
  cursor: not-allowed;
}

.sync-btn { 
  padding: 6px 12px; 
  background: #f5f5f5; 
  color: #333333; 
  border: 1px solid #e0e6ed;
  cursor: pointer; 
  border-radius: 4px;
  font-size: 12px;
  display: inline-flex;
  align-items: center;
}
.sync-btn:hover:not(:disabled) { background: #e8eaed; border-color: #0078d4; }
.sync-btn:disabled { 
  opacity: 0.6; 
  cursor: not-allowed;
  background: #f5f5f5;
}

.add-remote-section { margin-top: 24px; }

.btn { 
  padding: 8px 16px; 
  background: #0078d4; 
  color: #fff; 
  border: none; 
  cursor: pointer; 
  border-radius: 4px;
  font-size: 13px;
  transition: background 0.2s;
}
.btn:hover { background: #106ebe; }
.btn.primary { background: #0078d4; }
.btn.primary:hover { background: #106ebe; }
.btn:disabled { background: #e0e6ed; color: #999999; cursor: not-allowed; }

.empty-state { margin-top: 40px; text-align: center; color: #666666; }

.vscode-layout { 
  display: flex; 
  height: 100%; 
  width: 100%; 
  background: #f0f4fa;
}

.activity-bar {
  width: 48px;
  background: #e8ecf1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 12px;
  gap: 8px;
  border-right: 1px solid #e0e6ed;
}

.activity-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  cursor: pointer;
  color: #666666;
  border-left: 2px solid transparent;
  transition: all 0.2s;
}

.activity-icon:hover {
  color: #1a1a1a;
  background: #dbe3ee;
}

.activity-icon.active {
  color: #0078d4;
  border-left-color: #0078d4;
  background: #ffffff;
}

.icon-spinning {
  cursor: progress !important;
  pointer-events: none;
}

.sidebar-left {
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #e0e6ed;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e0e6ed;
  background: #ffffff;
}

.header-info { display: flex; align-items: center; gap: 8px; }

.header-title {
  font-size: 11px;
  font-weight: 600;
  color: #333333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.repo-tag {
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 3px;
}
.repo-tag.local { background: #dff6dd; color: #107c10; }
.repo-tag.remote { background: #deecf9; color: #0078d4; }

.close-btn {
  cursor: pointer;
  color: #999999;
  font-size: 18px;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2px;
}

.close-btn:hover {
  background: #e8eaed;
  color: #333333;
}

.search-box {
  padding: 8px;
  border-bottom: 1px solid #e0e6ed;
  background: #f8fafb;
}

.search-box input {
  width: 100%;
  padding: 5px 10px;
  background: #ffffff;
  border: 1px solid #e0e6ed;
  color: #1a1a1a;
  border-radius: 4px;
  font-size: 13px;
  box-sizing: border-box;
  outline: none;
}

.search-box input:focus {
  border-color: #0078d4;
  box-shadow: 0 0 0 2px rgba(0,120,212,0.15);
}

.search-box input::placeholder {
  color: #999999;
}

.toolbar {
  padding: 8px;
  border-bottom: 1px solid #e0e6ed;
  background: #f8fafb;
}

.toolbar-btn {
  width: 100%;
  padding: 6px 12px;
  background: #0078d4;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.toolbar-btn:hover { background: #106ebe; }

.file-tree { 
  flex: 1; 
  overflow-y: auto; 
  padding: 4px 0;
  background: #ffffff;
}

.tree-item-file { 
  display: flex; 
  align-items: center; 
  gap: 4px; 
  padding: 3px 8px 3px 20px; 
  cursor: pointer;
  font-size: 13px;
  color: #333333;
  line-height: 1.4;
}

.tree-item-file:hover { 
  background: #f0f4fa; 
}

.tree-item-file.selected { 
  background: #e5f1fb; 
  color: #0078d4; 
  font-weight: 500;
}

.file-icon { font-size: 14px; width: 16px; text-align: center; }
.file-name { 
  flex: 1; 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis;
}

.delete-icon {
  opacity: 0;
  color: #d13438;
  font-size: 14px;
  width: 16px;
  text-align: center;
  transition: opacity 0.2s;
}

.download-icon {
  opacity: 0;
  color: #0078d4;
  font-size: 12px;
  width: 16px;
  text-align: center;
  transition: opacity 0.2s;
}

.tree-item-file:hover .delete-icon,
.tree-item-file:hover .download-icon {
  opacity: 1;
}

.delete-icon:hover {
  color: #a4262c;
}

.download-icon:hover {
  color: #106ebe;
}

.tree-item-dir { 
  display: flex; 
  align-items: center; 
  gap: 2px; 
  padding: 3px 8px; 
  cursor: pointer;
  font-size: 13px;
  color: #333333;
  line-height: 1.4;
}

.tree-item-dir:hover { 
  background: #f0f4fa; 
}

.dir-icon { 
  font-size: 8px; 
  color: #999999;
  width: 12px;
  text-align: center;
  transition: transform 0.15s;
}

.dir-icon-folder {
  font-size: 14px;
  width: 16px;
  text-align: center;
}

.dir-name { 
  flex: 1; 
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tree-children { 
  border-left: 1px solid #e0e6ed;
  margin-left: 8px;
  padding-left: 4px;
}

.content-area { 
  flex: 1; 
  background: #ffffff; 
  overflow-y: auto;
  min-width: 0;
}

.empty-content { 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
  height: 100%; 
  color: #999999;
}

.empty-icon { font-size: 64px; margin-bottom: 16px; opacity: 0.5; }

.note-view { padding: 24px 32px; max-width: 900px; margin: 0 auto; }

.note-header { 
  margin-bottom: 20px; 
  padding-bottom: 16px; 
  border-bottom: 1px solid #e0e6ed; 
}

.note-header h1 { 
  margin: 0; 
  font-size: 22px;
  color: #1a1a1a;
}

.note-meta { 
  display: flex; 
  gap: 16px; 
  margin-top: 8px; 
  font-size: 12px; 
  color: #666666;
  align-items: center;
}

.download-link {
  color: #0078d4;
  cursor: pointer;
}

.download-link:hover {
  color: #106ebe;
  text-decoration: underline;
}

.delete-link {
  color: #d13438;
  cursor: pointer;
}

.delete-link:hover {
  color: #a4262c;
  text-decoration: underline;
}

.sidebar-right {
  width: 220px;
  background: #ffffff;
  border-left: 1px solid #e0e6ed;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.toc-header {
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e0e6ed;
  background: #ffffff;
  font-size: 11px;
  font-weight: 600;
  color: #333333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.empty-toc { padding: 16px; text-align: center; color: #999999; font-size: 13px; }

.toc-list { 
  flex: 1; 
  overflow-y: auto; 
  padding: 8px 0; 
}

.toc-item { 
  padding: 4px 12px; 
  cursor: pointer;
  font-size: 13px;
  border-radius: 2px;
  color: #333333;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.toc-item:hover { 
  background: #f0f4fa; 
  color: #0078d4;
}

.toc-item.level-1 { font-weight: 600; padding-left: 12px; }
.toc-item.level-2 { padding-left: 28px; }
.toc-item.level-3 { padding-left: 44px; }
.toc-item.level-4 { padding-left: 60px; }
.toc-item.level-5 { padding-left: 76px; }
.toc-item.level-6 { padding-left: 92px; }

.right-toggle {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 40px;
  background: #e8ecf1;
  color: #666666;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 0 4px 4px 0;
  font-size: 12px;
  z-index: 100;
  transition: all 0.2s;
  border: 1px solid #e0e6ed;
  border-right: none;
}

.right-toggle:hover {
  background: #0078d4;
  color: #ffffff;
}

.highlighted { 
  animation: highlight 1s ease; 
  background: #fff4ce; 
  padding: 4px 8px; 
  border-radius: 4px;
}

@keyframes highlight {
  0% { background: #fff4ce; }
  100% { background: transparent; }
}

.modal { 
  position: fixed; 
  top: 0; 
  left: 0; 
  right: 0; 
  bottom: 0; 
  background: rgba(0,0,0,0.4); 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  z-index: 1000; 
}

.modal-content { 
  background: #ffffff; 
  padding: 24px; 
  border-radius: 8px; 
  width: 90%; 
  max-width: 450px;
  border: 1px solid #e0e6ed;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
}

.modal-content h3 {
  margin: 0 0 16px 0;
  color: #1a1a1a;
}

.modal-content input { 
  width: 100%; 
  padding: 8px 12px; 
  margin: 8px 0; 
  background: #ffffff;
  border: 1px solid #e0e6ed; 
  color: #1a1a1a;
  border-radius: 4px; 
  box-sizing: border-box;
  outline: none;
}

.modal-content input:focus {
  border-color: #0078d4;
  box-shadow: 0 0 0 2px rgba(0,120,212,0.15);
}

.path-input {
  margin-top: 12px !important;
}

.modal-actions { 
  display: flex; 
  justify-content: flex-end; 
  gap: 8px; 
  margin-top: 16px; 
}

.upload-area {
  border: 2px dashed #e0e6ed;
  border-radius: 6px;
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
  margin: 16px 0;
}

.upload-area:hover {
  border-color: #0078d4;
  background: #f8fafb;
}

.upload-placeholder p {
  margin: 8px 0;
  color: #666666;
}

.upload-placeholder p:first-child {
  font-size: 48px;
}

.upload-placeholder .hint {
  font-size: 12px;
  color: #999999;
}

.upload-preview p {
  margin: 8px 0;
  color: #1a1a1a;
}

.upload-preview .hint {
  font-size: 12px;
  color: #999999;
}

.panel-enter-active,
.panel-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}

.panel-enter-from,
.panel-leave-to {
  width: 0;
  opacity: 0;
}

.panel-right-enter-active,
.panel-right-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}

.panel-right-enter-from,
.panel-right-leave-to {
  width: 0;
  opacity: 0;
}

.repo-branch {
  font-size: 12px;
  color: #ca5010;
  margin: 0 0 4px 0;
}

.branch-btn {
  padding: 6px 12px;
  background: #f5f5f5;
  color: #ca5010;
  border: 1px solid #e0e6ed;
  cursor: pointer;
  border-radius: 4px;
  font-size: 12px;
  transition: all 0.2s;
}

.branch-btn:hover:not(:disabled) {
  background: #fff4ce;
  border-color: #ca5010;
}

.branch-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid #e0e6ed;
  border-top-color: #0078d4;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 6px;
  vertical-align: middle;
}

.spinner-small {
  display: inline-block;
  width: 10px;
  height: 10px;
  border: 1.5px solid #e0e6ed;
  border-top-color: #0078d4;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 4px;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.branch-list {
  max-height: 300px;
  overflow-y: auto;
  margin: 12px 0;
}

.branch-item {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
  color: #333333;
  font-size: 14px;
}

.branch-item:hover {
  background: #f0f4fa;
}

.branch-item.active {
  background: #deecf9;
  color: #0078d4;
  font-weight: 600;
}

.hint {
  font-size: 13px;
  color: #666666;
  margin: 8px 0;
}

.error-modal {
  text-align: center;
  border-left: 4px solid #d13438;
}

.error-icon {
  font-size: 48px;
  margin: 0 0 16px 0;
}

.error-modal h3 {
  color: #d13438 !important;
  margin: 0 0 12px 0 !important;
}

.error-repo {
  color: #666666;
  font-size: 13px;
  margin: 0 0 16px 0 !important;
}

.error-message {
  background: #f8fafb;
  border: 1px solid #e0e6ed;
  border-radius: 4px;
  padding: 12px;
  margin: 0 0 16px 0 !important;
  text-align: left;
  max-height: 200px;
  overflow-y: auto;
}

.error-message p {
  color: #333333;
  font-size: 13px;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}
</style>
