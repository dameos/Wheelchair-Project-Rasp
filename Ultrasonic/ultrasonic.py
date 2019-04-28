import RPi.GPIO as IO
import time
from pygame import mixer

class Ultrasonic:

    def __init__(self, trig, echo, func):
        # Atributtes
        self.__trig = trig
        self.__echo = echo
        self.__func = func

        # GPIO setupt
        IO.setmode(IO.BCM)
        IO.setup(self.__trig, IO.OUT)
        IO.setup(self.__echo, IO.IN)

        # Init mixer and load sound
        mixer.init()

    def sense_distance(self):
        IO.output(self.__trig, False)
        time.sleep(0.1)

        IO.output(self.__trig, True)
        time.sleep(0.00001)
        IO.output(self.__trig, False)

        while IO.input(self.__echo) == 0:
            pulse_start = time.time()

        while IO.input(self.__echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = round(pulse_duration * 17150, 2)
        return distance

    '''
    The number of samples defines how long it takes and
    how precise the measure is
    1 sample  = 0.1 sec
    2 samples = 0.2 sec
    3 samples = 0.3 sec
    ... 
    '''
    def avg_distance(self, samples):
        distances = []
        for i in range(0, 5):
            distances.append(self.sense_distance())
        distances.remove(max(distances))
        avg = sum(distances) / len(distances)
        return avg

    def play_sound(self):
        sound = mixer.Sound('sound.wav')
        sound.play()

    def display_led(self, level, canv):
        self.__func(level, canv)
