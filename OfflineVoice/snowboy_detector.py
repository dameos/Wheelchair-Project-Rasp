import OfflineVoice.snowboydecoder_arecord as snowboydecoder_arecord
import sys
import signal

def start_snowboy_detector(models):
    sensitivity = [0.5]*len(models)
    detector = snowboydecoder_arecord.HotwordDetector(models, sensitivity=sensitivity)
    return detector
