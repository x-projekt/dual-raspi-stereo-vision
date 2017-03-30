## This is basic hardware configuration
CAMERA_1 = "L" # Connected to Master Pi
CAMERA_2 = "R" # Connected to Slave Pi
BASELINE = 150 # in mm

# Optimized values for disparity map generation
# These values are dependent on hardware used
DISP_VALUES = None

# Camera Constants
FRAME_RATE = 30 # in fps
IMAGE_RESOLUTION = (640, 480) # in pixels
FOCAL_LENGTH = (3.04, 2.0) # in (focal_length_in_mm, aperture)
FOV_H = 62.2 # in degrees
FOV_V = 48.8 # in degrees
PIXEL_SIZE = (1.12, 1.12) # Pixel size in um (10e-6 m)
PIXEL_COUNT = (3280, 2464) # Pixel count is of active pixels

# Path Constants
MASTER_IP = "192.168.120.170"
SLAVE_IP = "192.168.120.10"
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
