<template>
  <div class="home-page">
    <section class="hero">
      <div class="container">
        <h1>欢迎来到 Hub</h1>
        <p>一站式工具应用商店与社区论坛平台</p>
        <div class="hero-buttons">
          <router-link to="/store" class="btn btn-primary">探索商店</router-link>
          <router-link to="/forum" class="btn btn-secondary">进入论坛</router-link>
        </div>
      </div>
    </section>
    
    <section class="features">
      <div class="container">
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 7h16M4 17h16M10 12h4M4 12h2M18 12h2" />
            </svg>
          </div>
          <h3>工具商店</h3>
          <p>发现和下载各种实用工具，支持一键上传分享</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="16" x2="12" y2="12" />
              <line x1="12" y1="8" x2="12.01" y2="8" />
            </svg>
          </div>
          <h3>社区论坛</h3>
          <p>与志同道合的开发者交流，分享经验和想法</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <h3>安全认证</h3>
          <p>基于JWT的安全认证系统，保护您的账户安全</p>
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
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
}

.hero h1 {
  font-size: 48px;
  margin: 0 0 16px 0;
  font-weight: 700;
}

.hero p {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0 0 32px 0;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: white;
  color: #3b82f6;
}

.btn-primary:hover {
  background: rgba(255, 255, 255, 0.9);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
}

.features {
  padding: 60px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.features .container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}

.feature-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.feature-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin: 0 auto 16px auto;
}

.feature-icon svg {
  width: 32px;
  height: 32px;
}

.feature-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.feature-card p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}
</style>
