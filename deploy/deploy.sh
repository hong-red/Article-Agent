#!/usr/bin/env bash
# 妙文 · 公众号文章生成器 —— 一键部署脚本（Ubuntu/Debian/CentOS/OpenCloudOS 通用）
# 在服务器上执行：  bash deploy.sh
# 可选指定端口：    PORT=8080 bash deploy.sh
# 可选访问口令：    ACCESS_PASSWORD=你的口令 bash deploy.sh
set -euo pipefail

REPO_OWNER="${REPO_OWNER:-hong-red}"
REPO_NAME="${REPO_NAME:-Article-Agent}"
APP_DIR="${APP_DIR:-/opt/article-agent}"
PORT="${PORT:-8000}"
ACCESS_PASSWORD="${ACCESS_PASSWORD:-}"

SUDO=""
[ "$(id -u)" -eq 0 ] || SUDO="sudo"

echo "==> [1/6] 安装系统依赖 python3 / venv / pip / git / curl"
if command -v apt-get >/dev/null 2>&1; then
  $SUDO apt-get update -y -qq
  $SUDO apt-get install -y -qq python3 python3-venv python3-pip git curl
elif command -v dnf >/dev/null 2>&1; then
  $SUDO dnf install -y python3 python3-pip python3-venv git curl 2>/dev/null || true
elif command -v yum >/dev/null 2>&1; then
  $SUDO yum install -y python3 python3-pip python3-venv git curl 2>/dev/null || true
else
  echo "!! 未识别的包管理器，请手动装好 python3 / pip / git 后重试" >&2
  exit 1
fi

echo "==> [2/6] 拉取最新代码到 $APP_DIR"
if command -v git >/dev/null 2>&1 && git clone --depth 1 "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" "$APP_DIR" 2>/dev/null; then
  echo "    已通过 git clone 拉取"
else
  echo "    github.com 不可达，改用 codeload 下载源码包"
  tmp_tar="$(mktemp /tmp/article-agent.XXXXXX.tar.gz)"
  curl -fsSL "https://codeload.github.com/${REPO_OWNER}/${REPO_NAME}/tar.gz/refs/heads/main" -o "$tmp_tar"
  mkdir -p "$APP_DIR"
  tar -xzf "$tmp_tar" -C "$APP_DIR" --strip-components=1
  rm -f "$tmp_tar"
fi
$SUDO chown -R "$(id -u):$(id -g)" "$APP_DIR" 2>/dev/null || true

echo "==> [3/6] 创建虚拟环境并安装依赖"
cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/python -m pip install -q --upgrade pip
.venv/bin/pip install -q -r requirements.txt
mkdir -p data

echo "==> [4/6] 写入访问口令（可选）"
if [ -n "$ACCESS_PASSWORD" ]; then
  .venv/bin/python - "$APP_DIR/data/config.json" "$ACCESS_PASSWORD" <<'PY'
import json, sys
p, pw = sys.argv[1], sys.argv[2]
d = {}
try:
    d = json.load(open(p, encoding="utf-8"))
except Exception:
    pass
d["access_password"] = pw
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("    已设置访问口令（网页「设置 → 访问口令」需填同一个）")
PY
else
  echo "    （未设置，/api 无鉴权；建议设 ACCESS_PASSWORD=xxx 重跑）"
fi

echo "==> [5/6] 写入 systemd 服务并启动"
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
echo "==> [6/6] 部署完成 ✅"
IP="$(curl -sS -m 8 https://myip.ipip.net 2>/dev/null | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -1)"
echo ""
echo "    访问地址 : http://${IP}:$PORT"
echo "    ─────────────────────────────────────────────"
echo "    ★ 你的白名单 IP = ${IP}"
echo "      把它加入公众号「IP 白名单」："
echo "      mp.weixin.qq.com → 设置与开发 → 基本配置 → IP白名单"
echo "    ─────────────────────────────────────────────"
echo ""
echo "    查看状态 : sudo systemctl status wechat-agent"
echo "    查看日志 : sudo journalctl -u wechat-agent -f"
echo ""
echo "    接下来两件事："
echo "    1) 在云控制台「安全组」放行 TCP $PORT 端口"
echo "    2) 打开网页 → 右上角「设置」填入 DeepSeek API Key"
