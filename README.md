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
![Image of entire setup][setup-image]  
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

#### Camera Synchronization
Stereo vision depends heavily on synchronization of images taken from he two cameras. Since, we are using two boards it is necessary for us to synchronize the imgae capture process. This is especially needed for setup's to be mounted on mobile platforms. We have two suggested methods for performing camera synchronization, NTP (Network Time Protocol) based method and Pulse based synchronization.  
* NTP Synchronization:
    * This method useses synchronized time to perform cameras synchronization. We run two independent scripts on the two borads, each of which takes pictures at fixed intervals of time. 
    * This method is accurate but we can't control when to take pictures. So, we won't be able to correct camera triggers for any unexpected changes in execution times. 
* Hardware Synchronization:
    * This method uses pulses of voltage for triggering the cameras. We run independent scripts on the each of Pi's, which moniter hte GPIO pins for pulses.
    * This method is simple and robust. This also allows for controlling when the camera's are tirggered. The figure below shows the hardware trigger method.  

The implementation of the above two methods is **_still under development_**.  
##### NTP Synchronization
For NTP Synchronization, we setup and NTP server on the Master Pi and synchronize time on the Slave Pi. For this, follow the following steps:
* Setup static IP address for each of the Pi's.  
    Append the following lines to _etc/dhcpcd.conf_ on Master Pi.
    ```
    interface eth0
    static ip_address=192.168.120.170
    static routers=192.168.120.1
    static domain_name_servers=192.168.120.1
    ```
    Append the following lines to _etc/dhcpcd.conf_ on Slave Pi.
    ```
    interface eth0
    static ip_address=192.168.120.10
    static routers=192.168.120.1
    static domain_name_servers=192.168.120.1
    ```
* Setup NTP Server-client on Master and Slave Pi's respectively.  
    Replace the _etc/ntp.conf_ with the file in _piConfig_ directory of repository. The files are named as per the Pi on which they belong, i.e. _npt.conf.master_ to replace _etc/ntp.conf_ on Master Pi etc.  
    Now, to force synchronization of time on Slave Pi, run the following commands.
    ```
    $> sudo service ntp stop
    $> sudo ntpd -gq
    $> sudo service ntp start
    ```

**Note:** The time on Master Pi is not accurate to real world. But the time's on the Slave Pi and Master Pi are synchronized, and this is what we need.

##### Hardware Synchronization
The picture below shows the implementation of hardware synchronization of the two camera's. 
![Hardware Synchronization image][hardware-sync]  

#### Software Installation and Calibration
Clone the repository at a convenient location on both the Pi's. In this example we have cloned the repository in _~/Documents/_ directories of Master and Slave Pi's respectively. Run the following command to clone the repositroy:
```
$> git clone https://github.com/harshatech2012/dual-raspi-stereo-vision.git
```
Now, we need to perform camera calibration aand stereo calibration. This sterp requires a checkerboard pattern. Print the checkerboard pattern in _calibData/res/checkerboard.pdf_ onto a flat surface and Run the following commands and follow the on-screen instructions.
```
$> python3 cameraCalibration.py
...
$> python3 stereoCalibration.py
...
```
**Note:** For better results during calibration hold the checherboard pattern as close to the camera as possible. And make sure that the checkerboard pattern is on a flat surface.  

## Runing the application
Once the calibration has completed successfully. Start the application by running the _RUN.py_ file. Run the following command in terminal and follow the onscreen instructions.
```
$> python3 RUN.py
```

There are some test files available in _test/_ directory of the repository. Use them for testing the calibatration and performance of the sytem.



[PYIMAGESERACH-RPI-OPENCV-SETUP]: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

[setup-image]: https://github.com/harshatech2012/shared-resources/blob/master/readme_dump/DRSV_setup_image.jpg

[hardware-sync]: https://github.com/harshatech2012/shared-resources/blob/master/readme_dump/DRSV_hardware_trigger.png
