import requests,json,os,re,base64

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"

HTML_CONTENT="""<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333;line-height:1.8;font-size:16px;max-width:680px;margin:0 auto;padding:0 16px;">

<section style="text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0;">
  <section style="display:inline-block;font-size:12px;color:#3a8a8a;border:1px solid #3a8a8a;padding:4px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:2px;">调研纪实</section>
  <h1 style="font-size:26px;font-weight:700;line-height:1.4;margin-bottom:12px;color:#222;">走进平谷渔村<br>一支大学生队伍的三天四村调研纪实</h1>
  <p style="font-size:14px;color:#888;margin-bottom:12px;">从北京印刷学院出发，我们带着镜头和笔记本，走进了平谷的四个村庄</p>
  <p style="font-size:13px;color:#999;">数智渔韵 | 2026年7月16日 | 千人百村实践队</p>
</section>

<section style="font-size:16px;line-height:2;color:#333;margin-bottom:32px;padding:20px;background:#f8f6f3;border-left:4px solid #3a8a8a;">
  我们是北京印刷学院"千人百村"队伍的一支小分队。这个七月，我们用三天时间，走访了平谷区的北定福村、东双营村、天井村和马昌营村。我们想知道：在这片土地上，养鱼这件事，现在到底怎么样了？
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第一天：初探渔村，从北定福村开始</h2>

<p style="margin-bottom:16px;text-align:justify;">7月14日清晨，我们一行人驱车前往平谷。车窗外是熟悉的北京郊区风景，但心里却带着几分忐忑——我们要去的，是一个我们几乎一无所知的领域。</p>

<p style="margin-bottom:16px;text-align:justify;">北定福村是我们调研的第一站。这里的鱼塘并不算多，但足以让我们这些"城里孩子"大开眼界。塘水泛着微光，增氧机在水面上划出规律的波纹，岸边的养殖户正忙着投喂。我们举起相机，记录下这个夏天最初的几帧画面。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="assets/img1_beidingfu.jpg" alt="北定福村鱼塘实景" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">北定福村鱼塘，增氧机在水面划出白色的水花</p>
</section>

<p style="margin-bottom:16px;text-align:justify;">第一天的走访更像是一次"热身"。我们和村民聊天气、聊收成、聊这几年鱼价的起伏。虽然还没有深入到核心问题，但我们已经隐约感觉到：养鱼这件事，远比想象中复杂。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第二天上午：东双营村，宠物产业园旁的养鱼人</h2>

<p style="margin-bottom:16px;text-align:justify;">7月15日，我们来到东双营村。一个出乎我们意料的发现是：这里的主要产业并不是渔业，而是宠物产业园。</p>

<p style="margin-bottom:16px;text-align:justify;">在村干部的带领下，我们见到了村里的养鱼户。250亩鱼塘，分成了大约7块，由村干部带头搭建。我们了解到，这里的养殖体系受雨水影响极大，至今没有形成系统化的管理模式。</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <h4 style="font-size:15px;color:#3a8a8a;margin-bottom:10px;font-weight:700;">东双营村养鱼现状速记</h4>
  <ul style="margin-left:20px;font-size:14px;line-height:2;color:#555;">
    <li>水源：地下水，几乎不换水，尾水靠挑</li>
    <li>设备：配备增氧机，有智能设备</li>
    <li>销售：依赖鱼贩子，无网络销售渠道</li>
    <li>价格：不稳定，每斤7-9元</li>
    <li>困境：投资200多万，纯利不高，成本高</li>
    <li>特殊：养鱼的人变少了，年轻人不愿干</li>
  </ul>
</section>

<p style="margin-bottom:16px;text-align:justify;">"鱼特别好，养鱼的人也特别好。"一位养殖户这样告诉我们。但紧接着，他也道出了心酸：缺钱、缺宣传，35亩建设用地的规划在2020年就提出来了，至今不了了之。鱼病了要上实验室，要药品，这些成本都在无声地吞噬着利润。</p>

<blockquote style="margin:24px 0;padding:16px 20px;background:#f8f6f3;border-left:4px solid #c45c3e;color:#666;font-style:italic;">
  <p style="margin:0;">"7到8月份最忙，要勤溜达，要求高。一批鱼养23天，天天操心。"</p>
</blockquote>

<p style="margin-bottom:16px;text-align:justify;">让我们感到一丝欣慰的是，这里的交通特别方便，村干部也在积极推动产业联动，未来有望发展旅游业。临走时，我们录下了几段访谈视频——那些真实的面孔和声音，是这个夏天最珍贵的收获。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="assets/img2_interview.jpg" alt="东双营村采访场景" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">调研队员与东双营村养殖户交流</p>
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第二天下午：天井村，百亩鱼塘里的坚持</h2>

<p style="margin-bottom:16px;text-align:justify;">下午，我们转场天井村。这里的鱼塘更加分散——5到6个鱼塘，总共百十亩地，每个30到40亩，由不同的养殖户个人承包。</p>

<p style="margin-bottom:16px;text-align:justify;">天井村的养殖户给我们展示了另一种养鱼模式。他们使用光合细菌来调节水质、增加含氧量，尾水则排到藕池里循环利用。两个鱼塘没干，专门用来种藕，形成了简单的生态循环。</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <h4 style="font-size:15px;color:#3a8a8a;margin-bottom:10px;font-weight:700;">天井村养鱼亮点</h4>
  <ul style="margin-left:20px;font-size:14px;line-height:2;color:#555;">
    <li>亩产惊人：草鱼、鲤鱼可达1万斤/亩</li>
    <li>水质管理：光合细菌调节，绿色养殖</li>
    <li>尾水处理：排到藕池，循环利用</li>
    <li>销售渠道：老板收货+微信本地销售，部分企业对接</li>
    <li>困难：渗水严重，鸟类叼鱼，雨水影响大</li>
  </ul>
</section>

<p style="margin-bottom:16px;text-align:justify;">"一年收成不确定，7到8块钱一斤。"一位老养殖户算了算账。鱼苗来源多样，价格各异，孵化技术要看眼力，成活率各不相同。每个品种都需要不同的养殖方式，困难程度远超想象。</p>

<p style="margin-bottom:16px;text-align:justify;">和东双营村一样，天井村也面临着同样的结构性困境：没有年轻人愿意干这个。我们走访的几个鱼塘，养殖户几乎都是中老年人。这是一个让人不得不深思的问题。</p>

<section style="text-align:center;margin:24px 0;">
  <img src="assets/img3_tianjing.jpg" alt="天井村鱼塘" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">天井村鱼塘，水面如镜，倒映着蓝天绿树</p>
</section>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">第三天：马昌营村，十六个鱼塘的坚守</h2>

<p style="margin-bottom:16px;text-align:justify;">7月16日，我们来到最后一站——马昌营村。这里的规模更大：总共16到17个鱼塘，涉及7户散户。不过，已经有部分散户不再养鱼，集中到一块统一经营。</p>

<p style="margin-bottom:16px;text-align:justify;">马昌营村的养殖模式更为综合：既有食用鱼，也有观赏鱼。土地是租赁的，一年一茬，亩产2000多斤。冬天水结冰，鱼卖不掉，这是北方养鱼户共同的难题。</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <h4 style="font-size:15px;color:#3a8a8a;margin-bottom:10px;font-weight:700;">马昌营村访谈要点</h4>
  <ul style="margin-left:20px;font-size:14px;line-height:2;color:#555;">
    <li>规模：16-17个鱼塘，7户散户（部分已整合）</li>
    <li>模式：食用鱼+观赏鱼，租赁土地</li>
    <li>产量：1年1茬，亩产2000多斤</li>
    <li>设备：增氧机使用6-7年，早年有补贴</li>
    <li>鱼苗：自孵化+购买，成活率约90%</li>
    <li>销售：专业贩子来收，贩子挂网销售</li>
    <li>困难：成本高、收入少，水质需频繁调节</li>
  </ul>
</section>

<p style="margin-bottom:16px;text-align:justify;">"水质不好，一下雨就要调水质。"一位养殖户告诉我们。他们用试纸测水质，自己学会了调配。鱼病主要是烂鳃，"吃多了"也会生病。让人意外的是，这里还有"鱼大夫"——专门给鱼看病的人。</p>

<p style="margin-bottom:16px;text-align:justify;">谈到智能化设备，养殖户们很无奈：自动投喂机要三四千元，太贵了，目前还是手动撒药、手动投喂。增氧机用了六七年，早年有补贴，现在是自费维护。</p>

<blockquote style="margin:24px 0;padding:16px 20px;background:#f8f6f3;border-left:4px solid #c45c3e;color:#666;font-style:italic;">
  <p style="margin:0;">"没啥大问题，就是成本高、收入少。"——简单的一句话，道出了整个行业的辛酸。</p>
</blockquote>

<section style="text-align:center;margin:24px 0;">
  <img src="assets/img4_machangying.jpg" alt="马昌营村养殖户补网" style="max-width:100%;display:block;margin:0 auto;">
  <p style="font-size:13px;color:#888;margin-top:8px;font-style:italic;">马昌营村养殖户正在修补渔网</p>
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">三天走访后，我们看到的</h2>

<p style="margin-bottom:16px;text-align:justify;">三天四村，我们带回了满满的素材：采访笔记、访谈视频、实地照片，还有一肚子的问题和思考。</p>

<p style="margin-bottom:16px;text-align:justify;">平谷的渔业养殖，是一个充满矛盾的现实：</p>

<section style="margin:24px 0;padding-left:16px;border-left:2px solid #d4cfc7;">
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">有资源，也有困境</p>
    <p style="font-size:15px;color:#333;margin:0;">地下水充足，交通方便，但雨水影响大、渗水严重、水质不稳定</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">有人才，也在流失</p>
    <p style="font-size:15px;color:#333;margin:0;">养殖户经验丰富，但年轻人不愿接班，老龄化趋势明显</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">有技术，也有门槛</p>
    <p style="font-size:15px;color:#333;margin:0;">增氧机、智能设备、水质检测都有，但自动化设备太贵，小户用不起</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">有产品，缺渠道</p>
    <p style="font-size:15px;color:#333;margin:0;">鱼品质好，但主要靠贩子收购，没有自己的网络销售渠道</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">有规划，难落地</p>
    <p style="font-size:15px;color:#333;margin:0;">旅游联动、产业融合的想法都有，但资金、宣传、建设用地都是问题</p>
  </section>
</section>

<p style="margin-bottom:16px;text-align:justify;">这些问题不是某一个村独有的，而是整个行业面临的共性挑战。作为一支大学生调研队伍，我们无力给出标准答案，但我们可以把看到的一切，真实地记录下来，传递出去。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<p style="margin-bottom:16px;text-align:justify;">回到学校后，我们反复回看那些视频素材，整理采访记录，讨论每一个细节。我们想做的，不只是完成一次暑期实践，而是真正为这些养鱼人做点什么——哪怕只是让更多人知道他们的故事。</p>

<p style="margin-bottom:16px;text-align:justify;">这就是"数智渔韵"的起点。</p>

<section style="margin-top:40px;padding-top:24px;border-top:1px solid #e0e0e0;text-align:center;">
  <p style="font-size:14px;color:#888;margin-bottom:12px;">北京印刷学院 · 千人百村实践队 · 数智渔韵</p>
  <p style="font-size:13px;color:#999;margin-bottom:16px;">关注我们，了解更多平谷渔村的故事</p>
  
  <section style="margin-top:24px;padding:16px;background:#f8f6f3;text-align:left;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:8px;">下期预告</p>
    <p style="font-size:14px;color:#888;margin:0;">《养鱼人的一天》—— 我们将深入东双营村和天井村，讲述几位养殖户的真实故事。他们每天几点起床？怎么判断鱼是否生病？一批鱼从出生到上市要经历什么？敬请期待。</p>
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
    thumb=upload_thumb("img1.jpg",token)
    if not thumb:return
    urls=[]
    for i in range(1,5):
        url=upload_img(f"img{i}.jpg",token)
        urls.append(url or f"assets/img{i}.jpg")
    html=HTML_CONTENT
    for i,u in enumerate(urls,1):
        html=html.replace(f"assets/img{i}_beidingfu.jpg" if i==1 else f"assets/img{i}_interview.jpg" if i==2 else f"assets/img{i}_tianjing.jpg" if i==3 else f"assets/img{i}_machangying.jpg",u)
    html=html.replace("assets/img1.jpg",urls[0]).replace("assets/img2.jpg",urls[1]).replace("assets/img3.jpg",urls[2]).replace("assets/img4.jpg",urls[3])
    articles=[{"title":"Pingyu Fish Village","author":"SZYY","digest":"","content":html,"content_source_url":"","thumb_media_id":thumb,"need_open_comment":1,"only_fans_can_comment":0}]
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
