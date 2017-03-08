import numpy as np
import cv2

# Custom modules
from common import cameraTrigger as ct
from common import constantSource as cs
from common import cameraRectify as cr
from common import miscellaneous as msc

TOTAL_PICS = cs.getCalibReq()

while True:
    q = input("Do you want to perform stereo caliberation? (y/n): ")
    if q.lower() == 'y':
        print("Starting Stereo Caliberation...")
        print(str(TOTAL_PICS) + " pictures are needed to configure the stereo.\n")

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
        imgpoints_L = [] # 2d points in left camera image plane.
        imgpoints_R = [] # 2d points in right camera image plane.

        n = 1
        calibDir = cs.getCalibDataDir(cs.stereo)
        while n <= TOTAL_PICS:
            path_L = calibDir + "L" + str(format(n, '04')) + ".jpg"
            path_R = calibDir + "R" + str(format(n, '04')) + ".jpg"
            print("\n\n\nPicture No: " + str(n))
            input("Press Return/Enter key when ready: ")
            ct.takePic(path_L)
            ct.takeRemotePic(path_R)

            img_L = cv2.imread(path_L)
            img_R = cv2.imread(path_R)
            gray_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2GRAY)
            gray_R = cv2.cvtColor(img_R, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret_L, corners_L = cv2.findChessboardCorners(gray_L, (r, c), None)
            ret_R, corners_R = cv2.findChessboardCorners(gray_R, (r, c), None)

            # If found, add object points, image points (after refining them)
            if ret_L is True and ret_R is True:
                print("Good shoot...")
                objpoints.append(objp)

                cv2.cornerSubPix(gray_L, corners_L, (11, 11), (-1, -1), criteria)
                imgpoints_L.append(corners_L)
                cv2.cornerSubPix(gray_R, corners_L, (11, 11), (-1, -1), criteria)
                imgpoints_R.append(corners_R)

                # Draw and display the corners
                cv2.drawChessboardCorners(img_L, (r, c), corners_L, ret_L)
                cv2.imshow('img', img_L)
                cv2.drawChessboardCorners(img_R, (r, c), corners_R, ret_R)
                cv2.imshow('img', img_R)
                cv2.waitKey(500)
                n += 1
            else:
                print("Images not useful.!! Use a different orientation/position.")
        cv2.destroyAllWindows()

        # Loading camera calibration data
        print("Loading camera calibration data...")
        fileName = cs.getFileName(cs.camera, prefix="L")
        file = cs.getCalibDataDir(cs.root) + fileName
        dataSet = msc.readData(file)
        mtx_L, dist_L, rvecs, tvecs = dataSet

        fileName = cs.getFileName(cs.camera, prefix="R")
        file = cs.getCalibDataDir(cs.root) + fileName
        dataSet = msc.readData(file)
        mtx_R, dist_R, rvecs, tvecs = dataSet

        # Performing stereo calibration
        ret, rotate, translate, essential, fundamental = cv2.stereoCalibrate(
            objectPoints=objpoints, imagePoints1=imgpoints_L, imagePoints2=imgpoints_R,
            cameraMatrix1=mtx_L, distCoeffs1=dist_L, cameraMatrix2=mtx_R,
            distCoeffs2=dist_R, imageSize=gray_L.shape[::-1], flags=cv2.CV_CALIB_FIX_INTRINSIC)

        # Final stereo calibration dataset
        dataSet = (rotate, translate, essential, fundamental)

        while True:
            q = input("Would you like to store the calibration data? (y/n): ")
            if q.lower() == 'y':
                # Storing the calibration data in .data file
                print("\nStoring the following stereo caliberation data: ")
                print(" - Rotational Matrix\n - Translational Matrix\n - " +
                      "Essential Matrix\n - Fundamental Matrix\n")
                fileName = cs.getFileName(cs.stereo)
                file = cs.getCalibDataDir(cs.root) + fileName
                msc.writeData(file, dataSet)
                break
            elif q.lower() == 'n':
                print("Cancelling this will require you to perform the entire " +
                      "calibration again.!")
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
