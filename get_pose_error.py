# LAST UPDATED: JUN 06, 2023

#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped

# CODE CALCULATES THE ERROR BETWEEN THE POSE PUBLISHED FROM THE POSE FROM CAMERA SCRIPT AND THE LIDAR POSE
# LOCAL VARIABLES, DO NOT MODIFY ANYTHING ELSE IN THE CODE FOR SWITCHING BETWEEN CAMERAS
# CAMERA POSE -> STORES CAMERA POSE FOR CALCULATING THE ERROR
# MAE X -> MEAN ABSOLUTE ERROR IN X
# MAE Y -> MEAN ABSOLUTE ERROR IN Y
# MSE POSITION -> MEAN EUCLIDEAN DISTANCE ERROR
# E YAW -> ERROR IN YAW
# AVERAGE COUNTER -> TO KEEP A COUNT OF NUMBER OF POINTS TO AVERAGE OVER
# CAMERA NAME:
#             -> 219 FOR THE CAMERA INSIDE THE LAB
#             -> 220 FOR THE CAMERA NEAR THE LIFT
#             -> 221 FOR THE CAMERA NEAR Prof. BA's CABIN
# CAMERA CONDITIONS -> HOLDS THE BOOLEAN VALUE FOR WHETHER THE VOLTA IS WITHIN THE CAMERAS BEST VISIBLE REGION OR NOT
# CAMERA VISIBLE REGIONS FROM THE ORIGIN:
#       219 : -3m < x_camera < 0m , -4.8m < y_camera < 0m 
#       220 : -1.8m < x_camera < 0.45m , 2.4m < y_camera < 5.4m
#       221 : -1.8m < x_camera < 4.20m , -1.8m < y_camera < 2m 
# LIDAR CONDITION -> HOLDS THE BOOLEAN VALUE OF WHETHER THE PLANK ON THE VOLTA IS TRACKED OR NOT

# LIDAR NAME -> SICK OR VELODYNE
lidar_name = 'sick'

def lidar_callback(lidar_pose):
    
    global camera_pose, MAE_X, MAE_Y, MSE_position, average_counter, E_yaw 
    global MAE_X_history, MAE_Y_history, MSE_position_history, E_yaw_history # NOT BEING USED IN THE CODE BUT CAN BE USED FOR PLOTS

    average_counter += 1
    camera_name = '220'

    x_centre_lidar = lidar_pose.pose.position.x
    y_centre_lidar = lidar_pose.pose.position.y
    yaw_lidar = np.degrees(lidar_pose.pose.position.z)

    x_centre_camera = camera_pose.pose.position.x
    y_centre_camera = camera_pose.pose.position.y
    yaw_camera = np.degrees(camera_pose.pose.position.z)

    # TO ACCOMODATE FOR THE NOISY JUMPS IN YAW WHERE IT MAY JUMP TO 180 - YAW OR - YAW
    yaw_difference = min([abs(yaw_lidar - yaw_camera),
                          abs(yaw_lidar + yaw_camera),
                          abs(yaw_lidar - (180 - yaw_camera)),
                          abs(yaw_lidar - (180 + yaw_camera))])
    
    # THE LIDAR GIVES OUT UNREALISTIC VALUES WHEN NO OBJECT IS BEING TRACKED, TO IGNORE THOSE VALUES:
    lidar_condition = x_centre_lidar > 15 or y_centre_lidar > 15 or yaw_difference > 100

    camera_conditions = {'219' : (-3 < x_centre_camera < 0 and -4.8 < y_centre_camera < 0),
                         '220' : (-1.8 < x_centre_camera < 0.45 and 2.4 < y_centre_camera < 5.4),
                         '221' : (-1.8 < x_centre_camera < 4.2 and -1.8 < y_centre_camera < 2)}
    
    # print(f'camera pose (x, y, yaw): {x_centre_camera}, {y_centre_camera}, {yaw_camera}')
    # print(f'LiDAR pose (x, y, yaw): {x_centre_lidar}, {y_centre_lidar}, {yaw_lidar}')

    # IF YOU ARE JUST SWITCHING BETWEEN CAMERAS TO CALCULATE ERROR THEN DO NOT MODIFY BELOW

    if camera_conditions[camera_name]:

        if lidar_condition:
            pass

        else:
            absolute_error_x = abs(x_centre_camera - x_centre_lidar)
            absolute_error_y = abs(y_centre_camera - y_centre_lidar)
            euclidean_error = np.sqrt((x_centre_camera - x_centre_lidar)**2 + (y_centre_camera - y_centre_lidar)**2)

            MAE_X = ((MAE_X * (average_counter - 1)) + absolute_error_x) / average_counter
            MAE_Y = ((MAE_Y * (average_counter - 1)) + absolute_error_y) / average_counter
            MSE_position = ((MSE_position * (average_counter - 1)) + euclidean_error) / average_counter
            E_yaw = ((E_yaw * (average_counter - 1)) + yaw_difference) / average_counter

            MAE_X_history.append(MAE_X)
            MAE_Y_history.append(MAE_Y)
            MSE_position_history.append(MSE_position)
            E_yaw_history.append(E_yaw)
            
            print(f'Mean Absolute Error in X (cm): {round(MAE_X*100, 3)}', end=' | ')
            print(f'Mean Absolute Error in Y (cm): {round(MAE_Y*100, 3)}', end=' | ')
            print(f'Euclidean Distance (cm): {round(MSE_position*100, 3)}', end=' | ')
            print(f'Mean Error in Yaw (deg): {round(E_yaw, 3)}')

def camera_callback(cam1_pose):
    global camera_pose
    camera_pose = cam1_pose
    rospy.Subscriber(f"/final_gt_{lidar_name}", PoseStamped, lidar_callback, queue_size=10)

def pose_listener():
    rospy.init_node('pose_listener', anonymous=True)
    rospy.Subscriber("/camera_pose", PoseStamped, camera_callback, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    camera_pose = 0
    MAE_X = 0
    MAE_Y = 0
    MSE_position = 0
    average_counter = 0
    E_yaw = 0

    MAE_X_history = []
    MAE_Y_history = []
    MSE_position_history = []
    E_yaw_history = []

    try:
        pose_listener()
    except rospy.ROSInterruptException or KeyboardInterrupt:
        pass