import requests,json,os

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"
GHT=os.environ.get("GHT","")
REPO="hong-red/Article-Agent"
if not GHT:
    print("ERROR: set GHT env var");exit(1)

# Photos: 6 new uploads for article 5
PHOTOS=["deploy/article5/p1.jpg","deploy/article5/p2.jpg","deploy/article5/p3.jpg","deploy/article5/p4.jpg","deploy/article5/p5.jpg","deploy/article5/p6.jpg"]

HTML_CONTENT="""<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333;line-height:1.8;font-size:16px;max-width:680px;margin:0 auto;padding:0 16px;">

<section style="text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0;">
  <section style="display:inline-block;font-size:12px;color:#3a8a8a;border:1px solid #3a8a8a;padding:4px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:2px;">渔具图鉴</section>
  <h1 style="font-size:26px;font-weight:700;line-height:1.4;margin-bottom:12px;color:#222;">鱼塘里的那些"硬家伙"</h1>
  <p style="font-size:14px;color:#888;margin-bottom:12px;">一张照片，就是一件养鱼人的"兵器谱"</p>
  <p style="font-size:13px;color:#999;">数智渔韵 | 2026年7月16日 | 千人百村实践队</p>
</section>

<section style="font-size:16px;line-height:2;color:#333;margin-bottom:32px;padding:20px;background:#f8f6f3;border-left:4px solid #3a8a8a;">
  在三天的走访中，除了和养殖户聊天，我们还拍下了大量鱼塘设备的照片。这些"硬家伙"是养鱼人的生产工具，也是他们每天打交道的伙伴。这一篇，我们不讲故事，只看设备——从中你能读出一个行业的真实面貌。
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">增氧机：鱼塘的"呼吸系统"</h2>

<p style="margin-bottom:16px;text-align:justify;">四个村子的鱼塘里，你一定能看到的东西就是增氧机。它几乎是养鱼业最基础的设备——没有之一。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_1" alt="增氧机全景" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">北定福村的鱼塘，三台增氧机同时运转，水面翻起白色浪花</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">增氧机的原理很简单：通过电机带动叶轮高速旋转，把水打向空中，让水和空气充分接触，从而增加水中的溶解氧。鱼密度越高，耗氧越大，增氧机就必须开得越久。</p>

<p style="margin-bottom:16px;text-align:justify;">在东双营镇，增氧机几乎是从早开到晚，一天不停。马昌营村的老侯说，他的增氧机已经用了六七年了，早年买的时候有政府补贴，现在是纯自费维护。电费是一笔不小的开销——"电表转得飞一样快"。</p>

<p style="margin-bottom:16px;text-align:justify;">一台增氧机几千块钱，寿命五到十年。对于小户养殖户来说，这是最大的单项设备投入。自动投喂机要三四千，他们说"太贵了"；但增氧机再贵也得买——因为鱼会缺氧。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_2" alt="增氧机特写" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">增氧机的黄色叶轮和蓝色浮筒，是鱼塘最醒目的"标志物"</p>
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">防鸟网：一场无声的攻防战</h2>

<p style="margin-bottom:16px;text-align:justify;">如果你仔细看鱼塘的上空，你会发现一层层细密的网。这不是渔网，是防鸟网。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_3" alt="防鸟网" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">鱼塘上空拉起的防鸟网，在阳光下几乎透明</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">天井村的养殖户跟我们提到过一个让人头疼的问题："鸟类叼鱼"。白鹭、苍鹭、翠鸟……这些在生态摄影里被拍得美轮美奂的鸟，在养殖户眼里就是"偷鱼贼"。一批鱼苗放下去，被鸟吃掉的比例可不是小数目。</p>

<p style="margin-bottom:16px;text-align:justify;">防鸟网是最直接也最经济的应对方案。用铁杆或木桩在鱼塘四周架起框架，上面覆盖尼龙网眼，把整片鱼塘罩起来。成本不高，效果显著。</p>

<p style="margin-bottom:16px;text-align:justify;">但防鸟网也有烦恼。网用久了会老化破损，需要定期更换。风大的时候可能被吹歪甚至撕裂。有的地方网眼上积了落叶和灰尘，影响透光和通风。不过不管怎么说，这片网是养殖户和鸟类之间最实际的"停火协议"。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">渔船与浮台：水面上的"移动工位"</h2>

<p style="margin-bottom:16px;text-align:justify;">大一点的鱼塘，岸边够不着中间，就需要一条船。我们看到的渔船都很朴素——木板拼成的小划子，没有马达，靠竹篙或桨划行。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_4" alt="木船" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">一艘简易木船停在岸边，船里放着塑料桶和饲料箱</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">船的主要用途不是"捕鱼"，而是日常管理：撒饲料、巡塘、检查网具、捞死鱼。养殖户每天要在塘上跑好几趟，船就是他们的"水上自行车"。</p>

<p style="margin-bottom:16px;text-align:justify;">比船更有意思的是浮台。下面这张照片里，你能看到一个用废旧铁架、木板和煤气罐拼出来的简易浮台：</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_5" alt="自制浮台" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">养殖户自制的浮台，用废旧煤气罐当浮筒，实用主义满分</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">没错，那四个圆滚滚的灰色东西是废旧煤气罐。把它们密封起来固定在铁架两侧，就有了浮力，上面铺上木板就是一个稳固的平台。浮台的一端还放着一个黑色电箱，可能是增氧机或投喂机的控制面板。</p>

<p style="margin-bottom:16px;text-align:justify;">这种"废物利用"在我们看来可能有点粗糙，但在养殖户眼里，这是最经济的方案。买一个正规浮筒要花不少钱，而煤气罐不要钱（或者几乎不要钱）。实用主义，是养鱼人的基本哲学。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">电力与控制系统：现代化的"神经中枢"</h2>

<p style="margin-bottom:16px;text-align:justify;">别看鱼塘在郊外田野里，它们也是要用电的。增氧机、水泵、照明，全靠电力驱动。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_6" alt="控制箱" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">塘边的电线杆和控制箱，为增氧机等设备供电</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">电线从村子里拉出来，沿着塘边的电线杆延伸到各个增氧机的位置。控制箱通常是简单的防水电盒，里面就是开关和接触器。没有什么智能面板、远程控制——要开机就走到电箱前面，手动合闸。</p>

<p style="margin-bottom:16px;text-align:justify;">"要是能手机上控制就好了。"东双营镇的一位养殖户半开玩笑地说过。他不知道的是，市面上已经有物联网控制的增氧机了——可以手机远程开关，还能自动根据溶氧量启停。价格嘛，当然比普通增氧机贵不少。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">从这些"硬家伙"里，我们看到了什么？</h2>

<p style="margin-bottom:16px;text-align:justify;">这些设备看起来简单，甚至有些"土"，但每一件都是养殖户精打细算的结果。</p>

<section style="margin:24px 0;padding-left:16px;border-left:2px solid #d4cfc7;">
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">能省则省</p>
    <p style="font-size:15px;color:#333;margin:0;">煤气罐当浮筒，废铁管当桩子，旧木板当甲板。能用就绝不换新的。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">该花的花</p>
    <p style="font-size:15px;color:#333;margin:0;">增氧机再贵也要买，防鸟网再麻烦也要拉。因为不花的代价更大。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">经验替代技术</p>
    <p style="font-size:15px;color:#333;margin:0;">没有水质传感器？试纸凑合。没有自动投喂？手动撒。没有远程控制？走过去按开关。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">渴望升级</p>
    <p style="font-size:15px;color:#333;margin:0;">"要是能手机控制就好了"——这句话背后，是真实的需求，也是真实的无奈。</p>
  </section>
</section>

<p style="margin-bottom:16px;text-align:justify;">这些"硬家伙"不会说话，但它们讲述的故事，和我们从养殖户口中听到的一样真实。它们是这个行业最朴素的底色——不花哨，但每一件都有存在的理由。</p>

<p style="margin-bottom:16px;text-align:justify;">下次你再吃鱼的时候，也许可以想一想：这条鱼长大的过程中，头顶有一张防鸟网保护它，水里有增氧机给它供氧，有人划着小船每天来看它好几遍。</p>

<p style="margin-bottom:16px;text-align:justify;">养一条鱼，远没有吃一条鱼那么简单。</p>

<section style="margin-top:40px;padding-top:24px;border-top:1px solid #e0e0e0;text-align:center;">
  <p style="font-size:14px;color:#888;margin-bottom:12px;">北京印刷学院 · 千人百村实践队 · 数智渔韵</p>
  <p style="font-size:13px;color:#999;">关注我们，了解更多平谷渔村的故事</p>
</section>

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

    articles=[{"title":"鱼塘里的那些「硬家伙」：一张照片就是一件兵器谱","author":"数智渔韵","digest":"增氧机、防鸟网、渔船、浮台、控制箱……这些设备看起来简单，但每一件都是养殖户精打细算的结果。","content":html,"content_source_url":"","thumb_media_id":cover,"need_open_comment":1,"only_fans_can_comment":0}]
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