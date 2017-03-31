import time
from common import cameraTrigger as ct
from sense_hat import SenseHat

wait = [0, 0, 255]
go = [0, 255, 0]
red = [255, 0, 0]

sense = SenseHat()
basePath = "image_{Y}_{X}.png"

num = int(input("Number of images to take: "))

for i in range(num):
    sense.clear(wait)
    time.sleep(30)
    sense.clear(go)
    time.sleep(10)
    sense.clear(red)
    ct.takePic(basePath.format(Y="L", X=(i+1)))
    ct.takeRemotePic(basePath.format(Y="R", X=(i+1)))
    sense.clear()
