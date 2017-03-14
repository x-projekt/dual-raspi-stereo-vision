## Server should run on the Slave Pi

import socket
import struct
import io
import numpy as np
import logging as log
import pickle as p

# Custom modules
from common import constantSource as cs
from common import cameraTrigger as ct

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        log.basicConfig(filename="serverLog.log",
                        format="%(levelname)s:%(asctime)s:%(message)s",
                        level=log.DEBUG, datefmt="%Y-%m-%d %H:%M:%S UTC %z")

    def startServer(self):
        self.sock.listen(5)
        while True:
            log.info("Server Listening...")
            clientSocket, address = self.sock.accept()
            log.info("Connection Accepted:" + str(address[0]))
            self.serveClient(clientSocket, address)
        return

    def serveClient(self, clientSocket, address):
        try:
            conn = None
            # reading the mode information from the client
            data = clientSocket.recv(4096).decode("utf-8")
            if data == cs.single_capture:
                conn = clientSocket.makefile("wb")
                #stream = io.BytesIO()
                size = cs.getImageSize()
                data = np.empty((size[1], size[0], 3), dtype=np.uint8)
                ct.takePic(data, cs.stream_mode)
                stream = p.dumps(data)

                # Sending the image data
                conn.write(stream)
                conn.flush()
                conn.close()
            elif data == cs.rapid_capture:
                # TODO: write code here for max framerate
                pass
            else:
                log.error("Invalid Mode: '" + data + "': Closing Connection...")
                raise Exception()
        except socket.error as err:
            log.error("Error encountered: " + err.errno)
        except:
            log.error("Error encountered: ")
        finally:
            if conn is not None:
                conn.close()
            clientSocket.close()
        return
