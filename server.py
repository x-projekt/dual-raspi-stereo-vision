## Server should run on the Slave Pi

import socket
import struct
import io

# Custom modules
from common import constantSource as cs
from common import cameraTrigger as ct

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
            conn.write(stream.read())
            conn.flush()
        elif data == cs.burst_capture:
            # TODO: Add continuous capture functionality
            pass
        else:
            clientSocket.send("Invalid Capture Mode.!")
            clientSocket.sendall("Closing Connection...")
            break
    except socket.error as e:
        print("Error encountered: " + e)
    finally:
        clientSocket.close()
