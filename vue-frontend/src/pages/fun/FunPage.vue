<template>
  <div class="fun-page">
    <div class="container">
      <div class="page-head">
        <h1>趣味</h1>
        <p>一些有趣的、无厘头的小页面</p>
      </div>

      <div v-if="loading" class="tip">加载中…</div>
      <div v-else-if="!pages.length" class="tip">还没有页面，去 public/fun/ 放一个吧</div>

      <div v-else class="grid">
        <a
          v-for="page in pages"
          :key="page.id"
          :href="page.path"
          target="_blank"
          rel="noopener"
          class="card"
        >
          <div class="icon">{{ page.icon || '✨' }}</div>
          <h3>{{ page.title }}</h3>
          <p>{{ page.desc }}</p>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 趣味模块汇总页。
 *
 * 读取 public/fun-pages/manifest.json 中的页面清单，渲染为卡片列表。
 * 点击卡片在新标签页打开对应的静态 HTML 页面。
 * 新增趣味页只需：放入 public/fun-pages/ 并在 manifest.json 添加一条记录。
 *
 * 注意：静态目录名不能与 SPA 路由同名（路由为 /fun，故目录用 fun-pages），
 * 否则 nginx 会把 /fun 当成目录请求而返回 301/403。
 */
import { onMounted, ref } from 'vue'

const pages = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('/fun-pages/manifest.json')
    const data = await res.json()
    pages.value = data.pages || []
  } catch (error) {
    console.error('加载趣味页面清单失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.fun-page {
  min-height: calc(100vh - 80px);
  background: #f7f7f7;
  padding: 48px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.page-head {
  margin-bottom: 32px;
}

.page-head h1 {
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.page-head p {
  font-size: 14px;
  color: #888888;
  margin: 0;
}

.tip {
  color: #888888;
  font-size: 14px;
  padding: 24px 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.card {
  display: block;
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 28px 24px;
  text-align: center;
  text-decoration: none;
  transition: all 0.2s;
}

.card:hover {
  border-color: #1a1a1a;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.icon {
  font-size: 32px;
  line-height: 1;
  margin-bottom: 14px;
}

.card h3 {
  font-size: 17px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.card p {
  font-size: 13px;
  color: #666666;
  margin: 0;
  line-height: 1.6;
}
</style>
