#!/usr/bin/env python
#comment
import rospy
from std_msgs.msg import UInt16MultiArray
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

GPIO_CATPILR10 = 12  # front-left wheel
GPIO_CATPILR11 = 18  # rear-left wheel
GPIO_CATPILR20 = 13  # front-right wheel
GPIO_CATPILR21 = 19  # rear-right wheel

MTR_PWM_HZ = 10  # unit:Hz
MTR_PWM_HZ_ZERO = 0  # unit:Hz
LEFT_MTR_PWM_DUTY = 1000000  # unt:?
RIGHT_MTR_PWM_DUTY = 1000000  # unt:?
MTR_PWM_DUTY_ZERO = 0  # unt:?

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
mvstate = REST

#create instance of pigpio.pi() class
pi3 = pigpio.pi()
#GPIO I/Omode setting
pi3.set_mode(GPIO_CATPILR10, pigpio.OUTPUT)
pi3.set_mode(GPIO_CATPILR11, pigpio.OUTPUT)
pi3.set_mode(GPIO_CATPILR20, pigpio.OUTPUT)
pi3.set_mode(GPIO_CATPILR21, pigpio.OUTPUT)

#definition of state functions
#REST state function
def restfunc(data):
    #test code
    printf(mvstate)
    pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    
    if data.data[S_BUTTON] == 1:
        global mvstate
        mvstate = TURN_LEFT
        pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ, LEFT_MTR_PWM_DUTY)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ, RIGHT_MTR_PWM_DUTY)
        
    elif data.data[X_BUTTON] == 1:
        global mvstate
        mvstate = BACK
        pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ, LEFT_MTR_PWM_DUTY)
        pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ, RIGHT_MTR_PWM_DUTY)
        
    elif data.data[C_BUTTON] == 1:
        global mvstate
        mvstate = TURN_RIGHT
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ, LEFT_MTR_PWM_DUTY)
        pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ, RIGHT_MTR_PWM_DUTY)
        
    elif data.data[T_BUTTON] == 1:
        global mvstate
        mvstate = FORWARD
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ, LEFT_MTR_PWM_DUTY)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ, RIGHT_MTR_PWM_DUTY)
    
    else:
        global mvstate
        mvstate = REST
        
#FORWARD state function
def forwardfunc(data):
    #test code
    printf(mvstate)
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:

#BACK state function
def backfunc(data):
    #test code
    printf(mvstate)
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:

#TURN_RIGHT state function
def turnrightfunc(data):
    #test code
    printf(mvstate)
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:

#TURN_LEFT state function
def turnlestfunc(data):
    #test code
    printf(mvstate)
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:


def caterpillarMove(ds4msg):
    
    if mvstate = REST:
        restfunc(ds4data)
    elif mvstate = FORds4dataWARD:
        forwardfunc(ds4data.data[T_BUTTON])
    elif mvstate = BACK:
        backfunc(ds4data.data[X_BUTTON])
    elif mvstate = TURN_RIGHT:
        turnrightfunc(ds4data.data[C_BUTTON])
    elif mvstate = TURN_LEFT:
        turnlestfunc(ds4data.data[X_BUTTON])
    else:
        restfunc(ds4data)

if __name__ == '__main__':
  rospy.init_node('caterpillar')  
  rospy.Subscriber("ds4btns", UInt16MultiArray, caterpillarMove)
  rospy.spin()
  


