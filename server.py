## Server should run on the Slave Pi

import socket
import struct
import io
import time

# Custom modules
from common import constantSource as cs
from common import cameraTrigger as ct

def startServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = cs.getPort(cs.slave_entity)
    host = ""
    s.bind((host, port))
    s.listen(5)

    while True:
        print("Server Listening...")
        clientSocket = s.accept()[0]
        try:
            # reading the mode information from the client
            data = clientSocket.recv(4096).decode("utf-8")
            if data == cs.single_capture:
                conn = clientSocket.makefile("wb")
                stream = io.BytesIO()
                ct.takePic(stream, cs.stream_mode)

                # Sending the image size
                conn.write(struct.pack("<L", stream.tell()))
                conn.flush()
                stream.seek(0)

                # Sending the image data
                conn.write(stream.read())
                conn.write(struct.pack("<L", 0))
                conn.close()
            elif data == cs.rapid_capture:
                # TODO: write code here for max framerate
                pass
            else:
                clientSocket.send("Invalid Capture Mode.!")
                clientSocket.send("Closing Connection...")
                break
        except socket.error as e:
            print("Error encountered: " + e.errno)
        finally:
            clientSocket.close()
