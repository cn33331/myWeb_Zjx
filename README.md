# Tool Store - 工具应用商店

基于 Django 的工具应用商店平台，用于上传和下载开发的工具。

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
django-admin startproject tool_store

# 进入项目目录
cd tool_store

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
└── tool_store/       # Django 项目根目录
    ├── manage.py     # 管理脚本
    ├── tool_store/   # 项目配置
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── store/        # 应用商店应用
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── views.py
        ├── urls.py
        └── templates/
```

## 应用商店功能

- 工具列表展示
- 工具上传管理（管理员）
- 工具下载（带下载次数统计）
- 工具详情查看

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
# CentOS / RHEL / OpenCloudOS
yum install -y git python3 python3-venv

# Ubuntu / Debian
# apt update && apt install -y git python3 python3-venv

# 2. 克隆项目
git clone git@github.com:cn33331/myWeb_Zjx.git web
cd web

# 3. 启动服务（自动完成虚拟环境、依赖安装、数据库迁移）
chmod +x start.sh
./start.sh
```

**服务器部署注意事项：**

| 事项 | 说明 |
|------|------|
| 防火墙 | 需要开放 8000 端口：`firewall-cmd --permanent --add-port=8000/tcp && firewall-cmd --reload` |
| 安全组 | 云服务器安全组需要放行 8000 端口 |
| 后台运行 | 使用 `nohup ./start.sh &` 或 `screen` 后台运行 |
| 域名绑定 | 使用 Nginx 反向代理，配置域名和 HTTPS |

**后台运行方式：**

```bash
# 方式一：使用 nohup
nohup ./start.sh > server.log 2>&1 &

# 方式二：使用 screen（推荐，可随时恢复终端）
screen -S toolstore
./start.sh
# 按 Ctrl+A+D 退出screen，按 screen -r toolstore 恢复
```

**Nginx 反向代理配置示例（可选）：**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 手动启动

```bash
# 进入项目目录
cd tool_store
source ../venv/bin/activate

# 创建管理员账号（首次运行）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

## 访问地址

- 首页：http://localhost:8000/
- 管理后台：http://localhost:8000/admin/

## 使用说明

1. 通过管理后台上传工具文件
2. 在首页浏览和搜索工具
3. 点击下载链接获取工具文件
