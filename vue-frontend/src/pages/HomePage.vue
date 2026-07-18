<template>
  <div class="home-page">
    <section class="hero">
      <div class="container">
        <h1>Hub</h1>
        <p>一站式工具应用商店平台</p>
        <div class="hero-buttons">
          <router-link to="/store" class="btn btn-primary">探索商店</router-link>
        </div>
      </div>
    </section>
    
    <section class="features">
      <div class="container">
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M4 7h16M4 17h16M10 12h4M4 12h2M18 12h2" />
            </svg>
          </div>
          <h3>工具商店</h3>
          <p>发现和下载各种实用工具，支持一键上传分享</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  min-height: calc(100vh - 80px);
}

.hero {
  background: #1a1a1a;
  color: #ffffff;
  padding: 100px 0;
  text-align: center;
}

.hero h1 {
  font-size: 56px;
  margin: 0 0 12px 0;
  font-weight: 300;
  letter-spacing: -1px;
}

.hero p {
  font-size: 18px;
  color: #999999;
  margin: 0 0 40px 0;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  padding: 12px 36px;
  border-radius: 4px;
  font-size: 15px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #ffffff;
  color: #1a1a1a;
}

.btn-primary:hover {
  background: #e8e8e8;
}

.features {
  padding: 60px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.features .container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  max-width: 600px;
}

.feature-card {
  background: #ffffff;
  border-radius: 4px;
  padding: 40px 32px;
  text-align: center;
  border: 1px solid #e0e0e0;
}

.feature-icon {
  width: 56px;
  height: 56px;
  background: #f5f5f5;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666666;
  margin: 0 auto 20px auto;
}

.feature-icon svg {
  width: 24px;
  height: 24px;
}

.feature-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.feature-card p {
  font-size: 14px;
  color: #666666;
  margin: 0;
  line-height: 1.6;
}
</style>