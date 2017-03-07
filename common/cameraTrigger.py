import time
import io
import socket
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
        end = time.time()
        print("Trigger time: " + str(end-start))
    else:
        print("Invalid Mode: Mode can only be STREAM_MODE or PATH_MODE")
    return

# This should only be used from Master Pi
def takeRemotePic(path):
    ip = cs.getIP(cs.slave_entity)
    port = cs.getPort(cs.slave_entity)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSocket.connect((ip, port))

        # Sending capture mode information to server
        clientSocket.send(cs.single_capture.encode("utf-8"))

        # Saving data to file
        f = open(path, "wb")
        while True:
            data = clientSocket.recv(4096)
            if not data:
                break
            else:
                f.write(data)
        f.close()
    except socket.error as e:
        print("Error occured: " + e)
    return
