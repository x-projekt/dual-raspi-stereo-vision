import socket
from pathlib import Path
import io
from multiprocessing import Process

from sense_hat import SenseHat
import numpy as np
import cv2

# Custom modules
from common import constantSource as cs
from common import miscellaneous as msc
from common import cameraTrigger as ct
from common import cameraRectify as cr
import stereoRectify as sr
import disparityMap as dm
from server import Server

# Color codes
err = [255, 0 ,0]
go = [0, 255, 0]
wait = [0, 0, 255]

MATRIX_SIZE = 8
mainPixelMatrix = [wait for i in range(MATRIX_SIZE**2)]

currFrame = 0

if socket.gethostname() == cs.getHostName(cs.master_entity):
    # Starting the main process
    print("Starting appliction...")

    sense = SenseHat()
    sense.set_pixels(mainPixelMatrix)

    try:
        # Step 1: Starting application on the Master Pi
        currFrame = 1
        setPixelFrame(currFrame, go)

        # Step 2: Checking application status of Slave Pi
        currFrame = 2
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.settimeout(cs.connTimeout)
        clientSocket.connect((cs.getIP(cs.slave_entity),
                              cs.getPort(cs.slave_entity)))
        clientSocket.close()
        setPixelFrame(currFrame, go)

        # Step 3, 4 and 5: Checking for calibration data
        currFrame = 3
        filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera, prefix=cs.getCamera(1))
        camCalib1 = getFileData(filePath, currFrame)
        camMtx1, distCoeffs1 = camCalib1[0], camCalib1[1]

        currFrame = 4
        filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera, prefix=cs.getCamera(2))
        camCalib2 = getFileData(filePath, currFrame)
        camMtx2, distCoeffs2 = camCalib2[0], camCalib2[1]

        currFrame = 5
        filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.stereo)
        rotate, translate, essential, fundamental = getFileData(filePath, currFrame)

        # TODO: Run this on parallel threads
        # Step 6: Starting system process
        currFrame = 6
        setPixelFrame(currFrame, go, True)
        # TODO: Multi-process these step
        img1 = ct.takePic()
        img2 = ct.takeRemotePic()
        img1 = cr.rectifyImage((camMtx1, distCoeffs1), img1, cs.stream_mode)
        img2 = cr.rectifyImage((camMtx2, distCoeffs2), img2, cs.stream_mode)

        dataset = (camMtx1, distCoeffs1, camMtx2, distCoeffs2, rotate, translate)
        imgs = sr.stereoRectify(dataset, (img1, img2), cs.stream_mode)
        disp = dm.generateDisparityMap(imgs, cs.getDisparityValue(), cs.stream_mode, False)

        # Multi-process this step
        ## TODO: Add code to send disparity to slave pi for point cloud generation
        ## TODO: Add code for potential region selection
        ## TODO: Add code to call the required control planning system
        cv2.imshow("Disparity", disp)
        cv2.waitKey()
        cv2.destroyAllWindows()
    except:
        if currFrame == 2:
            clientSocket.close()
        setPixelFrame(currFrame, err)
    finally:
        pass

elif socket.gethostname() == cs.getHostName(cs.slave_entity):
    # Starting main process
    print("Starting server...")
    host = ""
    port = cs.getPort(cs.slave_entity)
    Server(host, port).startServer()
else:
    print("Invalid System being used.! The host name isn't registered.")

# only call this method from Master System
def setPixelFrame(frameNo, color, blink=False):
    """
    The frames are organised as follows:

    """
    if frameNo%2 == 0:
        j = frameNo + 30
        k = 1
    else:
        j = frameNo
        k = -1
    for i in range(4):
        mainPixelMatrix[j] = color
        mainPixelMatrix[j+k] = color
        j += MATRIX_SIZE

    sense.set_pixels(mainPixelMatrix)
    return

def getFileData(filePath, frameNo):
    if Path(filePath).is_file():
        setPixelFrame(frameNo, go)
        data = msc.readData(filePath)
    else:
        raise Exception()
    return data
