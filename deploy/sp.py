import requests,json,re,sys,os

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"
HTML_CONTENT="\n<div class=\"container\">\n\n  <!-- Header -->\n  <header class=\"article-header\">\n    <div class=\"tag\">调研纪实</div>\n    <h1>走进平谷渔村<br>一支大学生队伍的三天四村调研纪实</h1>\n    <p class=\"subtitle\">从北京印刷学院出发，我们带着镜头和笔记本，走进了平谷的四个村庄</p>\n    <div class=\"meta\">\n      <span>数智渔韵</span>\n      <span>|</span>\n      <span>2026年7月16日</span>\n      <span>|</span>\n      <span>千人百村实践队</span>\n    </div>\n  </header>\n\n  <!-- Lead -->\n  <div class=\"lead\">\n    我们是北京印刷学院\"千人百村\"队伍的一支小分队。这个七月，我们用三天时间，走访了平谷区的北定福村、东双营村、天井村和马昌营村。我们想知道：在这片土地上，养鱼这件事，现在到底怎么样了？\n  </div>\n\n  <!-- Day 1 -->\n  <h2>第一天：初探渔村，从北定福村开始</h2>\n\n  <p>7月14日清晨，我们一行人驱车前往平谷。车窗外是熟悉的北京郊区风景，但心里却带着几分忐忑——我们要去的，是一个我们几乎一无所知的领域。</p>\n\n  <p>北定福村是我们调研的第一站。这里的鱼塘并不算多，但足以让我们这些\"城里孩子\"大开眼界。塘水泛着微光，增氧机在水面上划出规律的波纹，岸边的养殖户正忙着投喂。我们举起相机，记录下这个夏天最初的几帧画面。</p>\n\n  <div class=\"article-img\">\n    <img src=\"assets/img1_beidingfu.jpg\" alt=\"北定福村鱼塘实景\">\n    <div class=\"caption\">北定福村鱼塘，增氧机在水面划出白色的水花</div>\n  </div>\n\n  <p>第一天的走访更像是一次\"热身\"。我们和村民聊天气、聊收成、聊这几年鱼价的起伏。虽然还没有深入到核心问题，但我们已经隐约感觉到：养鱼这件事，远比想象中复杂。</p>\n\n  <div class=\"divider\">* * *</div>\n\n  <!-- Day 2 morning -->\n  <h2>第二天上午：东双营村，宠物产业园旁的养鱼人</h2>\n\n  <p>7月15日，我们来到东双营村。一个出乎我们意料的发现是：这里的主要产业并不是渔业，而是宠物产业园。</p>\n\n  <p>在村干部的带领下，我们见到了村里的养鱼户。250亩鱼塘，分成了大约7块，由村干部带头搭建。我们了解到，这里的养殖体系受雨水影响极大，至今没有形成系统化的管理模式。</p>\n\n  <div class=\"highlight-box\">\n    <h4>东双营村养鱼现状速记</h4>\n    <ul>\n      <li>水源：地下水，几乎不换水，尾水靠挑</li>\n      <li>设备：配备增氧机，有智能设备</li>\n      <li>销售：依赖鱼贩子，无网络销售渠道</li>\n      <li>价格：不稳定，每斤7-9元</li>\n      <li>困境：投资200多万，纯利不高，成本高</li>\n      <li>特殊：养鱼的人变少了，年轻人不愿干</li>\n    </ul>\n  </div>\n\n  <p>\"鱼特别好，养鱼的人也特别好。\"一位养殖户这样告诉我们。但紧接着，他也道出了心酸：缺钱、缺宣传，35亩建设用地的规划在2020年就提出来了，至今不了了之。鱼病了要上实验室，要药品，这些成本都在无声地吞噬着利润。</p>\n\n  <blockquote>\n    <p>\"7到8月份最忙，要勤溜达，要求高。一批鱼养23天，天天操心。\"</p>\n  </blockquote>\n\n  <p>让我们感到一丝欣慰的是，这里的交通特别方便，村干部也在积极推动产业联动，未来有望发展旅游业。临走时，我们录下了几段访谈视频——那些真实的面孔和声音，是这个夏天最珍贵的收获。</p>\n\n  <div class=\"article-img\">\n    <img src=\"assets/img2_interview.jpg\" alt=\"东双营村采访场景\">\n    <div class=\"caption\">调研队员与东双营村养殖户交流</div>\n  </div>\n\n  <!-- Day 2 afternoon -->\n  <h2>第二天下午：天井村，百亩鱼塘里的坚持</h2>\n\n  <p>下午，我们转场天井村。这里的鱼塘更加分散——5到6个鱼塘，总共百十亩地，每个30到40亩，由不同的养殖户个人承包。</p>\n\n  <p>天井村的养殖户给我们展示了另一种养鱼模式。他们使用光合细菌来调节水质、增加含氧量，尾水则排到藕池里循环利用。两个鱼塘没干，专门用来种藕，形成了简单的生态循环。</p>\n\n  <div class=\"highlight-box\">\n    <h4>天井村养鱼亮点</h4>\n    <ul>\n      <li>亩产惊人：草鱼、鲤鱼可达1万斤/亩</li>\n      <li>水质管理：光合细菌调节，绿色养殖</li>\n      <li>尾水处理：排到藕池，循环利用</li>\n      <li>销售渠道：老板收货+微信本地销售，部分企业对接</li>\n      <li>困难：渗水严重，鸟类叼鱼，雨水影响大</li>\n    </ul>\n  </div>\n\n  <p>\"一年收成不确定，7到8块钱一斤。\"一位老养殖户算了算账。鱼苗来源多样，价格各异，孵化技术要看眼力，成活率各不相同。每个品种都需要不同的养殖方式，困难程度远超想象。</p>\n\n  <p>和东双营村一样，天井村也面临着同样的结构性困境：没有年轻人愿意干这个。我们走访的几个鱼塘，养殖户几乎都是中老年人。这是一个让人不得不深思的问题。</p>\n\n  <div class=\"article-img\">\n    <img src=\"assets/img3_tianjing.jpg\" alt=\"天井村鱼塘\">\n    <div class=\"caption\">天井村鱼塘，水面如镜，倒映着蓝天绿树</div>\n  </div>\n\n  <div class=\"divider\">* * *</div>\n\n  <!-- Day 3 -->\n  <h2>第三天：马昌营村，十六个鱼塘的坚守</h2>\n\n  <p>7月16日，我们来到最后一站——马昌营村。这里的规模更大：总共16到17个鱼塘，涉及7户散户。不过，已经有部分散户不再养鱼，集中到一块统一经营。</p>\n\n  <p>马昌营村的养殖模式更为综合：既有食用鱼，也有观赏鱼。土地是租赁的，一年一茬，亩产2000多斤。冬天水结冰，鱼卖不掉，这是北方养鱼户共同的难题。</p>\n\n  <div class=\"highlight-box\">\n    <h4>马昌营村访谈要点</h4>\n    <ul>\n      <li>规模：16-17个鱼塘，7户散户（部分已整合）</li>\n      <li>模式：食用鱼+观赏鱼，租赁土地</li>\n      <li>产量：1年1茬，亩产2000多斤</li>\n      <li>设备：增氧机使用6-7年，早年有补贴</li>\n      <li>鱼苗：自孵化+购买，成活率约90%</li>\n      <li>销售：专业贩子来收，贩子挂网销售</li>\n      <li>困难：成本高、收入少，水质需频繁调节</li>\n    </ul>\n  </div>\n\n  <p>\"水质不好，一下雨就要调水质。\"一位养殖户告诉我们。他们用试纸测水质，自己学会了调配。鱼病主要是烂鳃，\"吃多了\"也会生病。让人意外的是，这里还有\"鱼大夫\"——专门给鱼看病的人。</p>\n\n  <p>谈到智能化设备，养殖户们很无奈：自动投喂机要三四千元，太贵了，目前还是手动撒药、手动投喂。增氧机用了六七年，早年有补贴，现在是自费维护。</p>\n\n  <blockquote>\n    <p>\"没啥大问题，就是成本高、收入少。\"——简单的一句话，道出了整个行业的辛酸。</p>\n  </blockquote>\n\n  <div class=\"article-img\">\n    <img src=\"assets/img4_machangying.jpg\" alt=\"马昌营村养殖户补网\">\n    <div class=\"caption\">马昌营村养殖户正在修补渔网</div>\n  </div>\n\n  <!-- Summary -->\n  <h2>三天走访后，我们看到的</h2>\n\n  <p>三天四村，我们带回了满满的素材：采访笔记、访谈视频、实地照片，还有一肚子的问题和思考。</p>\n\n  <p>平谷的渔业养殖，是一个充满矛盾的现实：</p>\n\n  <div class=\"timeline\">\n    <div class=\"timeline-item\">\n      <div class=\"time\">有资源，也有困境</div>\n      <div class=\"content\">地下水充足，交通方便，但雨水影响大、渗水严重、水质不稳定</div>\n    </div>\n    <div class=\"timeline-item\">\n      <div class=\"time\">有人才，也在流失</div>\n      <div class=\"content\">养殖户经验丰富，但年轻人不愿接班，老龄化趋势明显</div>\n    </div>\n    <div class=\"timeline-item\">\n      <div class=\"time\">有技术，也有门槛</div>\n      <div class=\"content\">增氧机、智能设备、水质检测都有，但自动化设备太贵，小户用不起</div>\n    </div>\n    <div class=\"timeline-item\">\n      <div class=\"time\">有产品，缺渠道</div>\n      <div class=\"content\">鱼品质好，但主要靠贩子收购，没有自己的网络销售渠道</div>\n    </div>\n    <div class=\"timeline-item\">\n      <div class=\"time\">有规划，难落地</div>\n      <div class=\"content\">旅游联动、产业融合的想法都有，但资金、宣传、建设用地都是问题</div>\n    </div>\n  </div>\n\n  <p>这些问题不是某一个村独有的，而是整个行业面临的共性挑战。作为一支大学生调研队伍，我们无力给出标准答案，但我们可以把看到的一切，真实地记录下来，传递出去。</p>\n\n  <div class=\"divider\">* * *</div>\n\n  <!-- Closing -->\n  <p>回到学校后，我们反复回看那些视频素材，整理采访记录，讨论每一个细节。我们想做的，不只是完成一次暑期实践，而是真正为这些养鱼人做点什么——哪怕只是让更多人知道他们的故事。</p>\n\n  <p>这就是\"数智渔韵\"的起点。</p>\n\n  <!-- Footer -->\n  <div class=\"article-footer\">\n    <p class=\"team\">北京印刷学院 · 千人百村实践队 · 数智渔韵</p>\n    <p style=\"font-size:13px;color:var(--muted);margin-bottom:16px;\">关注我们，了解更多平谷渔村的故事</p>\n\n    <div class=\"next-preview\">\n      <h4>下期预告</h4>\n      <p>《养鱼人的一天》—— 我们将深入东双营村和天井村，讲述几位养殖户的真实故事。他们每天几点起床？怎么判断鱼是否生病？一批鱼从出生到上市要经历什么？敬请期待。</p>\n    </div>\n  </div>\n\n</div>\n"

def get_token():
    r=requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+APPID+"&secret="+SECRET)
    d=r.json()
    if "access_token" not in d: print("ERR:",d); sys.exit(1)
    print("Token OK"); return d["access_token"]

def upload_thumb(token):
    print("Uploading cover...")
    with open("/root/wp/img1.jpg","rb") as f:
        r=requests.post("https://api.weixin.qq.com/cgi-bin/material/add_material?access_token="+token+"&type=image",files={"media":("cover.jpg",f,"image/jpeg")})
    d=r.json()
    if "media_id" not in d: print("ERR:",d); sys.exit(1)
    print("Cover OK"); return d["media_id"]

def upload_img(token,name):
    print("Uploading "+name+"...")
    with open("/root/wp/"+name,"rb") as f:
        r=requests.post("https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token="+token,files={"media":(name,f,"image/jpeg")})
    d=r.json()
    if "url" not in d: print("ERR "+name+":",d); return None
    print(name+" OK"); return d["url"]

token=get_token()
thumb=upload_thumb(token)

urls=[]
for n in ["img1.jpg","img2.jpg","img3.jpg","img4.jpg"]:
    u=upload_img(token,n)
    if u: urls.append((n,u))

html=HTML_CONTENT
for fname,url in urls:
    idx=fname.replace(".jpg","").replace("img","")
    local="assets/img"+idx+"_"
    html=re.sub(r'src="'+local+r'[^"]*"','src="'+url+'"',html)

articles=[{"title":"走进平谷渔村：三天四村调研纪实","author":"数智渔韵","digest":"北京印刷学院千人百村实践队，用三天时间走访平谷四个渔村，记录下养鱼人的真实故事。","content":html,"content_source_url":"","thumb_media_id":thumb,"need_open_comment":1,"only_fans_can_comment":0}]
print("Creating draft...")
r=requests.post("https://api.weixin.qq.com/cgi-bin/draft/add?access_token="+token,json={"articles":articles})
d=r.json()
if "media_id" in d:
    print("="*50)
    print("SUCCESS! media_id:",d["media_id"])
    print("="*50)
else:
    print("FAIL:",d)
