#!/usr/bin/env python
# BEGIN ALL
import cv2
import numpy
import cv_bridge
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

class DetectedBar:
    def __init__(self):  # creator Detector_Bar
        self.bridge = cv_bridge.CvBridge()
        # cv2.namedWindow("window", 1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.bar_pub = rospy.Publisher('camera/rgb/image_raw/p2_bar', Image, queue_size=1)  # detect blockbar
        self.twist = Twist()
        self.linecount=0

    def image_callback(self, msg):
        barimage = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        hsv = cv2.cvtColor(barimage, cv2.COLOR_BGR2HSV)
        lower_red = numpy.array([0, 30, 30])
        upper_red = numpy.array([10, 255, 130])
        mask = cv2.inRange(hsv, lower_red, upper_red)  # color_into_red_color
        h, w, d = barimage.shape
        search_top = 1
        search_bot = 3 * h / 4
        mask[0:search_top, 0:w] = 0
        mask[search_bot:h, 0:w] = 0
        mask[0:h, 0:250] = 0

        M = cv2.moments(mask)
        self.twist.linear.x = 0.8
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(barimage, (cx, cy), 10, (255, 0, 0), -1)
            # BGR = RED
            # BEGIN CONTROL
            self.twist.linear.x = 0.0
            # END CONTROL
            rospy.loginfo('detecting bar...')
        self.cmd_vel_pub.publish(self.twist)
        bar_image_msg = self.bridge.cv2_to_imgmsg(barimage, 'bgr8')
        self.bar_pub.publish(bar_image_msg)  # publish