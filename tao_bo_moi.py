from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops,ImageFont
import json,base64,io,html,math,shutil
B=Path(__file__).resolve().parent;ROOT=B.parents[1];SRC=B.parent
A=ROOT/'output/logo-mau-vnpay-pos365/png'
# Final uses original source images only. AI-cleaned experiments are not used.
config={
'3.png':(64,40,420,'light'), '4.png':(64,36,420,'light'),
'5.png':(220,28,400,'light'), '6.png':(250,24,400,'light'), '7.png':(210,25,400,'light'),
'checkin-gala-cong-nghe-pos365-vnpay-demo.png':(592,27,300,'light'),
'checkin-gala-cong-nghe-pos365-vnpay-demo-2.png':(592,39,300,'light'),
'check-in-dia-diem.png':(64,35,300,'color'),
'check-in-dia-diem-2.png':(879,45,320,'color'),
'check-in-dia-diem-3.png':(60,32,280,'color'),
}
for p in sorted(SRC.glob('team-building-mua-he-pos365-demo*.png')):
 config[p.name]=(650,46,320,'light' if '-v3' not in p.name else 'color')

def crop_alpha(im):return im.crop(im.getchannel('A').getbbox())
pos_color=crop_alpha(Image.open(ROOT/'.agents/skills/pos365-photographer/assets/logos/logo_color.png').convert('RGBA'))
pos_white=crop_alpha(Image.open(ROOT/'.agents/skills/pos365-photographer/assets/logos/logo_white.png').convert('RGBA'))
vn=crop_alpha(Image.open(A/'VNPAY.png').convert('RGBA'))
# Adapt wordmark for dark backgrounds; retain original multicolor emblem, exact alpha and outlines.
vn_white=vn.copy();mask=vn.getchannel('A');white=Image.new('RGBA',vn.size,'white');white.putalpha(mask)
x=int(vn.width*.318);vn_white.paste(white.crop((x,0,vn.width,vn.height)),(x,0))
def data(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
(B/'assets').mkdir(exist_ok=True)
for name,im in [('POS365-mau',pos_color),('POS365-trang',pos_white),('VNPAY-mau',vn),('VNPAY-chu-trang',vn_white)]:im.save(B/'assets'/f'{name}.png')
rows=[]
for filename,(x,y,w,tone) in config.items():
 original=Image.open(SRC/filename).convert('RGB');im=original.convert('RGBA');W,H=im.size
 pos=pos_white if tone=='light' else pos_color;vnpay=vn_white if tone=='light' else vn
 layer=Image.new('RGBA',im.size);shadow=Image.new('RGBA',im.size);parts=[]
 # Balanced optical widths and generous separation; no surrounding card or shape.
 lw=int(w*.44);rw=int(w*.45);gap=w-lw-rw;ch=max(round(lw/pos.width*pos.height),round(rw/vnpay.width*vnpay.height))
 for name,asset,px,width in [('POS365',pos,x,lw),('VNPAY',vnpay,x+lw+gap,rw)]:
  height=round(width/asset.width*asset.height);py=y+(ch-height)//2;scaled=asset.resize((width,height),Image.Resampling.LANCZOS);layer.alpha_composite(scaled,(px,py));parts.append((name,asset,px,py,width,height))
 # A small separator is drawn with two strokes, never as part of either logo.
 d=ImageDraw.Draw(layer);cx=x+lw+gap/2;cy=y+ch/2;s=2.5
 color=(235,242,249,190) if tone=='light' else (41,62,85,160)
 d.line((cx-s,cy-s,cx+s,cy+s),fill=color,width=1);d.line((cx-s,cy+s,cx+s,cy-s),fill=color,width=1)
 # Subtle short shadow keeps white wordmarks readable on sky without a white box.
 alpha=layer.getchannel('A');is_gala=filename in ['3.png','4.png','5.png','6.png','7.png'];strength=.82 if is_gala else .35;blur=1.7 if is_gala else 1.2;a=alpha.point(lambda p:round(p*strength));shadow.putalpha(a);shadow=shadow.filter(ImageFilter.GaussianBlur(blur));im=Image.alpha_composite(im,shadow);im=Image.alpha_composite(im,layer).convert('RGB')
 stem=Path(filename).stem+'-tinh-gon';out=f'png/{stem}.png';sv=f'svg/{stem}.svg';im.save(B/out)
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<title>{html.escape(filename)} — logo không khung</title>',f'<image id="nen-goc" x="0" y="0" width="{W}" height="{H}" xlink:href="{data(original)}"/>',f'<image id="bong-nhe" x="0" y="0" width="{W}" height="{H}" xlink:href="{data(shadow)}"/>']
 for name,asset,px,py,width,height in parts:svg.append(f'<image id="logo-{name}" x="{px}" y="{py}" width="{width}" height="{height}" xlink:href="{data(asset)}"/>')
 svg.append(f'<path d="M{cx-s},{cy-s}L{cx+s},{cy+s}M{cx-s},{cy+s}L{cx+s},{cy-s}" stroke="'+('#ebf2f9' if tone=='light' else '#293e55')+'" stroke-opacity="0.7" stroke-width="1"/></svg>');(B/sv).write_text(''.join(svg))
 box=(x-8,y-8,x+w+9,y+ch+9);diff=ImageChops.difference(original,im);ImageDraw.Draw(diff).rectangle(box,fill=(0,0,0));assert diff.getbbox() is None
 for k,p in [('truoc',original),('sau',im)]:
  thumb=p.copy();thumb.thumbnail((1400,1000));thumb.save(B/'xem-truoc'/f'{stem}-{k}.webp',quality=91)
 rows.append(dict(source=filename,output=out,svg=sv,before=f'xem-truoc/{stem}-truoc.webp',after=f'xem-truoc/{stem}-sau.webp',size=[W,H],kind='Team building' if filename.startswith('team-building') else 'Gala / check-in',logo_box=box,tone=tone,original_pixels_preserved_outside_logo=True))
 print(filename,'OK')
(B/'danh-sach.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
for page in range(2):
 batch=rows[page*7:(page+1)*7];sheet=Image.new('RGB',(1200,math.ceil(len(batch)/2)*450),'#e9edf1');d=ImageDraw.Draw(sheet)
 for n,r in enumerate(batch):
  a=Image.open(B/r['output']);a.thumbnail((580,405));xx=n%2*600;yy=n//2*450;sheet.paste(a,(xx+(600-a.width)//2,yy+8+(405-a.height)//2));d.text((xx+10,yy+422),r['source'],font=font,fill='#162b42')
 sheet.save(B/f'tong-quan-{page+1}.jpg',quality=93)
