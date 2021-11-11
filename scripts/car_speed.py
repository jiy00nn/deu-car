#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist

class CarSpeed:

	def __init__(self):
		self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
		self.twist = Twist()
		self._speed = 0
		self._angular = 0

	def set_speed(self, speed):  
		self._speed = speed  #linear.x

	def set_angular(self, angular):
		self._angular = angular #angular.z

	def drive(self):
		self.twist.linear.x = self._speed
		self.twist.angular.z = self._angular
		self.cmd_vel_pub.publish(self.twist)


if __name__ == "__main__":
	rospy.init_node('car_speed')
	carspeed = CarSpeed()
	carspeed = set.speed(1)
	carspeed.drive
	rospy.spin()
