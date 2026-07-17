# Hub - 多功能 Web 平台

基于 Django 的多功能 Web 平台，采用模块化架构，按功能拆分为多个独立应用。目前已包含「应用商店」与「论坛」两个模块，后续可继续扩展新模块。

## 平台模块

| 模块 | 路径前缀 | 应用 | 说明 |
| --- | --- | --- | --- |
| 首页入口 | `/` | `home` | 展示各功能模块入口 |
| 应用商店 | `/store/` | `store` | 工具的上传、下载与详情查看 |
| 论坛 | `/forum/` | `forum` | 注册、登录、发帖与回复讨论 |
| 管理后台 | `/admin/` | Django Admin | 站点管理 |

## 项目环境搭建步骤

### 第一步：创建虚拟环境

```bash
python3 -m venv venv
```

激活虚拟环境：

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 第二步：创建 .gitignore 文件

创建 `.gitignore` 文件，屏蔽虚拟环境和 Django 项目中的敏感文件：

```
venv/
*.pyc
__pycache__/
*.egg-info/
db.sqlite3
media/
static/
.env
.DS_Store
```

### 第三步：安装 Django 模块

```bash
pip install django
```

### 第四步：创建 Django 项目

```bash
# 创建项目
django-admin startproject hub

# 进入项目目录
cd hub

# 创建应用
python manage.py startapp store

# 创建数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 项目结构

```
web/
├── venv/              # 虚拟环境
├── .gitignore        # Git 忽略规则
├── README.md         # 项目说明
├── start.sh          # Linux 启动脚本
├── 启动服务.command    # macOS 双击启动
└── hub/              # Django 项目根目录
    ├── manage.py     # 管理脚本
    ├── hub/          # 项目配置
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── home/         # 首页入口应用（根路径 / 展示模块入口）
    │   ├── views.py
    │   ├── urls.py
    │   └── templates/home/index.html
    ├── store/        # 应用商店模块
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   └── templates/store/
    └── forum/        # 论坛模块
        ├── models.py
        ├── views.py
        ├── urls.py
        └── templates/forum/
```

## 功能说明

### 首页（home）
- 根路径 `/` 展示平台各功能模块入口卡片
- 作为应用商店与论坛的统一展示入口

### 应用商店（store）
- 工具列表展示
- 工具上传管理（管理员）
- 工具下载（带下载次数统计）
- 工具详情查看

### 论坛（forum）
- 用户注册与管理员审核
- 登录 / 登出
- 发布话题与回复讨论
- 管理员审核面板

## 快速启动

### 方式一：双击运行（macOS 推荐）

直接双击 `启动服务.command` 文件即可启动，首次运行可能需要在系统设置中允许执行。

> 如果双击提示无法打开，请在文件上右键 → 打开，或在终端执行：
> ```bash
> chmod +x 启动服务.command
> ```

### 方式二：命令行运行（兼容 macOS / Linux）

```bash
cd web
chmod +x start.sh
./start.sh
```

脚本会自动完成以下操作：
1. 检测 Python 环境
2. 创建虚拟环境（如果不存在）
3. 安装 Django 依赖（使用清华镜像源加速）
4. 执行数据库迁移
5. 检测管理员账号，可选创建
6. 启动开发服务器

**可选环境变量：**
- `HOST` - 监听地址，默认 `0.0.0.0`
- `PORT` - 监听端口，默认 `8000`
- `PIP_INDEX_URL` - pip 镜像源地址，默认清华源

```bash
# 自定义端口启动
PORT=8080 ./start.sh

# 使用官方源
PIP_INDEX_URL=https://pypi.org/simple ./start.sh
```

### 方式三：Linux 云服务器部署

```bash
# 1. 安装系统依赖
# Ubuntu / Debian
apt update && apt install -y git python3 python3-venv

# 2. 克隆项目（两种方式任选其一）
# 方式A：使用 SSH（推荐，需要配置 SSH 密钥）
git clone git@github.com:cn33331/myWeb_Zjx.git web

# 方式B：使用 HTTPS（无需配置 SSH 密钥）
# git clone https://github.com/cn33331/myWeb_Zjx.git web

cd web

# 3. 启动服务（自动完成虚拟环境、依赖安装、数据库迁移）
chmod +x start.sh
./start.sh
```

**SSH 密钥配置（使用方式A时需要）：**

```bash
# 在服务器上生成 SSH 密钥（一路回车即可）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥内容
cat ~/.ssh/id_ed25519.pub
```

将输出的公钥内容复制到 GitHub：
1. 登录 GitHub → 点击头像 → Settings → SSH and GPG keys
2. 点击 New SSH key
3. 粘贴公钥内容，添加即可

### 方式四：云服务器 80 端口部署

> 适用于云服务器仅开放 80 端口的场景。Django 直接监听 80 端口，无需 Nginx。

```bash
cd /root/zjx/web
PORT=80 ./start.sh
```

后台运行：

```bash
PORT=80 nohup ./start.sh > server.log 2>&1 &
```

浏览器访问：`http://服务器公网IP/`

**常用运维命令：**

```bash
# 查看 Django 日志
tail -f /root/zjx/web/server.log

# 停止 Django（找到进程并结束）
ps aux | grep runserver
kill <PID>

# 更新代码后重启
cd /root/zjx/web
git pull origin main
# 重启 Django 服务
```

## 手动启动

```bash
# 进入项目目录
cd hub
source ../venv/bin/activate

# 创建管理员账号（首次运行）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 访问地址

- 平台首页：http://localhost:8000/
- 应用商店：http://localhost:8000/store/
- 论坛：http://localhost:8000/forum/
- 管理后台：http://localhost:8000/admin/

## 使用说明

1. 访问首页 `/` 选择要进入的功能模块
2. 应用商店：通过管理后台上传工具文件，在 `/store/` 浏览和下载
3. 论坛：在 `/forum/` 注册账号（需管理员审核）后发帖与回复

---

## 前后端分离方案（Vue 3 + Django REST API + Nginx）

### 架构总览

```
┌──────────────────────────────────────────────────────────────────┐
│                        前端层                                   │
│  Vue 3 + Vite + Pinia + Axios                                   │
│  /web/vue-frontend/                                             │
│  ├── src/pages/       # 页面组件（Home/Store/Forum/Auth）        │
│  ├── src/components/  # 通用组件（ToolCard/TopicCard/Header）    │
│  ├── src/api/         # API请求封装                             │
│  └── src/stores/      # Pinia状态管理                           │
└───────────────────────────┬──────────────────────────────────────┘
                            │ HTTP (Axios)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                        后端层                                   │
│  Django + Django REST Framework + JWT                           │
│  /web/hub/                                                      │
│  ├── hub/settings.py  # CORS配置、REST Framework配置            │
│  ├── store/api/       # 商店模块API（序列化器、视图、路由）      │
│  ├── forum/api/       # 论坛模块API（序列化器、视图、路由）      │
│  └── auth/api/        # 认证API（登录/注册/Token刷新）           │
└───────────────────────────┬──────────────────────────────────────┘
                            │ uwsgi / runserver
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                        部署层                                   │
│  Nginx 反向代理                                                 │
│  - 静态资源：/ → Vue dist                                       │
│  - API转发：/api/ → Django (127.0.0.1:8000)                     │
│  - 媒体文件：/media/ → Django MEDIA_ROOT                        │
└──────────────────────────────────────────────────────────────────┘
```

### 步骤一：前端项目初始化

#### 1.1 创建 Vue 项目

```bash
cd /Users/gdlocal/Desktop/myCode/myAPP/web
npm create vite@6.5.0 vue-frontend -- --template vue
cd vue-frontend
npm install axios pinia vue-router
```

#### 1.2 目录结构

```
vue-frontend/
├── src/
│   ├── api/                     # API封装
│   │   ├── index.js             # axios实例配置（baseURL、Token拦截）
│   │   ├── store.js             # 商店接口（列表/详情/上传/下载）
│   │   ├── forum.js             # 论坛接口（话题/帖子/评论）
│   │   └── auth.js              # 认证接口（登录/注册/刷新）
│   ├── components/              # 通用组件
│   │   ├── Header.vue           # 页头导航（Logo、菜单、登录状态）
│   │   ├── ToolCard.vue         # 工具卡片
│   │   ├── TopicCard.vue        # 话题卡片
│   │   └── Loading.vue          # 加载状态
│   ├── pages/                   # 页面组件
│   │   ├── HomePage.vue         # 首页入口（模块导航）
│   │   ├── StorePage.vue        # 商店列表（工具展示、搜索筛选）
│   │   ├── ToolDetailPage.vue   # 工具详情（详情、下载按钮）
│   │   ├── ToolUploadPage.vue   # 工具上传（表单、文件选择）
│   │   ├── ForumPage.vue        # 论坛首页（话题列表）
│   │   ├── TopicDetailPage.vue  # 话题详情（帖子、回复）
│   │   ├── TopicCreatePage.vue  # 发布话题
│   │   ├── LoginPage.vue        # 登录页
│   │   └── RegisterPage.vue     # 注册页
│   ├── stores/                  # Pinia状态管理
│   │   ├── auth.js              # 用户认证状态（Token、用户名、权限）
│   │   ├── store.js             # 商店数据缓存
│   │   └── forum.js             # 论坛数据缓存
│   ├── router/                  # 路由配置
│   │   └── index.js             # 路由定义与导航守卫
│   ├── App.vue                  # 根组件（路由出口）
│   └── main.js                  # 入口文件（挂载Vue、Router、Pinia）
├── .env.development             # 开发环境变量
├── .env.production              # 生产环境变量
├── vite.config.js               # Vite配置（代理、路径别名）
└── package.json                 # 依赖与脚本
```

#### 1.3 环境变量

**/.env.development**：

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

**/.env.production**：

```env
VITE_API_BASE_URL=/api
```

#### 1.4 Vite 代理配置

**vite.config.js** 添加开发代理（避免跨域）：

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

#### 1.5 路由配置

| 路径 | 组件 | 说明 | 权限 |
|------|------|------|------|
| `/` | HomePage | 首页入口 | 公开 |
| `/store` | StorePage | 商店列表 | 公开 |
| `/store/:id` | ToolDetailPage | 工具详情 | 公开 |
| `/store/upload` | ToolUploadPage | 工具上传 | 管理员 |
| `/forum` | ForumPage | 论坛首页 | 公开 |
| `/forum/:id` | TopicDetailPage | 话题详情 | 公开 |
| `/forum/new` | TopicCreatePage | 发布话题 | 登录用户 |
| `/login` | LoginPage | 登录 | 未登录 |
| `/register` | RegisterPage | 注册 | 未登录 |

#### 1.6 API 请求封装

**src/api/index.js**：统一 axios 实例，自动携带 Token、处理错误。

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const res = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/auth/refresh/`,
            { refresh: refreshToken }
          )
          localStorage.setItem('access_token', res.data.access)
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`
          return api(originalRequest)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
```

#### 1.7 构建与运行

```bash
# 开发模式（自动代理到后端）
npm run dev

# 生产构建（输出到 dist/）
npm run build
```

### 步骤二：后端 API 改造

#### 2.1 安装依赖

```bash
cd /Users/gdlocal/Desktop/myCode/myAPP/web/hub
../venv/bin/pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

#### 2.2 Django 配置修改

**hub/settings.py** 需要添加的配置：

```python
INSTALLED_APPS = [
    # ... 原有配置
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 放在最前面
    'django.middleware.common.CommonMiddleware',
    # ... 其余中间件
]

# CORS 配置
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:80',
    'http://你的域名',
]
CORS_ALLOW_CREDENTIALS = True

# REST Framework 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT 配置
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

#### 2.3 API 路由规划

**hub/urls.py** 新增 API 路由入口：

```python
urlpatterns = [
    # ... 原有路由
    path('api/', include('hub.api_urls')),
]
```

新建 **hub/api_urls.py**：

```python
from django.urls import path, include

urlpatterns = [
    path('auth/', include('auth.api.urls')),
    path('store/', include('store.api.urls')),
    path('forum/', include('forum.api.urls')),
]
```

#### 2.4 认证 API

新建 **auth/api/** 目录：

```python
# auth/api/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
```

```python
# auth/api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import LoginSerializer, RegisterSerializer

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'is_staff': user.is_staff
            })
        return Response({'detail': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username
        })
```

```python
# auth/api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='api_login'),
    path('register/', views.RegisterView.as_view(), name='api_register'),
    path('refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
```

#### 2.5 商店 API

**store/api/serializers.py**：

```python
from rest_framework import serializers
from store.models import Tool

class ToolSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Tool
        fields = ['id', 'name', 'description', 'version', 'downloads', 'upload_date', 'download_url']
    
    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/store/tools/{obj.id}/download/')
```

**store/api/views.py**：

```python
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.http import FileResponse
from store.models import Tool
from .serializers import ToolSerializer

class ToolListView(generics.ListCreateAPIView):
    queryset = Tool.objects.all().order_by('-upload_date')
    serializer_class = ToolSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save()

class ToolDetailView(generics.RetrieveDestroyAPIView):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [permissions.AllowAny()]

class ToolDownloadView(generics.GenericAPIView):
    queryset = Tool.objects.all()
    permission_classes = [permissions.AllowAny()]
    
    def get(self, request, pk):
        tool = self.get_object()
        tool.downloads += 1
        tool.save()
        return FileResponse(tool.file.open(), as_attachment=True)
```

**store/api/urls.py**：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('tools/', views.ToolListView.as_view(), name='api_tool_list'),
    path('tools/<int:pk>/', views.ToolDetailView.as_view(), name='api_tool_detail'),
    path('tools/<int:pk>/download/', views.ToolDownloadView.as_view(), name='api_tool_download'),
]
```

#### 2.6 论坛 API

**forum/api/serializers.py**：

```python
from rest_framework import serializers
from forum.models import ForumUser, Topic, Post

class ForumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumUser
        fields = ['id', 'username', 'email', 'is_approved', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'author_username', 'created_at']

class TopicSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    post_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Topic
        fields = ['id', 'title', 'content', 'author_username', 'views', 'post_count', 'created_at']
```

**forum/api/views.py**：

```python
from rest_framework import generics, permissions
from forum.models import ForumUser, Topic, Post
from .serializers import ForumUserSerializer, TopicSerializer, PostSerializer

class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.all().order_by('-created_at')
    serializer_class = TopicSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)

class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return Post.objects.filter(topic_id=self.kwargs['topic_pk'])
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

**forum/api/urls.py**：

```python
from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.TopicListView.as_view(), name='api_topic_list'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='api_topic_detail'),
    path('topics/<int:topic_pk>/posts/', views.PostListView.as_view(), name='api_post_list'),
]
```

#### 2.7 API 接口总览

| 模块 | API 路径 | 方法 | 说明 | 认证 |
|------|---------|------|------|------|
| 认证 | `/api/auth/login/` | POST | 用户登录 | 公开 |
| 认证 | `/api/auth/register/` | POST | 用户注册 | 公开 |
| 认证 | `/api/auth/refresh/` | POST | Token刷新 | 需refresh_token |
| 商店 | `/api/store/tools/` | GET | 工具列表 | 公开 |
| 商店 | `/api/store/tools/` | POST | 上传工具 | 管理员 |
| 商店 | `/api/store/tools/<id>/` | GET | 工具详情 | 公开 |
| 商店 | `/api/store/tools/<id>/` | DELETE | 删除工具 | 管理员 |
| 商店 | `/api/store/tools/<id>/download/` | GET | 工具下载 | 公开 |
| 论坛 | `/api/forum/topics/` | GET | 话题列表 | 公开 |
| 论坛 | `/api/forum/topics/` | POST | 发布话题 | 登录用户 |
| 论坛 | `/api/forum/topics/<id>/` | GET | 话题详情 | 公开 |
| 论坛 | `/api/forum/topics/<id>/posts/` | GET | 帖子列表 | 公开 |
| 论坛 | `/api/forum/topics/<id>/posts/` | POST | 回复帖子 | 登录用户 |

### 步骤三：Nginx 反向代理部署

#### 3.1 安装 Nginx

```bash
# Ubuntu / Debian
apt update && apt install -y nginx

# CentOS / RHEL
yum install -y nginx
```

#### 3.2 Nginx 配置文件

**/etc/nginx/sites-available/hub.conf**：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态资源（Vue构建产物）
    location / {
        root /root/zjx/web/vue-frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API 反向代理到 Django
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 媒体文件（上传的工具文件）
    location /media/ {
        alias /root/zjx/web/hub/media/;
        expires 30d;
        add_header Cache-Control "public";
    }

    # 管理后台（保留 Django Admin）
    location /admin/ {
        proxy_pass http://127.0.0.1:8000/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

#### 3.3 启用配置

```bash
# 创建符号链接
ln -s /etc/nginx/sites-available/hub.conf /etc/nginx/sites-enabled/hub.conf

# 测试配置
nginx -t

# 重启 Nginx
systemctl restart nginx
```

#### 3.4 Django 后端启动方式

**开发阶段**（使用 runserver）：

```bash
cd /root/zjx/web/hub
../venv/bin/python manage.py runserver 127.0.0.1:8000
```

**生产阶段**（使用 uwsgi）：

```bash
# 安装 uwsgi
../venv/bin/pip install uwsgi

# 创建 uwsgi 配置文件 hub_uwsgi.ini
[uwsgi]
chdir = /root/zjx/web/hub
module = hub.wsgi:application
home = /root/zjx/web/venv
master = true
processes = 4
threads = 2
socket = /tmp/hub.sock
chmod-socket = 666
vacuum = true
daemonize = /var/log/hub_uwsgi.log

# 启动 uwsgi
uwsgi --ini hub_uwsgi.ini

# 停止 uwsgi
uwsgi --stop /tmp/hub.sock
```

#### 3.5 完整部署流程

```bash
# 1. 克隆项目
git clone git@github.com:cn33331/myWeb_Zjx.git web
cd web

# 2. 后端准备
source venv/bin/activate
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
cd hub
python manage.py migrate

# 3. 前端构建
cd ../vue-frontend
npm install
npm run build

# 4. 启动服务
# 终端1：启动 Django
cd ../hub
../venv/bin/python manage.py runserver 127.0.0.1:8000

# 终端2：确保 Nginx 运行
systemctl start nginx
```

#### 3.6 安全注意事项

1. **CORS 限制**：生产环境 `CORS_ALLOWED_ORIGINS` 仅允许前端域名，禁止 `CORS_ALLOW_ALL_ORIGINS = True`
2. **DEBUG 模式**：生产环境设置 `DEBUG = False`
3. **SECRET_KEY**：使用环境变量或 `.env` 文件管理
4. **HTTPS**：部署 SSL 证书（Let's Encrypt），强制 HTTPS
5. **防火墙**：仅开放 80/443 端口，限制 8000 端口仅本地访问

#### 3.7 HTTPS 配置示例（Let's Encrypt）

```bash
# 安装 certbot
apt install -y certbot python3-certbot-nginx

# 申请证书
certbot --nginx -d your-domain.com

# 自动更新证书
certbot renew --dry-run
```

---

### 改造注意事项

1. **渐进式迁移**：先完成 API 层改造，前端逐步替换，可同时保留原 Django 模板作为备用
2. **文件上传**：Vue 前端使用 `FormData` 提交文件，后端需配置 `MEDIA_ROOT` 和 `MEDIA_URL`
3. **下载接口**：后端返回 `FileResponse`，前端需处理 blob 下载（设置响应头 `Content-Disposition`）
4. **认证状态**：前端使用 `localStorage` 存储 Token，路由守卫校验登录状态
5. **开发调试**：前端开发时使用 Vite 代理，无需配置 Nginx；生产环境使用 Nginx 反向代理
6. **数据库**：Django 继续使用原有 `db.sqlite3`，无需额外数据库配置
