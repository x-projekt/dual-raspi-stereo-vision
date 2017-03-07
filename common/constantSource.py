import common.constants as c

# Entity types
master_entity = "MASTER"
slave_entity = "SLAVE"

# Camera trigger/capture modes
stream_mode = "STREAM"
path_mode = "PATH"
single_capture = "SINGLE"
burst_capture = "BURST"

# Calibration type
camera = "CAMERA"
stereo = "STEREO"
root = "ROOT"

def getImageSize():
    return (c.IMAGE_WIDTH, c.IMAGE_HEIGHT)

# Returns a tuple of (height, width)
# Dimension is um (10e-6 m)
def getPixelSize():
    return c.PIXEL_SIZE

# Returns a tuple of (horizontal_count, vertical_count)
def getPixelCount():
    return c.PIXEL_COUNT

# Returns a tuple of (focal length in mm, aperture)
def getFocalLength():
    return c.FOCAL_LENGTH

# Returns a tuple of (FOV_H, FOV_V)
def getFOV():
    return (c.FOV_H, c.FOV_V)

def getFileName(file, prefix=""):
    if file == camera:
        fileName = prefix + c.CAMERA_CALIB_FILE
    elif file == stereo:
        fileName = prefix + c.STEREO_CALIB_FILE
    else:
        print("Invalid Input: invalid file name")
    return fileName

def getCalibDataDir(calibType):
    if calibType == camera:
        path = c.CALIB_DATA_DIR + c.CAMERA_DIR
    elif calibType == stereo:
        path = c.CALIB_DATA_DIR + c.STEREO_DIR
    elif calibType == root:
        path = c.CALIB_DATA_DIR
    else:
        print("Invalid Input: invalid calibration type.!")
        path = None
    return path

def getIP(entity):
    if entity.lower() == master_entity:
        ip = c.MASTER_IP
    elif entity.lower() == slave_entity:
        ip = c.SLAVE_IP
    else:
        print("Invalid Input: invalid entity type.!")
        ip = None
    return ip

def getPort(entity):
    if entity.lower() == master_entity:
        port = c.MASTER_SERVER_PORT
    elif entity.lower() == slave_entity:
        port = c.SLAVE_SERVER_PORT
    else:
        print("Invalid Input: invalid entity type.!")
        port = None
    return port

# Returns pixel size in um
def getSensorSize():
    x, y = getPixelCount()
    h, w = getPixelSize()
    return (x*h, y*w)