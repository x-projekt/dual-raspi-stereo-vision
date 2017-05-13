# Daul Rasberry Pi Stereo Vision
This project aims at performing 3D Stereo-mapping using Raspberry Pi's, Pi Camera CSI module and a custom designed 3D printed frame. We have also a Sense Hat for implementing localization in the future. We use [OpenCV](www.opencv.org) library for the purpose of computer vision.

## Setup and Configuration
Setting up the device consits of two phases, namely software and hardware setup phase. 
* **Hadware Setup:** This involves putting together the hardware and installing the required dirvers and libraries for running the software.
* **Software Setup:** This consistes of setting up the system configuration for running the stereo vision software, installing the stereo vision software, performing device calibration and making the device ready to use.  

### Hardware Setup
The most basic requirement is a frame to mount the electronics on to. The frame used for this project has a _baseline distance_ of 15 cm. The mechnical drawings are shown below. The STEP/STL files for 3D printing are available on [GrabCAD](https://grabcad.com/library/camera-mount-for-stereo-vision-1). You may download the SolidWorks part file and modify it as per your needs.

The following components were used in the project:

* [Raspberry Pi 2 Model B](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) (x1)
* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) (x1)
* [Pi NoIR CSI Camera Module](https://www.raspberrypi.org/products/pi-noir-camera-v2/) (x2)
* [Pi Sense Hat](https://www.raspberrypi.org/products/sense-hat/) (x1)

We will refer to Pi 2 as _Slave Pi_ and Pi 3 as _Master Pi_. All the image processing is performed on the Master Pi. The CSI Camera modules are attached to each of the Pi's. The Sense Hat is attached to the Master Pi. The two Pi's are connected to each other via ethernet cable. The entire setup is then mounted onto the 3D printed frame. This image below shows the entire hardware setup. 
![Image of entire setup]()  
**Note:** _Make sure that the two cameras are firmly fixed to the frame. Movement of cameras relative to each other can cause the user to perform the entire software again._

Now, flash an SD cards with Rasbpian OS. Follow the instaructions [here](https://www.raspberrypi.org/documentation/installation/installing-images/). Put the SD card into the Pi and boot into it. Now, connect SenseHat and CSI Camera module to the borad. Then in the device preferences enable the Camera, GPIO and SSH ports.  
**Note:** _You may also access the system configuration using the following command in the terminal and follow the instructions accordingly:_
```
$> sudo raspi-config
```    
After enabling the Camera, SSH and GPIO ports, run the following commands, to install the libraries for accessing the Cameras and Sense Hat. 
```
$> sudo apt-get update
$> sudo apt-get upgrade
```
The above commands will install the required python libraries and also update the raspbian OS. Now, we need to setup OpenCV on Raspberry Pi. We will be compiling OpenCV from source code and installing it. The steps for setting up OpenCV 3 in Raspberry Pi 3 model B are available at this [link][PYIMAGESERACH-RPI-OPENCV-SETUP] on pyimagesearach. Now that we have installed OpenCV and device drivers, we can move on to software setup.

### Software Setup
Stereo vision depends heavily on synchronization of images taken from he two cameras. Since, we are using two boards it is necessary for us to synchronize the imgae capture process. This is especially needed for setup's to be mounted on mobile platforms. We have two methods for performing synchronization of the cameras. We are performing 




[PYIMAGESERACH-RPI-OPENCV-SETUP]: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/