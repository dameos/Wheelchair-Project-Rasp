import RPi.GPIO as IO

class Motors:
    DEFAULTINPUTRANGE = (0, 100)
    FREQUENCY = 1000

    def __init__(self, pinS1, pinS2, pinBrake):
        self.__pinS1 = pinS1
        self.__pinS2 = pinS2
        self.__pinBrake = pinBrake

        # Setting up pins
        IO.setmode(IO.BCM)
        IO.setup(self.__pinS1, IO.OUT)
        IO.setup(self.__pinS2, IO.OUT)
        IO.setup(pinBrake, IO.OUT)

        # Motor variables
        self.__motor1 = IO.PWM(pinS1, self.FREQUENCY)
        self.__motor2 = IO.PWM(pinS2, self.FREQUENCY)

        # First state
        # Motors start at 50 since the idle state is 2.5V
        # Brakes starts LOW since the electric brake releases at 24V
        self.__motor1.start(50.27)
        self.__motor2.start(50.60)
        IO.output(self.__pinBrake, IO.LOW)

    def decode_power(self, power, inputRange, outputRange):
        left_factor = (power-inputRange[0])/(inputRange[1]-inputRange[0])
        temp = left_factor * (outputRange[1] - outputRange[0]) + outputRange[0]
        return temp

    def drive_forward(self, power):
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 100))
        self.__motor1.ChangeDutyCycle(decoded_power)
        self.__motor2.ChangeDutyCycle(decoded_power)

    def drive_backward(self, power):
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 0))
        self.__motor1.ChangeDutyCycle(decoded_power)
        self.__motor2.ChangeDutyCycle(decoded_power)

    def drive_right(self, power):
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 100))
        negative_decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 0))
        self.__motor2.ChangeDutyCycle(decoded_power)
        self.__motor1.ChangeDutyCycle(negative_decoded_power)

    def drive_left(self, power):
        decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 100))
        negative_decoded_power = self.decode_power(power, self.DEFAULTINPUTRANGE, (50, 0))
        self.__motor1.ChangeDutyCycle(decoded_power)
        self.__motor2.ChangeDutyCycle(negative_decoded_power)

    def brake(self):
        IO.output(self.__pinBrake, IO.LOW)

    def release_brake(self):
        IO.output(self.__pinBrake, IO.HIGH)
