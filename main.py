import sys
import multiprocessing
import OnlineVoice.mappping_utils as map_utils
from threading import RLock
from threading import Thread
from OnlineVoice import hotword
from Ultrasonic import ledultrasonic as led
from Ultrasonic.ultrasonic import Ultrasonic
from Motors.motors import Motors
from time import sleep

# Security system variables
MIN_DISTANCE_ALLOWED = 30

# Motors and Lock declaration
MOTORS = Motors(pinS1=20, pinS2=21, pinBrake=19)
motorLock = RLock()

# Ultrasonic sensors declaration
sensor1 = Ultrasonic(trig=18, echo=23, func=led.display_front)
sensor2 = Ultrasonic(trig=24, echo=25, func=led.display_right)
sensor3 = Ultrasonic(trig=13, echo=7,  func=led.display_left)
sensor4 = Ultrasonic(trig=12, echo=16, func=led.display_back)
sensor5 = Ultrasonic(trig=20, echo=21, func=led.display_diag_pos)
sensor6 = Ultrasonic(trig=19, echo=26, func=led.display_diag_neg)

ultrasonic_sensors = [sensor1, sensor2, sensor3, sensor4, sensor5]

def ultrasonic_security_system():
    canv = led.create_canvas()
    while 1:
        enumerated_sensors_canvas = []
        pool = multiprocessing.Pool()
        for i, sensor in enumerate(ultrasonic_sensors):
            enumerated_sensors_canvas.append((sensor, canv, i))

        distances = pool.map(led.sense_distance_enum, enumerated_sensors_canvas)
        pool.close()
        if min(distances) <= MIN_DISTANCE_ALLOWED:
            try:
                motorLock.acquire()
                MOTORS.drive_forward(0)
                MOTORS.brake()
                while 1:
                    None
            finally:
                motorLock.release()
        canv = led.create_canvas()

def autopilot_system():
    path = hotword.request_path_google_home()
    for i in range(0, len(path) - 1):
        currentCoord = path[i]
        nextCoord = path[i + 1]
        angle_degrees = map_utils.get_angle_between_points(currentCoord, nextCoord)
        commands = map_utils.decode_dreeges_into_motor_command(angle_degrees)
        if commands.swap_path == True:
            path = map_utils.flip_path_orientation(path)
        commands.execute_commands()


def main():
    security_thread = Thread(target=ultrasonic_security_system)
    autopilot_thread = Thread(target=autopilot_system)

    security_thread.run()
    autopilot_thread.run()

if __name__ == "__main__":
    main()