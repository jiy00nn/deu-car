#!/usr/bin/env python
import cv2
import numpy
import cv_bridge
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

class DetectedBar:
    def __init__(self):
        rospy.init_node("detected_bar")
        self.bridge = cv_bridge.CvBridge()
        self.cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
        self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
        self.bar_pub = rospy.Publisher('camera/rgb/image_raw/p2_bar', Image, queue_size=1)
        self.twist = Twist()
        self.bar_signal = False
        self.start_time = rospy.Time.now()

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
        self.bar_signal = True
        if M['m00'] > 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(barimage, (cx, cy), 10, (255, 0, 0), -1)
            self.bar_signal = False
        self.cmd_vel_pub.publish(self.twist)
        bar_image_msg = self.bridge.cv2_to_imgmsg(barimage, 'bgr8')
        self.bar_pub.publish(bar_image_msg)

    def go_forward(self):
        self.twist.linear.x = 0.8
        self.cmd_vel_pub.publish(self.twist)

    def stop(self):
        self.twist.linear.x = 0.0
        self.cmd_vel_pub.publish(self.twist)

    def loop(self):
        while not rospy.is_shutdown():
            if self.bar_signal == True:
                self.go_forward()
                if (rospy.Time.now() - self.start_time) > rospy.Duration.from_sec(10):
                    break
            else:
                self.stop()


if __name__=='__main__':
    rospy.init_node("detected_bar")
    detected_bar = DetectedBar()
    detected_bar.loop()
