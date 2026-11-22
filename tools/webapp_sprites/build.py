import numpy as np, json, os, glob
from PIL import Image
from scipy import ndimage
HC=1024; G=HC/1024
F={'mom':1.0,'kid':0.80,'grandma':0.98,'husband':1.0,'mistress':0.96,'friend':1.0,'rival':1.0,'guest':1.0}
# sheet -> (sprite prefix, mood names in pose order, factor key)
SHEETS={
 'momA':('momA',['normal','sad','cry','shock'],'mom'),
 'momB1':('momB',['normal','sad','cry','shock'],'mom'),
 'momC':('momC',['happy','cool','cry','shock'],'mom'),
 'kidA':('kidA',['normal','sad','cry','shock'],'kid'),
 'kidB':('kidB',['normal','sad','cry','shock'],'kid'),
 'kidC':('kidC',['happy','smug','cry','shock'],'kid'),
 'husband':('husband',['smug','normal','angry','shock'],'husband'),
 'mistress':('mistress',['smug','normal','angry','shock'],'mistress'),
 'friend':('friend',['happy','sad','angry','shock'],'friend'),
 'rival':('rival',['normal','smirk','serious','shock'],'rival'),
 'grandma':('grandma',['happy','angry','cry','shock'],'grandma'),
 'guest':('guest',['normal','shock','happy','thumb'],'guest'),
}
def load(sheet,i):
    p=f'posefix/{sheet}_{i}.png'
    if not os.path.exists(p): p=f'pose/{sheet}_{i}.png'
    return Image.open(p).convert('RGBA')
def prep(im):
    a=np.asarray(im)[:,:,3]
    # keep main components (drop tiny specks/effect lines far away)
    lab,k=ndimage.label(a>40); sz=ndimage.sum(a>40,lab,range(1,k+1))
    keep=np.isin(lab,[i+1 for i in range(k) if sz[i]>=sz.max()*0.02])
    keep=ndimage.binary_dilation(keep,iterations=3)
    arr=np.asarray(im).copy(); arr[:,:,3]=np.where(keep,arr[:,:,3],0)
    a=arr[:,:,3]; ys,xs=np.nonzero(a>40); top=ys.min()
    band=a[top:top+int((a.shape[0]-top)*0.14)]>40
    cx=np.nonzero(band.any(0))[0]; hx=(cx.min()+cx.max())/2
    return Image.fromarray(arr),top,hx,xs.min(),xs.max()
if __name__=='__main__':
    WC=int(os.environ.get('WC','600'))
    ext=[]; out={}
    os.makedirs('spr',exist_ok=True)
    for sheet,(pre,moods,fk) in SHEETS.items():
        for i,m in enumerate(moods,1):
            im,top,hx,x0,x1=prep(load(sheet,i)); s=G*F[fk]
            r=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
            c=Image.new('RGBA',(WC,HC),(0,0,0,0)); ox=round(WC/2-hx*s); oy=HC-r.height
            c.alpha_composite(r,(ox,oy)) if ox>=0 else c.paste(r,(ox,oy),r)
            l=ox+x0*s; rr=ox+x1*s; ext.append((pre+'_'+m,round(l),round(rr),round(oy+top*s)))
            c.save(f'spr/{pre}_{m}.png')
    for e in ext:
        flag='  <<OVER' if e[1]<0 or e[2]>WC else ''
        print(e,flag)
