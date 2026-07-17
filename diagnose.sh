#!/bin/bash
# Hub 平台部署诊断脚本
# 用法: chmod +x diagnose.sh && ./diagnose.sh

PROJECT_DIR="/root/zjx/web/web"
NGINX_BIN="/www/server/nginx/sbin/nginx"
NGINX_VHOST="/www/server/panel/vhost/nginx"

echo "=========================================="
echo "  Hub 平台部署诊断"
echo "=========================================="
echo

# 1. 系统信息
echo "【1. 系统信息】"
echo "主机名: $(hostname)"
echo "系统: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "时间: $(date)"
echo

# 2. 端口检查
echo "【2. 端口监听检查】"
echo "--- 8000 端口 (Gunicorn) ---"
if netstat -tlnp 2>/dev/null | grep -q ":8000"; then
    netstat -tlnp 2>/dev/null | grep ":8000"
    echo "[OK] 8000 端口已监听"
else
    echo "[FAIL] 8000 端口未监听 - Gunicorn 未运行"
fi
echo

echo "--- 80 端口 (Nginx) ---"
if netstat -tlnp 2>/dev/null | grep -q ":80 "; then
    netstat -tlnp 2>/dev/null | grep ":80 " | head -3
    echo "[OK] 80 端口已监听"
else
    echo "[FAIL] 80 端口未监听 - Nginx 未运行或未配置"
fi
echo

echo "--- 8888 端口 (宝塔) ---"
if netstat -tlnp 2>/dev/null | grep -q ":8888"; then
    echo "[OK] 8888 端口已监听"
else
    echo "[WARN] 8888 端口未监听"
fi
echo

# 3. 服务状态
echo "【3. 服务状态】"
echo "--- Gunicorn (hub.service) ---"
if systemctl status hub &>/dev/null; then
    systemctl status hub | head -5
    echo "[OK] hub 服务运行中"
else
    echo "[FAIL] hub 服务未运行"
    echo "启动命令: systemctl start hub"
fi
echo

echo "--- Nginx ---"
if [ -f "$NGINX_BIN" ]; then
    if pgrep -x nginx &>/dev/null; then
        echo "[OK] Nginx 进程运行中"
        pgrep -x nginx | head -3
    else
        echo "[FAIL] Nginx 未运行"
        echo "启动命令: $NGINX_BIN"
    fi
else
    echo "[FAIL] Nginx 未安装: $NGINX_BIN 不存在"
fi
echo

# 4. Gunicorn 后端测试
echo "【4. Gunicorn 后端测试】"
echo "--- 测试 http://127.0.0.1:8000/api/store/tools/ ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1:8000/api/store/tools/ 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "[OK] 后端 API 正常 (HTTP 200)"
    curl -s --max-time 5 http://127.0.0.1:8000/api/store/tools/ | head -c 200
    echo
else
    echo "[FAIL] 后端 API 异常 (HTTP $HTTP_CODE)"
    echo "可能原因: Gunicorn 未启动 或 Django 配置错误"
fi
echo

# 5. Nginx 转发测试
echo "【5. Nginx 转发测试】"
echo "--- 测试 http://127.0.0.1/api/store/tools/ ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1/api/store/tools/ 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "[OK] Nginx API 转发正常 (HTTP 200)"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "[FAIL] Nginx 未监听 80 端口"
else
    echo "[FAIL] Nginx 转发异常 (HTTP $HTTP_CODE)"
fi
echo

echo "--- 测试 http://127.0.0.1/ (前端首页) ---"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://127.0.0.1/ 2>/dev/null)
if [ "$HTTP_CODE" = "200" ]; then
    echo "[OK] 前端首页正常 (HTTP 200)"
elif [ "$HTTP_CODE" = "403" ]; then
    echo "[FAIL] 前端首页 403 Forbidden - dist 目录权限问题"
    echo "修复: chmod -R 755 $PROJECT_DIR/vue-frontend/dist"
elif [ "$HTTP_CODE" = "404" ]; then
    echo "[FAIL] 前端首页 404 - dist/index.html 不存在"
    echo "修复: cd $PROJECT_DIR/vue-frontend && npm run build"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "[FAIL] Nginx 未监听 80 端口"
else
    echo "[FAIL] 前端首页异常 (HTTP $HTTP_CODE)"
fi
echo

# 6. Nginx 配置检查
echo "【6. Nginx 配置检查】"
if [ -f "$NGINX_BIN" ]; then
    echo "--- Nginx 配置语法检查 ---"
    if $NGINX_BIN -t 2>&1; then
        echo "[OK] Nginx 配置语法正确"
    else
        echo "[FAIL] Nginx 配置语法错误"
    fi
    echo

    echo "--- 主配置 include 规则 ---"
    grep -n "include" /www/server/nginx/conf/nginx.conf 2>/dev/null | head -10
    echo

    echo "--- 检查 hub.conf 是否存在 ---"
    if [ -f "$NGINX_VHOST/hub.conf" ]; then
        echo "[OK] hub.conf 存在: $NGINX_VHOST/hub.conf"
        echo "--- hub.conf 内容（前 20 行）---"
        head -20 "$NGINX_VHOST/hub.conf"
    else
        echo "[FAIL] hub.conf 不存在"
        echo "修复: cp $PROJECT_DIR/nginx_bt.conf $NGINX_VHOST/hub.conf"
    fi
fi
echo

# 7. 文件检查
echo "【7. 关键文件检查】"
echo "--- 前端 dist 目录 ---"
if [ -d "$PROJECT_DIR/vue-frontend/dist" ]; then
    echo "[OK] dist 目录存在"
    ls -la "$PROJECT_DIR/vue-frontend/dist/" | head -10
    echo
    if [ -f "$PROJECT_DIR/vue-frontend/dist/index.html" ]; then
        echo "[OK] index.html 存在"
    else
        echo "[FAIL] index.html 不存在 - 需要重新构建前端"
        echo "修复: cd $PROJECT_DIR/vue-frontend && npm run build"
    fi
else
    echo "[FAIL] dist 目录不存在 - 前端未构建"
    echo "修复: cd $PROJECT_DIR/vue-frontend && npm install && npm run build"
fi
echo

echo "--- Django 静态文件目录 ---"
if [ -d "$PROJECT_DIR/hub/static" ]; then
    echo "[OK] static 目录存在"
else
    echo "[WARN] static 目录不存在 - 需要收集静态文件"
    echo "修复: cd $PROJECT_DIR/hub && ../venv/bin/python manage.py collectstatic --noinput"
fi
echo

echo "--- Django media 目录 ---"
if [ -d "$PROJECT_DIR/hub/media" ]; then
    echo "[OK] media 目录存在"
else
    echo "[WARN] media 目录不存在（上传文件需要）"
    echo "修复: mkdir -p $PROJECT_DIR/hub/media"
fi
echo

# 8. 防火墙检查
echo "【8. 防火墙检查】"
if command -v firewall-cmd &>/dev/null; then
    echo "--- firewalld 状态 ---"
    if systemctl is-active firewalld &>/dev/null; then
        echo "[INFO] firewalld 运行中"
        echo "已开放端口:"
        firewall-cmd --list-ports 2>/dev/null
        echo
        if firewall-cmd --query-port=80/tcp &>/dev/null; then
            echo "[OK] 80 端口已开放"
        else
            echo "[FAIL] 80 端口未开放"
            echo "修复: firewall-cmd --permanent --add-port=80/tcp && firewall-cmd --reload"
        fi
    else
        echo "[WARN] firewalld 未运行"
    fi
elif command -v iptables &>/dev/null; then
    echo "--- iptables 规则 ---"
    iptables -L -n | grep -E "80|8000" | head -5
fi
echo

# 9. 日志检查
echo "【9. 错误日志检查】"
echo "--- Nginx hub 错误日志 ---"
if [ -f "/www/wwwlogs/hub_error.log" ]; then
    echo "最近 10 行:"
    tail -10 /www/wwwlogs/hub_error.log
else
    echo "[INFO] /www/wwwlogs/hub_error.log 不存在"
fi
echo

echo "--- Gunicorn 日志 ---"
journalctl -u hub --no-pager -n 10 2>/dev/null || echo "[INFO] 无 systemd 日志"
echo

# 10. 诊断结论
echo "=========================================="
echo "  诊断结论"
echo "=========================================="

FAIL_COUNT=0
if ! netstat -tlnp 2>/dev/null | grep -q ":8000"; then
    echo "[问题] Gunicorn 未监听 8000 端口"
    FAIL_COUNT=$((FAIL_COUNT+1))
fi
if ! netstat -tlnp 2>/dev/null | grep -q ":80 "; then
    echo "[问题] Nginx 未监听 80 端口"
    FAIL_COUNT=$((FAIL_COUNT+1))
fi
if [ ! -f "$NGINX_VHOST/hub.conf" ]; then
    echo "[问题] Nginx 站点配置不存在"
    FAIL_COUNT=$((FAIL_COUNT+1))
fi
if [ ! -f "$PROJECT_DIR/vue-frontend/dist/index.html" ]; then
    echo "[问题] 前端未构建"
    FAIL_COUNT=$((FAIL_COUNT+1))
fi
if command -v firewall-cmd &>/dev/null && systemctl is-active firewalld &>/dev/null; then
    if ! firewall-cmd --query-port=80/tcp &>/dev/null; then
        echo "[问题] 防火墙未开放 80 端口"
        FAIL_COUNT=$((FAIL_COUNT+1))
    fi
fi

if [ $FAIL_COUNT -eq 0 ]; then
    echo
    echo "[OK] 所有检查通过！"
    echo "如果仍无法访问，请检查腾讯云安全组是否开放 80 端口"
    echo "腾讯云控制台 -> 轻量应用服务器/云服务器 -> 防火墙/安全组 -> 添加规则"
else
    echo
    echo "发现 $FAIL_COUNT 个问题，请按上述提示修复"
fi
echo
echo "=========================================="
