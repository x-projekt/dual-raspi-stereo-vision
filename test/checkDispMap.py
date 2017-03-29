import disparityMap as mp
import cv2
from common import constantSource as cs

basePath = "image_{X}_{Y}.png"
dispVal = (16, 112) # (min_disp, max_disp)

i=3
#for i in range(10):
path1 = basePath.format(X="L", Y=i)
path2 = basePath.format(X="R", Y=i)
imgSrc = (path1, path2)

#dispVal = cs.getDisparityValue()
disp = mp.generateDisparityMap(imgSrc, dispVal, cs.path_mode, False)
cv2.imwrite(basePath.format(X="disp", Y=i), disp)
