import sys
import multiprocessing
import queue
import speech_recognition as sr
from OnlineVoice import mappping_utils as map_utils
from threading import RLock
from threading import Thread
from OnlineVoice import hotword
from Ultrasonic import ledultrasonic as led
from Ultrasonic.ultrasonic import Ultrasonic
from Motors.motors import Motors
from time import sleep

# Runtime variables
RUN_OFFLINE_THREAD = True
queue_ans = queue.Queue()

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

def recognize_command_callback(recognizer, audio):
    try:
        spoken = recognizer.recognize_tensorflow(audio)
        try:
            motorLock.acquire()
            if MOTORS.isBrakeActive():
                MOTORS.release_brake()
            if spoken == 'go':
                MOTORS.drive_forward(OFFLINE_SYSTEM_POWER)
            if spoken == 'right':
                MOTORS.drive_right(OFFLINE_SYSTEM_POWER)
            if spoken == 'left':
                MOTORS.drive_left(OFFLINE_SYSTEM_POWER)
            if spoken == 'down':
                MOTORS.drive_backward(OFFLINE_SYSTEM_POWER)
            if spoken == 'stop' or spoken == 'off':
                MOTORS.drive_forward(0)
                if not MOTORS.isBrakeActive():
                    MOTORS.brake()

        finally:
            motorLock.release()

    except sr.UnknownValueError:
        print("Tensorflow could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Tensorflow service; {0}".format(e))

def offline_voice_recognizer():
    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        r.adjust_for_ambient_noise(source)

    stop_listening = r.listen_in_background(m, recognize_command_callback, phrase_time_limit=0.6)
    while True:
        sleep(0.1)
        stop_listening(wait_for_stop=False)

def main():
    security_thread = Thread(target=ultrasonic_security_system, daemon=True)
    autopilot_thread = Thread(target=autopilot_system, daemon=True)

    # Start ultrasonic security thread
    security_thread.start()

    # Run offline voice pattern thread if env var is set to True
    # Run autopilot otherwise
    if RUN_OFFLINE_THREAD == True:
        from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
        offline_thread = Thread(target=offline_voice_recognizer, daemon=True)
        offline_thread.start()
    else:
        autopilot_thread.start()

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
