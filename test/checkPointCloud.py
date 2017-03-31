import numpy as np
import cv2

import pointCloudGenerator as pcg
import disparityMap as dm
import zoneScanner as zs
from common import constantSource as cs

print('loading images...')
imgL = cv2.imread('test/aloeL.jpg')  # downscale images for faster processing
imgR = cv2.imread('test/aloeR.jpg')

# disparity range is tuned for 'aloe' image pair
window_size = 3
min_disp = 16
max_disp = 112
num_disp = max_disp-min_disp

print("Computing Disparity...")
disp = dm.generateDisparityMap((imgL, imgR), (min_disp, max_disp), cs.stream_mode, True)

# stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
#                                numDisparities=num_disp,
#                                blockSize=16,
#                                P1=8*3*window_size**2,
#                                P2=32*3*window_size**2,
#                                disp12MaxDiff=1,
#                                uniquenessRatio=10,
#                                speckleWindowSize=100,
#                                speckleRange=32)

# print('computing disparity...')
# disp = stereo.compute(imgL, imgR).astype(np.float32)/16.0

print("Generating point cloud...")
pcg.generatePointCloud(disp, (imgL, imgR), (min_disp, num_disp, None))
#zs.startScan(disp)
