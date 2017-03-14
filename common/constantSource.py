import common.constants as c

connTimeout = 15 # in sec

# Entity types
master_entity = "MASTER"
slave_entity = "SLAVE"

# Camera trigger/capture modes
stream_mode = "STREAM"
path_mode = "PATH"
single_capture = "SINGLE"
rapid_capture = "BURST"

# Calibration type
camera = "CAMERA"
stereo = "STEREO"
root = "ROOT"

# Error message prompts
invalid_mode = "MODE"
invalid_binary = "BINARY"
invalid_entity = "ENTITY"

# Returns camera mapping (1, 2) --> (L, R)
def getCamera(i):
    if i == 1:
        res = c.CAMERA_1
    if i == 2:
        res = c.CAMERA_2
    return res

# Returns tuple of image resolution (W, H) in pixels
def getImageSize():
    return c.IMAGE_RESOLUTION

# Returns the preffered frame rate (in fps)
def getFrameRate():
    return c.FRAME_RATE

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
    if entity == master_entity:
        ip = c.MASTER_IP
    elif entity == slave_entity:
        ip = c.SLAVE_IP
    else:
        print("Invalid Input: invalid entity type.!")
        ip = None
    return ip

def getPort(entity):
    if entity == master_entity:
        port = c.MASTER_SERVER_PORT
    elif entity == slave_entity:
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

def getCalibReq():
    return c.TOTAL_NO_PICS

def getMessage(type, AB=""):
    msg = None
    if type == invalid_mode:
        msg = c.INVALID_MODE
    elif type == invalid_binary:
        l = len(AB)
        if l == 2:
            msg = c.INVALID_AB.format(X=AB[0], Y=AB[1])
        else:
            print("Invalid Input: AB should be a 2-character string.")
    elif type == invalid_entity:
        msg = c.INVALID_ENTITY
    else:
        print("Invalid message type requested.!")
    return msg

def getHostName(entity):
    if entity == master_entity:
        hostName = c.MASTER_HOST
    elif entity == slave_entity:
        hostName = c.SLAVE_HOST
    else:
        print(getMessage(invalid_entity))
    return hostName
