import numpy as np
import cv2
from matplotlib import pyplot as plt

# Custom modules
from common import constantSource as cs

def generateDisparityMap(imageSource, dispValues, mode=cs.path_mode, show=False):
    """
    Returns the disparity map as ndarray

    imageSource: Tuple of (image_1, image_2)
                 These can either be path or ndarray depending on 'mode' (see below)
    dispValues: Tuple of (min_disp_value, max_disp_value)
                These values should be divisible by 16
    mode: Can be 'path_mode' or 'stream_mode'
          Specify whether 'imageSource' is path or ndarray
    show: Specifies whether to display the generated disparity map as image
    """
    if mode == cs.path_mode:
        img1 = cv2.imread(imageSource[0], 0)
        img2 = cv2.imread(imageSource[1], 0)
    elif mode == cs.stream_mode:
        img1 = imageSource[0]
        img2 = imageSource[1]
    else:
        print(cs.getMessage(cs.invalid_mode))
        raise Exception()

    numDisp = dispValues[1] - dispValues[0]
    if numDisp%16 != 0:
        print("Invalid Input: 'numDisparities' should be divisible by 16.")
        raise Exception()

    # TODO: check speckleRange=32 or 2

    block = 10
    p1 = 8*3*3**2
    p2 = 4*p1
    stereo = cv2.StereoSGBM_create(minDisparity=dispValues[0],
                                   numDisparities=numDisp, blockSize=block,
                                   P1=p1, P2=p2, disp12MaxDiff=1, uniquenessRatio=10,
                                   speckleWindowSize=100, speckleRange=32)

    disparity = stereo.compute(img1, img2)
    if show:
        plt.imshow(disparity, "gray")
        plt.show()
    return disparity
