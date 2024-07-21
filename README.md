# Camera Based Pose Estimation 
In this project, we compare the performance of Aruco marker-based pose estimation approach with a deep learning-based marker-less method. 

# Step 1 - Intrinsic Camera Calibration 
1. Refer to the detailed documentation provided here - [camera calibration](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

# Step 2 - Extrinsic Calibration
In simple terms, extrinsic calibration involves finding the relative position and orientation between two cameras. 
1. Calibrate the cameras individually using the instructions above.
2. Use OpenCV's ```stereoCalibrate``` to find the relative pose between two cameras.

# Step 3: Homography Computation
For understanding basic concepts about homography transformations, refer to this [link](https://docs.opencv.org/4.x/d9/dab/tutorial_homography.html)


