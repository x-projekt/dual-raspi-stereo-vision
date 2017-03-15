import time
import socket
import pickle as p
import numpy as np

# Custom modules
import cv2
from picamera import PiCamera

# Custom moudles
from common import constantSource as cs

camera = PiCamera()
size = cs.getImageSize()
camera.resolution = size

def takePic(path=None, mode=cs.path_mode):
    """
    This function triggers image capture on the current pi and returns
    the image as 'ndarray' or saves it to the specified path

    path: Path to which image has to be saved (optional)
          Do not specify this to get an ndarray return value
    """
    if mode == cs.path_mode:
        start = time.time()
        camera.capture(path)
        end = time.time()
        print("Trigger time: " + str(end-start))
        data = None
    elif mode == cs.stream_mode:
        start = time.time()
        data = np.empty((size[1], size[0], 3), dtype=np.uint8)
        camera.capture(data, "bgr")
        end = time.time()
        print("Trigger time: " + str(end-start))
    else:
        print(cs.getMessage(cs.invalid_mode))
    return data

# This should only be used from Master Pi
def takeRemotePic(path=None):
    """
    This function triggers image capture on slave pi and returns the
    image as 'ndarray' or saves it to specified path

    path: Path to which image has to be saved (optional)
          Do not specify this to get an ndarray return value
    """
    ip = cs.getIP(cs.slave_entity)
    port = cs.getPort(cs.slave_entity)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((ip, port))

        # Sending capture mode information to server
        clientSocket.send(cs.single_capture.encode("utf-8"))

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
    except socket.error as e:
        print("Error occured: " + e.errno)
    finally:
        clientSocket.close()
    return data
