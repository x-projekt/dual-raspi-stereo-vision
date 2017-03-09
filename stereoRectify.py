import cv2

# Custom modules
from common import constantSource as cs

def stereoRectify(dataset, sourcePath, targetPath, mode=cs.path_mode):
    if mode == cs.path_mode:
        camMtx1, distCoeffs1, camMtx2, distCoeffs2, rotation, translation, = dataset
        img1 = cv2.imread(sourcePath[0])
        img2 = cv2.imread(sourcePath[1])
        imgSize = img1.shape[:2]

        # Calculating rectification parameters
        ## Change the alpha to 0, will remove useless areas (black pixels)
        data = cv2.stereoRectify(cameraMatrix1=camMtx1, distCoeffs1=distCoeffs1,
                                 cameraMatrix2=camMtx2, distCoeffs2=distCoeffs2,
                                 imageSize=imgSize, R=rotation, T=translation,
                                 alpha=1, new_image_size=(0, 0))

        R1, R2, P1, P2, Q, validROI1, validROI2 = data

        # Performing rectification
        data = (camMtx1, distCoeffs1, R1, P1, imgSize)
        rectifyImage(sourcePath[0], targetPath[0], data)
        data = (camMtx2, distCoeffs2, R2, P2, imgSize)
        rectifyImage(sourcePath[1], targetPath[1], data)
    elif mode == cs.stream_mode:
        pass
    else:
        print(cs.getMessage(cs.invalid_mode))
    return

def rectifyImage(imgSrc, imgTgt, data):
    camMtx, distCoeffs, R, P, imgSize = data
    if imgSize is None:
        imgSize = cv2.imread(imgSrc).shape[:2]

    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix=camMtx,
                                             distCoeffs=distCoeffs, R=R,
                                             newCameraMatrix=P, size=imgSize,
                                             m1type=5)
    dst = cv2.remap(imgSrc, mapx, mapy, cv2.INTER_LINEAR)
    cv2.imwrite(imgTgt, dst)
    return
