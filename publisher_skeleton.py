import os
import json
import re
import requests
import urllib3
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException
from dotenv import load_dotenv

# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 加载环境变量
load_dotenv()

class WeChatPublisher:
    def __init__(self):
        self.app_id = os.getenv("WECHAT_APP_ID")
        self.app_secret = os.getenv("WECHAT_APP_SECRET")
        if not self.app_id or not self.app_secret:
            raise ValueError("请在 .env 文件中配置 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        
        self.client = WeChatClient(self.app_id, self.app_secret)

    def upload_image_from_url(self, image_url):
        """从 URL 下载图片并上传到微信素材库，返回 media_id"""
        proxies = {
            "http": os.getenv("HTTP_PROXY") or "http://127.0.0.1:7890",
            "https": os.getenv("HTTPS_PROXY") or "http://127.0.0.1:7890"
        }

        image_file = None
        try:
            print(f"   📸 正在下载图片: {image_url}")
            response = requests.get(image_url, proxies=proxies, timeout=15, verify=False)
            if response.status_code == 200:
                from io import BytesIO
                image_file = BytesIO(response.content)
            else:
                print(f"   ⚠️ 图片下载失败，HTTP 状态码: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️ 网络连接失败 (下载图片): {e}")
            
        if image_file:
            try:
                print(f"   📤 正在上传图片到微信素材库...")
                result = self.client.material.add('image', ('image.jpg', image_file, 'image/jpeg'))
                return result['media_id'], result['url']
            except WeChatClientException as e:
                print(f"   ❌ 微信 API 报错 (上传素材): {e}")
                if "40164" in str(e):
                    print("      💡 提示: 请登录微信公众号后台，将报错中的 IP 地址加入 'IP白名单'。")
            except Exception as e:
                print(f"   ❌ 上传图片到微信失败 (其他原因): {e}")

        print("   🔍 正在尝试使用本地默认封面 (default_cover.jpg)...")
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "default_cover.jpg"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "default_cover.jpg")
        ]
        
        local_fallback = None
        for p in possible_paths:
            if os.path.exists(p):
                local_fallback = p
                break
                
        if local_fallback:
            try:
                with open(local_fallback, 'rb') as f:
                    result = self.client.material.add('image', f)
                    print(f"   ✅ 已成功使用本地默认封面: {os.path.basename(local_fallback)}")
                    return result['media_id'], result['url']
            except Exception as e:
                print(f"   ❌ 本地封面上传也失败了: {e}")
        else:
            print(f"   ❌ 未找到本地默认封面。")
        
        return None, None

    def upload_local_image_for_content(self, image_path):
        """上传本地图片到微信，返回可用于文章正文的URL"""
        if not os.path.exists(image_path):
            print(f"   ⚠️ 图片文件不存在: {image_path}")
            return None
        try:
            print(f"   📤 上传正文图片: {os.path.basename(image_path)}")
            with open(image_path, 'rb') as f:
                from io import BytesIO
                img_bytes = BytesIO(f.read())
            result = self.client.post(
                'media/uploadimg',
                files={'media': ('image.jpg', img_bytes, 'image/jpeg')}
            )
            if isinstance(result, dict) and 'url' in result:
                print(f"   ✅ 正文图片上传成功")
                return result['url']
            else:
                print(f"   ⚠️ 正文图片上传返回异常: {result}")
                return None
        except WeChatClientException as e:
            print(f"   ❌ 正文图片上传失败: {e}")
            if "40164" in str(e):
                print("      💡 提示: 请将服务器IP加入微信公众号IP白名单。")
            return None
        except Exception as e:
            print(f"   ❌ 正文图片上传异常: {e}")
            return None

    def upload_local_image_as_material(self, image_path):
        """上传本地图片作为永久素材，返回 (media_id, url)"""
        if not os.path.exists(image_path):
            print(f"   ⚠️ 图片文件不存在: {image_path}")
            return None, None
        try:
            with open(image_path, 'rb') as f:
                result = self.client.material.add('image', ('image.jpg', f, 'image/jpeg'))
                return result['media_id'], result['url']
        except Exception as e:
            print(f"   ❌ 本地素材上传失败: {e}")
            return None, None

    def process_inline_images(self, html_content, article_folder):
        """处理HTML中的本地图片引用，上传到微信并替换URL"""
        def replace_image(match):
            src = match.group(1)
            # 只处理本地相对路径的图片
            if src.startswith('http://') or src.startswith('https://'):
                return match.group(0)
            
            # 构建完整路径
            img_path = os.path.join(article_folder, src)
            wechat_url = self.upload_local_image_for_content(img_path)
            if wechat_url:
                return f'<img src="{wechat_url}" alt="{match.group(2)}" />'
            else:
                print(f"   ⚠️ 图片替换失败，保留原引用: {src}")
                return match.group(0)
        
        # 匹配 <img src="..." alt="..." /> 或 <img src="..." alt="..." >
        pattern = r'<img\s+src="([^"]+)"\s+alt="([^"]*)"\s*/?>'
        processed = re.sub(pattern, replace_image, html_content)
        return processed

    def create_draft(self, title, content, thumb_media_id, author="CheersAI", digest=""):
        """创建草稿箱文章"""
        articles = [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }
        ]
        try:
            if hasattr(self.client, 'draft'):
                result = self.client.draft.add(articles)
            else:
                print("   ℹ️ 使用底层 API 调用草稿箱...")
                result = self.client.post('draft/add', data={'articles': articles})
            return result.get('media_id') if isinstance(result, dict) else result
        except WeChatClientException as e:
            print(f"创建草稿失败: {e}")
            return None

    def markdown_to_html(self, markdown_content):
        """Markdown 转 HTML"""
        import markdown
        html = markdown.markdown(markdown_content, extensions=['extra', 'nl2br'])
        return html

def publish_folder_to_wechat(folder_path):
    """将生成的文件夹内容同步到微信草稿箱"""
    article_path = os.path.join(folder_path, "article.md")
    meta_path = os.path.join(folder_path, "meta.json")

    if not os.path.exists(article_path) or not os.path.exists(meta_path):
        print(f"错误: 在 {folder_path} 未找到文章或元数据。")
        return

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    
    with open(article_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    publisher = WeChatPublisher()
    
    print(f"🚀 开始同步文章: {meta['topic']}")

    # 1. 处理封面图
    thumb_media_id = None
    cover_image = meta.get('cover_image')
    
    if cover_image:
        cover_path = os.path.join(folder_path, cover_image)
        print(f"📸 使用本地封面图: {cover_image}")
        thumb_media_id, _ = publisher.upload_local_image_as_material(cover_path)
    elif 'used_urls' in meta and meta['used_urls']:
        cover_url = meta['used_urls'][0]
        print(f"📸 正在上传封面图...")
        thumb_media_id, _ = publisher.upload_image_from_url(cover_url)
    else:
        print(f"📸 使用本地默认封面...")
        thumb_media_id, _ = publisher.upload_image_from_url("local_default")
    
    if not thumb_media_id:
        print("⚠️ 未能获取封面图 media_id，请检查网络或图片。")
        return

    # 2. 转换内容为 HTML
    print(f"📝 正在转换格式...")
    html_content = publisher.markdown_to_html(markdown_content)

    # 3. 处理正文中的本地图片
    print(f"🖼️ 正在处理正文图片...")
    html_content = publisher.process_inline_images(html_content, folder_path)

    # 4. 创建草稿
    print(f"📤 正在提交至微信草稿箱...")
    result = publisher.create_draft(
        title=meta['topic'],
        content=html_content,
        thumb_media_id=thumb_media_id,
        author=meta.get('author', ''),
        digest=meta.get('abstract', '')
    )

    if result:
        print(f"✅ 同步成功！请登录微信公众号后台草稿箱查看。")
        print(f"草稿 Media ID: {result}")
    else:
        print(f"❌ 同步失败。")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        publish_folder_to_wechat(sys.argv[1])
    else:
        print("请提供文章文件夹路径，例如: python publisher_skeleton.py ./articles/您的文章文件夹")
