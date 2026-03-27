import os
import json
import requests
import urllib3
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException
from dotenv import load_dotenv

# 禁用不安全请求警告（在使用代理且 verify=False 时）
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
            
        # 如果下载成功，尝试上传到微信
        if image_file:
            try:
                print(f"   📤 正在上传图片到微信素材库...")
                # 显式指定文件名 'image.jpg'，解决 40113 unsupported file type 错误
                result = self.client.material.add('image', ('image.jpg', image_file, 'image/jpeg'))
                return result['media_id'], result['url']
            except WeChatClientException as e:
                print(f"   ❌ 微信 API 报错 (上传素材): {e}")
                if "40164" in str(e):
                    print("      💡 提示: 请登录微信公众号后台，将报错中的 IP 地址加入 'IP白名单'。")
            except Exception as e:
                print(f"   ❌ 上传图片到微信失败 (其他原因): {e}")

        # 兜底方案：尝试加载本地默认封面
        print("   🔍 正在尝试使用本地默认封面 (default_cover.jpg)...")
        # 依次检查当前目录和上级目录
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
            print(f"   ❌ 未找到本地默认封面。检查路径：{possible_paths}")
            print("   💡 建议：在 gen_api 或上级目录下放一张名为 default_cover.jpg 的图片作为兜底。")
        
        return None, None

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
            # 兼容性处理：如果 client 没有 draft 属性，则直接调用底层 post 方法
            if hasattr(self.client, 'draft'):
                result = self.client.draft.add(articles)
            else:
                # 直接调用微信草稿箱 API 接口
                # 接口文档: https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
                print("   ℹ️ 检测到较旧版本的 wechatpy，正在使用底层 API 调用草稿箱...")
                result = self.client.post(
                    'draft/add',
                    data={'articles': articles}
                )
            
            # 返回草稿的 media_id
            return result.get('media_id') if isinstance(result, dict) else result
        except WeChatClientException as e:
            print(f"创建草稿失败: {e}")
            return None

    def markdown_to_html(self, markdown_content):
        """简单的 Markdown 转 HTML，微信后台只接受 HTML"""
        import markdown
        # 微信对 HTML 标签有严格限制，这里建议使用基础转换
        # 实际生产中可能需要更复杂的转换逻辑以适配公众号排版
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

    # 1. 处理封面图（微信草稿必须有封面图 thumb_media_id）
    # 尝试从元数据中获取第一张图片作为封面
    thumb_media_id = None
    if 'used_urls' in meta and meta['used_urls']:
        cover_url = meta['used_urls'][0]
        print(f"📸 正在上传封面图...")
        thumb_media_id, _ = publisher.upload_image_from_url(cover_url)
    
    if not thumb_media_id:
        print("⚠️ 未能获取封面图 media_id，请检查网络或图片 URL。")
        return

    # 2. 转换内容为 HTML
    print(f"📝 正在转换格式...")
    html_content = publisher.markdown_to_html(markdown_content)

    # 3. 创建草稿
    print(f"📤 正在提交至微信草稿箱...")
    result = publisher.create_draft(
        title=meta['topic'],
        content=html_content,
        thumb_media_id=thumb_media_id,
        digest=meta.get('abstract', '')
    )

    if result:
        print(f"✅ 同步成功！请登录微信公众号后台草稿箱查看。")
        print(f"草稿 Media ID: {result}")
    else:
        print(f"❌ 同步失败。")

if __name__ == "__main__":
    # 这是一个独立的同步脚本
    import sys
    if len(sys.argv) > 1:
        publish_folder_to_wechat(sys.argv[1])
    else:
        print("请提供文章文件夹路径，例如: python publisher_skeleton.py ./articles/您的文章文件夹")
