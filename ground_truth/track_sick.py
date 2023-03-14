#! /usr/bin/env python

import sensor_msgs.point_cloud2 as pc2
import rospy
from sensor_msgs import point_cloud2
from sensor_msgs.msg import PointCloud2, LaserScan,PointField
import laser_geometry.laser_geometry as lg
import math
import rospy
import struct
from std_msgs.msg import Header

lp = lg.LaserProjection()


class laserconvert:
	def __init__(self):
		self.point_list=[]
		self.pub = rospy.Publisher("/converted_pc", PointCloud2, queue_size=1)
		self.header = Header()
		self.rate=rospy.Rate(50)
		self.header.frame_id = "cloud"
		self.fields = [PointField('x', 0, PointField.FLOAT32, 1),
          PointField('y', 4, PointField.FLOAT32, 1),
          PointField('z', 8, PointField.FLOAT32, 1),
          # PointField('rgb', 12, PointField.UINT32, 1),
          PointField('rgba', 12, PointField.UINT32, 1),
          ]
		self.filtered_points=[]
		self.filtered_points_first=[]

	def scan_cb(self,msg):
	    # convert the message of type LaserScan to a PointCloud2
		pc2_msg = lp.projectLaser(msg)
		err_pts=[]
		# distarr=[]
		# print("called")

		# or a list of the individual points which is less efficient
		scans = pc2.read_points(pc2_msg)
		scan_points=list(scans)
		# print("scans and point_list",len(scan_points),len(self.point_list))
		try:
			for ii in range(len(scan_points)):
				# distarr=[]
				# print(len(self.point_list))
				for jj in range(len(self.point_list)):
					# print("dsss")
					dist=math.sqrt(((self.point_list[jj][0])-(scan_points[ii][0]))**2+((self.point_list[jj][1])-(scan_points[ii][1]))**2)

					# if dist<=0.2 and 
					#0.082
					if dist>=0.05 and dist<=0.1: #distance between consecutive frames
						# print(dist)


						x=scan_points[ii][0]
						y=scan_points[ii][1]
						z=scan_points[ii][2]
						self.filtered_points_first.append([x,y,z])
						break

			x_pt=[]
			y_pt=[]
			# for ll in range(len(self.filtered_points)):
				
			# xdist=[]
			# ydist=[]
			for ll in range(len(self.filtered_points_first)):
				for ii in range(len(scan_points)):
					# distnew=
				
				# dist=math.sqrt()
					xdist=(self.filtered_points_first[ll][0]-scan_points[ii][0])**2
					ydist=(self.filtered_points_first[ll][1]-scan_points[ii][1])**2
					distxy=math.sqrt(xdist+ydist)

					if distxy<0.06:#distance between the points
						# print(distxy)

				

						x_pt.append(self.filtered_points_first[ll][0])
						y_pt.append(self.filtered_points_first[ll][1])

						r = 255
						g = 250
						b = 220
						a = 255
						# print r, g, b, a
						rgb = struct.unpack('I', struct.pack('BBBB', b, g, r, a))[0]
						# print hex(rgb)
						pt = [self.filtered_points_first[ll][0], self.filtered_points_first[ll][1], self.filtered_points_first[ll][2], rgb]
						self.filtered_points.append(pt)
						break


			if len(x_pt)>0 and len(y_pt)>0:
				aa=min(x_pt)
				bb=max(x_pt)
				cc=min(y_pt)
				dd=max(y_pt)
				lengthplank=math.sqrt((aa-bb)**2+(cc-dd)**2)
# 				print("len",lengthplank)
			else:
				lengthplank=0.0
		except Exception as e:
			print(e)
			pass

		# if lengthplank!=0.0:
		if 0.35<=lengthplank<=0.81:
		# if lengthplank>0.0:
			# print("again")

			pc2new = point_cloud2.create_cloud(self.header, self.fields, self.filtered_points)

			pc2new.header.stamp = rospy.Time.now()

			self.pub.publish(pc2new)
		else:
			# print("end")
			# print(len(self.filtered_points))
			for mm in range(1000):
				err_pts.append([-1000.0,-1000.0,-1000.0,255])
			pc2new = point_cloud2.create_cloud(self.header, self.fields,err_pts)

			pc2new.header.stamp = rospy.Time.now()



			self.pub.publish(pc2new)

		# print("fil",len(self.filtered_points))
		if len(self.filtered_points)!=0:
		
			self.point_list=self.filtered_points
			self.filtered_points=[]
			self.filtered_points_first=[]
		self.rate.sleep()


	def callback(self,data):
		# filtered_points=[]

		gen = pc2.read_points(data, skip_nans=True)
		self.point_list = list(gen)
		print(len(self.point_list))


		rospy.Subscriber("/scan", LaserScan, self.scan_cb,queue_size=1)
		# except KeyboardInterrupt:
		# 	print "done"

def listener():
	rospy.init_node('listener', anonymous=True)
	obj=laserconvert()

	rospy.Subscriber("/rviz_selected_points",PointCloud2, obj.callback)

	rospy.spin()

if __name__ == '__main__':
    listener()


