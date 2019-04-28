import sys
from Ultrasonic import ledultrasonic as led
from Ultrasonic.ultrasonic import Ultrasonic
from Motors.motors import Motors
from time import sleep


sensor1 = Ultrasonic(trig=18, echo=23)
sensor2 = Ultrasonic(trig=24, echo=25)
sensor3 = Ultrasonic(trig=13, echo=7)
sensor4 = Ultrasonic(trig=12, echo=16)
sensor5 = Ultrasonic(trig=20, echo=21)
sensor6 = Ultrasonic(trig=19, echo=26)

ultrasonic_sensors = [sensor1, sensor2, sensor3, sensor4, sensor5]

canv = led.create_canvas()

while 1:
    distances = list(map(lambda x: x.sense_distance(), ultrasonic_sensors))
    for i, distance in enumerate(distances):
        print('Sensor' + str(i + 1) + ' : ' + str(distance))
        led.decode_sensor(i, led.from_distance_to_level(distance), canv)
    canv = led.create_canvas()
