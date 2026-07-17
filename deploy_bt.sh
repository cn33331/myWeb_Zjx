#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="hub"
SERVER_IP=""
SERVER_PORT="${SERVER_PORT:-80}"

log_info() {
    echo -e "\033[32m[INFO]\033[0m $1"
}

log_warn() {
    echo -e "\033[33m[WARN]\033[0m $1"
}

log_error() {
    echo -e "\033[31m[ERROR]\033[0m $1"
}

check_env() {
    log_info "检查本地环境..."
    
    if ! command -v git &> /dev/null; then
        log_error "未找到 git，请先安装 git"
        exit 1
    fi
    
    if ! command -v ssh &> /dev/null; then
        log_error "未找到 ssh，请先安装 openssh"
        exit 1
    fi
    
    log_info "本地环境检查通过"
}

read_config() {
    echo
    read -p "请输入服务器 IP 地址: " SERVER_IP
    if [ -z "$SERVER_IP" ]; then
        log_error "服务器 IP 不能为空"
        exit 1
    fi
    
    read -p "请输入服务器 SSH 端口 [默认22]: " SSH_PORT
    SSH_PORT=${SSH_PORT:-22}
    
    read -p "请输入服务器用户名 [默认root]: " SERVER_USER
    SERVER_USER=${SERVER_USER:-root}
    
    read -p "请输入项目部署路径 [默认/www/wwwroot/hub]: " DEPLOY_PATH
    DEPLOY_PATH=${DEPLOY_PATH:-/www/wwwroot/hub}
    
    read -p "请输入 Nginx 站点域名: " SITE_DOMAIN
}

upload_code() {
    log_info "上传代码到服务器..."
    rsync -avz --exclude='venv/' --exclude='node_modules/' --exclude='.git/' \
          --exclude='dist/' --exclude='*.log' \
          "$SCRIPT_DIR/" "$SERVER_USER@$SERVER_IP:$DEPLOY_PATH/"
    log_info "代码上传完成"
}

run_remote_setup() {
    log_info "在服务器上执行部署..."
    
    ssh -p "$SSH_PORT" "$SERVER_USER@$SERVER_IP" << EOF
    set -e
    
    echo "=========================================="
    echo "  Hub 平台 - 宝塔面板部署脚本"
    echo "=========================================="
    echo

    PROJECT_DIR="$DEPLOY_PATH"
    VENV_DIR="\$PROJECT_DIR/venv"
    PYTHON_BIN="/www/server/panel/pyenv/bin/python3"

    if [ ! -f "\$PYTHON_BIN" ]; then
        echo "[WARN] 宝塔 Python 环境未找到，使用系统 Python..."
        PYTHON_BIN="python3"
    fi

    echo "[INFO] 使用 Python: \$(\$PYTHON_BIN --version)"

    if [ ! -d "\$VENV_DIR" ]; then
        echo "[INFO] 创建虚拟环境..."
        \$PYTHON_BIN -m venv "\$VENV_DIR"
        echo "[INFO] 虚拟环境创建成功"
    fi

    echo "[INFO] 安装 Python 依赖..."
    \$VENV_DIR/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r "\$PROJECT_DIR/requirements.txt"
    echo "[INFO] Python 依赖安装完成"

    echo "[INFO] 安装 Node.js 依赖..."
    cd "\$PROJECT_DIR/vue-frontend"
    npm install --registry=https://registry.npmmirror.com
    echo "[INFO] Node.js 依赖安装完成"

    echo "[INFO] 构建前端..."
    npm run build
    echo "[INFO] 前端构建完成"

    echo "[INFO] 执行数据库迁移..."
    cd "\$PROJECT_DIR/hub"
    \$VENV_DIR/bin/python manage.py migrate --noinput
    echo "[INFO] 数据库迁移完成"

    echo "[INFO] 收集静态文件..."
    \$VENV_DIR/bin/python manage.py collectstatic --noinput
    echo "[INFO] 静态文件收集完成"

    echo "[INFO] 安装 Gunicorn..."
    \$VENV_DIR/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn
    echo "[INFO] Gunicorn 安装完成"

    echo "=========================================="
    echo "  部署完成！"
    echo "=========================================="
EOF
}

generate_nginx_config() {
    log_info "生成 Nginx 配置..."
    
    NGINX_CONF="server {
    listen $SERVER_PORT;
    listen [::]:$SERVER_PORT;
    server_name $SITE_DOMAIN $SERVER_IP localhost;

    charset utf-8;
    client_max_body_size 50M;

    location /static/ {
        root $DEPLOY_PATH/hub;
        expires 30d;
    }

    location /media/ {
        root $DEPLOY_PATH/hub;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_read_timeout 30s;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location / {
        root $DEPLOY_PATH/vue-frontend/dist;
        try_files \$uri \$uri/ /index.html;
    }

    access_log /www/wwwlogs/${PROJECT_NAME}_access.log;
    error_log /www/wwwlogs/${PROJECT_NAME}_error.log;
}"

    echo "$NGINX_CONF" > "$SCRIPT_DIR/nginx_bt.conf"
    log_info "Nginx 配置已生成: nginx_bt.conf"
}

generate_service_config() {
    log_info "生成 Gunicorn 服务配置..."
    
    SERVICE_CONF="[program:$PROJECT_NAME]
command=$DEPLOY_PATH/venv/bin/gunicorn hub.wsgi:application --bind 127.0.0.1:8000 --workers 4
directory=$DEPLOY_PATH/hub
autostart=true
autorestart=true
startsecs=5
stopwaitsecs=30
stdout_logfile=/www/wwwlogs/${PROJECT_NAME}_gunicorn.log
stderr_logfile=/www/wwwlogs/${PROJECT_NAME}_gunicorn_error.log
user=$SERVER_USER"

    echo "$SERVICE_CONF" > "$SCRIPT_DIR/${PROJECT_NAME}.ini"
    log_info "Gunicorn 服务配置已生成: ${PROJECT_NAME}.ini"
}

upload_configs() {
    log_info "上传配置文件..."
    scp -P "$SSH_PORT" "$SCRIPT_DIR/nginx_bt.conf" "$SERVER_USER@$SERVER_IP:/tmp/${PROJECT_NAME}_nginx.conf"
    scp -P "$SSH_PORT" "$SCRIPT_DIR/${PROJECT_NAME}.ini" "$SERVER_USER@$SERVER_IP:/tmp/${PROJECT_NAME}.ini"
    log_info "配置文件上传完成"
}

main() {
    echo "=========================================="
    echo "  Hub 平台 - 宝塔面板一键部署脚本"
    echo "=========================================="
    echo

    check_env
    read_config
    upload_code
    run_remote_setup
    generate_nginx_config
    generate_service_config
    upload_configs

    echo
    echo "=========================================="
    echo "  部署脚本执行完成！"
    echo "=========================================="
    echo
    echo "下一步操作（在宝塔面板中）："
    echo "1. 登录宝塔面板：http://$SERVER_IP:8888"
    echo "2. 进入 [网站] -> [添加站点]"
    echo "3. 域名: $SITE_DOMAIN"
    echo "4. 根目录: $DEPLOY_PATH/vue-frontend/dist"
    echo "5. 点击 [设置] -> [配置文件]"
    echo "6. 替换为 /tmp/${PROJECT_NAME}_nginx.conf 的内容"
    echo "7. 保存并重启 Nginx"
    echo
    echo "配置 Supervisor 守护进程："
    echo "1. 在宝塔面板中安装 Supervisor 插件"
    echo "2. 添加守护进程"
    echo "3. 名称: $PROJECT_NAME"
    echo "4. 启动命令: $DEPLOY_PATH/venv/bin/gunicorn hub.wsgi:application --bind 127.0.0.1:8000 --workers 4"
    echo "5. 启动目录: $DEPLOY_PATH/hub"
    echo "6. 启动用户: $SERVER_USER"
    echo
    echo "或者手动配置："
    echo "  cp /tmp/${PROJECT_NAME}.ini /etc/supervisor/conf.d/"
    echo "  supervisorctl reread"
    echo "  supervisorctl update"
    echo "  supervisorctl start $PROJECT_NAME"
    echo
}

main
