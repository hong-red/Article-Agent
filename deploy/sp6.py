import requests,json,os

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"
GHT=os.environ.get("GHT","")
REPO="hong-red/Article-Agent"
if not GHT:
    print("ERROR: set GHT env var");exit(1)

PHOTOS=["deploy/article6/p1.jpg","deploy/article6/p2.jpg","deploy/article6/p3.jpg"]

HTML_CONTENT="""<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333;line-height:1.8;font-size:16px;max-width:680px;margin:0 auto;padding:0 16px;">

<section style="text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0;">
  <section style="display:inline-block;font-size:12px;color:#3a8a8a;border:1px solid #3a8a8a;padding:4px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:2px;">调研笔记</section>
  <h1 style="font-size:26px;font-weight:700;line-height:1.4;margin-bottom:12px;color:#222;">五个渔村，一个结论：平谷的鱼需要一条新路</h1>
  <p style="font-size:14px;color:#888;margin-bottom:12px;">四天、五个村庄、十几次访谈——我们看到了什么？</p>
  <p style="font-size:13px;color:#999;">数智渔韵 | 2026年7月18日 | 千人百村实践队</p>
</section>

<section style="font-size:16px;line-height:2;color:#333;margin-bottom:32px;padding:20px;background:#f8f6f3;border-left:4px solid #3a8a8a;">
  7月14日到17日，我们走遍了平谷区马昌营镇的五个渔村——北定福、东双营、天井、马昌营、王各庄。和十几个养殖户聊了天，看了几十口鱼塘。这篇文章不讲单个村的故事，只讲我们发现的东西。
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第一个发现：鱼价，十年没动过</h2>

<p style="margin-bottom:16px;text-align:justify;">五个村的鱼价几乎一模一样——每斤7到9块钱。养殖户说，这个价跟十年前差不多。</p>

<p style="margin-bottom:16px;text-align:justify;">但十年间，饲料涨了，电费涨了，药品涨了，人工更涨了。成本在涨，售价没涨，利润自然越来越薄。</p>

<p style="margin-bottom:16px;text-align:justify;">鱼去了哪里？马昌营村的老侯说得很直白："专业贩子来收，贩子往网上挂，大小都收。"贩子以7到9块收走，转手在网上卖15到25块。差价，全在中间环节。</p>

<p style="margin-bottom:16px;text-align:justify;">五个村、五个不同的镇子，销售模式几乎完全一样：养殖户→鱼贩子→市场。没有一家有自己独立的销售渠道。</p>

<section style="margin:24px 0;padding:20px;background:#fff8e1;border-radius:8px;border-left:4px solid #f0a830;">
  <p style="margin:0;font-size:15px;color:#6b5b00;"><strong>一句话：</strong>养鱼的不如卖鱼的，卖鱼的不如网上卖鱼的。</p>
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第二个发现：没有人接班</h2>

<p style="margin-bottom:16px;text-align:justify;">我们访谈的养殖户，全部50岁以上。没有一个是年轻人。</p>

<p style="margin-bottom:16px;text-align:justify;">东双营的老赵，孩子在外打工，过年才回来。马昌营的老侯，儿子在北京上班。天井村的养殖户说得更直："没有年轻人搞这个。"</p>

<p style="margin-bottom:16px;text-align:justify;">为什么？收入不稳定，一年可能只挣五六万；劳动强度大，每天凌晨四点就得起来巡塘；社会地位低，"养鱼的说出去不好听"。年轻人不是不愿意吃苦，而是看不到希望。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第三个发现：设备，停在了"增氧机时代"</h2>

<p style="margin-bottom:16px;text-align:justify;">五个村，唯一的标配设备就是增氧机。自动投喂机？没人买，"太贵了"——3000到4000块一台。水质检测？靠试纸。鱼病诊断？靠眼睛看，严重了才请"鱼大夫"。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_1" alt="水质问题" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">马昌营村鱼塘水面泡沫——水质管理缺乏标准化方案</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">东双营的老赵是个例外。他投入了200多万添置智能设备，是唯一"敢花钱"的人。但他的评价是："纯利不高。"投入大、回报不确定，这让其他养殖户更加犹豫。</p>

<p style="margin-bottom:16px;text-align:justify;">唯一用上"智能设备"的是王各庄的一位养殖户——手机上的"塘管家"APP，年费100多块。但他说："岁数大的不会用。"</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第四个发现：天井村，一个值得关注的"异类"</h2>

<p style="margin-bottom:16px;text-align:justify;">五个村中，天井村是唯一一个有自己的水质管理方案的。他们用光合细菌调节水质，尾水排进藕池循环利用，形成了一个"鱼—藕"生态闭环。两个专门的藕塘，除了净水还额外产出莲藕。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_2" alt="养殖场全景" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">天井村鱼塘渔船作业——生态养殖模式的日常</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">天井村还是唯一有微信销售渠道的——虽然只是"老板收货+微信导鱼"的初步尝试，但已经迈出了脱离中间商的第一步。</p>

<p style="margin-bottom:16px;text-align:justify;">光合细菌不是高科技产品，操作门槛低，普通养殖户简单培训就能掌握。藕塘可以利甩现有闲置坑塘。这个模式成本低、易复制——是五个村中最有推广价值的。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第五个发现：隔壁的"宠物村"给了我们一个参照</h2>

<p style="margin-bottom:16px;text-align:justify;">调研东双营的时候，我们发现了一件有意思的事：这个村的主要产业已经不是渔业了，而是宠物文化。</p>

<p style="margin-bottom:16px;text-align:justify;">就在鱼塘几公里外，建了一个叫"宠想里"的宠物文化产业园。园区里有宠物食品生产企业、宠物主题咖啡空间，还有大型仓储物流中心。最关键的是——他们搞了一套"生产→仓储→直播带货→物流配送"的完整链条。</p>

<p style="margin-bottom:16px;text-align:justify;">单场直播销售额，最低50万，最高能到300万，直接卖空库存。</p>

<p style="margin-bottom:16px;text-align:justify;">请注意：这和我们调研的渔业，在同一个镇上。同样的平谷、同样的北京郊区、同样距离城区1.5小时车程。一个已经完成了数字化全链路，另一个还停在"贩子收鱼"的原始阶段。</p>

<section style="margin:24px 0;padding:20px;background:#e8f5e9;border-radius:8px;border-left:4px solid #4caf50;">
  <p style="margin:0;font-size:15px;color:#1b5e20;"><strong>一个思考：</strong>如果渔业也能"产地直发+直播电商"，平谷距北京城区1.5小时，"当日捕捞、当日送达"完全可行。宠物产业能做到的事，渔业为什么不能？</p>
</section>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">养殖户不是不想变，是不知道怎么变</h2>

<p style="margin-bottom:16px;text-align:justify;">这篇调研笔记最想说的，其实不是问题，而是一个很容易被忽略的事实：<strong>养殖户一直在尝试改变</strong>。</p>

<p style="margin-bottom:16px;text-align:justify;">老赵花200万买智能设备，是改变。天井村用光合细菌、搞藕池循环，是改变。马昌营的老侯推动散户整合、追求规模化，是改变。</p>

<p style="margin-bottom:16px;text-align:justify;">但他们的尝试是零散的、自发的、缺少系统支持的。没有人告诉他们应该先做什么后做什么，没有人帮他们算一笔"投入产出"的明白账，没有人帮他们对接电商渠道。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_3" alt="养殖场全景" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">马昌营村养殖场全景——增氧机、防鸟网、作业船，设备齐全但智能化程度低</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">我们问老侯："如果有人帮你把鱼挂到网上卖，你愿意吗？"</p>

<p style="margin-bottom:16px;text-align:justify;">他的回答只有三个字：</p>

<p style="font-size:20px;font-weight:700;text-align:center;color:#3a8a8a;margin:24px 0;">"那敢情好。"</p>

<p style="margin-bottom:16px;text-align:justify;">三个字，就是最真实的需求。</p>

<p style="margin-bottom:16px;text-align:justify;">他们不是不想变。他们只是不知道怎么变、不敢一个人变、变不起。</p>

<p style="margin-bottom:16px;text-align:justify;">而这，恰恰是我们这些学智能科学的学生，最应该思考的问题。</p>

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
    cover=upload_thumb(paths[2],token)  # p3 渔船作业作为封面
    if not cover:return

    print("=== Uploading images ===")
    urls=[]
    for p in paths:
        u=upload_img(p,token)
        urls.append(u or "MISSING")

    html=HTML_CONTENT
    for i,u in enumerate(urls):
        html=html.replace(f"IMG_PLACEHOLDER_{i+1}",u)

    articles=[{"title":"五个渔村，一个结论：平谷的鱼需要一条新路","author":"数智渔韵","digest":"四天、五个村庄、十几次访谈。鱼价十年没涨，年轻人全部外流，但养殖户那三个字——'那敢情好'——是我们最想讲的故事。","content":html,"content_source_url":"","thumb_media_id":cover,"need_open_comment":1,"only_fans_can_comment":0}]
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