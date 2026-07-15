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
