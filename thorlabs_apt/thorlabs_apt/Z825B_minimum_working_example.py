# equipment: Z825B replacing the micrometer in PT1

# minimum working example

# November 5, 2018
# Thiago S. Jota
# Applications Engineer
# THORLABS Inc.
# P: (973) 300 3000
# techsupport@thorlabs.com

''' From Kinesis: Settings > Device startup Settings > Actuator settings

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

Default Minimum Velocity = 0
Default Maximum Velocity = 2.2
Default Acceleration = 1.5

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
Minimum Position = 0
Maximum Position = 25
Maximum Velocity = 2.6
Maximum Acceleration = 4
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

motorNo = apt.list_available_devices()[0][1]
motor = apt.Motor(motorNo)


motor.set_hardware_limit_switches(2,2)
motor.set_motor_parameters(512,67)
motor.set_stage_axis_info(0.0,25.0,1,1.0)
motor.set_move_home_parameters(2,1,2.3,0.3)
motor.set_velocity_parameters(1.5,3.5,2.3)
# Maximum Velocity = 2.6
# Maximum Acceleration = 4


# home:

motor.move_home()
time.sleep(1)
wait_completion_1 = True

while wait_completion_1 is True:
     if motor.is_in_motion is False:
         wait_completion_1 = False
print('stage homing complete')


# move:

new_position_float = 7.0
wait_completion_2 = True
motor.move_to(new_position_float)
time.sleep(1)

while wait_completion_2 is True:
     if motor.is_in_motion is False:
         wait_completion_2 = False

print('stage moving complete')
