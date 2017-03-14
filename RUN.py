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
        filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera, prefix="L")
        camCalibL = getFileData(filePath, currFrame)
        cameraMatrix, distCoeffs = camCalibL[0], camCalibL[1]

        currFrame = 4
        filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera, prefix="R")
        camCalibR = getFileData(filePath, currFrame)
        cameraMatrix, distCoeffs = camCalibR[0], camCalibR[0]

        currFrame = 5
        filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.stereo)
        rotate, translate, essential, fundamental = getFileData(filePath, currFrame)

        # TODO: Run this on parallel threads
        # Step 6: Starting system process
        currFrame = 6
        setPixelFrame(currFrame, go, True)
        i = 0
        while True:
            pathL = "__cahce__/imageL_{x}".format(i) + ".png"
            pathR = "__cahce__/imageR_{x}".format(i) + ".png"
            paths = [pathL, pathR]
            procs = []
            for index, path in enumerate(paths):
                proc = Process(target=ct.takePic, args=(path))
                procs.append(proc)
                proc.start()

            for proc in procs:
                proc.join()

            imgL = cv2.imread(pathL)
            imgR = cv2.imread(pathR)
            stereoRectify(images)
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
