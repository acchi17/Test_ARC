#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import UInt816ultiArray

btnlist = UInt816ultiArray()
btnlist.data = [0] * 14

def joytostdarray(ds4msg):
    global btnlist
    for i in range(14):
      btnlist.data[i] = ds4msg.buttons[i]

if __name__ == '__main__':
  rospy.init_node('joytostdmsg')  
  rospy.Subscriber("joy", Joy, joytostdarray)
  pub = rospy.Publisher('ds4btns', UInt8MultiArray, queue_size = 1)
  
  rate = rospy.Rate(10)
  while not rospy.is_shutdown():
    pub.publish(btnlist)
    rate.sleep()
