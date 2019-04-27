import RPi.GPIO as IO
from time import sleep

# Global settings
defaultInputRange = (0, 100)
frequency = 1000

# Setting pins

pinS1 = 21
pinS2 = 20

# Setting GPIO
IO.setmode(IO.BCM)
IO.setup(pinS1, IO.OUT)
IO.setup(pinS2, IO.OUT)

# Selecting PWM
move = IO.PWM(pinS1, frequency)
direction = IO.PWM(pinS2, frequency)
move.start(0)
direction.start(0)

def decode_power(power, inputRange, outputRange):
    temp = (power-inputRange[0])/(inputRange[1]-inputRange[0]) * (outputRange[1] - outputRange[0]) + outputRange[0]
    return temp

# All powers are represented in percentage(0 - 100%)

def drive_forward(power):
    decoded_power = decode_power(power, defaultInputRange, (50, 100))
    move.ChangeDutyCycle(decoded_power)

def drive_backward(power):
    decoded_power = decode_power(power, defaultInputRange, (0, 50))
    move.ChangeDutyCycle(decoded_power)

def drive_right(power):
    decoded_power = decode_power(power, defaultInputRange, (50, 100))
    direction.ChangeDutyCycle(decoded_power)

def drive_left(power):
    decoded_power = decode_power(power, defaultInputRange, (0, 50))
    direction.ChangeDutyCycle(decoded_power)
