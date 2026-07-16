import requests,json,os,sys

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"

HTML_CONTENT="""<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333;line-height:1.8;font-size:16px;max-width:680px;margin:0 auto;padding:0 16px;">

<section style="text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0;">
  <section style="display:inline-block;font-size:12px;color:#3a8a8a;border:1px solid #3a8a8a;padding:4px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:2px;">人物故事</section>
  <h1 style="font-size:26px;font-weight:700;line-height:1.4;margin-bottom:12px;color:#222;">养鱼人的一天<br>三个村庄里，那些关于鱼的坚守与挣扎</h1>
  <p style="font-size:14px;color:#888;margin-bottom:12px;">他们每天四点起床，守着几十亩鱼塘，像守着自家孩子</p>
  <p style="font-size:13px;color:#999;">数智渔韵 | 2026年7月16日 | 千人百村实践队</p>
</section>

<section style="font-size:16px;line-height:2;color:#333;margin-bottom:32px;padding:20px;background:#f8f6f3;border-left:4px solid #3a8a8a;">
  文章发出后，有朋友在后台问："养鱼的人到底过着什么样的日子？"<br><br>我们把这个问题带回了平谷。三天四村，我们见到了十几位养殖户。他们大多五十岁以上，皮肤黝黑，手掌粗糙，说起鱼来眼睛发亮。这篇文章，想讲讲他们的故事。
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">老宋：北定福村的"鱼把式"</h2>

<p style="margin-bottom:16px;text-align:justify;">7月14日，我们调研的第一站是北定福村。老宋是我们在这里见到的第一位养殖户。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_1" alt="北定福村老宋" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">北定福村的老宋，在鱼塘边跟队员们聊起了养鱼的那些事</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">老宋站在塘边，指着眼前的水面跟我们说："你看这个增氧机，得一直开着，鱼才不会缺氧。"塘水在增氧机的搅动下泛着白花，远处几只白鹭低低地掠过水面。</p>

<p style="margin-bottom:16px;text-align:justify;">作为第一天的"热身"走访，我们和老宋聊了很多——聊天气对鱼塘的影响，聊这些年鱼价的起伏，聊村里的年轻人都去了哪里。老宋话不多，但句句实在。</p>

<blockquote style="margin:24px 0;padding:16px 20px;background:#f8f6f3;border-left:4px solid #c45c3e;color:#666;font-style:italic;">
  <p style="margin:0;">"养鱼这活儿，说简单也简单，说难也真难。全靠经验，一代传一代。"</p>
</blockquote>

<p style="margin-bottom:16px;text-align:justify;">离开北定福村时，我们带回了一肚子问题和满相机的素材。但那时我们还不知道，后面两天的走访，会让我们看到更加复杂的现实。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">老赵：250亩鱼塘，一个人的"战场"</h2>

<p style="margin-bottom:16px;text-align:justify;">7月15日一早，我们来到东双营镇。一个出乎意料的发现：这里的主要产业并不是渔业，而是宠物文化产业园。但老赵不搞宠物，他搞鱼。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_2" alt="东双营镇老赵" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">东双营镇的老赵，身后的鱼塘在山区层层叠叠地铺开</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">"7到8月份最忙，要勤溜达，高要求。"老赵一边说，一边领我们往塘边走。250亩鱼塘，分成了7块，由村干部带头搭建，他是承包者之一。受雨水影响大，至今没有形成系统的养殖体系。</p>

<p style="margin-bottom:16px;text-align:justify;">老赵在这里投入了200多万。"纯利不高，需要的成本太高了。"他掰着手指算：鱼苗、饲料、药品、电费——增氧机一天开到晚，电表转得飞一样快。最头疼的是鱼病。"烂鳃，这个病最麻烦。"鱼病了要药品，要上实验室检测，都是额外开销。</p>

<blockquote style="margin:24px 0;padding:16px 20px;background:#f8f6f3;border-left:4px solid #c45c3e;color:#666;font-style:italic;">
  <p style="margin:0;">"鱼特别好，养鱼的人也特别好。就是缺钱，缺宣传。"</p>
</blockquote>

<p style="margin-bottom:16px;text-align:justify;">销售是个更大的问题。老赵的鱼主要卖给鱼贩子，价格不稳定，每斤7到9块钱上下浮动。"没有通过网络卖过鱼，直播什么的更不会。"</p>

<p style="margin-bottom:16px;text-align:justify;">不过，老赵也不是没有尝试过改变。他增加了一些高价的鱼种，也添置了智能设备。35亩建设用地的规划在2020年就提出来了——想搞旅游联动——但至今没有下文。</p>

<p style="margin-bottom:16px;text-align:justify;">"养鱼的人变少了，年轻人不愿意干这个。"老赵望着远处的山说。他的儿子在城里打工，过年才回来一趟。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">老侯：十六个鱼塘，越养越"精打细算"</h2>

<p style="margin-bottom:16px;text-align:justify;">7月16日，我们来到最后一站——马昌营村。老侯是这里的养殖大户，管着十六七个鱼塘，涉及7户散户的地。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="IMG_PLACEHOLDER_3" alt="马昌营村老侯" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">马昌营村的老侯，正在给我们讲解鱼塘的情况</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">"以前各家各户各养各的，现在有部分不养了，集中到一块。"老侯说，"规模化才能降低成本。"他的养殖模式很综合：既有食用鱼，也有观赏鱼。土地是租赁的，一年一茬，亩产2000多斤。</p>

<p style="margin-bottom:16px;text-align:justify;">说到设备，老侯叹了口气："增氧机用了六七年，早年有补贴，现在自费了。"自动投喂机要三四千块一台，他到现在没舍得买，还是手动撒药、手动投喂。</p>

<p style="margin-bottom:16px;text-align:justify;">水质管理上，老侯有自己的土办法。他用试纸测水质，自己学会了看数据。"水质不好，一下雨就要调。地下水，但质量一般。"冬天水结冰，鱼卖不掉，这是北方养鱼户共同的难题。</p>

<blockquote style="margin:24px 0;padding:16px 20px;background:#f8f6f3;border-left:4px solid #c45c3e;color:#666;font-style:italic;">
  <p style="margin:0;">"没啥大问题，就是成本高、收入少。投喂的机器不买，太贵了，还是手动撒吧。"</p>
</blockquote>

<p style="margin-bottom:16px;text-align:justify;">销售上，老侯也是靠贩子来收。"专业贩子收了以后挂网上卖，大小都收，需要就来拿。"他其实知道贩子转手能卖更高的价，但"没办法，没那个渠道"。鱼病主要是烂鳃和吃多了造成的消化问题，不过好在"大病少，小病多"，有公司供应药品，还有专门的"鱼大夫"可以咨询。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">我们看到的，不只是鱼</h2>

<p style="margin-bottom:16px;text-align:justify;">写完这三个人的故事，我们想说的是：他们不是个例。</p>

<p style="margin-bottom:16px;text-align:justify;">在平谷，像老宋、老赵、老侯这样的养殖户还有很多。他们勤恳、坚韧、有经验，但也在时代的洪流中面临着共同的困境：</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <p style="font-size:14px;line-height:2.2;color:#555;margin:0;">
    <strong style="color:#3a8a8a;">老龄化</strong> — 养殖户多数在50岁以上，没有年轻人接班<br>
    <strong style="color:#3a8a8a;">渠道之困</strong> — 主要依赖鱼贩子，网络销售几乎为零<br>
    <strong style="color:#3a8a8a;">成本压力</strong> — 设备贵、药品贵、人工贵，利润薄<br>
    <strong style="color:#3a8a8a;">自然风险</strong> — 雨水、水质、鱼病，每一个都能让一年的辛苦打水漂<br>
    <strong style="color:#3a8a8a;">信息鸿沟</strong> — 知道有直播、有电商，但不知道怎么做，也没有精力学
  </p>
</section>

<p style="margin-bottom:16px;text-align:justify;">但我们也看到了希望。北定福村有像老宋这样经验丰富的老把式；东双营镇交通方便，有望联动旅游业；马昌营村已经开始尝试规模化整合。这些星星点点的变化，也许就是未来的起点。</p>

<p style="margin-bottom:16px;text-align:justify;">我们问老侯，如果有一天，有人帮你们把鱼挂到网上卖，你愿意吗？</p>

<p style="margin-bottom:16px;text-align:justify;">他笑了："那敢情好。"</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<p style="margin-bottom:16px;text-align:justify;">这就是三个养鱼人的一天。他们的故事没有惊天动地，但每一句话都带着泥土和鱼腥味的气息。我们把这些记录下来，是想让更多人知道：在你吃到的每一条鱼背后，都有这样一群人在默默坚守。</p>

<p style="margin-bottom:16px;text-align:justify;font-weight:700;">他们值得被看见。</p>

<section style="margin-top:40px;padding-top:24px;border-top:1px solid #e0e0e0;text-align:center;">
  <p style="font-size:14px;color:#888;margin-bottom:12px;">北京印刷学院 · 千人百村实践队 · 数智渔韵</p>
  
  <section style="margin-top:24px;padding:16px;background:#f8f6f3;text-align:left;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:8px;">下期预告</p>
    <p style="font-size:14px;color:#888;margin:0;">《平谷渔业的困局与希望》—— 我们将调研数据放在一起，整理出八个核心发现：鱼价为什么上不去？年轻人为什么不回来？智能化养殖离平谷有多远？深度分析，敬请期待。</p>
  </section>
</section>

</section>"""

def get_token():
    r=requests.get(f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}",timeout=30)
    d=r.json()
    if "access_token" not in d:
        print("Token ERR:",d);return None
    print("Token OK");return d["access_token"]

def upload_img(path,token):
    url=f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    with open(path,"rb") as f:
        r=requests.post(url,files={"media":f},timeout=60)
    d=r.json()
    if "url" in d:print(f"{os.path.basename(path)} OK");return d["url"]
    print(f"img ERR {path}:",d);return None

def upload_thumb(path,token):
    url=f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"
    with open(path,"rb") as f:
        r=requests.post(url,files={"media":f},timeout=60)
    d=r.json()
    if "media_id" in d:print("Cover OK");return d["media_id"]
    print("thumb ERR:",d);return None

def main():
    token=get_token()
    if not token:return
    thumb=upload_thumb("article2/img1.jpg",token)
    if not thumb:return
    urls=[]
    for i in range(1,4):
        url=upload_img(f"article2/img{i}.jpg",token)
        urls.append(url or f"article2/img{i}.jpg")
    html=HTML_CONTENT
    for i,u in enumerate(urls,1):
        html=html.replace(f"IMG_PLACEHOLDER_{i}",u)
    articles=[{"title":"养鱼人的一天：三个村庄里，那些关于鱼的坚守与挣扎","author":"数智渔韵","digest":"他们每天四点起床，守着几十亩鱼塘。三位养殖户的真实故事，关于鱼的坚守与挣扎。","content":html,"content_source_url":"","thumb_media_id":thumb,"need_open_comment":1,"only_fans_can_comment":0}]
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