#!/usr/bin/env python
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from std_msgs.msg import Bool, Float32
from car_speed import CarSpeed

class stopline():
	def __init__ (self):
		self.speed = CarSpeed()
		self.bridge = cv_bridge.CvBridge()
		#cv2.namedWindow("window", 1)
		self.image_sub = rospy.Subscriber('camera/rgb/image_raw', Image, self.image_callback)
		self.image_pub = rospy.Publisher('detect/stop_line', Image, queue_size=1)
		self.detect_stop_line = rospy.Publisher('detect/is_stop_line', Bool, queue_size=1)
		self.x = 0
		self.w = 0
		self.rate = rospy.Rate(3)

	def image_callback(self, msg):
		image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		lower_white = numpy.array([0, 0, 200])
		upper_white = numpy.array([0, 0, 255])

		mask = cv2.inRange(hsv, lower_white, upper_white)
		h, w = mask.shape
		image_stop = 2/h
		mask[0:image_stop, 0:w] = 0

		ret, thr = cv2.threshold(mask, 127, 255, 0)
		_, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		if contours:
			if len(contours) <= 0:
				return
			cnt = contours[len(contours) - 1]
			area = max(list(map(lamda x: cv2.contourArea(x), contours)))
			self.x, y, self.w, h = cv2.boundingRect(cnt)
			mask2 = cv2.ractangle(mask, (self.x, y), (self.x+self.w, y+h), (0, 0, 255), 2)
			cv2.drawContours(mask2, [cnt], 0, (255, 255, 0), 1)

			if 10000.0 < area:
				self.detect_stop_line(True)
				self.speed.set_speed(0)
				self.rate.sleep
				self.speed.set_speed(1)
				

			

