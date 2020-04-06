import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image as msg_Image
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
import sys
import os

node_name = os.path.basename(sys.argv[0]).split('.')[0]
rospy.init_node(node_name)

rospy.loginfo("Hello ROS!")
bridge = CvBridge()

x,y,z = 0,0,0
font = cv2.FONT_HERSHEY_SIMPLEX

def image_callback(img_msg):
    global x,y,z

    #log some info about the image topic
    rospy.loginfo(img_msg.header)

    try:
        cv_image = bridge.imgmsg_to_cv2(img_msg, "passthrough")
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))
    
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    lo_color = np.array([0,120,120])
    hi_color = np.array([10,255,255])

    mask = cv2.inRange(hsv,lo_color,hi_color)
    
    image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(cnt) for cnt in contours]
    
    if len(areas) == 0:
        return

    big_index = np.argmax(areas)

    big_area = contours[big_index]

    M = cv2.moments(big_area)

    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])
    
    print("BigArea:",big_area)

    cv_image = cv2.circle(cv_image,(x,y),5,(0,255,0),-1)
    
    show_text = "Z=" + str(int(z)) + " X=" + str(x) + " Y=" + str(y)
    cv2.putText(cv_image,show_text,(x,y), font, 1,(0,0,255),2,cv2.LINE_AA)

    cv2.imshow("Show Mask!",mask)
    cv2.imshow("Show Color!",cv_image)

    k = cv2.waitKey(1)
    if k == ord('q'):
        rospy.is_shutdown()

class ImageListener:
    def __init__(self, topic):
        self.topic = topic
        self.bridge = CvBridge()
        self.sub = rospy.Subscriber(topic, msg_Image, self.imageDepthCallback)

    def imageDepthCallback(self, data):
        global x,y,z
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, data.encoding)
            pix = (x, y)
            z = cv_image[pix[1], pix[0]]
            sys.stdout.write('Distance:%f'% (z))
            sys.stdout.flush()
        except CvBridgeError as e:
            print(e)
            return
    
sub_image = rospy.Subscriber("/camera/color/image_raw", Image, image_callback)

topic = '/camera/depth/image_rect_raw'
listener = ImageListener(topic)

while not rospy.is_shutdown():
    rospy.spin()

