#!/usr/bin/env python
#comment
import rospy
from sensor_msgs.msg import Joy
#from transitions import Machine
import pigpio  # sudo apt install pigpio

#definition of const values
S_BUTTON = 0
X_BUTTUON = 1
C_BUTTON = 2
T_BUTTON = 3

REST = 10
FORWARD = 20
BACK = 30
TURN_RIGHT = 40
TURN_LEFT = 50

GPIO_CATPILR10 = 12
GPIO_CATPILR11 = 18
GPIO_CATPILR20 = 13
GPIO_CATPILR21 = 19

#definition of transitions
'''
states = ['REST', 'FORWARD', 'BACK', 'TURN_RIGHT', 'TURN_LEFT']

transitions = [
    { 'trigger': 'PUSH_T', 'source': 'REST', 'dest': 'FORWARD' },
    { 'trigger': 'PUSH_X', 'source': 'REST', 'dest': 'BACK' },
    { 'trigger': 'PUSH_C', 'source': 'REST', 'dest': 'TURN_RIGHT' }, 
    { 'trigger': 'PUSH_S', 'source': 'REST', 'dest': 'TURN_LEFT' },
    { 'trigger': 'PULL_T', 'source': 'FORWARD', 'dest': 'REST' },
    { 'trigger': 'PULL_X', 'source': 'BACK', 'dest': 'REST' },
    { 'trigger': 'PULL_C', 'source': 'TURN_RIGHT', 'dest': 'REST' },
    { 'trigger': 'PULL_S', 'source': 'TURN_LEFT', 'dest': 'REST' },
]
'''

#definition of gloval values
#initial state = REST 
mvstate = 10

#create instance of pigpio.pi() class
pi3 = pigpio.pi()
#GPIO I/Omode setting
pi3.set_mode()

#definition of state functions
def restfunc
    pi3.set
    if ds4msg.button[S_BUTTON] = 1:
        

def caterpillarMove(ds4msg):
    #test code
    rospy.loginfo(type(ds4msg))
    rospy.loginfo(ds4msg.data)
    
    if mvstate = REST:
    elif mvstate = 20
    elif mvstate = 30
    elif mvstate = 40
    elif mvstate = 50
    else:
    

if __name__ == '__main__':
  rospy.init_node('caterpillar')  
  rospy.Subscriber("joy", Joy, caterpillarMove)
  rospy.spin()
  


