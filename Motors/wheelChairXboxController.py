import time
import os
import RPi.GPIO as GPIO
import motors 
import math
from evdev import InputDevice, categorize, ecodes

# Global variables
controller = InputDevice('/dev/input/event0')
electric_brake = 19
max_speed_cap = 50

# Pad Controller Commands
speed_pad = 5
brake_pad = 2
direction_pad = 16

# States
speed = 0
state_dir = 0

#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(electric_brake, GPIO.OUT)

def is_control(code):
    return code == speed_pad or code == brake_pad or code == direction_pad

def get_key_worker():
    for event in controller.read_loop():
        if is_control(event.code):
            yield event

def handle_state(speed, state_dir):
    str_speed = str(speed)
    if state_dir == 0:
        if speed > 0:
            motors.drive_forward(speed)
        else:
            motors.drive_backward(-1 * speed)

    if state_dir == 1:
        motors.drive_right(speed)

    if state_dir == -1:
        motors.drive_left(speed)

gen = get_key_worker()
while True:
    if (math.trunc(speed) == 0):
        GPIO.output(electric_brake, GPIO.LOW)
    else:
        GPIO.output(electric_brake, GPIO.HIGH)
    event = next(gen)
    if event.code == direction_pad:
        state_dir = event.value
    if event.code == speed_pad:
        speed = event.value * max_speed_cap / 1023
    if event.code == brake_pad:
        speed = - event.value * max_speed_cap / 1023
    handle_state(speed, state_dir)
    time.sleep(0.01)
