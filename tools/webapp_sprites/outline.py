import glob, os, numpy as np
from PIL import Image
from scipy import ndimage
R=4.0; COL=(43,30,37)
os.makedirs('spr_ol',exist_ok=True)
for f in sorted(glob.glob('spr/*.png')):
    arr=np.array(Image.open(f).convert('RGBA')).astype(float); a=arr[...,3]/255
    solid=ndimage.binary_opening(a>0.5,iterations=1)
    ol=np.clip(R+0.8-ndimage.distance_transform_edt(~solid),0,1)
    sa=np.maximum(np.clip(ndimage.distance_transform_edt(solid),0,1)*solid, a*solid)
    ta=sa+ol*(1-sa); out=np.zeros_like(arr)
    for ch in range(3): out[...,ch]=(arr[...,ch]*sa+COL[ch]*ol*(1-sa))/np.maximum(ta,1e-6)
    out[...,3]=ta*255
    Image.fromarray(out.clip(0,255).astype(np.uint8),'RGBA').save('spr_ol/'+os.path.basename(f))
