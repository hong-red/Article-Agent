#!/usr/bin/env bash
# 智能精灵 · 公众号文章生成器 —— 一键部署脚本（Ubuntu/Debian/CentOS 通用）
# 在服务器上执行：  bash deploy.sh
# 可选指定端口：    PORT=8080 bash deploy.sh
set -euo pipefail

REPO="${REPO:-https://github.com/hong-red/Article-Agent.git}"
APP_DIR="${APP_DIR:-/opt/article-agent}"
PORT="${PORT:-8000}"

SUDO=""
[ "$(id -u)" -eq 0 ] || SUDO="sudo"

echo "==> [1/5] 安装系统依赖 python3 / venv / pip / git"
if command -v apt-get >/dev/null 2>&1; then
  $SUDO apt-get update -y -qq
  $SUDO apt-get install -y -qq python3 python3-venv python3-pip git curl
elif command -v dnf >/dev/null 2>&1; then
  $SUDO dnf install -y python3 python3-pip git curl
elif command -v yum >/dev/null 2>&1; then
  $SUDO yum install -y python3 python3-pip git curl
else
  echo "!! 未识别的包管理器，请手动装好 python3 / pip / git 后重试" >&2
  exit 1
fi

echo "==> [2/5] 拉取最新代码到 $APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
  $SUDO git -C "$APP_DIR" pull --ff-only
else
  $SUDO mkdir -p "$APP_DIR"
  $SUDO git clone "$REPO" "$APP_DIR"
fi
$SUDO chown -R "$(id -u):$(id -g)" "$APP_DIR"

echo "==> [3/5] 创建虚拟环境并安装依赖"
cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt
mkdir -p data

echo "==> [4/5] 写入 systemd 服务并启动"
$SUDO tee /etc/systemd/system/wechat-agent.service >/dev/null <<EOF
[Unit]
Description=WeChat Article Agent (FastAPI)
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/.venv/bin/uvicorn app:app --host 0.0.0.0 --port $PORT
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

$SUDO systemctl daemon-reload
$SUDO systemctl enable wechat-agent
$SUDO systemctl restart wechat-agent

echo ""
echo "==> [5/5] 部署完成 ✅"
echo "    查看状态 : sudo systemctl status wechat-agent"
echo "    查看日志 : sudo journalctl -u wechat-agent -f"
echo "    访问地址 : http://<服务器公网IP>:$PORT"
echo ""
echo "    接下来两件事："
echo "    1) 在腾讯云「安全组」放行 TCP $PORT 端口"
echo "    2) 打开网页 → 右上角「设置」填入 DeepSeek API Key"
