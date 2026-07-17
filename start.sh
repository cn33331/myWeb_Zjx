#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR/hub"
VENV_DIR="$SCRIPT_DIR/venv"
DJANGO_SETTINGS_MODULE="hub.settings"

PYTHON_BIN=""
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
MODE="${MODE:-development}"

log_info() {
    echo -e "\033[32m[INFO]\033[0m $1"
}

log_warn() {
    echo -e "\033[33m[WARN]\033[0m $1"
}

log_error() {
    echo -e "\033[31m[ERROR]\033[0m $1"
}

detect_python() {
    log_info "检测 Python 环境..."
    if command -v python3 &> /dev/null; then
        PYTHON_BIN="python3"
    elif command -v python &> /dev/null; then
        PYTHON_BIN="python"
    else
        log_error "未找到 Python，请先安装 Python 3.x"
        exit 1
    fi
    log_info "使用 Python: $($PYTHON_BIN --version)"
}

check_venv() {
    if [ -d "$VENV_DIR" ]; then
        log_info "虚拟环境已存在: $VENV_DIR"
    else
        log_info "创建虚拟环境..."
        $PYTHON_BIN -m venv "$VENV_DIR"
        log_info "虚拟环境创建成功"
    fi
}

install_dependencies() {
    log_info "检查依赖..."
    VENV_PYTHON="$VENV_DIR/bin/python"
    if [ ! -f "$VENV_PYTHON" ]; then
        log_error "虚拟环境 Python 解释器不存在"
        exit 1
    fi

    if ! $VENV_PYTHON -c "import django" &> /dev/null; then
        log_info "安装依赖（使用镜像源: $PIP_INDEX_URL）..."
        "$VENV_DIR/bin/pip" install -i "$PIP_INDEX_URL" -r "$SCRIPT_DIR/requirements.txt"
        log_info "依赖安装完成"
    else
        log_info "Django 已安装: $($VENV_PYTHON -c "import django; print(django.VERSION)")"
    fi
}

run_migrations() {
    log_info "执行数据库迁移..."
    cd "$PROJECT_DIR"
    "$VENV_DIR/bin/python" manage.py migrate --noinput
    log_info "数据库迁移完成"
}

collect_static() {
    log_info "收集静态文件..."
    cd "$PROJECT_DIR"
    "$VENV_DIR/bin/python" manage.py collectstatic --noinput
    log_info "静态文件收集完成"
}

check_admin_user() {
    log_info "检查管理员账号..."
    cd "$PROJECT_DIR"
    ADMIN_EXISTS=$("$VENV_DIR/bin/python" manage.py shell -c "
from django.contrib.auth.models import User
if User.objects.filter(is_superuser=True).exists():
    print('yes')
else:
    print('no')
" 2>&1)

    if [[ "$ADMIN_EXISTS" == *"yes"* ]]; then
        log_info "检测到已有管理员账号"
    else
        log_warn "未检测到管理员账号"
        read -p "是否创建管理员账号？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "创建管理员账号..."
            read -p "请输入用户名: " ADMIN_USER
            read -p "请输入邮箱: " ADMIN_EMAIL
            read -s -p "请输入密码: " ADMIN_PASS
            echo
            "$VENV_DIR/bin/python" manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.create_superuser('$ADMIN_USER', '$ADMIN_EMAIL', '$ADMIN_PASS')
print('管理员账号创建成功:', user.username)
"
            log_info "管理员账号创建完成"
        else
            log_warn "跳过管理员账号创建"
        fi
    fi
}

start_dev_server() {
    log_info "启动 Django 开发服务器..."
    log_info "监听地址: http://$HOST:$PORT"
    log_info "管理后台: http://$HOST:$PORT/admin"
    log_info "API 地址: http://$HOST:$PORT/api/"
    log_info "按 Ctrl+C 停止服务器"
    echo
    cd "$PROJECT_DIR"
    "$VENV_DIR/bin/python" manage.py runserver "$HOST:$PORT"
}

start_production_server() {
    log_info "启动 Gunicorn 生产服务器..."
    log_info "监听地址: http://$HOST:$PORT"
    log_info "管理后台: http://$HOST:$PORT/admin"
    log_info "API 地址: http://$HOST:$PORT/api/"
    log_info "按 Ctrl+C 停止服务器"
    echo
    cd "$PROJECT_DIR"
    "$VENV_DIR/bin/gunicorn" hub.wsgi:application --bind "$HOST:$PORT" --workers 4
}

main() {
    echo "=========================================="
    echo "  Hub - 多功能 Web 平台启动脚本"
    echo "=========================================="
    echo
    echo "当前模式: $MODE"
    echo

    detect_python
    check_venv
    install_dependencies
    run_migrations
    
    if [ "$MODE" = "production" ]; then
        collect_static
    fi
    
    check_admin_user

    if [ "$MODE" = "production" ]; then
        start_production_server
    else
        start_dev_server
    fi
}

main
