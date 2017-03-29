from multiprocessing import Queue, Process
import threading
import time
import queue
from common import cameraTrigger as ct
import cv2


# # Multi-threading test code:
# class myThread (threading.Thread):
#     def __init__(self, dev, ret):
#         threading.Thread.__init__(self)
#         self.dev = dev
#         self.ret = ret

#     def run(self):
#         if self.dev == 1:
#             #self.ret.append(ct.takePic())
#             self.ret.put(ct.takePic())
#         elif self.dev == 2:
#             #self.ret.append(ct.takeRemotePic())
#             self.ret.put(ct.takeRemotePic())

# #retVals = []
# retVals = queue.Queue()
# thread1 = myThread(1, retVals)
# thread2 = myThread(2, retVals)

# print("Starting threads...")
# start = time.time()
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# end = time.time()
# print("Process Ended...\n")

# count = 1
# while not retVals.empty():
#     cv2.imwrite("image{j}.png".format(j=count), retVals.get())
#     count += 1
# print("Complete time: " + str(end  - start))



# # Multi-processing test code:
# def processImage(id, q):
#     if id == 1:
#         q.put(ct.takePic())
#     elif id == 2:
#         q.put(ct.takeRemotePic())

# if __name__ == "__main__":
#     print("Starting threads...")
#     start = time.time()
#     retVals = Queue()
#     jobs = []
#     for i in range(2):
#         print("Starting process: " + str(i+1))
#         p = Process(target=processImage, args=((i+1), retVals, ))
#         jobs.append(p)

#     for job in jobs:
#         print("Starting job...")
#         job.start()

#     for job in jobs:
#         print("Joining job...")
#         job.join()

#     end = time.time()
#     print("Process Ended...\n")
#     count = 1
#     while not retVals.empty():
#         #cv2.imwrite("image{j}.png".format(j=count), retVals.get())
#         #print("Value {i} is {j}".format(i=count, j=retVals.get()))
#         count += 1
#     print("Complete time: " + str(end  - start))
