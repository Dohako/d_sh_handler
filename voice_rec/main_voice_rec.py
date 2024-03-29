import psutil
import os
import time
import random
import subprocess
import datetime
from os import name as os_name

if os_name != 'nt':
    # TODO change to dynamic
    import pyaudio
    import pyttsx3
    from vosk import Model, KaldiRecognizer


class VoiceHandler():
    def __init__(self) -> None:
        self.hello_list = ['I am listening', 'Yes', 'I am here']
        self.model = Model("model-ru")
        self.rate = 110

    def start(self):
        while True:
            pass


    def previous_voice_recognition(self):
        # pyttsx settings
        engine = pyttsx3.init()
        # engine.setProperty('voice', 'ru')
        engine.setProperty('rate', rate)
        rec = KaldiRecognizer(model, 48000)  # 16000
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=48000,
                        input=True,
                        frames_per_buffer=30000)  # 30000
        stream.start_stream()
        # was here
        # time.sleep(3)
        kws = False
        time_start = int(time.time())
        checking_time = time_start
        s = {}
        print(p.get_device_info_by_index(0)['defaultSampleRate'])

        while True:
            data = stream.read(5000, exception_on_overflow=False)  # было 5000
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                first_res = rec.Result()
                print(first_res)
                if len(first_res) > 17:
                    if "компьютер" in first_res:
                        time_start = int(time.time())
                        kws = True
                    time_now = int(time.time())
                    if kws == True and time_now - time_start < 10:
                        if "свет" in first_res:
                            if "включ" in first_res:
                                engine.say("Turning on the light")
                                engine.runAndWait()
                                kws = False
                            elif "выключ" in first_res:
                                engine.say("Turning off the light")
                                engine.runAndWait()
                                kws = False
                        elif "увеличить скорость речи" in first_res:
                            engine.say("Speed up")
                            engine.runAndWait()
                        elif "уменьшить скорость речи" in first_res:
                            engine.say("Speed down")
                            engine.runAndWait()
                        elif "врем" in first_res:
                            now_time = datetime.datetime.now() + datetime.timedelta(hours=2)
                            engine.say(f"the time is {now_time.strftime('%H %M')}")
                            engine.runAndWait()
                        else:
                            engine.say(random.choice(hello_list))
                            engine.runAndWait()
                            time_start = int(time.time())
                    if time_now - time_start > 15:
                        kws = False
            # else:
            # print(rec.PartialResult())
        print(rec.FinalResult())
