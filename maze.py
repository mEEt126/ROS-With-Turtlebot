#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

class maze_solving():
	def __init__(self):
		rospy.init_node('mazesolvingnode')
		self.vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size = 5 )
		self.laser_subscriber = rospy.Subscriber('/kobuki/laser/scan', LaserScan, self.laser_callback)
		self.cmd = Twist()
        	self.laser_msg = LaserScan()
		self.rate = rospy.Rate(10)
		self.destination_flag = 0

	def laser_callback(self, msg):
        	self.laser_msg = msg

	def get_laser(self, pos):
        	time.sleep(1)
       	 	return self.laser_msg.ranges[pos]

	def stop_turtlebot(self):
		self.cmd.linear.x = 0.0
		self.cmd.angular.z = 0.0

		self.vel_publisher.publish(self.cmd)
		rospy.loginfo("Turtlebot Stopped.!")

	def go_straight(self):
		self.cmd.linear.x = 0.5
		self.cmd.linear.y = 0
		self.cmd.linear.z = 0
		self.cmd.angular.x = 0
		self.cmd.angular.y = 0
		self.cmd.angular.z = 0

		self.vel_publisher.publish(self.cmd)
		rospy.loginfo("cmd Published")

	def destination(self):
		rospy.loginfo("Destination Reached.!")
		self.destination_flag = 1


	def node_detected(self):
		self.stop_turtlebot()
		left=self.get_laser(0)
		straight=self.get_laser(360)
		right=self.get_laser(719)
		rospy.loginfo("left:" + str(left))
		rospy.loginfo("straight:" + str(straight))
		rospy.loginfo("right:" + str(right))
		time.sleep(1)
		if left > right:
			self.turn('left')
		else:
			self.turn('right')

	def turn(self, node_type):
		self.cmd.linear.x = 0
		self.cmd.linear.y = 0
		self.cmd.linear.z = 0
		self.cmd.angular.x = 0
		self.cmd.angular.y = 0
		if node_type == "left":
            		self.cmd.angular.z = -0.5
        	else:
            		self.cmd.angular.z = 0.5
		self.vel_publisher.publish(self.cmd)
		time.sleep(3)
		rospy.loginfo("turing")			
		self.stop_turtlebot()

	def main(self):
		while(self.destination_flag != 1):
			present_reading = self.get_laser(360)
			rospy.loginfo(present_reading)
			if (present_reading == 'inf'):
				self.destination()
				self.stop_turtlebot()
				time.sleep(5)
			elif (present_reading <= 1):
				self.node_detected()
			else :
				self.go_straight()
		


if __name__ == '__main__':
    
    Maze_solver_turtlebot = maze_solving()
    try:
        Maze_solver_turtlebot.main()

    except rospy.ROSInterruptException:
        pass
