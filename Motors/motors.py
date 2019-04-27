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
motor1 = IO.PWM(pinS1, frequency)
motor2 = IO.PWM(pinS2, frequency)

# Starting both motors
motor1.start(50)
motor2.start(50)

def decode_power(power, inputRange, outputRange):
    temp = (power-inputRange[0])/(inputRange[1]-inputRange[0]) * (outputRange[1] - outputRange[0]) + outputRange[0]
    return temp

# All powers are represented in percentage(0 - 100%)

def drive_forward(power):
    decoded_power = decode_power(power, defaultInputRange, (50, 100))
    print("Decoded Power Forward: " + str(decoded_power))
    motor1.ChangeDutyCycle(decoded_power)
    motor2.ChangeDutyCycle(decoded_power)

def drive_backward(power):
    decoded_power = decode_power(power, defaultInputRange, (50, 0))
    print("Decoded Power Backward: " + str(decoded_power))
    motor1.ChangeDutyCycle(decoded_power)
    motor2.ChangeDutyCycle(decoded_power)

def drive_right(power):
    decoded_power = decode_power(power, defaultInputRange, (50, 100))
    negative_decoded_power = decode_power(power, defaultInputRange, (50, 0))
    motor2.ChangeDutyCycle(decoded_power)
    motor1.ChangeDutyCycle(negative_decoded_power)
    

def drive_left(power):
    decoded_power = decode_power(power, defaultInputRange, (50, 100))
    negative_decoded_power = decode_power(power, defaultInputRange, (50, 0))
    motor1.ChangeDutyCycle(decoded_power)
    motor2.ChangeDutyCycle(negative_decoded_power)

