import sys, numpy as np
from PIL import Image, ImageDraw
# fill2.py in out spec...   spec = side:y0:y1:W:shape:mode   shape=arm|bump  mode=tex|mirror
src,dst=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGBA'); A=np.asarray(im).astype(float); Hd,Wd=A.shape[:2]
LINE=np.array([58,40,33],float); S=4
rng=np.random.default_rng(1)
def prof(t,shape):
    if shape=='bump': return np.sin(np.pi*t)**0.75
    up=np.where(t<0.15,np.sin(np.pi/2*np.clip(t/0.15,0,1)),1.0)
    dn=np.where(t>0.55,1-np.clip((t-0.55)/0.45,0,1)**1.6,1.0)
    return up*dn
def clean_patch(ex,y0,y1,sg,size=28):
    g=np.abs(np.diff(A[:,:,:3].mean(2),axis=0))[:, :-1]+np.abs(np.diff(A[:,:,:3].mean(2),axis=1))[:-1,:]
    best=None
    for y in range(y0,y1-size,6):
        for k in range(8,140,6):
            x=ex-sg*k if sg<0 else ex-k-size
            x=ex+k if sg<0 else ex-k-size
            if x<0 or x+size>=Wd: continue
            if A[y:y+size,x:x+size,3].min()<250: continue
            s=g[y:y+size,x:x+size].max()
            if best is None or s<best[0]: best=(s,x,y)
    s,x,y=best
    return A[y:y+size,x:x+size,:3].copy()
for spec in sys.argv[3:]:
    side,y0,y1,W,shape,mode=spec.split(':'); y0,y1,W=int(y0),int(y1),float(W)
    a=A[:,:,3]; xs=np.nonzero(a[y0:y1].max(0)>200)[0]
    ex = xs.min() if side=='L' else xs.max()
    sg = -1 if side=='L' else 1
    ys=np.arange(y0,y1+1)
    if shape=='auto':
        def xo(y):
            r=np.nonzero(a[y]>128)[0]
            return (r.max() if side=='R' else r.min()) if len(r) else ex
        k=22
        s1=max(0.15,sg*(ex-xo(y0-k))/k) ; s2=max(0.15,sg*(ex-xo(y1+k))/k)
        wv=np.minimum.reduce([np.full(len(ys),W),s1*(ys-y0),s2*(y1-ys)])
        ker=np.hanning(31); ker/=ker.sum(); pad=np.r_[np.zeros(15),wv,np.zeros(15)]
        wv=np.convolve(pad,ker,'same')[15:-15]; wv=np.maximum(wv,0)
        print('slopes',round(s1,2),round(s2,2))
    else: wv=W*prof((ys-y0)/(y1-y0),shape)
    if shape=='auto':
        K=40; yy=np.arange(y0-K,y1+K+1)
        xo_=np.array([xo(y) for y in yy],float)
        C=xo_.copy(); C[K:K+len(ys)]=ex+sg*wv
        ker=np.hanning(25); ker/=ker.sum()
        Cs=np.convolve(np.r_[np.full(12,C[0]),C,np.full(12,C[-1])],ker,'same')[12:-12]
        NC=np.maximum(Cs*sg,xo_*sg)*sg
        on=np.nonzero(np.abs(NC-xo_)>0.6)[0]; i0=max(on.min()-6,0); i1=min(on.max()+6,len(yy)-1)
        ys=yy[i0:i1+1]; nc=NC[i0:i1+1]; xin=xo_[i0:i1+1]-sg*3
        wv=np.abs(nc-ex)
        outer=[(nc[i],ys[i]) for i in range(len(ys))]
        poly=outer+[(xin[i],ys[i]) for i in range(len(ys)-1,-1,-1)]
    else:
        outer=[(ex+sg*wv[i],ys[i]) for i in range(len(ys))]
        poly=outer+[(ex-sg*3,y1),(ex-sg*3,y0)]
    m=Image.new('L',(Wd*S,Hd*S),0); ImageDraw.Draw(m).polygon([(x*S,y*S) for x,y in poly],fill=255)
    M=np.asarray(m.resize((Wd,Hd),Image.LANCZOS)).astype(float)/255
    o=Image.new('L',(Wd*S,Hd*S),0); ImageDraw.Draw(o).line([(x*S,y*S) for x,y in outer],fill=255,width=int(3.8*S),joint='curve')
    O=np.asarray(o.resize((Wd,Hd),Image.LANCZOS)).astype(float)/255
    F=A[:,:,:3].copy()
    if mode=='mirror':
        for i,y in enumerate(ys):
            for k in range(0,int(np.ceil(wv[i]))+6):
                xt=int(ex+sg*(k-3)); xs_=int(ex-sg*(k+4))
                if 0<=xt<Wd and 0<=xs_<Wd: F[y,xt]=A[y,xs_,:3]
    else:
        p=clean_patch(ex,y0,y1,sg); ps=p.shape[0]
        tiles=[p,p[:,::-1],p[::-1],p[::-1,::-1]]
        for ty in range(0,Hd,ps):
            for tx in range(0,Wd,ps):
                t=tiles[rng.integers(4)]; hh=min(ps,Hd-ty); ww=min(ps,Wd-tx)
                F[ty:ty+hh,tx:tx+ww]=t[:hh,:ww]
    Mx=M[:,:,None]; A[:,:,:3]=A[:,:,:3]*(1-Mx)+F*Mx; A[:,:,3]=np.maximum(A[:,:,3],M*255)
    Ox=O[:,:,None]; A[:,:,:3]=A[:,:,:3]*(1-Ox)+LINE*Ox; A[:,:,3]=np.maximum(A[:,:,3],O*255)
Image.fromarray(A.clip(0,255).astype(np.uint8)).save(dst)
