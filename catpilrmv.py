#!/usr/bin/env python
#comment
import rospy
from transitions import Maschine


if __name__ == '__main__':
  rospy.init_node('caterpillar')
  rospy.Subscriber("joy", Joy, CaterpillarMove)
  
#definition of transitions





#definition of callback function

def CaterpillarMove
