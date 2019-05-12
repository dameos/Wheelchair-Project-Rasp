import sys
import multiprocessing
from Ultrasonic import ledultrasonic as led
from Ultrasonic.ultrasonic import Ultrasonic
from Motors.motors import Motors
from time import sleep

sensor1 = Ultrasonic(trig=18, echo=23, func=led.display_front)
sensor2 = Ultrasonic(trig=24, echo=25, func=led.display_right)
sensor3 = Ultrasonic(trig=13, echo=7,  func=led.display_left)
sensor4 = Ultrasonic(trig=12, echo=16, func=led.display_back)
sensor5 = Ultrasonic(trig=20, echo=21, func=led.display_diag_pos)
sensor6 = Ultrasonic(trig=19, echo=26, func=led.display_diag_neg)

ultrasonic_sensors = [sensor1, sensor2, sensor3, sensor4, sensor5]

def sense_and_distance(sensor_iter_canvas):
    sensor = sensor_iter_canvas[0]
    canv = sensor_iter_canvas[1]
    i = sensor_iter_canvas[2]
    distance = sensor.sense_distance()
    print('Sensor ' + str(i) + ' : ' + str(distance))
    sensor.display_led(led.from_distance_to_level(distance), canv)

def main():
    canv = led.create_canvas()
    while 1:
        enumerated_sensors_canvas = []
        pool = multiprocessing.Pool()
        for i, sensor in enumerate(ultrasonic_sensors):
            enumerated_sensors_canvas.append((sensor, canv, i))

        pool.map(sense_and_distance, enumerated_sensors_canvas)
        pool.close()
        canv = led.create_canvas()

main()


