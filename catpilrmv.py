#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16MultiArray
import pigpio  # sudo apt install pigpio

#debug code
debuginfo = UInt16MultiArray()
debuginfo.data = [0] * 2

#definition of const values
S_BUTTON = 0
X_BUTTON = 1
C_BUTTON = 2
T_BUTTON = 3

REST = 10
FORWARD = 20
BACK = 30
TURN_RIGHT = 40
TURN_LEFT = 50

GPIO_CATPILR10 = 12  # front-left wheel
GPIO_CATPILR11 = 5   # rear-left wheel
#GPIO_CATPILR11 = 18  # rear-left wheel
GPIO_CATPILR20 = 13  # front-right wheel
GPIO_CATPILR21 = 6   # rear-right wheel
#GPIO_CATPILR21 = 19  # rear-right wheel

MTR_PWM_HZ = 100  # unit:Hz
MTR_PWM_HZ_ZERO = 0  # unit:Hz
F_LEFT_MTR_PWM_DUTY = 1000000   # unit:?
R_LEFT_MTR_PWM_DUTY = 255       # unit:?
F_RIGHT_MTR_PWM_DUTY = 1000000  # unit:?
R_RIGHT_MTR_PWM_DUTY = 255      # unit:?
MTR_PWM_DUTY_ZERO = 0  # unt:?

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
    pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    pi3.set_PWM_dutycycle(GPIO_CATPILR11, MTR_PWM_DUTY_ZERO)
    #pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    pi3.set_PWM_dutycycle(GPIO_CATPILR21, MTR_PWM_DUTY_ZERO)
    #pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    
    if data.data[S_BUTTON] == 1:
        global mvstate
        mvstate = TURN_LEFT
        pi3.set_PWM_frequency(GPIO_CATPILR11, MTR_PWM_HZ)
        pi3.set_PWM_dutycycle(GPIO_CATPILR11, R_LEFT_MTR_PWM_DUTY)
        #pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ, LEFT_MTR_PWM_DUTY)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ, F_RIGHT_MTR_PWM_DUTY)
        
    elif data.data[X_BUTTON] == 1:
        global mvstate
        mvstate = BACK
        pi3.set_PWM_frequency(GPIO_CATPILR11, MTR_PWM_HZ)
        pi3.set_PWM_dutycycle(GPIO_CATPILR11, R_LEFT_MTR_PWM_DUTY)
        #pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ, LEFT_MTR_PWM_DUTY)
        pi3.set_PWM_frequency(GPIO_CATPILR21, MTR_PWM_HZ)
        pi3.set_PWM_dutycycle(GPIO_CATPILR21, R_RIGHT_MTR_PWM_DUTY)
        #pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ, RIGHT_MTR_PWM_DUTY)
        
    elif data.data[C_BUTTON] == 1:
        global mvstate
        mvstate = TURN_RIGHT
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ, F_LEFT_MTR_PWM_DUTY)
        pi3.set_PWM_frequency(GPIO_CATPILR21, MTR_PWM_HZ)
        pi3.set_PWM_dutycycle(GPIO_CATPILR21, R_RIGHT_MTR_PWM_DUTY)
        #pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ, RIGHT_MTR_PWM_DUTY)
        
    elif data.data[T_BUTTON] == 1:
        global mvstate
        mvstate = FORWARD
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ, F_LEFT_MTR_PWM_DUTY)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ, F_RIGHT_MTR_PWM_DUTY)
    
    else:
        global mvstate
        mvstate = REST
        
#FORWARD state function
def forwardfunc(data):
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:
        pass

#BACK state function
def backfunc(data):
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.set_PWM_dutycycle(GPIO_CATPILR11, MTR_PWM_DUTY_ZERO)
        #pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.set_PWM_dutycycle(GPIO_CATPILR21, MTR_PWM_DUTY_ZERO)
        #pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:
        pass

#TURN_RIGHT state function
def turnrightfunc(data):
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.hardware_PWM(GPIO_CATPILR10, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.set_PWM_dutycycle(GPIO_CATPILR21, MTR_PWM_DUTY_ZERO)
        #pi3.hardware_PWM(GPIO_CATPILR21, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:
        pass

#TURN_LEFT state function
def turnlestfunc(data):
    if data != 1:
        global mvstate
        mvstate = REST
        pi3.set_PWM_dutycycle(GPIO_CATPILR11, MTR_PWM_DUTY_ZERO)
        #pi3.hardware_PWM(GPIO_CATPILR11, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
        pi3.hardware_PWM(GPIO_CATPILR20, MTR_PWM_HZ_ZERO, MTR_PWM_DUTY_ZERO)
    else:
        pass

def caterpillarMove(ds4msg):
    
    if mvstate == REST:
        restfunc(ds4msg)
    elif mvstate == FORWARD:
        forwardfunc(ds4msg.data[T_BUTTON])
    elif mvstate == BACK:
        backfunc(ds4msg.data[X_BUTTON])
    elif mvstate == TURN_RIGHT:
        turnrightfunc(ds4msg.data[C_BUTTON])
    elif mvstate == TURN_LEFT:
        turnlestfunc(ds4msg.data[S_BUTTON])
    else:
        restfunc(ds4data)
    #debug code
    global debuginfo
    debuginfo.data[0] = mvstate
    pub.publish(debuginfo)
    
if __name__ == '__main__':
  rospy.init_node('caterpillar')  
  rospy.Subscriber("ds4btns", UInt16MultiArray, caterpillarMove)
  #debug code
  pub = rospy.Publisher('debug_ctplr', UInt16MultiArray, queue_size = 1)
  rospy.spin()
