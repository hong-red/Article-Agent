# 部署到服务器

网页版已经可以部署到一台有**固定公网 IP** 的服务器上，手机/电脑都能通过外网访问，公众号推送也会更稳定（服务器 IP 固定，正好解决「家宽动态 IP 白名单失效」的问题）。

## 一键部署

在服务器终端里执行（需要能 `sudo`，腾讯云轻量服务器默认用户通常是 `lighthouse` 或 `root`）：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/hong-red/Article-Agent/main/deploy/deploy.sh)
```

或者手动：

```bash
git clone https://github.com/hong-red/Article-Agent.git
cd Article-Agent
bash deploy/deploy.sh
```

脚本会自动：装 Python 依赖 → 拉代码到 `/opt/article-agent` → 建虚拟环境装包 → 注册 `wechat-agent` systemd 服务并启动。

> 换端口：`PORT=8080 bash deploy.sh`（默认 8000）。

## 部署后要做的两件事

1. **放行端口**：腾讯云控制台 → 你的实例 → 「安全组」→ 放行 `TCP 8000`（或你指定的端口）。
2. **填密钥**：浏览器打开 `http://<服务器公网IP>:8000` → 右上角「设置」→ 填 DeepSeek API Key（公众号 AppID/AppSecret 也要填）。

## 常用运维命令

```bash
sudo systemctl status wechat-agent        # 看状态
sudo journalctl -u wechat-agent -f        # 看实时日志
sudo systemctl restart wechat-agent       # 重启
# 更新到最新代码：
cd /opt/article-agent && sudo git pull && sudo systemctl restart wechat-agent
```

## ⚠️ 公众号推送的 IP 白名单

服务器公网 IP 是**固定**的，把**服务器公网 IP**（不是本地家宽 IP）加到公众号「IP白名单」即可，一次配置长期有效：

> [mp.weixin.qq.com](https://mp.weixin.qq.com/) → 设置与开发 → 基本配置 → IP白名单 → 加入服务器公网 IP。
