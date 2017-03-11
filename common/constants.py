# Camera Constants
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# FOV in degrees
FOV_H = 62.2
FOV_V = 48.8

# Focal length (focal_length_in_mm, aperture)
FOCAL_LENGTH = (3.04, 2.0)

# Pixel size in um (10e-6 m)
# Pixel count is of active pixels
PIXEL_SIZE = (1.12, 1.12)
PIXEL_COUNT = (3280, 2464)

# Path Constants
MASTER_IP = "192.168.137.170"
SLAVE_IP = "192.168.137.10"
MASTER_SERVER_PORT = 6060
SLAVE_SERVER_PORT = 6061

# Directory names
CALIB_DATA_DIR = "calibData/"
CAMERA_DIR = "camera/"
STEREO_DIR = "stereo/"

# File names
CAMERA_CALIB_FILE = "_CamCalib.data"
STEREO_CALIB_FILE = "SeteroCalib.data"

TOTAL_NO_PICS = 30

# Error messages:
INVALID_MODE = "Invalid Mode: Values taken 'path_mode' or 'stream_mode'"
INVALID_AB = "Invalid Input: The option are {X} and {Y}"
INVALID_ENTITY = "Invalid Entity: Values taken 'master_entity' or 'slave_entity'"

# Hostnames of systems
MASTER_HOST = "raspberrypi3"
SLAVE_HOST = "raspberrypi2"
