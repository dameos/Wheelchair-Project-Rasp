import speech_recognition as sr
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio # noqa

r = sr.Recognizer()
with sr.Microphone() as source:
    print('Say something')
    audio = r.listen(source)

try:
    print('Tensorflow said: ' + r.recognize_tensorflow(audio))

except sr.UnkwonValueError:
    print('Penee')
