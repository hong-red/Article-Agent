import requests,json,os

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"
GHT=os.environ.get("GHT","")
REPO="hong-red/Article-Agent"
if not GHT:
    print("ERROR: set GHT env var");exit(1)

# 9 images used in the article (in order of appearance)
PHOTOS=[
    "deploy/article7/01.jpg",  # 蓝色步道 (封面+首图)
    "deploy/article7/02.jpg",  # 石砌护坡与紫薇花
    "deploy/article7/04.jpg",  # 蓝色步道与垂柳
    "deploy/article7/03.jpg",  # 安昌河畔风光
    "deploy/article7/06.jpg",  # 步道与石砌挡土墙
    "deploy/article7/05.jpg",  # 卵石滩亲子嬉戏
    "deploy/article7/09.jpg",  # 桥下墙绘壁画
    "deploy/article7/11.jpg",  # 桥下市民纳凉
    "deploy/article7/10.jpg",  # 傍晚公园广场
]

HTML_CONTENT="""<section style="font-family:'Noto Serif SC','Songti SC','SimSun',serif;color:#3f3f3f;line-height:1.9;max-width:677px;margin:0 auto;">

<p style="font-size:17px;color:#555;text-align:center;margin-bottom:30px;padding:0 10px;line-height:2;">安昌河畔，新建不久的洞天水岸公园悄然开放。蓝色步道沿河蜿蜒，市民三三两两散步纳凉，孩子们在卵石滩上嬉戏——这里是绵阳涪城区最新的滨水休闲空间，也是家门口的诗和远方。</p>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">作为一个绵阳人，每次回家总想看看这座城市又多了什么新变化。听朋友说安昌河边新修了个公园，趁着傍晚凉快，我便过来走走。</p>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">公园位于滨河南路东段，飞云隧道旁，就在涪城万达广场河对面。作为绵阳"三江六岸"重点打造项目之一，这里原先是安昌河的岸线区域，经过生态景观重塑后，变成了一条约2.3公里的滨水生态廊道，2026年年中正式投用。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_1" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">蓝色塑胶步道沿河延伸，市民散步慢跑各得其乐</p>
</section>

<h2 style="font-size:19px;font-weight:bold;color:#2c5f8a;margin:35px 0 18px;padding-left:14px;border-left:4px solid #4a90d9;line-height:1.5;">蓝色步道，城市里的一抹清凉</h2>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">踏入公园，最先抓住视线的就是那条醒目的蓝色步道。塑胶铺面，弹性适中，中间用白色标线分隔，一侧点缀着圆形标记——既适合散步，也适合慢跑。下午时分，已有不少附近居民在此遛弯，有提着购物袋慢慢走的阿姨，有慢跑锻炼的年轻人，甚至还有人带着小狗出来溜达。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_2" style="width:48%;border-radius:6px;display:inline-block;" />
  <img src="IMG_PLACEHOLDER_3" style="width:48%;border-radius:6px;display:inline-block;margin-left:2%;" />
</section>
<p style="font-size:13px;color:#999;text-align:center;margin-top:8px;margin-bottom:20px;">石砌护坡上紫薇花开，垂柳掩映下的蓝色步道</p>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">步道左侧是高大的石砌护坡，墙体上有镂空装饰，垂柳从墙顶探出枝条，随风轻摆。步道右侧则是开阔的草地，一直延伸到河边。新栽的景观树用木支架固定着，虽然还没有长成浓荫，但已经能看出未来的绿化格局。整个空间开阔而通透，河风穿堂而过，暑气消了大半。</p>

<h2 style="font-size:19px;font-weight:bold;color:#2c5f8a;margin:35px 0 18px;padding-left:14px;border-left:4px solid #4a90d9;line-height:1.5;">安昌河畔，水清岸绿的生态画卷</h2>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">走过步道，来到河边的草坪区域。安昌河在眼前静静流淌，对岸是层叠的山丘和错落的建筑。远处一座蓝色拱桥横跨河面，线条优美，成为整个景观的视觉锚点。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_4" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">河面开阔，对岸山丘连绵，远处蓝色拱桥清晰可见</p>
</section>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">河岸边保留了大片自然植被，芦苇和高草在水边摇曳，几只白鹭偶尔掠过水面。岸上新栽的树木虽然还不高大，但搭配着原有的老树，已经有了层次感。一块云朵形状的蓝色提示牌立在草丛中，写着"水深危险，请勿戏水"——既是安全提醒，也是公园管理细节的体现。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_5" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">石砌老墙与新修步道并行，历史与现代在此交汇</p>
</section>

<h2 style="font-size:19px;font-weight:bold;color:#2c5f8a;margin:35px 0 18px;padding-left:14px;border-left:4px solid #4a90d9;line-height:1.5;">卵石滩上，孩子们的秘密基地</h2>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">继续往前走，河边出现了一片天然的卵石滩。大大小小的鹅卵石铺满了河岸，一条浅浅的水流从石缝间穿过。几个孩子已经迫不及待地脱了鞋，拿着小棍子在水边戳来戳去，旁边的家长一边看着一边笑着聊天。一只黄色的塑料小桶放在石头上，里面大概已经装了几颗"宝贝"鹅卵石。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_6" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">孩子在水边玩耍，家长在一旁守护</p>
</section>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">这种在城市里就能接触自然水岸的设计，在绵阳的公园中并不多见。不需要去远郊，下了班、放了学，走几步就能到河边踩踩石头、听听水声，对孩子来说，这就是最好的"自然课"。</p>

<h2 style="font-size:19px;font-weight:bold;color:#2c5f8a;margin:35px 0 18px;padding-left:14px;border-left:4px solid #4a90d9;line-height:1.5;">桥下别有洞天，墙绘里的市井烟火</h2>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">沿着步道走到桥梁下方，原本以为会是阴暗压抑的桥洞空间，没想到眼前一亮——桥下的一面长墙上画满了彩色壁画。一头卡通舞狮张着大嘴、瞪着大眼睛，喜庆又俏皮；旁边是绵阳城市天际线的剪影，高楼林立；橙色的竖条装饰在灰色水泥墙面上格外醒目。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_7" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">桥下空间的卡通墙绘，为灰色的水泥桥墩增添了一抹亮色</p>
</section>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">桥洞下比想象中凉快得多，几根粗壮的桥墩直插入水，桥壁上留着水位涨落的痕迹。几位阿姨坐在桥下的石头上纳凉，一位穿橙红色衣服的阿姨手里摇着粉色扇子，另一位戴墨镜的年轻姑娘双手抱胸望着河面出神。桥墩遮挡了午后的阳光，河风穿堂而过，这里成了天然的"空调房"。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_8" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">桥下空间成了市民纳凉的好去处</p>
</section>

<h2 style="font-size:19px;font-weight:bold;color:#2c5f8a;margin:35px 0 18px;padding-left:14px;border-left:4px solid #4a90d9;line-height:1.5;">傍晚时分，公园最热闹的时刻</h2>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">临近傍晚，公园里的人渐渐多了起来。步道旁，一辆红色的电动三轮车支起了黑色遮阳棚，卖些小零食和饮品。几个灰色塑料凳围成一圈，两个黑色音箱摆在凳子上，几位大叔已经开始了"露天KTV"——歌声在河面上飘荡，倒也不觉得吵，反而添了几分市井的热闹。</p>

<section style="margin:24px 0;text-align:center;">
  <img src="IMG_PLACEHOLDER_9" style="width:100%;border-radius:6px;display:block;" />
  <p style="font-size:13px;color:#999;margin-top:8px;">傍晚的公园广场，摊贩、KTV、骑车的小朋友，烟火气十足</p>
</section>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">一个小姑娘骑着白色小自行车在广场上晃悠，车轮碾过蓝色的地面标线，咯咯笑着。远处步道上，散步的人三三两两，有的快走锻炼，有的慢悠悠遛狗。这就是绵阳傍晚最真实的模样——没有大城市的匆忙，只有小城市的从容和松弛。</p>

<section style="background:#f0f6fc;border-radius:8px;padding:20px 24px;margin:24px 0;">
  <p style="font-size:13px;color:#4a90d9;font-weight:bold;margin-bottom:6px;">公园小贴士</p>
  <p style="font-size:15px;color:#555;line-height:1.9;">
    地址：滨河南路东段，飞云隧道旁（涪城万达广场河对面）<br/>
    特色：蓝色塑胶步道、卵石滩亲水区、桥下墙绘、运动场地<br/>
    建议：傍晚前往最佳，河风凉爽，人流适中，适合散步、慢跑、亲子游玩
  </p>
</section>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">从蓝色步道到卵石滩，从桥下墙绘到傍晚的露天KTV，洞天水岸公园虽然不大，却装下了绵阳人日常生活的许多切面。它不是那种需要特意"打卡"的网红景点，而是那种你下班后、周末里，随时可以走进去坐一坐的地方。</p>

<p style="font-size:16px;margin-bottom:20px;text-align:justify;">安昌河的水在流，步道上的人在走。这座新建的公园，正在慢慢长成绵阳人生活的一部分。</p>

<p style="text-align:center;margin:36px 0;color:#ccc;font-size:14px;letter-spacing:8px;">· · ·</p>

<p style="text-align:center;font-size:15px;color:#888;margin-bottom:8px;">文 / 摄影 &nbsp;<strong style="color:#4a90d9;">范潇麟</strong></p>
<p style="text-align:center;font-size:13px;color:#bbb;">美丽家乡印象系列 · 绵阳洞天水岸公园</p>

</section>"""

def dl_file(path):
    headers={"Authorization":"token "+GHT,"Accept":"application/vnd.github.v3.raw"}
    r=requests.get(f"https://api.github.com/repos/{REPO}/contents/{path}",headers=headers,timeout=120)
    if r.status_code!=200:
        print(f"  FAIL {path}: {r.status_code}");return None
    tmp=f"/tmp/{os.path.basename(path)}"
    open(tmp,"wb").write(r.content)
    print(f"  OK {path} ({len(r.content)//1024}KB)")
    return tmp

def get_token():
    r=requests.get(f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}",timeout=30)
    d=r.json()
    if "access_token" not in d:
        print("Token ERR:",d);return None
    print("Token OK");return d["access_token"]

def upload_thumb(path,token):
    url=f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"
    with open(path,"rb") as f:
        r=requests.post(url,files={"media":f},timeout=60)
    d=r.json()
    if "media_id" in d:print("Cover OK");return d["media_id"]
    print("thumb ERR:",d);return None

def upload_img(path,token):
    url=f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    with open(path,"rb") as f:
        r=requests.post(url,files={"media":f},timeout=60)
    d=r.json()
    if "url" in d:print(f"  {os.path.basename(path)} OK");return d["url"]
    print(f"  img ERR {path}:",d);return None

def main():
    print("=== Downloading photos ===")
    paths=[]
    for p in PHOTOS:
        tmp=dl_file(p)
        if not tmp:exit(1)
        paths.append(tmp)

    token=get_token()
    if not token:return
    cover=upload_thumb(paths[0],token)
    if not cover:return

    print("=== Uploading images ===")
    urls=[]
    for p in paths:
        u=upload_img(p,token)
        urls.append(u or "MISSING")

    html=HTML_CONTENT
    for i,u in enumerate(urls):
        html=html.replace(f"IMG_PLACEHOLDER_{i+1}",u)

    articles=[{"title":"【美丽家乡印象-绵阳洞天水岸公园】","author":"范潇麟","digest":"安昌河畔，新建不久的洞天水岸公园悄然开放。蓝色步道沿河蜿蜒，市民三三两两散步纳凉，孩子们在卵石滩上嬉戏——这里是绵阳涪城区最新的滨水休闲空间。","content":html,"content_source_url":"","thumb_media_id":cover,"need_open_comment":1,"only_fans_can_comment":0}]
    print("Creating draft...")
    r=requests.post("https://api.weixin.qq.com/cgi-bin/draft/add?access_token="+token,data=json.dumps({"articles":articles},ensure_ascii=False).encode("utf-8"),headers={"Content-Type":"application/json"})
    d=r.json()
    if "media_id" in d:
        print("="*50)
        print("SUCCESS! media_id:",d["media_id"])
        print("="*50)
    else:
        print("FAIL:",d)

if __name__=="__main__":
    main()
