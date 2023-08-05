# LAST UPDATED: JUN 06, 2023

#!/usr/bin/env python3

import cv2
import rospy

import math
import numpy as np

from cv_bridge import CvBridge
bridge=CvBridge()

from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped

# COMPUTES THE POSE OF THE BOT FROM THE CAMERA IMAGES BY DETECTING THE MARKER AND USING THE HOMOGRAPHY TO PROJECT IT TO THE REAL WORLD
# AND CALCULATES THE CENTRE OF THE VOLTA WITH THE POSE AND PUBLISHES IT AS 'CAMERA POSE'
# LOCAL VARIABLES, TO SWITCH BETWEEN CAMERAS FOR ERROR CALCULATION MODIFY THESE
# THESE VARIBALES CONTAIN:
# CAMERA NUMBERS:
#             -> 219 FOR THE CAMERA INSIDE THE LAB
#             -> 220 FOR THE CAMERA NEAR THE LIFT
#             -> 221 FOR THE CAMERA WITH THE L - VIEW
# TOPICS : CORRESPONDING TIME SYNCHRONIZED TOPICS FOR EACH CAMERA
# LATEST HOMOGRAPHY MATRICES -> 3x3 MATRIX MAPPING THE IMAGE PLANE TO THE CHOSEN REAL WORLD PLANE, 1 FOR EACH CAMERA
# CAMERA MATRICES -> 3x3 MATRIX WITH INTRINSICS, 1 FOR EACH CAMERA
# DISTORTION COEFFICIENTS -> 5x1 ARRAY OF DISTORTION COEFFICIENTS, 1 FOR EACH CAMERA

camera_number = '220'   # EITHER 219, 220, 221

topics = {'219' : 'cam1_sync',
          '220' : 'cam2_sync',
          '221' : 'cam3_sync'}

homography_matrix = {'219' : np.matrix([[ 1.36836082e+00,  9.75493567e-01,  9.59715657e+02],
                                        [-2.81827277e-02, -4.62794652e-01,  7.48434225e+01],
                                        [-1.79816570e-04,  1.24865401e-03,  1.00000000e+00]]),

                     '220' : np.matrix([[-1.36488680e+00, -6.64874500e-01,  5.07514340e+02],
                                        [-5.42129847e-03,  4.52024802e-01,  5.17564977e-01],
                                        [-5.78633051e-05, -1.06907560e-03,  1.00000000e+00]]),
                                        
                     '221' : np.matrix([[ 3.11583553e+00, -1.64346396e+00,  6.30826925e+02],
                                        [-1.27823680e+00, -1.17509894e+00,  4.15479230e+02],
                                        [ 1.65512427e-03,  1.26165579e-03,  1.00000000e+00]])}

camera_matrix = {'219' : np.array([[970.13975699,   0.        , 661.05696322], 
                                   [  0.        , 965.0683426 , 324.24867006], 
                                   [  0.        ,    0.       ,   1.        ]]),

                 '220' : np.array([[977.2273506776794,         0        , 654.9532086627172 ],
                                   [        0        , 974.6151749641901, 362.84191610521367],
                                   [        0        ,         0        ,         1         ]]),
                                   
                 '221' : np.array([[1001.9635615468297,         0.       , 640.3863811774163], 
                                   [       0.         , 997.5638802886575, 378.5734955839838],
                                   [       0.         ,         0.       ,        1.        ]])}

distortion_coefficients = {'219' : np.array([-0.44779831, 
                                             0.21493212, 
                                             0.0086979, 
                                             -0.00269077, 
                                             0.00281984]),

                           '220' : np.array([-0.45615534935009594,
                                             0.3052813779221815, 
                                             -0.0006738773409164597, 
                                             0.00014276677343467208, 
                                             -0.1678854476252372]),

                           '221' : np.array([-0.4772898916850898, 
                                              0.3687769534321386, 
                                              -0.004534580076559861, 
                                              0.003313908373350052,
                                              -0.2617377054540228])}

# IF YOU ARE JUST SWITCHING BETWEEN CAMERAS TO CALCULATE ERROR THEN DO NOT MODIFY BELOW

# A FUNCTION TO COMPUTE THE OBJECT POINTS GIVEN THE IMAGE POINTS AND HOMOGRAPHY MATRIX
def homo3d(goal):
    point = [goal[0],goal[1],1] # MAKING THE COORDINATES HOMOGENOUS
    mat = np.linalg.inv(homography_matrix[camera_number])
    # DEPENDING ON WHETHER THE MAPPING WAS FROM IMAGE -> WORLD OR WORLD -> IMAGE, THE ABOVE LINE MAY VARY AS INVERSE OR NOT

    prod=np.dot(mat,point)

    scalar=prod[0,2]
    return [(prod[0,0]/scalar),(prod[0,1]/scalar)] # RETURNING THE NON-H+++++++++++++++4rfOMOGENOUS COORDINATES

def callback(img):
    camera_pose = PoseStamped()
    pub = rospy.Publisher('/camera_pose',PoseStamped, queue_size=1)
    image = bridge.imgmsg_to_cv2(img, desired_encoding='passthrough')

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # THE SUBSCRIBED IMAGE GOES HERE
    aruco_dict_type = cv2.aruco.DICT_6X6_1000
    arucoDict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()
    corners, ids, _ = cv2.aruco.detectMarkers(gray, 
                                              arucoDict,
                                              parameters=parameters)

    
    # TO PLOT THE DETECTED MARKER
    # IF YOU ARE UNCOMMENTING THIS KEEP IN MIND TO COMMENT "TO FIND POSE"
    # PART OF THE CODE, IT IS NOT CONSISTENT

    # if len(corners) > 0:
	# # flatten the ArUco IDs list
    #     ids = ids.flatten()
	# # loop over the detected ArUCo corners
    #     for (markerCorner, markerID) in zip(corners, ids):
    #         # extract the marker corners (which are always returned in
    #         # top-left, top-right, bottom-right, and bottom-left order)
    #         corners = markerCorner.reshape((4, 2))
    #         (topLeft, topRight, bottomRight, bottomLeft) = corners
    #         # convert each of the (x, y)-coordinate pairs to integers
    #         topRight = (int(topRight[0]), int(topRight[1]))
    #         bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    #         bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    #         topLeft = (int(topLeft[0]), int(topLeft[1]))
    #         cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
    #         cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
    #         cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
    #         cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)
    #         # compute and draw the center (x, y)-coordinates of the ArUco
    #         # marker
    #         cX = int((topLeft[0] + bottomRight[0]) / 2.0)
    #         cY = int((topLeft[1] + bottomRight[1]) / 2.0)
    #         cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
    #         # draw the ArUco marker ID on the image
    #         cv2.putText(image, str(markerID),
    #             (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
    #             0.5, (0, 255, 0), 2)
    #         print("[INFO] ArUco marker ID: {}".format(markerID))
    #         # show the output image
    #         cv2.imshow("Image", image)
    #         cv2.waitKey(40)


    # TO FIND POSE  
    # UNDISTORT CORNER POINTS OBTAINED FROM THE IMAGE OF THE MARKER

    if len(corners) > 0:
        distorted_corner1 = [corners[0][0][0][0], corners[0][0][0][1]]
        distorted_corner2 = [corners[0][0][1][0], corners[0][0][1][1]]
        distorted_corner3 = [corners[0][0][2][0], corners[0][0][2][1]]
        distorted_corner4 = [corners[0][0][3][0], corners[0][0][3][1]]

        undistorted_corner1 = cv2.undistortPoints(np.array(distorted_corner1), camera_matrix[camera_number], distortion_coefficients[camera_number], P = camera_matrix[camera_number])
        undistorted_corner2 = cv2.undistortPoints(np.array(distorted_corner2), camera_matrix[camera_number], distortion_coefficients[camera_number], P = camera_matrix[camera_number])
        undistorted_corner3 = cv2.undistortPoints(np.array(distorted_corner3), camera_matrix[camera_number], distortion_coefficients[camera_number], P = camera_matrix[camera_number])
        undistorted_corner4 = cv2.undistortPoints(np.array(distorted_corner4), camera_matrix[camera_number], distortion_coefficients[camera_number], P = camera_matrix[camera_number])

        # COMPUTE YAW USING DIAGONAL1
        X2Y2 = homo3d([undistorted_corner2[0][0][0],undistorted_corner2[0][0][1]])
        X2 = X2Y2[0]
        Y2 = X2Y2[1]

        X4Y4 = homo3d([undistorted_corner4[0][0][0],undistorted_corner4[0][0][1]])
        X4 = X4Y4[0]
        Y4 = X4Y4[1]
        yaw1 = math.atan2((Y2-Y4), (X2-X4))
        yaw1 = yaw1 - math.pi/4
        if yaw1 > math.pi:
            yaw1 = yaw1 - 2*math.pi
        if yaw1 < -math.pi:
            yaw1 = 2*math.pi + yaw1

        # COMPUTE YAW USING DIAGONAL2

        X3Y3 = homo3d([undistorted_corner3[0][0][0],undistorted_corner3[0][0][1]])
        X3 = X3Y3[0]
        Y3 = X3Y3[1]

        X1Y1 = homo3d([undistorted_corner1[0][0][0],undistorted_corner1[0][0][1]])
        X1 = X1Y1[0]
        Y1 = X1Y1[1]
        yaw2 = math.atan2((Y3-Y1), (X3-X1)) + math.pi/4
        if yaw2 > math.pi:
            yaw2 = yaw2 - 2*math.pi
        if yaw2 < -math.pi:
            yaw2 = 2*math.pi + yaw2

        # COMMENT THE ENTIRE IF CONDITION IF HIGH YAW ERRORS ARE ENCOUNTERED
        if (yaw2 < 0 and yaw1 > 0) or (yaw2 > 0 and yaw1 < 0):
            print("diff",np.degrees(yaw1),np.degrees(yaw2))
            yaw = (yaw1 - yaw2) / 2
            
        else:
            yaw = (yaw1 + yaw2) / 2

        # TO FIND POSITION
        c1X = (X1 + X3) / 2.0
        c1Y = (Y1 + Y3) / 2.0
        c2X = (X2 + X4) / 2.0
        c2Y = (Y2 + Y4) / 2.0

        Xcentre = (c1X + c2X) / 2.0
        Ycentre = (c1Y + c2Y) / 2.0

        camera_pose.pose.position.x = Xcentre / 100
        camera_pose.pose.position.y = Ycentre / 100
        camera_pose.pose.position.z = yaw
        camera_pose.pose.orientation.x = 0.0
        camera_pose.pose.orientation.y = 0.0
        camera_pose.pose.orientation.z = 0.0
        camera_pose.pose.orientation.w = 1.0

        print("robot pose wrt world", camera_pose.pose.position.x, camera_pose.pose.position.y, np.degrees(camera_pose.pose.position.z))

        pub.publish(camera_pose)

    else:
        camera_pose.pose.position.x = 1000
        camera_pose.pose.position.y = 1000
        camera_pose.pose.position.z = 1000
        camera_pose.pose.orientation.x = 0.0
        camera_pose.pose.orientation.y = 0.0
        camera_pose.pose.orientation.z = 0.0
        camera_pose.pose.orientation.w = 1.0

        print("robot pose wrt world", camera_pose.pose.position.x, camera_pose.pose.position.y, np.degrees(camera_pose.pose.position.z))

        pub.publish(camera_pose)

def cam1_listener():
    rospy.init_node('cam_listener', anonymous=True)
    rospy.Subscriber(f"{topics[camera_number]}", Image, callback, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    try:
        cam1_listener()
    except rospy.ROSInterruptException:
        pass