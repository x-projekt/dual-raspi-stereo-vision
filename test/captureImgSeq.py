""" From the root directory run the following command:
    '$> python3 -m test.imgSeqCapture'
"""

import time
from common import cameraTrigger as ct
from sense_hat import SenseHat

if __name__ == "__main__":
    wait = [0, 0, 255]
    go = [0, 255, 0]
    red = [255, 0, 0]

    sense = SenseHat()
    basePath = "test/image_{Y}_{X}.png"

    waitTime = int(input("Enter wait time (in sec): "))
    num = int(input("Number of images to take: "))

    for i in range(num):
        sense.clear(wait)
        time.sleep(waitTime)
        sense.clear(go)
        time.sleep(2)
        sense.clear(red)
        ct.takePic(basePath.format(Y="L", X=(i+1)))
        ct.takeRemotePic(basePath.format(Y="R", X=(i+1)))
        sense.clear()
