import requests,json,os,base64

APPID="wxa0748159b59e486c"
SECRET="c52820b965ef16a89bcb52f8da32d3e5"

HTML_CONTENT="""<section style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;color:#333;line-height:1.8;font-size:16px;max-width:680px;margin:0 auto;padding:0 16px;">

<section style="text-align:center;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid #e0e0e0;">
  <section style="display:inline-block;font-size:12px;color:#3a8a8a;border:1px solid #3a8a8a;padding:4px 16px;border-radius:20px;margin-bottom:16px;letter-spacing:2px;">未来展望</section>
  <h1 style="font-size:26px;font-weight:700;line-height:1.4;margin-bottom:12px;color:#222;">数智赋能<br>平谷渔村的未来可能</h1>
  <p style="font-size:14px;color:#888;margin-bottom:12px;">从困局到出路，我们尝试给出一些方向</p>
  <p style="font-size:13px;color:#999;">数智渔韵 | 2026年7月16日 | 千人百村实践队</p>
</section>

<section style="font-size:16px;line-height:2;color:#333;margin-bottom:32px;padding:20px;background:#f8f6f3;border-left:4px solid #3a8a8a;">
  前三篇文章，我们记录了走访的过程、养鱼人的故事，也分析了八个核心发现。这篇是"数智渔韵"系列的收官之作。我们想回答一个问题：<strong>大学生能为平谷渔村做些什么？</strong>
</section>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">一、智能投喂机真的太贵了吗？</h2>

<p style="margin-bottom:16px;text-align:justify;">自动投喂机，三四千一台。对于个体养殖户来说，确实不便宜。但如果我们换个角度算一笔账呢？</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <h4 style="font-size:15px;color:#3a8a8a;margin-bottom:10px;">经济账：自动化投喂 vs 人工投喂</h4>
  <p style="font-size:14px;line-height:2.2;color:#555;margin:0;">
    <strong>人工投喂：</strong>每天2-3次，每次30-60分钟，7-8月高峰期天天不能断<br>
    <strong>自动投喂机：</strong>一次性投入3000-4000元，可使用3-5年<br>
    <strong>分摊成本：</strong>约800-1300元/年，约2-3.5元/天<br>
    <strong>节省时间：</strong>每天1-3小时，可用于巡塘、水质管理等更高价值的工作
  </p>
</section>

<p style="margin-bottom:16px;text-align:justify;">如果按照老侯"16个鱼塘"的规模来算，一台投喂机覆盖3-5个塘，需要4-5台，总投入约1.5-2万元。但每年节省的人工时间超过1000小时。问题不是"贵不贵"，而是<strong>"能不能先看到效果再投入"</strong>。</p>

<p style="margin-bottom:16px;text-align:justify;">这恰恰是可以介入的切入点：引入低成本的试点方案，让一个鱼塘先用起来，用数据说话。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">二、电商卖鱼，到底难在哪里？</h2>

<p style="margin-bottom:16px;text-align:justify;">贩子收鱼7-9元一斤，消费者买鱼15-25元一斤。差价有10-16元。如果养殖户能直接面向消费者，利润可以翻倍。</p>

<p style="margin-bottom:16px;text-align:justify;">但我们不能简单地说"开个网店就行了"。养殖户面临的现实障碍是：</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <p style="font-size:14px;line-height:2.2;color:#555;margin:0;">
    <strong style="color:#3a8a8a;">技术门槛</strong> — 不会开店、不会拍照、不会写文案、不会打包发货<br>
    <strong style="color:#3a8a8a;">物流问题</strong> — 活鱼运输需要专业设备，死鱼损耗率高<br>
    <strong style="color:#3a8a8a;">时间成本</strong> — 养鱼已经占用了全部精力，没有多余时间做电商<br>
    <strong style="color:#3a8a8a;">信任缺失</strong> — 没有品牌背书，消费者凭什么买你的鱼？<br>
    <strong style="color:#3a8a8a;">规模不足</strong> — 单户产量有限，难以形成稳定的供应链
  </p>
</section>

<p style="margin-bottom:16px;text-align:justify;">所以，可行的方案不是让每个养殖户都去开网店，而是<strong>建立统一的品牌和运营平台</strong>——由一个团队来负责品牌、电商、物流，养殖户只需要专心把鱼养好。</p>

<p style="margin-bottom:16px;text-align:justify;">平谷距北京城区仅1.5小时车程，"当日捕捞、当日送达"的生鲜模式完全可行。这比从南方空运鱼到北京，成本低得多，新鲜度也高得多。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">三、天井村的生态模式值得推广</h2>

<p style="margin-bottom:16px;text-align:justify;">在四个村子的走访中，天井村的养殖方式最让我们眼前一亮。</p>

<p style="margin-bottom:16px;text-align:justify;">他们使用光合细菌调节水质，增加含氧量；尾水不直接排放，而是排到藕池里循环利用；两个鱼塘专门种藕，形成了"鱼-藕"生态循环。这种方式不仅环保，还额外产出了莲藕，增加了一份收入。</p>

<p style="margin-bottom:16px;text-align:justify;">更关键的是，这个方法<strong>成本低</strong>。光合细菌不是昂贵的高科技产品，操作也不复杂。对于其他村子来说，这是一个可以快速复制的方案。</p>

<p style="margin-bottom:16px;text-align:justify;">如果能把天井村的经验系统化、标准化，形成一套"平谷生态养鱼指南"，推广到周边更多村庄，整个区域的养殖水平都能上一个台阶。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">四、休闲渔业：被低估的潜力</h2>

<p style="margin-bottom:16px;text-align:justify;">东双营村的35亩建设用地规划虽然搁浅了，但"城里人来钓鱼、吃鱼、体验渔村生活"这个方向并没有错。</p>

<p style="margin-bottom:16px;text-align:justify;">北京有超过2000万常住人口，周末休闲消费需求巨大。平谷本身就有桃花节、大桃采摘等成熟的乡村旅游基础。渔业完全可以融入这个体系——"夏赏荷花秋品鱼"，和现有旅游线路形成互补。</p>

<p style="margin-bottom:16px;text-align:justify;">但休闲渔业不能只是"找个鱼塘让人钓鱼"。它需要：</p>

<section style="margin:24px 0;padding:16px 20px;background:#f0f7f7;border:1px solid #cde5e5;">
  <p style="font-size:14px;line-height:2.2;color:#555;margin:0;">
    <strong style="color:#3a8a8a;">场景设计</strong> — 不只是钓鱼，而是"渔文化体验"，包括拉网、喂鱼、水质检测等互动环节<br>
    <strong style="color:#3a8a8a;">内容输出</strong> — 养殖户的故事本身就是最好的内容，需要被记录、被传播<br>
    <strong style="color:#3a8a8a;">线上引流</strong> — 通过短视频、社交平台吸引城市消费者<br>
    <strong style="color:#3a8a8a;">产品配套</strong> — 鲜鱼、加工产品（鱼干、鱼酱）、文创周边
  </p>
</section>

<p style="margin-bottom:16px;text-align:justify;">说到底，休闲渔业的本质不是"卖鱼"，而是<strong>卖体验、卖故事、卖一种"向往的生活"</strong>。</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">五、我们（大学生）能做什么？</h2>

<p style="margin-bottom:16px;text-align:justify;">回到最初的问题。作为北京印刷学院"千人百村"实践队，我们不是渔业专家，也不是技术大牛。但我们有自己的优势：</p>

<section style="margin:24px 0;padding-left:16px;border-left:2px solid #d4cfc7;">
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">内容创作能力</p>
    <p style="font-size:15px;color:#333;margin:0;">我们擅长文字、图片、视频的创作和传播。可以帮助渔村建立品牌故事、运营社交媒体、制作宣传内容。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">数字化技能</p>
    <p style="font-size:15px;color:#333;margin:0;">我们可以搭建简单的电商页面、帮助注册和运营网店、设计包装和品牌标识。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">调研和数据整理</p>
    <p style="font-size:15px;color:#333;margin:0;">我们已经完成了四村的基线调研，这些数据可以作为后续项目的决策依据。</p>
  </section>
  <section style="margin-bottom:20px;">
    <p style="font-size:14px;color:#3a8a8a;font-weight:600;margin-bottom:4px;">桥梁作用</p>
    <p style="font-size:15px;color:#333;margin:0;">连接学校的技术资源、政府的政策支持、市场的消费需求，做那个"串联各方"的角色。</p>
  </section>
</section>

<p style="margin-bottom:16px;text-align:justify;">具体来说，我们接下来想做几件事：</p>

<p style="margin-bottom:16px;text-align:justify;"><strong>第一，</strong>为平谷渔村设计一套品牌视觉系统——logo、slogan、产品包装。让"平谷鱼"不再是一个模糊的地理概念，而是一个有辨识度的品牌。</p>

<p style="margin-bottom:16px;text-align:justify;"><strong>第二，</strong>搭建一个简单的线上销售渠道。不需要复杂的电商平台，哪怕只是一个微信小程序或者社群团购，让养殖户的鱼能直接触达消费者。</p>

<p style="margin-bottom:16px;text-align:justify;"><strong>第三，</strong>持续记录和传播。用视频、图文、播客等各种形式，把平谷渔村的故事讲给更多人听。让"数智渔韵"不仅仅是一个暑期实践项目的名字，而是一个持续运营的内容品牌。</p>

<p style="margin-bottom:16px;text-align:justify;"><strong>第四，</strong>推动智能养殖试点。联系学校的工学院、信息工程学院，为至少一个鱼塘引入低成本的智能水质监测方案，用数据验证效果。</p>

<p style="text-align:center;margin:32px 0;color:#ccc;font-size:18px;letter-spacing:8px;">* * *</p>

<h2 style="font-size:20px;font-weight:700;margin-top:40px;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #3a8a8a;color:#222;display:inline-block;">写在最后</h2>

<p style="margin-bottom:16px;text-align:justify;">三天四村的调研结束了，但"数智渔韵"的故事才刚刚开始。</p>

<p style="margin-bottom:16px;text-align:justify;">我们不是来"拯救"渔村的。那些养了几十年鱼的老把式，比我们更懂鱼。我们能做的，是把自己会的那些东西——写文章、拍视频、做设计、写代码——用在需要它们的地方。</p>

<p style="margin-bottom:16px;text-align:justify;">老侯说"那敢情好"的时候，我们看到了一种朴素的期待。他们不是不需要改变，他们只是需要有人帮他们迈出第一步。</p>

<p style="margin-bottom:16px;text-align:justify;">我们愿意做那个帮忙迈出第一步的人。</p>

<p style="margin-bottom:16px;text-align:justify;">如果你也觉得这个故事值得被更多人看到，欢迎关注"数智渔韵"。接下来的日子里，我们会持续记录平谷渔村的每一点变化。</p>

<p style="margin-bottom:16px;text-align:justify;font-weight:700;">我们相信，每一尾鱼都值得一条更好的出路。</p>

<section style="margin-top:40px;padding-top:24px;border-top:1px solid #e0e0e0;text-align:center;">
  <p style="font-size:14px;color:#888;margin-bottom:12px;">北京印刷学院 · 千人百村实践队 · 数智渔韵</p>
  <p style="font-size:13px;color:#999;">关注我们，见证平谷渔村的每一步改变</p>
</section>

</section>"""

GHT=os.environ.get("GHT","")
REPO="hong-red/Article-Agent"
if not GHT:
    print("ERROR: set GHT env var");exit(1)

def dl_cover(path):
    print(f"Downloading cover: {path}")
    headers={"Authorization":"token "+GHT,"Accept":"application/vnd.github.v3.raw"}
    r=requests.get(f"https://api.github.com/repos/{REPO}/contents/{path}",headers=headers,timeout=120)
    if r.status_code!=200:
        print(f"Cover download FAIL: {r.status_code}");return None
    tmp="/tmp/cover4.jpg"
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
    cover_path=dl_cover("deploy/article2/img2.jpg")
    if not cover_path:return
    token=get_token()
    if not token:return
    thumb=upload_thumb(cover_path,token)
    if not thumb:return
    articles=[{"title":"数智赋能：平谷渔村的未来可能","author":"数智渔韵","digest":"智能投喂、电商卖鱼、生态养殖、休闲渔业……从困局到出路，大学生能做什么？","content":HTML_CONTENT,"content_source_url":"","thumb_media_id":thumb,"need_open_comment":1,"only_fans_can_comment":0}]
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