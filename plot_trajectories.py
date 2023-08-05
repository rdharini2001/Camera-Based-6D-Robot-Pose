import json
import matplotlib.pyplot as plt

trajectories = {}

f1 = open('/home/rbccps/Desktop/ROS_Scripts/trajectory_220.json', 'r')
trajectories = json.load(f1)

X_history_cam = trajectories['X_history_cam']
Y_history_cam = trajectories['Y_history_cam']
X_history_lidar = trajectories['X_history_lidar']
Y_history_lidar = trajectories['Y_history_lidar']
yaw_history_cam = trajectories['yaw_history_cam']
yaw_history_lidar = trajectories['yaw_history_lidar']


f2 = open('/home/rbccps/Desktop/ROS_Scripts/trajectory_221.json', 'r')
trajectories = json.load(f2)

X_history_cam.extend(trajectories['X_history_cam'])
Y_history_cam.extend(trajectories['Y_history_cam'])
X_history_lidar.extend(trajectories['X_history_lidar'])
Y_history_lidar.extend(trajectories['Y_history_lidar'])
yaw_history_cam.extend(trajectories['yaw_history_cam'])
yaw_history_lidar.extend(trajectories['yaw_history_cam'])

f1.close()
f2.close()

plt.figure()
plt.xlim(-1.8, 4.2)
plt.ylim(-1.8, 5.4)
plt.plot(X_history_cam, Y_history_cam, 'r-', X_history_lidar, Y_history_lidar, 'g-')
plt.show()

f3 = open('/home/rbccps/Desktop/ROS_Scripts/trajectory_219.json', 'r')
trajectories = json.load(f3)

X_history_cam = trajectories['X_history_cam']
Y_history_cam = trajectories['Y_history_cam']
X_history_lidar = trajectories['X_history_lidar']
Y_history_lidar = trajectories['Y_history_lidar']
yaw_history_cam = trajectories['yaw_history_cam']
yaw_history_lidar = trajectories['yaw_history_cam']
f3.close()

plt.figure()
plt.xlim(-3, 0)
plt.ylim(-4.8, 0)
plt.plot(X_history_cam, Y_history_cam, 'r-', X_history_lidar, Y_history_lidar, 'g-')
plt.show()