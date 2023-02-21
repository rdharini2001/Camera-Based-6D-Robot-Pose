import numpy as np
import cv2 as cv
import glob
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((5*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:5].T.reshape(-1,2)
# print(objp)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('*.jpeg')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (8,5), None)
    # print(corners)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (8,5), corners2, ret)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        # print()
        print(mtx)
        # print(type(mtx))
        cv.imshow('img', img)
        h,  w = img.shape[:2]
        print(h,w)
        # mtx1=np.array([[644.483,0,644.483*2],[0,644.483,644.483*2],[0,0,1]])
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
    # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite('calibresult.png', dst)
        
        mean_error = 0
        for i in range(len(objpoints)):
         imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
         error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
         mean_error += error
        print( "total error: {}".format(mean_error/len(objpoints)) )
        cv.waitKey(0)
cv.destroyAllWindows()