import OnlineVoice.mapping
import numpy as np
import os
from google.assistant.library.event import EventType

def process_event(event):
    if event.type == EventType.ON_RENDER_RESPONSE:
        text = event.args["text"]
        text_replaced =  text.replace("Going from", "")
        splitted = list(map(lambda x: x.strip(), text_replaced.split("to")))
        if len(splitted) == 2:
            start = mapping.decode_place(splitted[0])
            end = mapping.decode_place(splitted[1])
            if start != None and  end != None:
                maze = np.loadtxt('map.txt', delimiter=',')
                mapping.calculate_and_print_maze(maze, start, end)
