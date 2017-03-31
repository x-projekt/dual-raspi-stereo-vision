import numpy as np
import cv2

import pointCloudGenerator as pcg
import disparityMap as dm
import zoneScanner as zs
from common import constantSource as cs

basePath = "image_{X}_{Y}.png"
imgSrc = ()
dispVal = (16, 112) # replace with cs.getDisparityValue()

print('loading images...')
# for j in range(2):
#     path = basePath.format(X=cs.getCamera(j+1), Y=(j+1))
#     imgSrc[j] = cv2.imread(path, 0)
imgL = cv2.imread('test/aloeL.jpg')
imgR = cv2.imread('test/aloeR.jpg')
imgSrc = (imgL, imgR)

# disparity range is tuned for 'aloe' image pair
window_size = 3
min_disp = dispVal[0]
max_disp = dispVal[1]
num_disp = max_disp-min_disp

print("Computing Disparity...")
# stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
#                                numDisparities=num_disp,
#                                blockSize=16,
#                                P1=8*3*window_size**2,
#                                P2=32*3*window_size**2,
#                                disp12MaxDiff=1,
#                                uniquenessRatio=10,
#                                speckleWindowSize=100,
#                                speckleRange=32)
disp = dm.generateDisparityMap(imgSrc, dispVal, cs.stream_mode, True)

print("Generating point cloud...")
pcg.generatePointCloud(disp, imgSrc, (min_disp, num_disp, None))
#zs.startScan(disp)
