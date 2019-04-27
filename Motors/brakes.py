import RPi.GPIO as GPIO

electric_brake = 19
GPIO.setup(electric_brake, GPIO.OUT)

def brake():
    GPIO.output(electric_brake, GPIO.LOW)

def release():
    GPIO.output(electric_brake, GPIO.HIGH)

brake()
