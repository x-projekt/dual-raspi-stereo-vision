import cv2

def rectifyImage(dataset, sourcePath, targetPath):
    ret, mtx, dist, rvecs, tvecs = dataset

    img = cv2.imread(sourcePath)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    cv2.imwrite(targetPath, dst)
