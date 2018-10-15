#!/usr/bin/env python
#comment
import rospy
from sensor_msgs.msg import Joy
#from transitions import Maschine

#definition of transitions


def caterpillarMove(data):
    rospy.loginfo(type(data))
    rospy.loginfo(data.data)

if __name__ == '__main__':
  rospy.init_node('caterpillar')
  rospy.Subscriber("joy", Joy, caterpillarMove)
  rospy.spin()
  


