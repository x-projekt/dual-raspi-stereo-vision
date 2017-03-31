import cv2
import numpy as np
from common import constantSource as cs

def startScan(disp):
    print("Scanning for potential zones...")

    # Acquiring standard data
    baseline = cs.getBaseline()
    fl = cs.getFocalLength()[0]
    pixSize = cs.getPixelSize()[0]

    # Calculation of Depth (Z) matrix
    k = baseline*fl/pixSize
    Z_depth = np.reciprocal(disp)*k

    #TODO: add code for recognizing the potential passages
    cv2.imshow("Depth map", Z_depth)
    cv2.waitKey()
    cv2.destroyAllWindows()
