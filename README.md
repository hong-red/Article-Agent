# 智能精灵 · 公众号文章生成器

四步生成公众号文章的本地网页工具：**选题 → 成文 → 选图 → 排版**，支持一键推送到个人公众号草稿箱（可选）。

## ✨ 功能

1. **选题**：输入主题 → DeepSeek 生成多个标题 → 挑选一个
2. **成文**：按标题生成正文，可反复提修改意见迭代（`开头更吸引人` / `语气再活泼些` …）
3. **选图**：本地上传 / 全网搜索（必应图片）挑选配图，选中的图会在排版步骤智能插入正文对应位置
4. **排版**：格式优化 + 自定义美化（配色方案、语气、导语摘要、金句、引导关注）+ AI 智能配图插位
5. **本地库**：SQLite 存记录，Markdown / HTML 存本地文件
6. **推送草稿箱**（可选）：前端自行配置公众号 AppID / AppSecret，一键推到草稿箱

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动（或直接双击 run.bat）
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

浏览器打开 **http://127.0.0.1:8000**。

## ⚙️ 配置

所有配置都在网页右上角「设置」里填，保存在本地 `data/config.json`（已加入 `.gitignore`，不会上传）。

| 配置项 | 说明 |
| --- | --- |
| DeepSeek API Key | 内容生成用，必填 |
| DeepSeek 模型 | `deepseek-chat`（快）/ `deepseek-reasoner`（推理强） |
| 公众号 AppID / AppSecret | 推送到草稿箱用，可选 |
| 作者名 / 原文链接 | 推送草稿时写入，可选 |

## 🔐 推送前必读：公众号 IP 白名单

微信草稿箱接口会校验**调用方公网 IP**，没加白名单会报错：`errcode=40164 invalid ip <你的IP> not in whitelist`。

### 第 1 步 · 找到要加的 IP

- 打开本工具网页 → 右上角「设置」→ 点「**获取本机公网IP**」，会列出本机所有出口 IP 并自动复制第一个。
- 或手动访问 [myip.ipip.net](https://myip.ipip.net) 查看。

> ⚠️ 有些网络（双出口 / 多出口 / 负载均衡）会有**多个公网 IP**，而且不同时刻可能不一样。建议把列出的 IP **全部**加进白名单。

### 第 2 步 · 加入白名单

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 左侧「设置与开发」→「基本配置」→ 页面下方「IP白名单」
3. 点「修改」，把上一步拿到的 IP 逐行填入、保存（一般 1 分钟内生效）

### 第 3 步 · 为什么 IP 要「固定」

白名单绑定的就是公网 IP。**普通家用宽带的公网 IP 通常不是固定的**——重启光猫/路由器、或运营商重新分配后 IP 会变，白名单就失效了。想稳定推送，任选其一：

- 向宽带运营商申请**固定公网 IP**（部分运营商免费/收费提供）；
- 把程序部署到**有固定公网 IP 的服务器**上；
- 每次 IP 变了，重新点「获取本机公网IP」并更新白名单。

> 若使用代理 / VPN，微信看到的是**代理的出口 IP**，需要把代理出口 IP 也加进白名单（或推送时关掉代理）。

## 📂 项目结构

```text
├── app.py              # FastAPI 后端（四步生成 + 本地库 + 图片库 + 推送）
├── llm.py              # DeepSeek 客户端
├── markdown_html.py    # Markdown → 微信内联样式 HTML
├── imagesearch.py      # 全网图片搜索（必应，无需 Key）+ 图片下载
├── wechat.py           # 公众号草稿箱推送（access_token / 素材上传 / draft/add）
├── db.py               # SQLite 本地库
├── config.py           # 配置读写
├── static/             # 网页前端（原生 HTML/CSS/JS）
├── data/               # 本地库 + 生成文件（gitignore）
└── run.bat             # Windows 一键启动
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
| DELETE | `/api/images/{name}` | 删除图片 |
| POST | `/api/images/search` | 全网搜索图片（必应） |
| POST | `/api/images/fetch` | 下载网络图片到本地 |
| GET/POST | `/api/config` | 读取 / 保存设置 |
| POST | `/api/test/llm` | 测试 DeepSeek 连接 |

## 📱 后续

网页版为第一版，后端已做成 REST API 并开启 CORS，后续可直接套 APP 复用同一套接口。
