#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

class PickLine:
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        rospy.init_node('go_to_point_2')
        self.state_change_time = rospy.Time.now()
        self.driving_forward = True
        self.step_1 = False
        self.step_2 = False
        self.step_3 = False
        self.rate = rospy.Rate(10)

    def loop(self):
        while not rospy.is_shutdown():
            if self.driving_forward:
                if rospy.Time.now() > self.state_change_time:
                    self.step_1 = True
                    self.driving_forward = False
                    self.state_change_time = rospy.Time.now() + rospy.Duration(3.4)

            elif self.step_1:
                if rospy.Time.now() > self.state_change_time:
                    self.step_2 = True
                    self.step_1 = False
                    self.state_change_time = rospy.Time.now() + rospy.Duration(3)

            elif self.step_2:
                if rospy.Time.now() > self.state_change_time:
                    self.step_1 = False
                    self.step_3 = True
                    self.step_2 = False
                    self.state_change_time = rospy.Time.now() + rospy.Duration(3.4)

            elif self.step_3:
                if rospy.Time.now() > self.state_change_time:
                    self.step_3 = False
                    self.state_change_time = rospy.Time.now() + rospy.Duration(3.5)

            twist = Twist()
            if self.step_1:
                twist.angular.z = -0.45
            if self.step_2:
                twist.linear.x = 0.4
            if self.step_3:
                twist.angular.z = 0.45
            self.cmd_vel_pub.publish(twist)

            self.rate.sleep()

if __name__=='__main__':
    handler = PickLine()
    handler.loop()

