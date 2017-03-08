import numpy as np
import cv2

# Custom modules
from common import cameraTrigger as ct
from common import constantSource as cs
from common import cameraRectify as cr
from common import miscellaneous as msc

TOTAL_PICS = cs.getCalibReq()

while True:
    q = input("Do you want to perform camera caliberation? (y/n): ")
    if q.lower() == 'y':
        print("Starting Camera Caliberation...")
        print(str(TOTAL_PICS) + " pictures are needed to configure the camera.\n")
        while True:
            camType = input("Enter the camera that you want to caliberate (l/r): ")
            camType = camType.upper()
            if camType == "L" or camType == "R":
                break
            else:
                print("Invalid Input: The camera options are R-right and L-left.!")

        checkerBoard = (9, 6)
        r = checkerBoard[0]
        c = checkerBoard[1]

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((r*c, 3), np.float32)
        objp[:, :2] = np.mgrid[0:r, 0:c].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        n = 1
        calibDir = cs.getCalibDataDir(cs.camera)
        while n <= TOTAL_PICS:
            path = calibDir + camType + str(format(n, '04')) + ".jpg"
            print("\n\nPicture No: " + str(n))
            input("Press Return/Enter key when ready: ")
            ct.takePic(path)

            img = cv2.imread(path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (r, c), None)

            # If found, add object points, image points (after refining them)
            if ret is True:
                print("Good shoot...")
                objpoints.append(objp)

                cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

                # Draw and display the corners
                cv2.drawChessboardCorners(img, (r, c), corners, ret)
                cv2.imshow('img', img)
                cv2.waitKey(500)
                n += 1
            else:
                print("Image not useful.!! Use a different orientation/position.")
        cv2.destroyAllWindows()

        # Performing camera calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPoints=objpoints,
            imagePoints=imgpoints, imageSize=gray.shape[::-1], cameraMatrix=None,
            distCoeffs=None)

        # Final camera specific dataSet
        dataSet = (mtx, dist, rvecs, tvecs)

        while True:
            q = input("Would you like to test the camera calibration " +
                    "parameters before proceeding? (y/n): ")
            if q.lower() == 'y':
                source = calibDir + camType + "_skewedImage.png"
                target = calibDir + camType + "_undistortImage.png"
                ct.takePic(source)
                cr.rectifyImage(dataSet, source, target)
                cv2.imshow("Rectified Image", cv2.imread(target))
                break
            elif q.lower() == 'n':
                print("Canceling calibration parameters test...")
                break
            else:
                print("Invalid Input: valid inputs are 'y' and 'n' only.")

        while True:
            q = input("Would you like to calculate re-projection error? (y/n): ")
            if q.lower() == 'y':
                print("Starting error calculation...")
                mean_error = 0
                tot_error = 0
                for i in range(len(objpoints)):
                    imgpoints2 = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)[0]
                    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
                    tot_error += error

                print("Total Error: ", mean_error/len(objpoints))
                break
            elif q.lower() == 'n':
                print("Canceling error calculation...")
                break
            else:
                print("Invalid Input: valid inputs are 'y' and 'n' only.")

        while True:
            q = input("Would you like to store the calibration data? (y/n): ")
            if q.lower() == 'y':
                # Storing the calibration data in .data file
                print("\nStoring the following caliberation data: ")
                print(" - Camera Matrix\n - Distrotion Coefficients\n - " +
                      "Rotation Vector\n - Translation Vector\n")
                fileDir = cs.getCalibDataDir(cs.root)
                fileName = cs.getFileName(cs.camera, prefix=camType)
                file = fileDir + fileName
                msc.writeData(file, dataSet)
                break
            elif q.lower() == 'n':
                print("Cancelling this will require you to perform the" +
                      " entire calibration again.!")
                q = input("Confirm cancellation? (y/n): ")
                if q.lower() == 'y':
                    break
                else:
                    pass

        print("Process completed successfully...")
        break
    elif q.lower() == 'n':
        print("Canceling Caliberation...")
        break
    else:
        print("Invalid Input: valid inputs are 'y' and 'n' only.")
