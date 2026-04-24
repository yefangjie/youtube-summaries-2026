from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap, os
W,H = 1600,900
BG = "#FFFFFF"
PANEL = "#F8F9FA"
BLUE = "#2563EB"
CORAL = "#F97316"
GREEN = "#10B981"
AMBER = "#F59E0B"
INK = "#1A1A1A"
MUTED = "#4A5568"
DIV = "#D1D5DB"
OUT = Path(os.environ['DECKDIR'])

font_candidates = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
    '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc',
]
regular_path = next((p for p in font_candidates if Path(p).exists() and 'Regular' in p), None)
bold_path = next((p for p in font_candidates if Path(p).exists() and 'Bold' in p), regular_path)
if not regular_path:
    from PIL import ImageFont
    def f(size, bold=False): return ImageFont.load_default()
else:
    def f(size, bold=False): return ImageFont.truetype(bold_path if bold else regular_path, size)

def wrap(text, width):
    lines=[]
    for para in text.split('\n'):
        lines.extend(textwrap.wrap(para, width=width, break_long_words=False) or [''])
    return lines

def draw_header(draw, kicker, title, subtitle=None):
    draw.text((90,65), kicker, font=f(24, True), fill=BLUE)
    y=110
    for line in wrap(title, 15):
        draw.text((90,y), line, font=f(54, True), fill=INK)
        y += 68
    if subtitle:
        y += 10
        for line in wrap(subtitle, 34):
            draw.text((90,y), line, font=f(24, False), fill=MUTED)
            y += 34
    return y

def bullet(draw, x, y, lines, color=BLUE, width=28, textwidth=32, size=28):
    yy=y
    for item in lines:
        draw.rounded_rectangle((x, yy+10, x+12, yy+22), radius=4, fill=color)
        wrapped=wrap(item, textwidth)
        for j,line in enumerate(wrapped):
            draw.text((x+width, yy+j*38), line, font=f(size, False), fill=INK if j==0 else MUTED)
        yy += max(46, len(wrapped)*38 + 8)
    return yy

def footer(draw, n):
    draw.line((90,H-56,W-90,H-56), fill=DIV, width=2)
    draw.text((90,H-42), 'IBM Technology · 视频中文解读', font=f(18,False), fill=MUTED)
    draw.text((W-140,H-42), f'{n}/10', font=f(18,True), fill=MUTED)

def save(img, name):
    img.save(OUT/name)

# slide 1
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img)
for x,c in [(1080,BLUE),(1160,CORAL),(1240,GREEN)]:
    d.rounded_rectangle((x,130,x+18,740), radius=9, fill=c)
for i,y in enumerate([260,390,520]):
    d.rounded_rectangle((960,y,1360,y+82), radius=24, outline=[BLUE,CORAL,GREEN][i], width=4, fill=PANEL)
labels=['入口 / Entry','Intent / 分发','Infra / 成本']
for i,y in enumerate([280,410,540]): d.text((995,y), labels[i], font=f(30,True), fill=INK)
y=draw_header(d,'Mixture of Experts / IBM Technology','IBM 这期播客，讲透了 2026 AI 竞争的三条主线','Apple 入口｜Intent 分发｜Anthropic x AWS 基础设施绑定')
d.rounded_rectangle((90,620,830,760),radius=28,fill=PANEL)
d.text((125,655),'不是四条散新闻，而是一个完整框架：\n谁控制入口，谁理解需求，谁掌握成本。',font=f(30,False),fill=INK,spacing=12)
footer(d,1); save(img,'01-slide-cover.png')

# slide2
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Episode map','表面是四条新闻，底层是一个问题','谁控制 AI 的入口、分发与成本？')
boxes=[(90,250,470,470,BLUE,'Apple 新 CEO','硬件式 AI 路线'),(510,250,890,470,CORAL,'Customer intent','Agent-to-Agent 搜索'),(930,250,1310,470,GREEN,'Anthropic x AWS','芯片 / 云协同'),(350,520,730,740,AMBER,'Claude Mythos','透明度 tension')]
for x1,y1,x2,y2,c,t,s in boxes:
    d.rounded_rectangle((x1,y1,x2,y2),radius=28,fill=PANEL,outline=c,width=5)
    d.text((x1+26,y1+34),t,font=f(34,True),fill=INK)
    d.text((x1+26,y1+92),s,font=f(24,False),fill=MUTED)
d.rounded_rectangle((840,540,1420,740),radius=32,fill='#EEF4FF')
d.text((880,595),'核心判断：\nAI 正在从模型层，\n扩展成入口层、分发层和算力层的全面战争。',font=f(34,True),fill=INK,spacing=14)
footer(d,2); save(img,'02-slide-episode-summary.png')

# slide3
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Apple','Apple 不是远离 AI，而是想把 AI 做成“苹果式产品”')
d.rounded_rectangle((90,250,700,760),radius=30,fill=PANEL)
d.ellipse((180,330,360,510), outline=BLUE, width=8)
d.rounded_rectangle((390,330,590,520), radius=30, outline=CORAL, width=8)
d.line((360,420,390,420), fill=GREEN, width=8)
d.text((170,560),'硬件、系统、终端体验\n会成为 Apple 的 AI 护城河',font=f(34,True),fill=INK,spacing=14)
d.rounded_rectangle((760,250,1410,760),radius=30,fill='#F9FAFB')
items=['John Ternus 的标签是 reliability / durability / repairability / accessibility','Apple 的优势不一定是最强模型，而是最强终端整合','慢，不等于弱；可能只是更重产品工程']
bullet(d,810,320,items,color=BLUE,textwidth=22,size=30)
d.text((810,640),'Take: 把 AI 从 demo 拉回产品工程，正是 Apple 最擅长的事。',font=f(28,True),fill=CORAL)
footer(d,3); save(img,'03-slide-apple.png')

# slide4
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Intent era','搜索正在从关键词时代，进入 intent 时代')
for i,(x,t,s,c) in enumerate([(110,'关键词','人搜索 / 人点击',BLUE),(560,'意图','Agent 理解需求',CORAL),(1010,'选择','Agent 推荐答案',GREEN)]):
    d.rounded_rectangle((x,320,x+320,600),radius=30,fill=PANEL,outline=c,width=5)
    d.text((x+34,360),t,font=f(42,True),fill=INK)
    d.text((x+34,435),s,font=f(28,False),fill=MUTED)
    if i<2: d.line((x+320,460,x+410,460),fill=AMBER,width=8)
    if i<2: d.polygon([(x+410,460),(x+380,440),(x+380,480)],fill=AMBER)
d.rounded_rectangle((140,660,1460,760),radius=24,fill='#FFF7ED')
d.text((180,693),'未来优化目标：不是单纯抢 SEO 排名，而是让你的内容、产品和服务被 Agent 视为最可信、最合适的答案来源。',font=f(28,True),fill=INK)
footer(d,4); save(img,'04-slide-intent.png')

# slide5
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Brand rules','在 Agent 分发世界，品牌必须满足三条新规则')
cols=[(90,300,480,720,BLUE,'1 信息结构化','让系统读得懂，而不只是人觉得文案顺。'),(530,300,920,720,CORAL,'2 信号可信','评价、证据、上下文要一致，机器不吃空话。'),(970,300,1360,720,GREEN,'3 响应可编排','产品、API、库存、服务能力要能接入自动化流程。')]
for x1,y1,x2,y2,c,t,s in cols:
    d.rounded_rectangle((x1,y1,x2,y2),radius=28,fill=PANEL,outline=c,width=5)
    d.ellipse((x1+30,y1+28,x1+90,y1+88),fill=c)
    d.text((x1+115,y1+34),t,font=f(30,True),fill=INK)
    for i,line in enumerate(wrap(s,14)):
        d.text((x1+34,y1+130+i*42),line,font=f(26,False),fill=MUTED)
footer(d,5); save(img,'05-slide-brand-rules.png')

# slide6
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Infrastructure','大模型竞争，已经下沉到芯片与云的协同效率')
d.rounded_rectangle((120,280,690,700),radius=28,fill='#EFF6FF',outline=BLUE,width=5)
d.rounded_rectangle((910,280,1480,700),radius=28,fill='#ECFDF5',outline=GREEN,width=5)
d.text((200,330),'通用 GPU',font=f(42,True),fill=INK)
d.text((990,330),'定制芯片 / Trainium',font=f(42,True),fill=INK)
bullet(d,180,420,['强通用性','生态成熟','但成本高、优化空间有限'],color=BLUE,textwidth=14,size=30)
bullet(d,970,420,['更专用','效率更高','适合做深度联合优化'],color=GREEN,textwidth=14,size=30)
d.line((700,490,900,490),fill=CORAL,width=10); d.polygon([(900,490),(860,462),(860,518)],fill=CORAL)
d.text((675,535),'成本 / 延迟 / 吞吐',font=f(26,True),fill=CORAL)
footer(d,6); save(img,'06-slide-anthropic-aws.png')

# slide7
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Open vs Closed','封闭模型的基础设施耦合，可能让开放生态更难打')
d.rounded_rectangle((100,270,740,740),radius=30,fill='#FFF7ED',outline=CORAL,width=5)
d.rounded_rectangle((860,270,1500,740),radius=30,fill='#EEF4FF',outline=BLUE,width=5)
d.text((150,320),'Closed stack',font=f(40,True),fill=INK)
d.text((910,320),'Open ecosystem',font=f(40,True),fill=INK)
bullet(d,150,410,['更容易做深度联合优化','性能与成本优势更容易积累','但透明度与锁定风险更高'],color=CORAL,textwidth=18,size=28)
bullet(d,910,410,['适配面更广','替换与迁移空间更大','但很难享受专有供应链红利'],color=BLUE,textwidth=18,size=28)
footer(d,7); save(img,'07-slide-open-vs-closed.png')

# slide8
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Transparency','AI 越走向核心基础设施，透明度争议就越大')
d.rounded_rectangle((600,300,1000,600),radius=40,fill=INK)
d.text((695,425),'BLACK BOX',font=f(44,True),fill='white')
points=[('audit',800,210,BLUE),('risk',1150,430,CORAL),('control',800,690,GREEN),('trust',440,430,AMBER)]
for label,x,y,c in points:
    d.line((800,450,x,y),fill=c,width=8)
    d.ellipse((x-70,y-42,x+70,y+42),fill=PANEL,outline=c,width=5)
    d.text((x-42,y-16),label,font=f(28,True),fill=INK)
d.text((110,725),'企业不只问“好不好用”，还会问：能不能审计、能不能替换、出了问题谁负责。',font=f(28,True),fill=MUTED)
footer(d,8); save(img,'08-slide-mythos.png')

# slide9
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img); draw_header(d,'Strategic frame','2026 AI 竞争，归根结底看三件事')
levels=[('入口层','谁控制用户接触 AI 的界面与终端',BLUE,560),('分发层','谁更懂 intent，谁更容易被 Agent 选中',CORAL,450),('基础设施层','谁掌握长期成本曲线与系统效率',GREEN,340)]
for i,(t,s,c,y) in enumerate(levels):
    w=920-180*i
    x=(W-w)//2
    d.polygon([(x,y+110),(x+w,y+110),(x+w-60,y),(x+60,y)],fill=c)
    d.text((x+60,y+25),t,font=f(38,True),fill='white')
    d.text((x+270,y+30),s,font=f(24,False),fill='white')
d.text((390,710),'结论：谁把这三层串得最顺，谁就更可能赢。',font=f(34,True),fill=INK)
footer(d,9); save(img,'09-slide-framework.png')

# slide10
img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img)
d.rounded_rectangle((90,90,1510,810),radius=36,fill='#F8FAFC')
d.rounded_rectangle((130,140,1470,760),radius=30,outline=BLUE,width=5,fill=BG)
d.text((180,210),'赢到最后的，不只是更聪明的模型，\n而是更完整的系统。',font=f(56,True),fill=INK,spacing=16)
d.text((185,400),'产品团队：把 AI 拉回真实工作流\n增长团队：为 Agent 重写信息结构\n平台团队：提前优化推理成本与供应链风险',font=f(34,False),fill=MUTED,spacing=20)
d.rounded_rectangle((185,620,1280,700),radius=22,fill='#EEF4FF')
d.text((220,644),'Closing take：AI 竞争已经同时发生在入口、意图理解和基础设施三层。',font=f(30,True),fill=INK)
d.text((1320,710),'🦞',font=f(46,True),fill=CORAL)
footer(d,10); save(img,'10-slide-back-cover.png')
print('generated slides in', OUT)
