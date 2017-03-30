import cv2
import numpy as np
from common import constantSource as cs

def startScan(data):
    print("Scanning for potential zones...")
    disp = data
    baseline = cs.getBaseline()
    fl = cs.getFocalLength()[0]
    pixSize = cs.getPixelSize()[0]

    # Calculation of Depth (Z) matrix
    k = baseline*fl/pixSize
    Z_depth = disp*k

    cv2.imshow("Depth map", Z_depth)
    cv2.waitKey()
    cv2.destroyAllWindows()
