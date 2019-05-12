from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)
centre = (3, 3, 4, 4)

def display_front(level, canv):
    __display(2, level, canv)

def display_right(level, canv):
    __display(3, level, canv)

def display_left(level, canv):
    __display(1, -level, canv)

def display_back(level, canv):
    __display(0, -level, canv)

def __display(pos, level, canv):
    centre_list = list(centre)
    centre_list[pos] = centre[pos] + level
    with canv as draw:
        draw.rectangle(tuple(centre_list), outline='red', fill=None)

def display_diag_pos(level, canv):
    pos = centre[3]
    with canv as draw:
        for i in range(pos, pos + level + 1):
            draw.point((i, i), fill='red')

def display_diag_neg(level, canv):
    pos = 4
    with canv as draw:
        for i in range(1, level + 1):
            draw.point((pos + i, (pos - 1) - i), fill='red')

def create_canvas():
    return canvas(device)

def from_distance_to_level(distance):
    if distance > 30:
        return 0
    if distance <= 30 and distance > 20:
        return 1
    if distance <= 20 and distance > 10:
        return 2
    if distance <= 10:
        return 3
