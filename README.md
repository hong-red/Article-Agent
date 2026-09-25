# 妙文 · 公众号文章生成器

四步生成公众号文章的网页工具：**选题 → 成文 → 选图 → 排版**，支持一键推送到个人公众号草稿箱（可选）。

> 网页版面向**技术用户**：自己部署、自己填密钥、数据全在自己机器。一条命令部署，部署完自动告诉你「白名单 IP 是多少」。

## ✨ 功能

1. **选题**：输入主题 → DeepSeek 生成多个标题 → 挑选一个
2. **成文**：按标题生成正文，可反复提修改意见迭代（`开头更吸引人` / `语气再活泼些` …）
3. **选图**：本地上传 / 全网搜索（必应图片）挑选配图，选中的图会在排版步骤智能插入正文对应位置
4. **排版**：格式优化 + 自定义美化（配色、语气、导语摘要、金句、引导关注）+ AI 智能配图插位
5. **本地库**：SQLite 存记录，Markdown / HTML 存本地文件
6. **推送草稿箱**（可选）：前端自行配置公众号 AppID / AppSecret，一键推到草稿箱

## 🚀 一键部署（自己挂后端）

在一台**有固定公网 IP** 的服务器上执行：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/hong-red/Article-Agent/main/deploy/deploy.sh)
```

脚本会自动：装依赖 → 拉代码 → 建虚拟环境 → 注册 systemd 服务并启动，**最后打印你的「白名单 IP」**。

```text
★ 你的白名单 IP = 1.2.3.4
  把它加入公众号「IP 白名单」：mp.weixin.qq.com → 设置与开发 → 基本配置 → IP白名单
```

> 可选：`PORT=8080 ACCESS_PASSWORD=你的口令 bash deploy.sh`（设端口 / 给 API 加访问口令）。

部署后打开 `http://<服务器公网IP>:8000`，右上角「设置」里填你自己的 **DeepSeek API Key** 和公众号 **AppID / AppSecret**。

## 🌐 前端挂 GitHub Pages（可选）

前端是纯静态页面，也可以直接托管到 GitHub Pages，后端仍然自己挂：

1. 仓库 `Settings → Pages → Source` 选 `GitHub Actions`（本仓库已带 `.github/workflows/pages.yml`，push `static/` 后自动发布）。
2. 打开 Pages 地址 → 右上角「设置」→「后端地址」填你自己的 `http://<你的IP>:8000`。

这样前端在 GitHub 上、数据在后端你自己的机器，**不需要任何人提供服务器**。

## 🔐 鉴权

后端支持一个简单的**访问口令**（`access_password`）：

- 部署时 `ACCESS_PASSWORD=xxx bash deploy.sh` 设置；
- 前端「设置 → 访问口令」填同一个即可（存浏览器 localStorage，随每个请求发送）。

适合自己部署的场景，防陌生人访问你的 API（里面有密钥、能触发生成和推送）。

## ⚙️ 配置

所有配置在网页右上角「设置」里填，保存在本地 `data/config.json`（已 `.gitignore`，不上传）。

| 配置项 | 说明 |
| --- | --- |
| 后端地址 | 连哪个后端；留空 = 同源，填 `http://IP:8000` = 连远程后端 |
| 访问口令 | 后端设置了 `access_password` 时填写 |
| DeepSeek API Key | 内容生成用，必填 |
| DeepSeek 模型 | `deepseek-chat`（快）/ `deepseek-reasoner`（推理强） |
| 公众号 AppID / AppSecret | 推送到草稿箱用，可选 |

## 🔐 推送前必读：公众号 IP 白名单

微信草稿箱接口会校验**调用方公网 IP**，没加白名单会报错 `errcode=40164 invalid ip ... not in whitelist`。

1. 部署脚本结束时打印的 `★ 你的白名单 IP`，就是你要加的 IP（服务器出口公网 IP，固定不变）。
2. 加入白名单：`mp.weixin.qq.com` → 设置与开发 → 基本配置 → IP 白名单 → 修改 → 填入该 IP。
3. 家宽公网 IP 多为动态（会变），所以推荐部署到有**固定公网 IP 的服务器**，一次配置长期有效。

## 📂 项目结构

```text
├── app.py              # FastAPI 后端（四步生成 + 本地库 + 图片库 + 推送）
├── llm.py              # DeepSeek 客户端
├── markdown_html.py    # Markdown → 微信内联样式 HTML
├── imagesearch.py      # 全网图片搜索（必应，无需 Key）+ 图片下载
├── wechat.py           # 公众号草稿箱推送（access_token / 素材上传 / draft/add）
├── db.py               # SQLite 本地库
├── config.py           # 配置读写（含 access_password 访问口令）
├── static/             # 网页前端（原生 HTML/CSS/JS，可独立托管到 GitHub Pages）
├── deploy/deploy.sh    # 一键部署脚本（部署完打印白名单 IP）
├── .github/workflows/  # GitHub Pages 发布工作流
└── data/               # 本地库 + 生成文件（gitignore）
```

## 🔌 API 一览

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/generate/titles` | 主题 → 生成标题列表 |
| POST | `/api/generate/content` | 标题 → 生成正文（支持 feedback 迭代） |
| POST | `/api/generate/format` | 格式优化 + 美化 |
| POST | `/api/render` | Markdown → HTML（实时预览） |
| GET/POST/PUT/DELETE | `/api/articles` | 本地库 CRUD |
| POST | `/api/articles/{id}/cover` | 上传封面图 |
| POST | `/api/articles/{id}/push` | 推送到草稿箱 |
| GET/POST | `/api/images` | 图片库：列出 / 上传图片 |
| POST | `/api/images/search` | 全网搜索图片（必应） |
| POST | `/api/images/fetch` | 下载网络图片到本地 |
| GET/POST | `/api/config` | 读取 / 保存设置 |
| GET | `/api/wechat/ip` | 获取本机出口公网 IP |
| GET | `/api/health` | 健康检查（无需口令） |

## 📱 后续

网页版为第一版，后端已做成 REST API 并开启 CORS，后续 App 可直接复用同一套接口。App（面向小白的托管版）单独开仓库，带登录 / 密钥加密 / 数据导出 / 邀请制。
