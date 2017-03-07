import pickle as p

def writeData(path, data):
    f = open(path, 'wb')
    p.dump(data, f)
    f.close()
    print("Write successful.!")
    return

def readData(path):
    f = open(path, 'rb')
    data = p.load(f)
    return data
