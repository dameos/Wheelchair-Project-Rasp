import math
from main import motorLock
from main import MOTORS
from time import sleep

class MotorSingleCommand:
    def __init__(self, command, time, power=50):
        self.command = command
        self.time = time
        self.power = power

    def execute_command(self):
        try:
            motorLock.acquire()
            if self.command == 'forward':
                MOTORS.drive_forward(self.power)
            if self.command == 'right':
                MOTORS.drive_right(self.power)
            if self.command == 'left':
                MOTORS.drive_left(self.power)
        finally:
            motorLock.release()
        sleep(self.time)


class MotorCommands:
    def __init__(self, commands, swap_path=False):
        self.commands = commands
        self.swap_path = swap_path

    def execute_commands(self):
        for command in self.commands:
            command.execute_command()

'''
Returns the angle in degrees between two given points following the formula:
    angle = arctan((y2 - y1 )/(x2 - x1))
'''
def get_angle_between_points(point1, point2):
    inverse_tan = math.atan2((point2[0] - point1[0]), (point2[0] - point1[0])) 
    return math.degrees(inverse_tan)

'''
Swaps all x and y for every coord in the list of path
'''
def flip_path_orientation(path):
    return list(map(lambda coord: (coord[1], coord[0])))

def decode_dreeges_into_motor_command(degrees):
    if degrees == 0:
        forward_command = MotorSingleCommand(command='forward', time=1)
        return MotorCommands(commands=[forward_command])
    if degrees == 90:
        rotate_command = MotorSingleCommand(command='right', time=0.5)
        forward_command = MotorSingleCommand(command='forward', time=1)
        return MotorCommands(commands=[rotate_command, forward_command], swap_path=True)
    if degrees == -90:
        rotate_command = MotorSingleCommand(command='left', time=0.5)
        forward_command = MotorSingleCommand(command='forward', time=1)
        return MotorCommands(commands=[rotate_command, forward_command], swap_path=True)
