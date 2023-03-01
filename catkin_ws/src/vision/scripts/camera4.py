#!/usr/bin/env python3 
import cv2
from subprocess import Popen, PIPE
import shlex
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge=CvBridge()
rtsp_url = 'rtsp://admin:artpark123@192.168.0.222:554/Streaming/Channels/1/'
gstreamer_exe = 'gst-launch-1.0' 

p = Popen(shlex.split(f'{gstreamer_exe} --quiet rtspsrc location={rtsp_url} latency=0 ! queue2 ! rtph264depay ! avdec_h264 ! videoconvert ! capsfilter caps="video/x-raw, format=BGR" ! timeoverlay ! fdsink'), stdout=PIPE)
width = 1280
height = 720

def talker():
    pub=rospy.Publisher('/cam4',Image,queue_size=1)
    rospy.init_node('camera4',anonymous=False)
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        raw_image = p.stdout.read(width * height * 3)
        frame = np.frombuffer(raw_image, np.uint8).reshape((height, width, 3))
        # cv2.imshow('Frames',frame)
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        
        msg=bridge.cv2_to_imgmsg(frame,"bgr8")
        pub.publish(msg)

         
        if rospy.is_shutdown():
            p.release()
            cv2.destroyAllWindows()
         
if __name__ == '__main__':
    try:
       talker()
    except rospy.ROSInterruptException:
        pass