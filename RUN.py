import socket
from pathlib import Path
import pickle as p
from sense_hat import SenseHat

# Custom modules
from common import constantSource as cs
from common import miscellaneous as msc
import server

# Color codes
err = [255, 0 ,0]
go = [0, 255, 0]
wait = [0, 0, 255]

MATRIX_SIZE = 8
mainPixelMatrix = [wait for i in range(MATRIX_SIZE**2)]

if socket.gethostname() == cs.getHostName(cs.master_entity):
    # Starting the main process
    sense = SenseHat()
    sense.set_pixels(mainPixelMatrix)

    filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera, prefix="L")
    camCalibL = getFile(filePath, 3)

    filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera, prefix="R")
    camCalibR = getFile(filePath, 4)

    filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.stereo)
    stereoCalib = getFile(filePath, 5)

elif socket.gethostname() == cs.getHostName(cs.slave_entity):
    # Starting main process
    print("Starting server...")
    server.startServer()
else:
    print("Invalid System being used.! The host name isn't registered.")

# only call this method from Master System
def setPixelFrame(frameNo, color):
    """
    The frames are organised as follows:

    """
    for i in range(4):
        j = i + mainPixelMatrix
        mainPixelMatrix[j] = color
        mainPixelMatrix[j+1] = color
        if blink:
            pass
    return None

def refreshSense():
    return

def getFile(filePath, frameNo):
    if Path(filePath).is_file():
        setPixelFrame(frameNo, go)
        data = msc.readData(filePath)
    else:
        setPixelFrame(frameNo, err)
        data = None
    return data

