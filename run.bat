@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动「妙文 · 公众号文章生成器」...
echo 启动后请用浏览器打开: http://127.0.0.1:8000
start "" http://127.0.0.1:8000
python -m uvicorn app:app --host 127.0.0.1 --port 8000
pause
