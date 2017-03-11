import socket
from pathlib import Path
import io
from sense_hat import SenseHat
import numpy as np
import cv2

# Custom modules
from common import constantSource as cs
from common import miscellaneous as msc
from common import cameraTrigger as ct
import server

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
        setPixelFrame(1, go)

        # Step 2: Checking application status of Slave Pi
        currFrame = 2
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.settimeout(cs.connTimeout)
        clientSocket.connect((cs.getIP(cs.slave_entity),
                              cs.getPort(cs.slave_entity)))
        clientSocket.close()

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
        stream = io.BytesIO()
        ct.takeRemotePic(stream, cs.stream_mode)

    except socket.timeout as error:
        if currFrame == 2:
            clientSocket.close()
        # Add code to log the details
    except:
        setPixelFrame(currFrame, err)
    finally:
        pass

elif socket.gethostname() == cs.getHostName(cs.slave_entity):
    # Starting main process
    print("Starting server...")
    server.startServer()
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
