import cv2

# Custom modules
from common import constantSource as cs

def rectifyImage(dataset, imageSource, mode=cs.path_mode):
    """
    Returns rectified camera image as ndarray

    dataset: Tuple of (cameraMatrix, distortion_coefficients)
    mode: Can be 'path_mode' or 'stream_mode'
          Specify whether 'imageSource' is path or ndarray
    """
    if mode == cs.path_mode:
        img = cv2.imread(imageSource, 0)
    elif mode == cs.stream_mode:
        img = imageSource
    else:
        print(cs.getMessage(cs.invalid_mode))
        raise Exception()

    mtx, dist = dataset

    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    return dst
