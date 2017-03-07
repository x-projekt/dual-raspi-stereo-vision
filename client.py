import socket

# Custom modules
from common import constantSource as cs

s = socket.socket()
host = cs.getIP(cs.master_entity)
port = cs.getPort(cs.master_entity)

s.connect((host, port))
print("Connection Established...")

f = open("received_file.txt", "wb")
print("File opened")
while True:
    data = s.recv(1024)
    if not data:
        break
    else:
        print("receiving data...")
        print("data=%s", data)
        f.write(data)
f.close()

print("Successfully recieved file")
s.close()
print("Connection closed")
