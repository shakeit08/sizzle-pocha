import sys, numpy as np
from PIL import Image
def cuts(a, minrun=35):
    H,W=a.shape; out=[]
    for x in range(W):
        for side in ('R','L'):
            if side=='R':
                if x+3>=W: m=(a[:,x]>200)&(x>=W-3)
                else: m=(a[:,x]>200)&(a[:,x+3]<40)&(a[:,x+1]<200)
            else:
                if x-3<0: m=(a[:,x]>200)
                else: m=(a[:,x]>200)&(a[:,x-3]<40)&(a[:,x-1]<200)
            # longest contiguous run
            best=(0,0,0);s=None
            for y in range(H+1):
                v=m[y] if y<H else False
                if v and s is None: s=y
                if not v and s is not None:
                    if y-s>best[0]: best=(y-s,s,y-1)
                    s=None
            if best[0]>=minrun: out.append((side,x,best[1],best[2]))
    return out
if __name__=='__main__':
    for f in sys.argv[1:]:
        a=np.asarray(Image.open(f).convert('RGBA'))[:,:,3].astype(int)
        print(f,cuts(a))
