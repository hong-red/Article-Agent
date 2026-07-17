import requests,json,os,base64

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"

HTML_CONTENT="""<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333;line-height:1.8;font-size:16px;max-width:680px;margin:0 auto;padding:0 16px;">

<section style="text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0;">
  <section style="display:inline-block;font-size:12px;color:#3a8a8a;border:1px solid #3a8a8a;padding:4px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:2px;">深度分析</section>
  <h1 style="font-size:26px;font-weight:700;line-height:1.4;margin-bottom:12px;color:#222;">平谷渔业的困局与希望</h1>
  <p style="font-size:14px;color:#888;margin-bottom:12px;">四个村庄、三天走访，我们整理出八个核心发现</p>
  <p style="font-size:13px;color:#999;">数智渔韵 | 2026年7月16日 | 千人百村实践队</p>
</section>

<section style="font-size:16px;line-height:2;color:#333;margin-bottom:32px;padding:20px;background:#f8f6f3;border-left:4px solid #3a8a8a;">
  前两篇文章，我们记录了走访的过程和养鱼人的故事。这一篇，我们想把三天的调研数据摊开来看一看。当四个村庄的信息放在一起时，一些被个体故事遮盖的结构性问题，变得清晰起来。<br><br>以下是我们整理出的八个核心发现。
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现一：鱼价十年没涨，卡在7到9元</h2>

<p style="margin-bottom:16px;text-align:justify;">四个村庄的养殖户，给出的鱼价几乎一模一样：每斤7到9元。这个价格，和十年前相比几乎没有变化。</p>

<p style="margin-bottom:16px;text-align:justify;">但成本呢？饲料涨价了、电费涨价了、药品涨价了、人工更贵了。增氧机一天开到晚，一个月电费就是一笔不小的数字。东双营镇的老赵投了200多万，"纯利不高"四个字道出了所有养殖户的心声。</p>

<p style="margin-bottom:16px;text-align:justify;">鱼价为什么上不去？因为养殖户没有定价权。他们的鱼全部通过鱼贩子收购，贩子给什么价就是什么价。没有自己的品牌，没有直接面向消费者的渠道，鱼的品质再好，也只能按大宗价走。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现二：年轻人全部出走，后继无人</h2>

<p style="margin-bottom:16px;text-align:justify;">这是我们听到最多的一句话："年轻人不愿意干这个。"</p>

<p style="margin-bottom:16px;text-align:justify;">北定福村、东双营村、天井村、马昌营村——四个村子的养殖户，几乎全部在50岁以上。老赵的儿子在城里打工，过年才回来一趟。老侯的孩子也不在身边。没有人接班，是这个行业最根本的危机。</p>

<p style="margin-bottom:16px;text-align:justify;">年轻人不是不愿意留在农村，而是养鱼这件事在当前的条件下，确实留不住人。收入不稳定、劳动强度大、社会地位低、缺乏发展空间。同样的辛苦，在城里能赚更多。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现三：销售渠道单一，利润被中间商拿走</h2>

<p style="margin-bottom:16px;text-align:justify;">四个村庄的销售模式几乎完全相同：<strong>养殖户 → 鱼贩子 → 市场/网络</strong>。</p>

<p style="margin-bottom:16px;text-align:justify;">鱼贩子来收鱼，价格压到7到9元一斤。转手到市场上，消费者买到的价格往往是15到25元。中间的差价，全部被流通环节吃掉了。</p>

<p style="margin-bottom:16px;text-align:justify;">更值得注意的一个细节是：老侯告诉我们，"专业贩子收了以后挂网上卖"。也就是说，贩子们在用养殖户们不会用的电商平台，赚着养殖户们赚不到的差价。</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <h4 style="font-size:15px;color:#3a8a8a;margin-bottom:10px;">四个村庄销售渠道对比</h4>
  <p style="font-size:14px;line-height:2.2;color:#555;margin:0;">
    北定福村：鱼贩子收购<br>
    东双营村：鱼贩子收购，无网络销售<br>
    天井村：老板收货 + 微信本地销售（部分）<br>
    马昌营村：专业贩子收购，贩子挂网销售
  </p>
</section>

<p style="margin-bottom:16px;text-align:justify;">天井村是唯一有"微信本地销售"的村子，但也只是部分。绝大多数鱼的出路，仍然掌握在贩子手里。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现四：设备能用就不换，智能化遥不可及</h2>

<p style="margin-bottom:16px;text-align:justify;">四个村子的养殖户都在用增氧机，这算是唯一的"标配"设备。但状态参差不齐：</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <p style="font-size:14px;line-height:2.2;color:#555;margin:0;">
    东双营村：配备增氧机，有部分智能设备<br>
    天井村：增氧机 + 光合细菌水质调节<br>
    马昌营村：增氧机使用6-7年，早年有补贴，现在自费维护<br>
    北定福村：增氧机运转中
  </p>
</section>

<p style="margin-bottom:16px;text-align:justify;">自动投喂机要三四千元一台，没有一个人买。水质检测靠试纸，凭经验判断。鱼病靠肉眼观察，严重了才找"鱼大夫"。这并非养殖户保守，而是一个简单的经济账：设备投入 > 额外收益。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现五：水质管理全凭经验，缺乏标准化</h2>

<p style="margin-bottom:16px;text-align:justify;">"水质不好，一下雨就要调。"这是老侯的原话。但怎么调？调多少？全凭多年积累的经验。</p>

<p style="margin-bottom:16px;text-align:justify;">天井村是个例外——他们使用光合细菌调节水质，尾水排到藕池循环利用，形成了一个简单的生态闭环。这个方法成本低、效果好，但其他村子并没有采用。</p>

<p style="margin-bottom:16px;text-align:justify;">水质不稳定是一个系统性问题：地下水质量一般，几乎不换水（东双营村），下雨后水质突变，渗水严重（天井村）。没有一个村庄有系统的水质监测方案。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现六：北方养鱼的季节性困境</h2>

<p style="margin-bottom:16px;text-align:justify;">"冬天水结冰，鱼卖不掉。"这是北方养鱼独有的问题。</p>

<p style="margin-bottom:16px;text-align:justify;">南方可以一年多茬，但平谷的养殖户一年只能养一茬。冬天长达数月无法捕捞销售，但增氧机、设备维护、土地租赁的成本不会停止。这意味着他们的"有效营收期"只有大约半年。</p>

<p style="margin-bottom:16px;text-align:justify;">马昌营村的亩产2000多斤，看似不少，但如果除以全年成本和只有半年的销售窗口，利润就被大幅稀释了。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现七：规划不少，落地很难</h2>

<p style="margin-bottom:16px;text-align:justify;">东双营村的35亩建设用地规划，2020年就提出来了。想法很好：搞旅游联动，让城里人来钓鱼、吃鱼、体验渔村生活。但五年过去了，仍然"不了了之"。</p>

<p style="margin-bottom:16px;text-align:justify;">规划落地的障碍是多方面的：资金不足、建设用地审批困难、缺乏运营经验、宣传渠道缺失。村干部有想法，养殖户有意愿，但中间缺少一个能把各方资源串联起来的执行主体。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">发现八：他们不是不想变，是不知道怎么变</h2>

<p style="margin-bottom:16px;text-align:justify;">这是我们最想强调的一个发现。</p>

<p style="margin-bottom:16px;text-align:justify;">老赵添置了智能设备，尝试了高价鱼种。老侯推动了散户整合，尝试规模化经营。天井村引进了光合细菌，搞起了生态循环。他们不是固步自封的"老农民"，他们一直在用自己的方式寻找出路。</p>

<p style="margin-bottom:16px;text-align:justify;">但他们的尝试是零散的、自发的，缺少系统的技术支持和市场指导。老侯说"那敢情好"——当被问到是否愿意把鱼挂到网上卖时，他的回答简单而真诚。</p>

<blockquote style="margin:24px 0;padding:16px 20px;background:#f8f6f3;border-left:4px solid #c45c3e;color:#666;font-style:italic;">
  <p style="margin:0;">"不是不想变，是不知道从哪儿变起。"</p>
</blockquote>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">困局之外，我们看到了什么？</h2>

<p style="margin-bottom:16px;text-align:justify;">八个发现，指向的是一个系统性困局。但如果只看到困局，我们的调研就失去了意义。</p>

<p style="margin-bottom:16px;text-align:justify;">我们同样看到了希望：</p>

<section style="margin:24px 0;padding-left:16px;border-left:2px solid #d4cfc7;">
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">经验是最好的财富</p>
    <p style="font-size:15px;color:#333;margin:0;">老一辈养殖户积累了几十年的经验，对水质、鱼病、饲料的理解，是任何教材都替代不了的。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">生态模式已有雏形</p>
    <p style="font-size:15px;color:#333;margin:0;">天井村的光合细菌+藕池循环，证明绿色养殖在平谷是可行的。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">规模化整合已经开始</p>
    <p style="font-size:15px;color:#333;margin:0;">马昌营村从7户散户走向统一经营，说明行业自我优化的趋势已经出现。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">地理位置有优势</p>
    <p style="font-size:15px;color:#333;margin:0;">平谷距北京城区仅1.5小时车程，东双营镇交通便利，具备发展休闲渔业的条件。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">养殖户愿意接受改变</p>
    <p style="font-size:15px;color:#333;margin:0;">"那敢情好"三个字，比任何市场调研报告都有说服力。</p>
  </section>
</section>

<p style="margin-bottom:16px;text-align:justify;">困局是真实的，但不是死局。关键在于：有没有人能帮他们把"不知道怎么变"变成"知道怎么变"。</p>

<p style="margin-bottom:16px;text-align:justify;">这就是我们下一篇文章要聊的。</p>

<section style="margin-top:40px;padding-top:24px;border-top:1px solid #e0e0e0;text-align:center;">
  <p style="font-size:14px;color:#888;margin-bottom:12px;">北京印刷学院 · 千人百村实践队 · 数智渔韵</p>
  
  <section style="margin-top:24px;padding:16px;background:#f8f6f3;text-align:left;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:8px;">下期预告</p>
    <p style="font-size:14px;color:#888;margin:0;">《数智赋能：平谷渔村的未来可能》—— 智能投喂机真的太贵了吗？电商卖鱼到底难在哪里？大学生能为渔村做什么？从困局到出路，我们尝试给出一些方向。</p>
  </section>
</section>

</section>"""

GHT=os.environ.get("GHT","")
REPO="hong-red/Article-Agent"
if not GHT:
    print("ERROR: set GHT env var");exit(1)

def dl_cover(path):
    """Download cover image from GitHub via API"""
    print(f"Downloading cover: {path}")
    headers={"Authorization":"token "+GHT,"Accept":"application/vnd.github.v3.raw"}
    r=requests.get(f"https://api.github.com/repos/{REPO}/contents/{path}",headers=headers,timeout=120)
    if r.status_code!=200:
        print(f"Cover download FAIL: {r.status_code}");return None
    tmp="/tmp/cover3.jpg"
    open(tmp,"wb").write(r.content)
    print(f"Cover OK ({len(r.content)//1024}KB)")
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
    if "media_id" in d:print("Cover upload OK");return d["media_id"]
    print("thumb ERR:",d);return None

def main():
    cover_path=dl_cover("deploy/article2/img1.jpg")
    if not cover_path:return
    token=get_token()
    if not token:return
    thumb=upload_thumb(cover_path,token)
    if not thumb:return
    articles=[{"title":"平谷渔业的困局与希望：四个村庄的八个核心发现","author":"数智渔韵","digest":"四个村庄、三天走访，我们把调研数据摊开来看。鱼价为什么上不去？年轻人为什么不回来？八个核心发现，揭开平谷渔业的真实面貌。","content":HTML_CONTENT,"content_source_url":"","thumb_media_id":thumb,"need_open_comment":1,"only_fans_can_comment":0}]
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