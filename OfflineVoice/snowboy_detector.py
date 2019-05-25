import snowboydecoder_arecord
import sys
import signal

signal.signal(signal.SIGINT, signal_handler)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

interrupted = False

def start_snowboy_detector(models, callbacks):
    sensitivity = [0.5]*len(models)
    detector = snowboydecoder_arecord.HotwordDetector(models, sensitivity=sensitivity)
    detector.start(detected_callback=callbacks,
                interrupt_check=interrupt_callback,
                sleep_time=0.03)
    detector.terminate()
