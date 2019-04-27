import sys
sys.path.append('../../Motors/')
import motors
import brakes
import time

# Constants
LEFT_COMMAND = "left"
RIGHT_COMMAND = "right"
FORWARD_COMMAND = "forward"
STOP_COMMAND = "stop"
MAX_SPEED = 60   # max speed in %speed
TIME_STEP = 0.01 # time step
SPEED_STEP = 0.3 #  acceleration in  %speed per centisecond

# Variables
firstRun = False
speed = 0

def forward():
    run_command(FORWARD_COMMAND)

def left():
    run_command(LEFT_COMMAND)

def right():
    run_command(RIGHT_COMMAND)

def stop():
    run_command(STOP_COMMAND)

def run_command(command):
    global firstRun
    if firstRun == False:
        brakes.release()
        increase_gradually(MAX_SPEED, command)
        firstRun = True
    elif command == STOP_COMMAND:
        decrease_gradually(MAX_SPEED)
    else:
        execute_normally(MAX_SPEED, command)

def decrease_gradually(init_speed):
    while init_speed > 0:
        execute_normally(init_speed, STOP_COMMAND)
        init_speed = init_speed - SPEED_STEP
        time.sleep(TIME_STEP)
    brakes.brake()
    

def increase_gradually(top_speed, command):
    acum_speed = 0
    while acum_speed <= top_speed:
        execute_normally(acum_speed, command)
        acum_speed = acum_speed + SPEED_STEP
        time.sleep(TIME_STEP)

def execute_normally(speed, command):
    if command == LEFT_COMMAND:
        motors.drive_left(speed)
    elif command == RIGHT_COMMAND:
        motors.drive_right(speed)
    elif command == FORWARD_COMMAND or command == STOP_COMMAND:
        motors.drive_forward(speed)
