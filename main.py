import multiprocessing
import sys
import signal
from threading import RLock, Thread
from time import sleep
from queue import Queue

from Motors.motors import Motors
from OnlineVoice import hotword
from OnlineVoice import mappping_utils as map_utils
from Ultrasonic import ledultrasonic as led
from Ultrasonic.ultrasonic import Ultrasonic
from OfflineVoice.snowboy_detector import start_snowboy_detector

# Runtime variables
RUN_OFFLINE_THREAD = True
queue_ans = Queue()
interrupted = False

# Security system variables
MIN_DISTANCE_ALLOWED = 30
OFFLINE_SYSTEM_POWER = 40

# Motors and Lock declaration
MOTORS = None
motorLock = None

# Ultrasonic sensors declaration
sensor1 = Ultrasonic(trig=18, echo=23, func=led.display_front)
sensor2 = Ultrasonic(trig=24, echo=25, func=led.display_right)
sensor3 = Ultrasonic(trig=13, echo=7,  func=led.display_left)
sensor4 = Ultrasonic(trig=12, echo=16, func=led.display_back)
sensor5 = Ultrasonic(trig=20, echo=21, func=led.display_diag_pos)
sensor6 = Ultrasonic(trig=19, echo=26, func=led.display_diag_neg)

#ultrasonic_sensors = [sensor1, sensor2, sensor3, sensor4, sensor5]
ultrasonic_sensors = [sensor1]

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

signal.signal(signal.SIGINT, signal_handler)

def ultrasonic_security_system():
    canv = led.create_canvas()
    while 1:
        enumerated_sensors_canvas = []
        for i, sensor in enumerate(ultrasonic_sensors):
            enumerated_sensors_canvas.append((sensor, canv, i))

        distances = list(map(lambda x: led.sense_distance_enum(x), enumerated_sensors_canvas))
        if min(distances) <= MIN_DISTANCE_ALLOWED:
            try:
                motorLock.acquire()
                MOTORS.drive_forward(0)
                if not MOTORS.isBrakeActive:
                    MOTORS.brake()
                while 1:
                    print('Motor blocked')
                    sleep(1)
                    None
            finally:
                motorLock.release()
        canv = led.create_canvas()

def autopilot_system():
    path = hotword.request_path_google_home(queue_ans)
    try:
        motorLock.acquire()
        if MOTORS.isBrakeActive():
            MOTORS.release_brake()
    finally:
        motorLock.release()
    for i in range(0, len(path) - 1):
        currentCoord = path[i]
        nextCoord = path[i + 1]
        angle_degrees = map_utils.get_angle_between_points(currentCoord, nextCoord)
        commands = map_utils.decode_dreeges_into_motor_command(angle_degrees)
        if commands.swap_path == True:
            path = map_utils.flip_path_orientation(path)
        commands.execute_commands(motorLock, MOTORS)

def offline_voice_recognizer():
    stop_model = 'OfflineVoice/resources/models/parar.pmdl'
    forward_model = 'OfflineVoice/resources/models/adelante.pmdl'
    left_model = 'OfflineVoice/resources/models/izquierda.pmdl'
    right_model = 'OfflineVoice/resources/models/derecha.pmdl'
    backwards_model = 'OfflineVoice/resources/models/atras.pmdl'

    forward_model_callback = lambda: generic_model_callback(MOTORS.drive_forward)
    left_model_callback = lambda: generic_model_callback(MOTORS.drive_left)
    right_model_callback = lambda: generic_model_callback(MOTORS.drive_right)
    backwards_model_callback = lambda: generic_model_callback(MOTORS.drive_backward)

    models = [stop_model, forward_model, left_model, right_model, backwards_model]
    callbacks = [stop_model_callback, forward_model_callback, left_model_callback, right_model_callback, backwards_model_callback]

    detector = start_snowboy_detector(models=models)
    detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback ,sleep_time=0.03)
    detector.terminate()

def stop_model_callback():
    try:
        motorLock.acquire()
        MOTORS.drive_forward(0)
        if not MOTORS.isBrakeActive():
            MOTORS.brake()
    finally:
        motorLock.release()

def generic_model_callback(motor_command):
    try:
        motorLock.acquire()
        motor_command(OFFLINE_SYSTEM_POWER)
    finally:
        motorLock.release()

def dummy_autopilot_system():
    a = input()
    while 1:
        try:
            motorLock.acquire()
            if MOTORS.isBrakeActive():
                MOTORS.release_brake()
            MOTORS.drive_forward(30)
            print('I am SPEED')
            sleep(1)
        finally:
            motorLock.release()


def main():
    security_thread = Thread(target=ultrasonic_security_system, daemon=True)
    autopilot_thread = Thread(target=autopilot_system, daemon=True)

    # Start ultrasonic security thread
    security_thread.start()

    # Run offline voice pattern thread if env var is set to True
    # Run autopilot otherwise
    if RUN_OFFLINE_THREAD == True:
        offline_thread = Thread(target=offline_voice_recognizer, daemon=True)
        offline_thread.start()
    else:
        autopilot_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Finishing execution...')

def calibrating():
    try:
        MOTORS.release_brake()
        while 1:
            print('Calibrating')
            sleep(3)
    except KeyboardInterrupt:
        MOTORS.brake()

if __name__ == "__main__":
    MOTORS = Motors(pinS1=20, pinS2=21, pinBrake=19)
    motorLock = RLock()
    #calibrating()
    main()
