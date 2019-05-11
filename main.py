from Ultrasonic.ultrasonic import Ultrasonic
from Motors.motors import Motors
from time import sleep

sensor1 = Ultrasonic(trig=18, echo=23)
sensor2 = Ultrasonic(trig=24, echo=25)
sensor3 = Ultrasonic(trig=8, echo=7)
sensor4 = Ultrasonic(trig=12, echo=16)
sensor5 = Ultrasonic(trig=20, echo=21)
sensor6 = Ultrasonic(trig=19, echo=26)

utlrasonic_sensors = [sensor1, sensor2, sensor3, sensor4, sensor5, sensor6]

while 1:
    for i, sensor in enumerate(utlrasonic_sensors):
        print('Sensor' + str(i + 1) + ' : ' + str(sensor.sense_distance()))
    sleep(0.2)
