#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rospy.init_node('gogo')

gogo_twist = Twist()
gogo_twist.linear.x = 1

driving_forward = False
light_cahnge_time = rospy.Time.now()
rate = rospy.Rate(10)

while not rospy.is_shutdown():
   if driving_forward:
      cmd_vel_pub.publish(gogo_twist)
