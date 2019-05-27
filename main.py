import multiprocessing
import signal
import sys
from queue import Queue
from threading import RLock, Thread
from time import sleep

import yaml
from pygame import mixer
from termcolor import colored

from Motors.motors import Motors
from OfflineVoice.snowboy_detector import start_snowboy_detector
from OnlineVoice import mappping_utils as map_utils
from OnlineVoice.hotword import request_path_google_home
from Ultrasonic import ledultrasonic as led
from Ultrasonic.ultrasonic import Ultrasonic

''' General variables '''
RUN_OFFLINE_THREAD = None
RUN_ONLINE_THREAD = None

''' Ultrasonic sensors variables'''
MIN_DISTANCE_ALLOWED = None
ultrasonic_sensors = []

''' Offline variables'''
stop_model = None
forward_model = None
left_model = None
right_model = None
backwards_model = None
OFFLINE_SYSTEM_POWER = None

''' Motors and Lock declaration '''
MOTORS = None
motorLock = None

''' Runtime variables '''
queue_ans = Queue()
interrupted = False


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

        distances = list(
            map(lambda x: led.sense_distance_enum(x), enumerated_sensors_canvas))
        if min(distances) <= MIN_DISTANCE_ALLOWED:
            try:
                motorLock.acquire()
                MOTORS.drive_forward(0)
                ultrasonic_sensors[0].play_sound()
                if not MOTORS.isBrakeActive:
                    MOTORS.brake()
                while True:
                    print('Motor blocked')
                    sleep(1)
            finally:
                motorLock.release()
        canv = led.create_canvas()


def autopilot_system():
    try:
        google_home_thread = Thread(
            target=request_path_google_home, daemon=True, args=(queue_ans, ))
        google_home_thread.start()
        while queue_ans.empty():
            sleep(0.1)

        path = queue_ans.get()
        song = mixer.sound('OnlineVoice/iluminatti.wav')
        song.play()
        try:
            motorLock.acquire()
            if MOTORS.isBrakeActive():
                MOTORS.release_brake()
        finally:
            motorLock.release()
        for i in range(0, len(path) - 1):
            currentCoord = path[i]
            nextCoord = path[i + 1]
            angle_degrees = map_utils.get_angle_between_points(
                currentCoord, nextCoord)
            commands = map_utils.decode_dreeges_into_motor_command(
                angle_degrees)
            if commands.swap_path == True:
                path = map_utils.flip_path_orientation(path)
            commands.execute_commands(motorLock, MOTORS)
    except KeyboardInterrupt:
        pass


def offline_voice_recognizer():
    def forward_model_callback(): return generic_model_callback(MOTORS.drive_forward)
    def left_model_callback(): return generic_model_callback(MOTORS.drive_left)
    def right_model_callback(): return generic_model_callback(MOTORS.drive_right)
    def backwards_model_callback(): return generic_model_callback(MOTORS.drive_backward)

    models = [stop_model, forward_model,
              left_model, right_model, backwards_model]
    callbacks = [stop_model_callback, forward_model_callback,
                 left_model_callback, right_model_callback, backwards_model_callback]

    detector = start_snowboy_detector(models=models)
    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback, sleep_time=0.03)
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
    input()
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
    elif RUN_ONLINE_THREAD == True:
        autopilot_thread.start()

    while not interrupted:
        pass
    print(colored('Finishing execution...', 'blue'))


def calibrating():
    try:
        MOTORS.release_brake()
        while 1:
            print('Calibrating')
            sleep(3)
    except KeyboardInterrupt:
        MOTORS.brake()


def decode_ultrasonic(sensors):
    ultrasonic_ans = []
    for sensor in sensors:
        led_func = led.decode_func_sensor(sensor['led'])
        ultrasonic = Ultrasonic(
            trig=sensor['trigger'], echo=sensor['echo'], func=led_func)
        ultrasonic_ans.append(ultrasonic)
    return ultrasonic_ans


def print_error_and_exit(error_msg):
    print(colored('ERROR: ' + error_msg, 'red'))
    sys.exit()


if __name__ == "__main__":
    with open('config.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    # Main configuration
    RUN_OFFLINE_THREAD = cfg['general']['use_manual']
    RUN_ONLINE_THREAD = cfg['general']['use_autopilot']

    if RUN_OFFLINE_THREAD and RUN_ONLINE_THREAD:
        print_error_and_exit(
            'Automatic and manual mode selected at the same time')

    if not RUN_OFFLINE_THREAD and not RUN_ONLINE_THREAD:
        print_error_and_exit('No mode selected')

    # Ultrasonic config
    MIN_DISTANCE_ALLOWED = cfg['ultrasonic_sensors']['min_distance_allowed']
    ultrasonic_sensors = decode_ultrasonic(
        cfg['ultrasonic_sensors']['sensors'])

    # Motor config
    MOTORS = Motors(pinS1=cfg['motors']['pin_s1'], pinS2=cfg['motors']
                    ['pin_s2'], pinBrake=cfg['motors']['pin_brake'])
    motorLock = RLock()

    # Offline Models and power
    configuration_models = cfg['offline_voice']['models']
    stop_model = configuration_models['stop_model']
    forward_model = configuration_models['forward_model']
    left_model = configuration_models['left_model']
    right_model = configuration_models['right_model']
    backwards_model = configuration_models['backwards_model']
    OFFLINE_SYSTEM_POWER = cfg['offline_voice']['motor_power']

    main()
