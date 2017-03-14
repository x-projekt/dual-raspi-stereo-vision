import time
import io
import struct
import socket
import pickle as p

# Custom modules
import cv2
from picamera import PiCamera

# Custom moudles
from common import constantSource as cs

camera = PiCamera()
camera.resolution = cs.getImageSize()

def takePic(path, mode=cs.path_mode):
    if mode == cs.path_mode:
        start = time.time()
        camera.capture(path)
        end = time.time()
        print("Trigger time: " + str(end-start))
    elif mode == cs.stream_mode:
        start = time.time()
        camera.capture(path, "bgr")
        end = time.time()
        print("Trigger time: " + str(end-start))
    else:
        print(cs.getMessage(cs.invalid_mode))
    return

# This should only be used from Master Pi
def takeRemotePic(path=None, mode=cs.single_capture):
    ip = cs.getIP(cs.slave_entity)
    port = cs.getPort(cs.slave_entity)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((ip, port))

        if mode == cs.single_capture:
            # Sending capture mode information to server
            clientSocket.send(mode.encode("utf-8"))

            # Receiving image data from server
            imgData = clientSocket.recv(4096)
            while True:
                buff = clientSocket.recv(4096)
                if buff:
                    imgData += buff
                else:
                    break

            if path is None:
                data = p.loads(imgData)
            else:
                # Saving image data to file
                cv2.imwrite(path, imgData)
                data = None
        elif mode == cs.rapid_capture:
            # Sending capture mode information to server
            clientSocket.send(mode.encode("utf-8"))
            # TODO: write code using picamera advanced recipes

    except socket.error as e:
        print("Error occured: " + e.errno)
    finally:
        clientSocket.close()
    return data
