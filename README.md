# Hub - 多功能 Web 平台

基于 Django + Vue 3 的工具应用商店平台，采用前后端分离架构。

## 平台模块

| 模块 | 路径前缀 | 应用 | 说明 |
| --- | --- | --- | --- |
| 首页入口 | `/` | `home` | 展示平台入口 |
| 应用商店 | `/store/` | `store` | 工具的上传、下载与详情查看 |
| 管理后台 | `/admin/` | Django Admin | 站点管理 |
| API 接口 | `/api/` | DRF | RESTful API 服务 |

## 架构总览

```
┌──────────────────────────────────────────────────────────────────┐
│                        前端层                                    │
│  Vue 3 + Vite + Pinia + Axios                                    │
│  /vue-frontend/                                                  │
│  ├── src/pages/       # 页面组件（Home/Store/Auth）               │
│  ├── src/components/  # 通用组件（ToolCard/Header）               │
│  ├── src/api/         # API请求封装                              │
│  └── src/stores/      # Pinia状态管理                            │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP (Axios + JWT)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                        后端层                                    │
│  Django + Django REST Framework + SimpleJWT                      │
│  /hub/                                                           │
│  ├── hub/settings.py  # CORS、REST Framework、JWT 配置           │
│  ├── hub/auth_*.py    # 认证模块（登录/注册/Token刷新）          │
│  └── store/api/       # 商店模块 API                             │
└───────────────────────────┬──────────────────────────────────────┘
                            │ Gunicorn / runserver
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                        部署层                                    │
│  Nginx 反向代理                                                  │
│  - 静态资源：/ → Vue dist                                        │
│  - API转发：  /api/ → Django (127.0.0.1:8000)                    │
│  - 媒体文件： /media/ → Django MEDIA_ROOT                        │
│  - 管理后台： /admin/ → Django Admin                              │
└──────────────────────────────────────────────────────────────────┘
```

## 项目结构

```
web/
├── hub/                      # Django 后端项目
│   ├── manage.py
│   ├── hub/                  # 项目配置
│   │   ├── settings.py       # Django + DRF + JWT + CORS 配置
│   │   ├── urls.py           # 根路由（含 /api/ 入口）
│   │   ├── api_urls.py       # API 路由聚合
│   │   ├── auth_views.py     # 登录/注册视图
│   │   ├── auth_serializers.py
│   │   └── auth_urls.py
│   ├── home/                 # 首页入口应用
│   └── store/                # 应用商店模块
│       ├── models.py
│       ├── api/              # REST API（serializers/views/urls）
│       └── templates/store/
├── vue-frontend/             # Vue 3 前端项目
│   ├── src/
│   │   ├── api/              # axios 封装（index/store/auth）
│   │   ├── components/       # 通用组件（Header/ToolCard/Loading）
│   │   ├── pages/            # 页面组件
│   │   ├── stores/           # Pinia 状态管理（auth/store）
│   │   ├── router/           # 路由配置与导航守卫
│   │   ├── App.vue
│   │   └── main.js
│   ├── .env.development      # 开发环境 API 地址
│   ├── .env.production       # 生产环境 API 地址
│   └── vite.config.js        # Vite 配置（代理、别名）
├── nginx_bt_80.conf          # 宝塔 Nginx 配置（80端口）
├── requirements.txt          # Python 依赖
├── start.sh                  # 启动脚本（支持开发/生产模式）
├── deploy_bt.sh              # 宝塔面板部署脚本
└── 启动服务.command           # macOS 双击启动
```

## 功能说明

### 首页（home）
- 根路径 `/` 展示平台各功能模块入口卡片

### 应用商店（store）
- 工具列表展示与搜索
- 工具上传管理（管理员）
- 工具下载（带下载次数统计）
- 工具详情查看

## API 接口总览

| 模块 | API 路径 | 方法 | 说明 | 认证 |
|------|---------|------|------|------|
| 认证 | `/api/auth/login/` | POST | 用户登录 | 公开 |
| 认证 | `/api/auth/register/` | POST | 用户注册 | 公开 |
| 认证 | `/api/auth/refresh/` | POST | Token 刷新 | 需 refresh_token |
| 商店 | `/api/store/tools/` | GET | 工具列表 | 公开 |
| 商店 | `/api/store/tools/` | POST | 上传工具 | 管理员 |
| 商店 | `/api/store/tools/<id>/` | GET | 工具详情 | 公开 |
| 商店 | `/api/store/tools/<id>/` | DELETE | 删除工具 | 管理员 |
| 商店 | `/api/store/tools/<id>/download/` | GET | 工具下载 | 公开 |

## 前端路由

| 路径 | 组件 | 说明 | 权限 |
|------|------|------|------|
| `/` | HomePage | 首页入口 | 公开 |
| `/store` | StorePage | 商店列表 | 公开 |
| `/store/:id` | ToolDetailPage | 工具详情 | 公开 |
| `/store/upload` | ToolUploadPage | 工具上传 | 管理员 |
| `/login` | LoginPage | 登录 | 未登录 |
| `/register` | RegisterPage | 注册 | 未登录 |

## 技术栈

### 后端
- Django 4.2
- Django REST Framework 3.16
- SimpleJWT（Token 认证）
- django-cors-headers（跨域）
- Gunicorn（生产 WSGI）
- SQLite（默认数据库）

### 前端
- Vue 3 + Vite
- Pinia（状态管理）
- Vue Router（路由）
- Axios（HTTP 请求）

### 部署
- Nginx（反向代理 + 静态资源）
- systemd / Supervisor（进程守护）

## 本地部署

### macOS 开发环境

```bash
# 克隆项目
git clone https://github.com/cn33331/myWeb_Zjx.git web
cd web

# 一键启动前后端
chmod +x 启动服务.command
./启动服务.command
```

启动后访问：
- 前端：http://localhost:5173/
- 后端：http://localhost:8000/admin

### Linux 生产环境（宝塔面板）

```bash
# 克隆项目
cd /root/zjx
git clone https://github.com/cn33331/myWeb_Zjx.git web
cd web

# 一键部署
chmod +x deploy_bt.sh
./deploy_bt.sh

# 配置 Gunicorn 服务（systemd）
cat > /etc/systemd/system/hub.service << 'EOF'
[Unit]
Description=Hub Platform Gunicorn Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/zjx/web/web/hub
ExecStart=/root/zjx/web/web/venv/bin/gunicorn hub.wsgi:application --bind 127.0.0.1:8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start hub
systemctl enable hub

# 配置 Nginx 反向代理
cp nginx_bt.conf /www/server/panel/vhost/nginx/hub.conf
/www/server/nginx/sbin/nginx -t && /www/server/nginx/sbin/nginx -s reload
```

启动后访问：`http://服务器公网IP/`

### 代码更新流程

服务器上代码更新后的操作步骤：

```bash
cd /root/zjx/web/web

# 1. 拉取最新代码
git pull origin main

# 2. 重新部署（更新依赖、迁移数据库、构建前端）
./deploy_bt.sh

# 3. 重启 Gunicorn 服务
systemctl restart hub

# 4. 重载 Nginx 配置（若 nginx_bt.conf 有变更）
/www/server/nginx/sbin/nginx -t && /www/server/nginx/sbin/nginx -s reload
```

**说明：**
- `git pull` - 拉取远程仓库最新代码
- `./deploy_bt.sh` - 自动完成依赖安装、前端构建、数据库迁移、静态文件收集
- `systemctl restart hub` - 重启 Gunicorn 使后端代码生效
- Nginx 重载仅在 Nginx 配置文件变更时需要

## 安全注意事项

1. 生产环境设置 `DEBUG = False`
2. `CORS_ALLOWED_ORIGINS` 仅允许前端域名
3. `SECRET_KEY` 使用环境变量管理
4. 仅开放 80/443 端口，限制 8000 端口仅本地访问
5. 部署 SSL 证书（Let's Encrypt）强制 HTTPS
