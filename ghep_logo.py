"""Composite original brand assets onto the 14 demo backdrops, without generative edits."""
from pathlib import Path
import base64, io, json, math, html, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageChops

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=HERE.parent
ASSETS=ROOT/'output/logo-mau-vnpay-pos365/png'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SCALE=3
GROUPS=[['VNPAY-QR','SmartPOS','PhonePOS'],['POS365'],['VNPAY-Invoice'],['VNPAY-CA'],['VNPAY-eKYC'],['VNPAY-App','VNPAY-Taxi','VnShop']]
CONFIG={
'3.png':dict(centers=[156,396,636,860,1092,1323],y=589,h=112,w=205,brand=[56,32,310,62],theme='gold'),
'4.png':dict(centers=[148,389,628,861,1092,1339],y=690,h=114,w=208,brand=[56,32,310,62],theme='gold'),
'5.png':dict(centers=[160,392,626,857,1091,1325],y=730,h=98,w=190,brand=[56,32,310,62],theme='blue'),
'6.png':dict(centers=[154,395,626,853,1088,1331],y=735,h=120,w=208,brand=[56,32,310,62],theme='gold'),
'7.png':dict(centers=[168,398,625,858,1086,1317],y=665,h=123,w=190,brand=[56,32,310,62],theme='blue'),
'checkin-gala-cong-nghe-pos365-vnpay-demo.png':dict(centers=[154,392,628,860,1094,1328],y=403,h=121,w=208,brand=[547,24,390,70],theme='blue'),
'checkin-gala-cong-nghe-pos365-vnpay-demo-2.png':dict(centers=[198,420,645,852,1052,1287],y=451,h=98,w=184,brand=[547,32,390,70],theme='blue'),
'check-in-dia-diem.png':dict(centers=[632,803,978,1132,1285,1448],y=334,h=58,w=148,brand=[60,28,360,66],theme='blue'),
'check-in-dia-diem-2.png':dict(centers=[460,719,978,1173,1368,1613],y=542,h=64,w=176,brand=[819,35,440,80],theme='blue'),
'check-in-dia-diem-3.png':dict(centers=[526,707,883,1034,1177,1335],y=314,h=74,w=144,brand=[42,27,340,66],theme='blue'),
}
for name in ['team-building-mua-he-pos365-demo.png','team-building-mua-he-pos365-demo-v2.png','team-building-mua-he-pos365-demo-v3.png','team-building-mua-he-pos365-demo-v4.png']:
 CONFIG[name]=dict(brand=[589,34,440,82],theme='gold' if '-v3' in name or '-v4' in name else 'blue')


def png_data(im):
 buf=io.BytesIO();im.save(buf,format='PNG');return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()

logos={}
for name in set(sum(GROUPS,[])+['VNPAY']):
 im=Image.open(ASSETS/f'{name}.png').convert('RGBA')
 box=im.getchannel('A').getbbox();im=im.crop(box)
 logos[name]=im

def fit(name,box):
 im=logos[name];x,y,w,h=box;scale=min(w/im.width,h/im.height)
 rw,rh=im.width*scale,im.height*scale
 return [x+(w-rw)/2,y+(h-rh)/2,rw,rh]

records=[]
for filename,cfg in CONFIG.items():
 src=SOURCE/filename;original=Image.open(src).convert('RGB');canvas=original.copy();W,H=canvas.size
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<title>{html.escape(filename)} — logo gốc</title>',f'<image id="anh-goc" x="0" y="0" width="{W}" height="{H}" xlink:href="data:image/png;base64,{base64.b64encode(src.read_bytes()).decode()}"/>']
 placements=[];regions=[]
 def panel(rect,items,label):
  x,y,w,h=map(int,rect);assert x>=0 and y>=0 and x+w<=W and y+h<=H
  regions.append([x,y,x+w,y+h]);r=min(12,h*.18);border='#cfb77b' if cfg['theme']=='gold' else '#a9cddd'
  tile=Image.new('RGBA',(w*SCALE,h*SCALE));d=ImageDraw.Draw(tile)
  d.rounded_rectangle((0,0,w*SCALE-1,h*SCALE-1),radius=int(r*SCALE),fill='#ffffff',outline=border,width=3)
  svg.append(f'<g id="{label}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="white" stroke="{border}" stroke-width="1"/>')
  for name,box in items:
   fx,fy,fw,fh=fit(name,box);raster=logos[name].resize((max(1,round(fw*SCALE)),max(1,round(fh*SCALE))),Image.Resampling.LANCZOS)
   tile.alpha_composite(raster,(round(fx*SCALE),round(fy*SCALE)))
   svg.append(f'<image id="{label}-{name}" x="{x+fx:.3f}" y="{y+fy:.3f}" width="{fw:.3f}" height="{fh:.3f}" xlink:href="{png_data(logos[name])}"/>')
   placements.append(dict(logo=name,rect=[round(x+fx,3),round(y+fy,3),round(fw,3),round(fh,3)]))
  if label=='thuong-hieu':
   mid=w/2;f=ImageFont.truetype(FONT,round(h*.24*SCALE));d.text((mid*SCALE,h*.51*SCALE),'×',font=f,anchor='mm',fill='#6b7280')
   # Vector crossing mark; independent from either logo.
   a=h*.05;cy=y+h*.5;cx=x+mid
   svg.append(f'<path d="M{cx-a},{cy-a}L{cx+a},{cy+a}M{cx-a},{cy+a}L{cx+a},{cy-a}" fill="none" stroke="#6b7280" stroke-width="1.6"/>')
  svg.append('</g>');tile=tile.resize((w,h),Image.Resampling.LANCZOS);canvas.paste(tile,(x,y),tile)
 if 'centers' in cfg:
  for idx,(cx,names) in enumerate(zip(cfg['centers'],GROUPS)):
   w,h=cfg['w'],cfg['h'];pad=10 if h>85 else 7
   if len(names)==1:items=[(names[0],[pad,pad,w-2*pad,h-2*pad])]
   elif h>=85:
    line=(h-2*pad-8)/3
    items=[(name,[w*.17,pad+i*(line+4),w*.66,line]) for i,name in enumerate(names)]
   else:
    line=(h-2*pad-3)/2
    items=[(names[0],[pad,pad,w-2*pad,line]),(names[1],[pad,pad+line+3,(w-3*pad)/2,line]),(names[2],[w/2+pad/2,pad+line+3,(w-3*pad)/2,line])]
   panel([round(cx-w/2),cfg['y'],w,h],items,f'giai-phap-{idx+1}')
 x,y,w,h=cfg['brand'];pad=15;logo_w=w/2-pad*2
 panel(cfg['brand'],[('POS365',[pad,13,logo_w,h-26]),('VNPAY',[w/2+pad,11,logo_w,h-22])],'thuong-hieu')
 svg.append('</svg>');stem=Path(filename).stem+'-logo'
 (HERE/'svg'/f'{stem}.svg').write_text(''.join(svg))
 canvas.save(HERE/'png'/f'{stem}.png',compress_level=6)
 # Every pixel outside composited panel rectangles must remain exactly original.
 diff=ImageChops.difference(original,canvas);d=ImageDraw.Draw(diff)
 for x1,y1,x2,y2 in regions:d.rectangle([x1,y1,x2-1,y2-1],fill=(0,0,0))
 assert diff.getbbox() is None,filename
 records.append(dict(source=filename,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),output=f'png/{stem}.png',svg=f'svg/{stem}.svg',size=[W,H],regions=regions,logos=placements,unchanged_outside_panels=True))
 print(filename,'OK',len(placements),'logos')
(HERE/'vi-tri-logo.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
# Contact sheet for visual inspection; deliverables retain original resolution.
thumb_w,thumb_h=600,450
sheet=Image.new('RGB',(thumb_w*2,thumb_h*math.ceil(len(records)/2)),'#eaf0f5');d=ImageDraw.Draw(sheet);font=ImageFont.truetype(FONT,17)
for n,r in enumerate(records):
 im=Image.open(HERE/r['output']);im.thumbnail((576,405));x=n%2*thumb_w;y=n//2*thumb_h
 sheet.paste(im,(x+(thumb_w-im.width)//2,y+12+(405-im.height)//2));d.text((x+12,y+423),r['source'],font=font,fill='#16304c')
sheet.save(HERE/'tong-quan.jpg',quality=92)
