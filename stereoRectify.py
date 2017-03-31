import cv2

# Custom modules
from common import constantSource as cs

def stereoRectify(dataset, imageSource, mode=cs.path_mode, retQ=False):
    """
    Returns the rectified images in a tuple (image_1, image_2 [, Q]) after rectification
    and each image_# is an ndarray. Q will be returned depending on retQ.

    dataset: Tuple of (cameraMatrix_1, distortion_coefficients_1,
                       cameraMatrix_2, distortion_coefficients_2,
                       rotation, translation)
             Refer to 'constants.py' for the camera mapping (1, 2) --> (L, R)
    imageSource: Tuple of (image_1, image_2)
                 These can either be path or ndarray depending on 'mode' (see below)
    mode: Can be 'path_mode' or 'stream_mode'
          Specify whether 'imageSource' is path or ndarray
    retQ: Can be True or False
          Specify whether to return the perspective transformation matrix
          True - return value will be tuple of 3-elements
          False - return value will be tuple of 2-elements
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

    camMtx1, distCoeffs1, camMtx2, distCoeffs2, rotation, translation, = dataset
    h, w = img1.shape[:2]
    imgSize = (w, h)

    # Calculating rectification parameters
    ## Change the alpha to 0, will remove useless areas (black pixels)
    ## Change the alpha to 1, will keep the useless areas (black pixels)
    data = cv2.stereoRectify(cameraMatrix1=camMtx1, distCoeffs1=distCoeffs1,
                             cameraMatrix2=camMtx2, distCoeffs2=distCoeffs2,
                             imageSize=imgSize, R=rotation, T=translation,
                             alpha=0, newImageSize=(0, 0))
    R1, R2, P1, P2, Q, validROI1, validROI2 = data

    # Performing rectification
    data = (camMtx1, distCoeffs1, R1, P1, imgSize)
    dstImg1 = rectifyImage(img1, data)
    data = (camMtx2, distCoeffs2, R2, P2, imgSize)
    dstImg2 = rectifyImage(img2, data)

    if retQ:
        res = (dstImg1, dstImg2, Q)
    else:
        res = (dstImg1, dstImg2)
    return res

def rectifyImage(imgSrc, data):
    camMtx, distCoeffs, R, P, imgSize = data

    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix=camMtx,
                                             distCoeffs=distCoeffs, R=R,
                                             newCameraMatrix=P, size=imgSize,
                                             m1type=5)
    dst = cv2.remap(imgSrc, mapx, mapy, cv2.INTER_LINEAR)
    return dst
