import numpy as np
import cv2
from matplotlib import pyplot as plt

# Custom modules
from common import constantSource as cs

def generateDisparityMap(imageSource, dispValues, mode=cs.path_mode, show=False):
    if mode == cs.path_mode:
        imgL = cv2.imread(imageSource[0])
        imgR = cv2.imread(imageSource[1])
    elif mode == cs.stream_mode:
        imgL = imageSource[0]
        imgR = imageSource[1]
    else:
        print(cs.getMessage(cs.invalid_mode))

    numDisp = dispValues[1] - dispValues[0]
    # if numDisp%16 != 0:
    #     print("Invalid Input: 'numDisparities' should be divisible by 16.")
    # TODO: check if the above test is required
    # TODO: check speckleRange=32 or 2

    block = 10
    p1 = 8*3*3**2
    p2 = 4*p1
    stereo = cv2.StereoSGBM_create(minDisparity=dispValues[0],
                                   numDisparity=numDisp, blockSize=block,
                                   P1=p1, P2=p2, disp12MaxDiff=1, uniquenessRatio=10,
                                   speckleWindowSize=100, speckleRange=32)

    disparity = stereo.compute(imgL, imgR)
    if show:
        plt.imshow(disparity, "gray")
        plt.show()
    return
