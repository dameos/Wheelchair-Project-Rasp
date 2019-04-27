import RPi.GPIO as GPIO
import time
from pygame import mixer

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Init mixer and load sound
mixer.init()
sound = mixer.Sound('sound.wav')


def sense_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = round(pulse_duration * 17150, 2)
    return distance

def avg_distance():
    distances = []
    for i in range(0, 10):
        distances.append(sense_distance())
    distances.remove(max(distances))
    avg = sum(distances) / len(distances)
    return avg

while 1:
    avg = avg_distance()
    print("Distance: " + str(avg) + " cm")
    if (avg <= 20):
        sound.play()
        while(mixer.get_busy()):
            True

