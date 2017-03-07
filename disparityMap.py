import numpy as np
import cv2
from matplotlib import pyplot as plt

def generateDisparityMap(imgL, imgR, maxDisparity, minDisparity, show=False):
    numDisparity = maxDisparity - minDisparity
    blockSize = 10
    P1 = 8*3*3**2
    P2 = 4*P1
    stereo = cv2.StereoSGBM_create(
        minDisparity,
        numDisparity,
        blockSize, P1, P2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=2)

    disparity = stereo.compute(imgL,imgR)
    if show:
        plt.imshow(disparity, "gray")
        plt.show()
    return
