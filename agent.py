import os
import json
import datetime
import requests
import re
import argparse
from openai import OpenAI
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from docx import Document
except ImportError:
    Document = None

# 解决网络连接问题：排除对 Kimi API 的代理
os.environ["NO_PROXY"] = "api.moonshot.cn"

def extract_text_from_docx(file_path):
    """从 docx 文件中提取纯文本"""
    if not Document or not os.path.exists(file_path):
        return ""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception:
        return ""

def get_knowledge_base(docs_dir):
    """从 Documents 文件夹中提取业务背景知识"""
    knowledge = []
    if not docs_dir or not os.path.exists(docs_dir):
        return ""
    
    all_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(('.docx', '.md')) and not file.startswith('~$'):
                all_files.append(os.path.join(root, file))
    
    priority_keywords = ["定位", "规划", "slogan", "卖点", "audience"]
    def sort_key(path):
        filename = os.path.basename(path).lower()
        for i, kw in enumerate(priority_keywords):
            if kw in filename: return i
        return len(priority_keywords)
    
    all_files.sort(key=sort_key)
    for path in all_files[:5]:
        filename = os.path.basename(path)
        text = extract_text_from_docx(path) if filename.endswith('.docx') else ""
        if not text and filename.endswith('.md'):
            try:
                with open(path, "r", encoding="utf-8") as f: text = f.read()
            except: pass
        if text:
            knowledge.append(f"--- 核心文档: {filename} ---\n{text[:800]}")
    return "\n\n".join(knowledge)

def generate_article(topic, audience, core_features, product_position, history=None):
    """使用 Kimi API (Moonshot) 生成或优化文章正文（支持 Memory 交互）"""
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 MOONSHOT_API_KEY")
        return ""

    client = OpenAI(api_key=api_key, base_url="https://api.moonshot.cn/v1")
    
    # 尝试加载本地知识库以增强文章专业度
    base_dir = os.path.dirname(__file__)
    docs_dir = os.path.join(base_dir, "Documents", "Lark")
    local_knowledge = get_knowledge_base(docs_dir)

    system_prompt = f"""你是一个拥有 100w+ 粉丝的科技大号主笔，擅长撰写极具质感、审美在线的深度长文。

【你的身份】
你代表 CheersAI 团队。产品定位：{product_position}。核心价值：{core_features}。

【业务背景深度参考】
{local_knowledge if local_knowledge else "（基于 AI 办公安全趋势发挥，强调私有化与合规）"}

【写作高标准】
1. 开篇钩子：用具体的办公痛点开场。
2. 结构美学：使用 H2 标题（如：## 01 效率的终点...）、Markdown 引用块（>）。
3. 风格：专业克制，金句频出。
4. 排版：段落极短（1-3行）。

【任务】
如果你收到了修改建议，请基于之前的文章版本进行精准优化，保持风格统一。
"""
    
    if history is None:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请根据选题“{topic}”撰写一篇深度好文。"}
        ]
    else:
        messages = history

    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.7,
            timeout=40.0,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"调用 Kimi API 出错: {str(e)}")
        return ""

def get_image_urls(keywords, count=1):
    """根据关键词获取图片 URL，支持关键词过滤和兜底逻辑"""
    urls = []
    # 使用完整的 User-Agent 伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 1. 关键词预处理：提取英文，过滤掉中文（Unsplash 对中文支持较差）
    safe_keywords = []
    for kw in keywords:
        # 提取英文、数字和空格
        english_kw = " ".join(re.findall(r'[a-zA-Z0-9]+', kw)).strip()
        if english_kw:
            safe_keywords.append(english_kw)
    
    # 2. 准备搜索关键词列表（原始关键词 + 兜底科技感关键词）
    search_kws = safe_keywords + ["technology", "security", "data", "office", "ai", "cyber", "business"]
    
    # 3. 循环搜索，直到满足所需数量
    for kw in search_kws:
        if len(urls) >= count:
            break
        try:
            # 尝试多个图片源
            # 优先使用 Unsplash 提供的随机图接口
            source_url = f"https://source.unsplash.com/1600x900/?{kw}"
            # 或者使用 LoremFlickr 作为 Unsplash 的稳定代理（无需 API Key）
            # source_url = f"https://loremflickr.com/1080/720/{kw}"
            
            response = requests.get(source_url, headers=headers, allow_redirects=True, timeout=10)
            
            if response.status_code == 200:
                final_url = response.url
                # 检查是否获取到了真实的图片（防止重定向到 generic 页面）
                if "images.unsplash.com" in final_url or "loremflickr.com" in final_url:
                    if final_url not in urls:
                        urls.append(final_url)
                        # print(f"成功获取图片 ({kw}): {final_url}")
        except Exception:
            continue
            
    # 4. 如果还是没拿到，最后用一张固定的科技感图片兜底，确保不会没有图片
    if not urls:
        urls.append("https://images.unsplash.com/photo-1518770660439-4636190af475?w=1080&q=80")
            
    return urls[:count]

def insert_images_into_article(article_md, cover_keywords, inline_keywords):
    """在文章中插入封面图和内文配图"""
    # 1. 插入封面图
    cover_urls = get_image_urls(cover_keywords, count=1)
    if cover_urls:
        article_md = f"![cover]({cover_urls[0]})\n\n" + article_md
    
    # 2. 插入内文配图
    inline_urls = get_image_urls(inline_keywords, count=3) # 预取 3 张
    if not inline_urls:
        return article_md, cover_urls + inline_urls

    # 简单的规则：在 H2 标题后插入
    lines = article_md.split("\n")
    new_lines = []
    img_idx = 0
    h2_count = 0
    
    for line in lines:
        new_lines.append(line)
        if line.startswith("## ") and img_idx < len(inline_urls):
            h2_count += 1
            # 在第二个和第三个 H2 标题后插入图片
            if h2_count >= 2:
                new_lines.append(f"\n![image]({inline_urls[img_idx]})")
                img_idx += 1
                
    return "\n".join(new_lines), cover_urls + inline_urls

def main():
    parser = argparse.ArgumentParser(description="公众号文章自动写作与配图工具")
    # 支持位置参数作为主题，同时也支持 --topic
    parser.add_argument("topic_pos", nargs='*', help="选题标题 (作为位置参数)")
    parser.add_argument("--topic", type=str, help="选题标题 (作为可选参数)")
    parser.add_argument("--audience", type=str, default="职场人士、政企员工", help="目标读者")
    parser.add_argument("--features", type=str, default="本地脱敏、私有化部署、开箱即用", help="核心卖点（逗号分隔）")
    parser.add_argument("--position", type=str, default="让AI办公安全又简单", help="产品定位")
    parser.add_argument("--cover_keywords", type=str, help="封面图关键词")
    parser.add_argument("--inline_keywords", type=str, help="内文配图关键词")
    
    args = parser.parse_args()
    
    # 优先从位置参数获取主题，如果没有则从 --topic 获取，最后提示输入
    topic = " ".join(args.topic_pos) if args.topic_pos else args.topic
    if not topic:
        topic = input("请输入选题标题: ")
    audience = args.audience
    features = args.features
    position = args.position
    
    cover_kws = [args.cover_keywords] if args.cover_keywords else ["technology", "office", "security"]
    inline_kws = args.inline_keywords.split(",") if args.inline_keywords else ["AI", "data", "workspace", "cloud"]

    print(f"\n🚀 正在为主题《{topic}》生成文章...")
    
    # 交互式对话历史
    history = [
        {"role": "system", "content": "你是一个拥有 100w+ 粉丝的科技大号主笔，擅长撰写极具质感、审美在线的深度长文。"},
        {"role": "user", "content": f"请根据选题“{topic}”撰写一篇深度好文。"}
    ]
    
    article_content = generate_article(topic, audience, features, position, history=history)
    history.append({"role": "assistant", "content": article_content})

    while True:
        if not article_content:
            print("❌ 生成文章失败。")
            return

        print("\n--- 当前文章预览 ---")
        print(article_content[:500] + "..." if len(article_content) > 500 else article_content)
        
        feedback = input("\n💡 对文章满意吗？您可以输入【修改建议】进行优化，或输入【y】确认并发布，输入【q】退出: ").strip()
        
        if feedback.lower() == 'y':
            break
        elif feedback.lower() == 'q':
            print("已取消发布。")
            return
        else:
            print(f"🔄 正在根据建议“{feedback}”优化文章...")
            history.append({"role": "user", "content": feedback})
            article_content = generate_article(topic, audience, features, position, history=history)
            history.append({"role": "assistant", "content": article_content})

    print("🖼️ 正在获取并插入配图...")
    final_article, used_urls = insert_images_into_article(article_content, cover_kws, inline_kws)

    # 自动生成文件名
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    safe_topic = re.sub(r'[\\/:*?"<>|]', '', topic).replace(' ', '_')
    filename = f"{safe_topic}_{date_str}.md"
    
    # 确保 articles 目录存在
    output_dir = os.path.join(os.path.dirname(__file__), "articles")
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    article_folder = os.path.join(output_dir, safe_topic)
    os.makedirs(article_folder, exist_ok=True)
    
    # 重新定义文件路径到文件夹内
    file_path = os.path.join(article_folder, "article.md")
    meta_path = os.path.join(article_folder, "meta.json")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_article)
    
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "topic": topic,
            "created_at": date_str,
            "audience": audience,
            "core_features": features,
            "product_position": position,
            "used_urls": used_urls
        }, f, indent=4, ensure_ascii=False)

    print("\n✅ 生成成功！")
    print(f"📄 文件路径: {file_path}")
    
    # 询问是否同步到微信
    sync_choice = input("\n是否现在同步到微信草稿箱？(y/n): ").lower()
    if sync_choice == 'y':
        try:
            from publisher_skeleton import publish_folder_to_wechat
            publish_folder_to_wechat(article_folder)
        except Exception as e:
            print(f"同步失败: {e}")

if __name__ == "__main__":
    main()
