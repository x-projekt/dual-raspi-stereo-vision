import socket
from pathlib import Path
import time

from sense_hat import SenseHat
import numpy as np
import cv2

# Custom modules
from common import constantSource as cs
from common import miscellaneous as msc
from common import cameraTrigger as ct
import cameraRectify as cr
import stereoRectify as sr
import verifyEpipole as ve
import disparityMap as dm
import pointCloudGenerator as pcg
from server import Server

class mainProgram():
    def __init__(self):
        self.sense = None

        # Color codes
        self.err = [255, 0, 0]
        self.go_green = [0, 255, 0]
        self.wait = [0, 0, 255]

        self.MATRIX_SIZE = 8
        self.mainPixelMatrix = [self.wait for i in range(self.MATRIX_SIZE**2)]

    def run(self):
        if socket.gethostname() == cs.getHostName(cs.master_entity):
            # Starting the main process
            print("Starting main structure...")
            self.sense = SenseHat()
            self.sense.set_pixels(self.mainPixelMatrix)

            try:
                # Step 1: Starting application on the Master Pi
                currFrame = 1
                self.setPixelFrame(currFrame, self.go_green)

                # Step 2: Checking application status of Slave Pi
                currFrame = 2
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientSocket.settimeout(cs.connTimeout)
                clientSocket.connect((cs.getIP(cs.slave_entity),
                                      cs.getPort(cs.slave_entity)))
                clientSocket.close()
                self.setPixelFrame(currFrame, self.go_green)

                # Step 3, 4 and 5: Checking for calibration data
                currFrame = 3
                filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera,
                                                                        prefix=cs.getCamera(1))
                camCalib1 = self.getFileData(filePath, currFrame)
                camMtx1, distCoeffs1 = camCalib1[0], camCalib1[1]

                currFrame = 4
                filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.camera,
                                                                        prefix=cs.getCamera(2))
                camCalib2 = self.getFileData(filePath, currFrame)
                camMtx2, distCoeffs2 = camCalib2[0], camCalib2[1]

                currFrame = 5
                filePath = cs.getCalibDataDir(cs.root) + cs.getFileName(cs.stereo)
                rotate, translate, essential, fundamental = self.getFileData(filePath,
                                                                             currFrame)

                # TODO: Run this on parallel threads
                # Step 6: Starting system process
                currFrame = 6
                self.setPixelFrame(currFrame, self.go_green)
                # TODO: Multi-process these step
                q = True
                while q:
                    img1 = ct.takePic()
                    img2 = ct.takeRemotePic()
                    img1 = cr.rectifyImage((camMtx1, distCoeffs1), img1, cs.stream_mode)
                    img2 = cr.rectifyImage((camMtx2, distCoeffs2), img2, cs.stream_mode)

                    dataset = (camMtx1, distCoeffs1, camMtx2, distCoeffs2, rotate, translate)
                    data = sr.stereoRectify(dataset, (img1, img2), cs.stream_mode, True)
                    imgs = (data[0], data[1])
                    disp = dm.generateDisparityMap(imgs, cs.stream_mode, True)

                    pcg.generatePointCloud(disp, imgs, data[2])
                    q = input("Try one more time (y/n): ")
                    if q.lower() == "y":
                        q = True
                    elif q.lower() == "n":
                        q = False
                    else:
                        print(cs.getMessage(cs.invalid_binary, "YN"))
                # Multi-process this step
                ## TODO: Add code to send disparity to slave pi for point cloud generation
                ## TODO: Add code for potential region selection
                ## TODO: Add code to call the required control planning system
            except:
                if currFrame == 2:
                    clientSocket.close()
                self.setPixelFrame(currFrame, self.err)
            finally:
                time.sleep(10)
                self.sense.clear()

        elif socket.gethostname() == cs.getHostName(cs.slave_entity):
            # Starting main process
            print("Starting server...")
            host = ""
            port = cs.getPort(cs.slave_entity)
            Server(host, port).startServer()
        else:
            print("Invalid System being used.! The host name isn't registered.")

    def setPixelFrame(self, frameNo, color):
        """
        Only call this method from Master System.
        The frames are organised as follows:
        """
        if frameNo%2 == 0:
            j = frameNo + 30
            k = 1
        else:
            j = frameNo
            k = -1
        for i in range(4):
            self.mainPixelMatrix[j] = color
            self.mainPixelMatrix[j+k] = color
            j += self.MATRIX_SIZE
        time.sleep(1)
        self.sense.set_pixels(self.mainPixelMatrix)
        return

    def getFileData(self, filePath, frameNo):
        if Path(filePath).is_file():
            self.setPixelFrame(frameNo, self.go_green)
            data = msc.readData(filePath)
        else:
            raise Exception()
        return data

if __name__ == "__main__":
    print("Starting application...")
    mainProgram().run()
