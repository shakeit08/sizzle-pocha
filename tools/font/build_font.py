import sys,glob,re,io
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.merge import Merger
fam=sys.argv[1];out=sys.argv[2]
txt=open('/home/claude/plugin/risu_sizzle_pocha.js').read()+open('/home/claude/geoji/index.html').read()
txt=re.sub(r'data:[a-z0-9/+.-]+;base64,[A-Za-z0-9+/=]+','',txt)
chars=set(c for c in txt if ord(c)>=0x20)|set(chr(i) for i in range(0x20,0x7f))
chars=set(c for c in chars if not (0x1F000<=ord(c)<=0x1FFFF or 0x2600<=ord(c)<=0x27BF or 0xFE00<=ord(c)<=0xFE0F or ord(c)==0x200D))
files=sorted(glob.glob(f'node_modules/@fontsource/{fam}/files/{fam}-*-400-normal.woff2'))
parts=[]
for f in files:
    ft=TTFont(f);cmap=ft.getBestCmap();need=[c for c in chars if ord(c) in cmap]
    if not need: continue
    opt=subset.Options();opt.flavor=None;opt.layout_features=['*'];opt.notdef_outline=True
    s=subset.Subsetter(opt);s.populate(text=''.join(need));s.subset(ft)
    b=io.BytesIO();ft.flavor=None;ft.save(b);b.seek(0);parts.append(b)
print('parts',len(parts))
tmp=[]
for i,b in enumerate(parts):
    p=f'/tmp/{fam}_{i}.ttf';open(p,'wb').write(b.getvalue());tmp.append(p)
m=Merger().merge(tmp)
m.flavor='woff2';m.save(out)
import os;print(out,os.path.getsize(out)//1024,'KB', 'chars',len(chars))
