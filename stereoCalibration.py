import numpy as np
import cv2

# Custom modules
from common import cameraTrigger as ct
from common import constantSource as cs
from common import miscellaneous as msc
import stereoRectify as sr

TOTAL_PICS = cs.getCalibReq()

while True:
    q = input("Do you want to perform stereo caliberation? (y/n): ")
    if q.lower() == 'y':
        print("Starting Stereo Caliberation...")
        print(str(TOTAL_PICS) + " pictures are needed to configure the stereo.\n")

        checkerBoard = (9, 6)
        squareSize = None # square edge length in cm

        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((np.product(checkerBoard), 3), np.float32)
        objp[:, :2] = np.indices(checkerBoard).T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints1 = [] # 2d points in left camera image plane.
        imgpoints2 = [] # 2d points in right camera image plane.

        n = 1
        calibDir = cs.getCalibDataDir(cs.stereo)
        while n <= TOTAL_PICS:
            path1 = calibDir + cs.getCamera(1) + str(format(n, '04')) + ".png"
            path2 = calibDir + cs.getCamera(2) + str(format(n, '04')) + ".png"
            print("\nPicture No: " + str(n))
            input("Press Return/Enter key when ready: ")
            img1 = ct.takePic()
            img2 = ct.takeRemotePic()

            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            h, w = gray1.shape[:2]

            # Find the chess board corners
            ret1, corners1 = cv2.findChessboardCorners(gray1, checkerBoard, None)
            ret2, corners2 = cv2.findChessboardCorners(gray2, checkerBoard, None)

            # If found, add object points, image points (after refining them)
            if ret1 is True and ret2 is True:
                print("Good shoot...")
                cv2.imwrite(path1, img1)
                cv2.imwrite(path2, img2)

                cv2.cornerSubPix(gray1, corners1, (5, 5), (-1, -1), criteria)
                imgpoints1.append(corners1.reshape(-1, 2))
                cv2.cornerSubPix(gray2, corners1, (5, 5), (-1, -1), criteria)
                imgpoints2.append(corners2.reshape(-1, 2))
                objpoints.append(objp)

                # Draw and display the corners
                cv2.drawChessboardCorners(img1, checkerBoard, corners1, ret1)
                cv2.imshow('Image-1', img1)
                cv2.drawChessboardCorners(img2, checkerBoard, corners2, ret2)
                cv2.imshow('Image-2', img2)
                cv2.waitKey(500)
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
        result = cv2.stereoCalibrate(objectPoints=objpoints, imagePoints1=imgpoints1,
                                     imagePoints2=imgpoints2, cameraMatrix1=mtx1,
                                     distCoeffs1=dist1, cameraMatrix2=mtx2,
                                     distCoeffs2=dist2, imageSize=(w, h),
                                     flags=cv2.CALIB_FIX_INTRINSIC)

        # Final stereo calibration dataset
        dataSet = (result[5], result[6], result[7], result[8])

        while True:
            q = input("Would you like to test the stereo calibration " +
                      "parameters before proceeding? (y/n): ")
            if q.lower() == 'y':
                srcImage1 = ct.takePic()
                srcImage2 = ct.takeRemotePic()

                rectImage = sr.stereoRectify((mtx1, dist1, mtx2, dist2, result[5], result[6]),
                                             (srcImage1, srcImage2), cs.stream_mode)
                cv2.imshow("Rectified Image-1", rectImage[0])
                cv2.imshow("Rectified Image-2", rectImage[1])
                cv2.waitKey()
                cv2.destroyAllWindows()

                print("Saving rectified image...")
                source = calibDir + "_skewedImage1.png"
                target = calibDir + "_undistortImage1.png"
                cv2.imwrite(source, srcImage1)
                cv2.imwrite(target, rectImage[0])

                source = calibDir + "_skewedImage2.png"
                target = calibDir + "_undistortImage2.png"
                cv2.imwrite(source, srcImage2)
                cv2.imwrite(target, rectImage[1])
                break
            elif q.lower() == 'n':
                print("Canceling calibration parameters test...")
                break
            else:
                print(cs.getMessage(cs.invalid_binary, AB="YN"))


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
