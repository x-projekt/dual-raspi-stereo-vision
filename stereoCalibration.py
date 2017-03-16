import numpy as np
import cv2

# Custom modules
from common import cameraTrigger as ct
from common import constantSource as cs
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
        imgpoints1 = [] # 2d points in left camera image plane.
        imgpoints2 = [] # 2d points in right camera image plane.

        n = 1
        calibDir = cs.getCalibDataDir(cs.stereo)
        while n <= TOTAL_PICS:
            path1 = calibDir + cs.getCamera(1) + str(format(n, '04')) + ".png"
            path2 = calibDir + cs.getCamera(2) + str(format(n, '04')) + ".png"
            print("\n\n\nPicture No: " + str(n))
            input("Press Return/Enter key when ready: ")
            img1 = ct.takePic()
            img2 = ct.takeRemotePic()

            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret1, corners1 = cv2.findChessboardCorners(gray1, (r, c), None)
            ret2, corners2 = cv2.findChessboardCorners(gray2, (r, c), None)

            # If found, add object points, image points (after refining them)
            if ret1 is True and ret2 is True:
                print("Good shoot...")
                objpoints.append(objp)

                cv2.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
                imgpoints1.append(corners1)
                cv2.cornerSubPix(gray2, corners1, (11, 11), (-1, -1), criteria)
                imgpoints2.append(corners2)

                # Draw and display the corners
                cv2.drawChessboardCorners(img1, (r, c), corners1, ret1)
                cv2.imshow('img', img1)
                cv2.drawChessboardCorners(img2, (r, c), corners2, ret2)
                cv2.imshow('img', img2)
                cv2.waitKey(500)
                cv2.imwrite(path1, img1)
                cv2.imwrite(path2, img2)
                n += 1
            else:
                print("Images not useful.!! Use a different orientation/position.")
        cv2.destroyAllWindows()

        # Loading camera calibration data
        print("Loading camera calibration data...")
        fileName = cs.getFileName(cs.camera, prefix=cs.getCamera(1))
        file = cs.getCalibDataDir(cs.root) + fileName
        dataSet = msc.readData(file)
        mtx1, dist1, rvecs, tvecs = dataSet

        fileName = cs.getFileName(cs.camera, prefix=cs.getCamera(2))
        file = cs.getCalibDataDir(cs.root) + fileName
        dataSet = msc.readData(file)
        mtx2, dist2, rvecs, tvecs = dataSet

        # Performing stereo calibration
        ret, rotate, translate, essential, fundamental = cv2.stereoCalibrate(
            objectPoints=objpoints, imagePoints1=imgpoints1, imagePoints2=imgpoints2,
            cameraMatrix1=mtx1, distCoeffs1=dist1, cameraMatrix2=mtx2,
            distCoeffs2=dist2, imageSize=gray1.shape[::-1], flags=cv2.CV_CALIB_FIX_INTRINSIC)

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
                    print("Calibration data not stored.!")
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
