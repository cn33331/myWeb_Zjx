#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

clear

echo "=========================================="
echo "  Hub - 多功能 Web 平台启动脚本"
echo "=========================================="
echo

PYTHON_BIN=""
VENV_DIR="$SCRIPT_DIR/venv"
PROJECT_DIR="$SCRIPT_DIR/hub"
FRONTEND_DIR="$SCRIPT_DIR/vue-frontend"
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}"
HOST="${HOST:-0.0.0.0}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

log_info() {
    echo -e "\033[32m[INFO]\033[0m $1"
}

log_warn() {
    echo -e "\033[33m[WARN]\033[0m $1"
}

log_error() {
    echo -e "\033[31m[ERROR]\033[0m $1"
}

log_backend() {
    echo -e "\033[34m[BACKEND]\033[0m $1"
}

log_frontend() {
    echo -e "\033[35m[FRONTEND]\033[0m $1"
}

detect_python() {
    log_info "检测 Python 环境..."
    if command -v python3 &> /dev/null; then
        PYTHON_BIN="python3"
    elif command -v python &> /dev/null; then
        PYTHON_BIN="python"
    else
        log_error "未找到 Python，请先安装 Python 3.x"
        echo "按回车键退出..."
        read
        exit 1
    fi
    log_info "使用 Python: $($PYTHON_BIN --version)"
}

detect_node() {
    log_info "检测 Node.js 环境..."
    if command -v node &> /dev/null; then
        log_info "使用 Node.js: $(node --version)"
        if command -v npm &> /dev/null; then
            log_info "使用 npm: $(npm --version)"
        else
            log_error "未找到 npm，请先安装完整的 Node.js"
            echo "按回车键退出..."
            read
            exit 1
        fi
    else
        log_error "未找到 Node.js，请先安装 Node.js"
        echo "按回车键退出..."
        read
        exit 1
    fi
}

check_venv() {
    if [ -d "$VENV_DIR" ]; then
        log_info "虚拟环境已存在"
    else
        log_info "创建虚拟环境..."
        $PYTHON_BIN -m venv "$VENV_DIR"
        log_info "虚拟环境创建成功"
    fi
}

install_backend_dependencies() {
    log_info "检查后端依赖..."
    VENV_PYTHON="$VENV_DIR/bin/python"
    if [ ! -f "$VENV_PYTHON" ]; then
        log_error "虚拟环境 Python 解释器不存在"
        echo "按回车键退出..."
        read
        exit 1
    fi

    if ! $VENV_PYTHON -c "import django" &> /dev/null; then
        log_info "安装 Django 依赖（使用镜像源: $PIP_INDEX_URL）..."
        "$VENV_DIR/bin/pip" install -i "$PIP_INDEX_URL" django
        log_info "依赖安装完成"
    else
        log_info "Django 已安装: $($VENV_PYTHON -c "import django; print(django.VERSION)")"
    fi

    if ! $VENV_PYTHON -c "import rest_framework" &> /dev/null; then
        log_info "安装 REST Framework 依赖..."
        "$VENV_DIR/bin/pip" install -i "$PIP_INDEX_URL" djangorestframework djangorestframework-simplejwt django-cors-headers
        log_info "REST Framework 依赖安装完成"
    else
        log_info "REST Framework 已安装"
    fi
}

install_frontend_dependencies() {
    if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
        log_info "安装前端依赖..."
        cd "$FRONTEND_DIR"
        npm install
        log_info "前端依赖安装完成"
        cd "$SCRIPT_DIR"
    else
        log_info "前端依赖已安装"
    fi
}

run_migrations() {
    log_info "执行数据库迁移..."
    cd "$PROJECT_DIR"
    "$VENV_DIR/bin/python" manage.py migrate --noinput
    log_info "数据库迁移完成"
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

check_port() {
    local port=$1
    local port_name=$2

    log_info "检查端口 $port 是否被占用..."

    local PIDS=""
    if command -v lsof &> /dev/null; then
        PIDS=$(lsof -ti tcp:$port 2>/dev/null || true)
    elif command -v ss &> /dev/null; then
        PIDS=$(ss -tlnp "sport = :$port" 2>/dev/null | grep -oP 'pid=\K[0-9]+' || true)
    elif command -v netstat &> /dev/null; then
        PIDS=$(netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1 || true)
    fi

    if [ -z "$PIDS" ]; then
        log_info "端口 $port 空闲"
        return 0
    fi

    log_warn "端口 $port ($port_name) 已被以下进程占用:"
    for pid in $PIDS; do
        if [ -n "$pid" ]; then
            local cmd=""
            if command -v ps &> /dev/null; then
                cmd=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
            fi
            log_warn "  PID: $pid  命令: $cmd"
        fi
    done

    log_info "自动释放端口 $port..."
    for pid in $PIDS; do
        if [ -n "$pid" ]; then
            kill -9 $pid 2>/dev/null || true
        fi
    done
    sleep 1
    log_info "端口 $port 已释放"
}

start_backend() {
    log_info "启动 Django 后端服务..."
    cd "$PROJECT_DIR"
    "$VENV_DIR/bin/python" manage.py runserver "$HOST:$BACKEND_PORT" > "$SCRIPT_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    log_info "后端服务已启动 (PID: $BACKEND_PID)"
    log_backend "地址: http://localhost:$BACKEND_PORT/"
    log_backend "管理后台: http://localhost:$BACKEND_PORT/admin"
    log_backend "API 地址: http://localhost:$BACKEND_PORT/api/"
}

start_frontend() {
    log_info "启动 Vue 前端服务..."
    cd "$FRONTEND_DIR"
    npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT > "$SCRIPT_DIR/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    log_info "前端服务已启动 (PID: $FRONTEND_PID)"
    log_frontend "地址: http://localhost:$FRONTEND_PORT/"
}

stop_services() {
    echo
    log_info "正在停止服务..."
    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        log_info "后端服务已停止"
    fi
    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        log_info "前端服务已停止"
    fi
    rm -f "$SCRIPT_DIR/backend.log" "$SCRIPT_DIR/frontend.log"
}

show_logs() {
    echo
    log_info "实时日志输出（按 Ctrl+C 停止）..."
    echo "=========================================="
    tail -f "$SCRIPT_DIR/backend.log" "$SCRIPT_DIR/frontend.log" 2>/dev/null &
    TAIL_PID=$!
    wait $TAIL_PID
}

main() {
    detect_python
    detect_node
    check_venv
    install_backend_dependencies
    install_frontend_dependencies
    run_migrations
    check_admin_user
    check_port $BACKEND_PORT "后端"
    check_port $FRONTEND_PORT "前端"

    trap stop_services EXIT INT TERM

    start_backend
    start_frontend

    sleep 3

    echo
    echo "=========================================="
    echo "  Hub 平台启动完成！"
    echo "=========================================="
    echo
    log_frontend "前端页面: http://localhost:$FRONTEND_PORT/"
    log_backend "后端管理: http://localhost:$BACKEND_PORT/admin"
    log_backend "API 接口: http://localhost:$BACKEND_PORT/api/"
    echo
    echo "按 Ctrl+C 停止所有服务"
    echo "=========================================="
    echo

    show_logs
}

main
