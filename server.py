## Server should run on the Slave Computer

import socket

# Custom modules
from common import constantSource as cs

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = cs.getPort(cs.master_entity)
host = ""
s.bind((host, port))
s.listen(5)

while True:
    print("Server Listening...")
    conn, addr = s.accept()
    print("Connected to: ", addr)

    filename = "mytext.txt"
    f = open(filename, 'rb')
    l = f.read(1024)
    while l:
        conn.send(l)
        l = f.read(1024)
    f.close()

    print('Done sending')
    conn.close()
