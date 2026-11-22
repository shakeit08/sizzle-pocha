import sys, os, numpy as np
from PIL import Image
src=sys.argv[1]; outdir=sys.argv[2]; PAD=100
im=Image.open(src).convert('RGBA'); A=np.asarray(im).copy(); a=A[:,:,3].astype(float)
H,W=a.shape
def seam(b,win=90):
    lo,hi=b-win,b+win; c=a[:,lo:hi]/255.0+0.001; n=hi-lo
    D=np.zeros_like(c); P=np.zeros(c.shape,int); D[0]=c[0]
    for y in range(1,H):
        prev=D[y-1]; l=np.r_[np.inf,prev[:-1]]; r=np.r_[prev[1:],np.inf]
        st=np.stack([l,prev,r]); k=st.argmin(0); D[y]=c[y]+st.min(0); P[y]=np.arange(n)+k-1
    x=int(D[-1].argmin()); path=[0]*H
    for y in range(H-1,-1,-1): path[y]=x+lo; x=P[y,x]
    cost=sum(a[y,path[y]] for y in range(H))/255
    return np.array(path),cost
seams=[np.zeros(H,int)]
for b in (W//4,W//2,3*W//4):
    p,c=seam(b); seams.append(p); print(os.path.basename(src),b,'seam cost',round(c,1))
seams.append(np.full(H,W))
name=os.path.splitext(os.path.basename(src))[0]
xs=np.arange(W)[None,:]
for i in range(4):
    L=seams[i][:,None]; R=seams[i+1][:,None]
    m=(xs>=L)&(xs<R)
    B=A.copy(); B[:,:,3]=np.where(m,B[:,:,3],0)
    x0=int(seams[i].min()); x1=int(seams[i+1].max())
    p=Image.fromarray(B).crop((x0,0,x1,H))
    can=Image.new('RGBA',(x1-x0+2*PAD,H),(0,0,0,0)); can.paste(p,(PAD,0))
    can.save(f'{outdir}/{name}_{i+1}.png')
