# equipment: 3 KDC101 DC Servo Motor Controllers
#            connected to PT1-Z8 25mm motorized translation stages

# Full fiber pulling err_code
# Simply light the torch and then execute this file in the Anaconda Prompt

# January 4, 2019
# Matthew Simmons
# P: (949)910-2223

''' From Kinesis: Settings > Device startup Settings > Actuator settings
These parameters are from Kinesis, under (stock) settings.
I just copied and pasted to be sure the device parameters are not exceeded; very important.

Z825

General

Name =
Stage ID = 99
Axis ID = Single axis

Home Settings

Home Direction = Reverse
Home Limit Switch Mode = Reverse (Hard)
Home Velocity = 1
Home Zero Offset = 0.3

Jog Settings

Jog Mode = Single step
Jog Step = 0.1
Jog Minimum Velocity = 0
Jog Maximum Velocity = 2
Jog Acceleration = 2
Jog Stop Mode = Profiled stop

Control Settings

Default Minimum Velocity = 0 mm/s
Default Maximum Velocity = 2.2 mm/s
Default Acceleration = 1.5 mm/s/s

Limit Settings

Clockwise Hard Limit mode = Switch Makes
Counter Clockwise Hard Limit mode = Switch Makes
Clockwise Soft Limit = 3
Counter Clockwise Soft Limit = 1
Soft Limit Mode = Ignore
Software Limits Approach PolicyMode = Complete moves only

Physical Settings

Use Device Units = False
Travel Mode = Linear
Direction Sense = Reverse
Minimum Achievable Incremental Movement = .05 um
Minimum Repeatable Incremental Movement = .2 um
Minimum Position = 0 mm
Maximum Position = 25 mm
Maximum Velocity = 2.6 mm/s
Maximum Acceleration = 4 mm/s/s
MM to Unit factor = 1
Units = mm

Misc. Settings

Backlash Distance = 0.025
Move Factor = 100
Rest Factor = 20

MMI Settings

Wheel Mode = Jog
Wheel Max Velocity = 1
Wheel Acceleration = 2
Wheel Direction Sense = Forward
Prest Position 1 = 0
Preset Position 2 = 0
Display Intensity = 60
Display Timeout = 10
Display Dim Intensity = 2

Trigger Config Settings

Trigger 1 Mode = Disabled
Trigger 1 Polarity = Trigger High
Trigger 2 Mode = Disabled
Trigger 2 Polarity = Trigger High

Trigger Params Settings

Trigger Start Position Fwd = 0
Trigger Interval Fwd = 0
Trigger Pulse Count Fwd = 1
Trigger Start Position Rev = 0
Trigger Interval Rev = 0
Trigger Pulse Count Rev = 1
Trigger Pulse Width = 50
Cycle Count = 1

DC Motor Settings

Use Device Units = False
Travel Mode = Linear
Direction Sense = Reverse
Minimum Position = 0
Maximum Position = 25
Maximum Velocity = 2.6
Maximum Acceleration = 4
MM to Unit factor = 1
Units = mm
Pitch Size = 1
Steps per revolution = 512
Gearbox Ratio = 67

DC Servo Settings

DC Servo Enabled = 1
DC Proportional Constant = 435
DC Integral Constant = 195
DC Differential Constant = 993
DC Integral Limit = 195
'''

import thorlabs_apt as apt
import time
import numpy as np

motorTorch = apt.Motor(27003356) #serial number of the stage with the torch on it
motorLeft = apt.Motor(27003323) #serial number of the left stage
motorRight = apt.Motor(27003363) #serial number of the right stage

# Maximum Velocity = 2.6
# Maximum Acceleration = 4
motorTorch.set_hardware_limit_switches(2,2)
motorTorch.set_motor_parameters(512,67)
motorTorch.set_stage_axis_info(0.0,25.0,1,1.0)
motorTorch.set_move_home_parameters(2,1,2.3,0.3)
motorTorch.set_velocity_parameters(1.0,1.0,1.0)

motorLeft.set_hardware_limit_switches(2,2)
motorLeft.set_motor_parameters(512,67)
motorLeft.set_stage_axis_info(0.0,25.0,1,1.0)
motorLeft.set_move_home_parameters(2,1,2.3,0.3)
motorLeft.set_velocity_parameters(1.0,1.0,1.0)

motorRight.set_hardware_limit_switches(2,2)
motorRight.set_motor_parameters(512,67)
motorRight.set_stage_axis_info(0.0,25.0,1,1.0)
motorRight.set_move_home_parameters(2,1,2.3,0.3)
motorRight.set_velocity_parameters(1.0,1.0,1.0)


# Home the stages:

motorTorch.move_home()
time.sleep(1)
wait_completion_1 = True

while wait_completion_1 is True:
     if motorTorch.is_in_motion is False:
         wait_completion_1 = False
print('Torch stage homing complete')


motorLeft.move_home()
time.sleep(1)
wait_completion_2 = True

while wait_completion_2 is True:
     if motorLeft.is_in_motion is False:
         wait_completion_2 = False
print('Left stage homing complete')

motorRight.move_home()
time.sleep(1)
wait_completion_3 = True

while wait_completion_3 is True:
     if motorRight.is_in_motion is False:
         wait_completion_3 = False
print('Right stage homing complete')


'''
When ready and the torch is lit, press "enter" on the keyboard
This will begin the rest of the fiber pulling sequence
'''
input("Press enter to continue")

#move the torch into position:

moveTorch_to_fiber = 20.0 #distance stage holding the torch needs to move so that the torch is heating the fiber
wait_completion_4 = True
motorTorch.move_to(moveTorch_to_fiber) #move the stage holding the torch 20 mm to be on the fiber
time.sleep(1)
while wait_completion_4 is True:
     if motorTorch.is_in_motion is False:
         wait_completion_4 = False

print('Torch moved to fiber')

wait_pullFiber=5 #the amount of time (seconds) to wait before the stages start to pull the fiber
time.sleep(wait_pullFiber)

#pull the fiber:

moveIncrement = .01 #distance the stages move
start_pos = .01 #starting position should be the increment size
end_pos = 3.01 #distance each stage should move when pulling the fiber


for x in np.arange(start_pos, end_pos, moveIncrement):
    motorLeft.move_to(x)
    motorRight.move_to(x)
    time.sleep(.01)

print('Fiber stretched')

'''
At this point I really just added examples of how to move the fiber to the left and the right
with both stages moving at the same time so that the fiber isn't being pulled anymore that it
already was pulled initially

These will have to be changed when we actually start pulling the fibers and see what we actually need
to do to get the pulling down correctly
'''

time.sleep(2)
print('Moving left')

moveBack_start = end_pos-(2*moveIncrement)
moveBack_end = start_pos-moveIncrement

leftMotor_pos = end_pos-moveIncrement
for y in np.arange(moveBack_start, moveBack_end, -moveIncrement):
    leftMotor_pos = leftMotor_pos+moveIncrement
    #print("Left motor position: ", leftMotor_pos) #optional print statement to see if where you think the motor is moving is actually where it's moving
    motorLeft.move_to(leftMotor_pos)
    motorRight.move_to(y)
    #print("Right motor position: ", y)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    time.sleep(.01)

time.sleep(2)
print("Now move back")

leftMotor_pos = leftMotor_pos+moveIncrement
for z in np.arange(start_pos, end_pos, moveIncrement):
    leftMotor_pos = leftMotor_pos-moveIncrement
    #print("Left motor position: ", leftMotor_pos)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    motorLeft.move_to(leftMotor_pos)
    motorRight.move_to(z)
    #print("Right motor position: ", z)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    time.sleep(.01)

time.sleep(2)
print("Moving Right")

rightMotor_pos = end_pos-moveIncrement
for y in np.arange(moveBack_start, moveBack_end, -moveIncrement):
    rightMotor_pos = rightMotor_pos+moveIncrement
    #print("Left motor position: ", y)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    motorLeft.move_to(y)
    motorRight.move_to(rightMotor_pos)
    #print("Right motor position: ", rightMotor_pos)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    time.sleep(.01)

print("blah")
print("Now move back again")

rightMotor_pos = rightMotor_pos+moveIncrement
for z in np.arange(start_pos, end_pos, moveIncrement):
    rightMotor_pos = rightMotor_pos-moveIncrement
    #print("Left motor position: ", z)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    motorLeft.move_to(z)
    motorRight.move_to(rightMotor_pos)
    #print("Right motor position: ", rightMotor_pos)  #optional print statement to see if where you think the motor is moving is actually where it's moving
    time.sleep(.01)

print("Fiber pulling complete, home torch stage")
motorTorch.move_home()
time.sleep(1)
wait_completion_1 = True

while wait_completion_1 is True:
     if motorTorch.is_in_motion is False:
         wait_completion_1 = False
print('Torch stage homing complete')
