import RPi.GPIO as IO
from termcolor import colored

class Motors:
    DEFAULTINPUTRANGE = (0, 100)
    FREQUENCY = 1000
    VERBOSE = True

    def __init__(self, pinS1, pinS2, pinBrake, isBraked=False):
        self.__pinS1 = pinS1
        self.__pinS2 = pinS2
        self.__pinBrake = pinBrake
        self.__isBraked = isBraked

        # Setting up pins
        IO.setmode(IO.BCM)
        IO.setup(self.__pinS1, IO.OUT)
        IO.setup(self.__pinS2, IO.OUT)
        IO.setup(self.__pinBrake, IO.OUT)

        # Motor variables
        self.__motor1 = IO.PWM(pinS1, self.FREQUENCY)
        self.__motor2 = IO.PWM(pinS2, self.FREQUENCY)

        # First state
        # Motors start at some point around 50% since the idle state is 2.5V
        # Brakes starts at isBraked
        self.__motor1.start(50.27)
        self.__motor2.start(50.60)

        if self.__isBraked == True:
            self.brake()
        else:
            self.release_brake()


    def decode_power(self, power, inputRange, outputRange):
        left_factor = (power-inputRange[0])/(inputRange[1]-inputRange[0])
        temp = left_factor * (outputRange[1] - outputRange[0]) + outputRange[0]
        return temp

    def drive_forward(self, power):
        if self.VERBOSE:
            self.print_command('Forward', power)
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 100))
        self.__motor1.ChangeDutyCycle(decoded_power)
        self.__motor2.ChangeDutyCycle(decoded_power)

    def drive_backward(self, power):
        if self.VERBOSE:
            self.print_command('Backward', power)
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 0))
        self.__motor1.ChangeDutyCycle(decoded_power)
        self.__motor2.ChangeDutyCycle(decoded_power)

    def drive_right(self, power):
        if self.VERBOSE:
            self.print_command('Right', power)
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 100))
        negative_decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 0))
        self.__motor2.ChangeDutyCycle(decoded_power)
        self.__motor1.ChangeDutyCycle(negative_decoded_power)

    def drive_left(self, power):
        if self.VERBOSE:
            self.print_command('Left', power)
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 100))
        negative_decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 0))
        self.__motor1.ChangeDutyCycle(decoded_power)
        self.__motor2.ChangeDutyCycle(negative_decoded_power)

    def brake(self):
        self.__isBraked = True
        IO.output(self.__pinBrake, IO.LOW)

    def release_brake(self):
        self.__isBraked = False
        IO.output(self.__pinBrake, IO.HIGH)

    def isBrakeActive(self):
        return self.__isBraked

    def print_command(self, command, power):
        print(colored('Executing command: ' + command + ' at ' + str(power) + '%', 'green'))
