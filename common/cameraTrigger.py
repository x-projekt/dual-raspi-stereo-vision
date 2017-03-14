import time
import io
import struct
import socket

# Custom modules
import cv2
from picamera import PiCamera

# Custom moudles
from common import constantSource as cs

# setting height and width of picture (in pixels)
w, h = cs.getImageSize()

camera = PiCamera()
camera.resolution = (w, h)

def takePic(path, mode=cs.path_mode):
    if mode == cs.path_mode:
        start = time.time()
        camera.capture(path)
        end = time.time()
        print("Trigger time: " + str(end-start))
    elif mode == cs.stream_mode:
        start = time.time()
        camera.capture(path, format="png")
        # TODO: make it use ndarray and replace format with "rgb"
        # OR
        # TODO: find a way of converting BytesIO into ndarray (seems like overkill)
        end = time.time()
        print("Trigger time: " + str(end-start))
    else:
        print(cs.getMessage(cs.invalid_mode))
    return

# This should only be used from Master Pi
def takeRemotePic(path, mode=cs.single_capture):
    ip = cs.getIP(cs.slave_entity)
    port = cs.getPort(cs.slave_entity)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((ip, port))

        if mode == cs.single_capture:
            # Sending capture mode information to server
            clientSocket.send(mode.encode("utf-8"))

            conn = clientSocket.makefile("rb")
            imgLen = struct.unpack("<L", conn.read(struct.calcsize("<L")))[0]

            # Saving data to file
            f = open(path, "wb")
            f.write(conn.read(imgLen))
            f.close()
            conn.close()
        elif mode == cs.rapid_capture:
            # Sending capture mode information to server
            clientSocket.send(mode.encode("utf-8"))
            # TODO: write code using picamera advanced recipes

    except socket.error as e:
        print("Error occured: " + e.errno)
    finally:
        clientSocket.close()
    return
