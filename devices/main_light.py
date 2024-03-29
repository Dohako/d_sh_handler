import sys
import yeelight
import time
import subprocess

# python3 devices\main.py yeelight brightness 10

_, device, state, param = sys.argv


def turn_on_light_tuya():
    sub = subprocess.Popen(["./light_tuya_1.sh true"], shell=True)
    time.sleep(1)
    sub.kill()


def turn_off_light_tuya():
    sub = subprocess.Popen(["./light_tuya_1.sh false"], shell=True)
    time.sleep(1)
    sub.kill()


def turn_on_light_yeelight():
    pass


def turn_off_light_yeelight():
    pass


if device is "tuya":
    if state is 'on':
        turn_on_light_tuya()
    elif state is 'off':
        turn_off_light_tuya()
elif device is "yeelight":
    bulbs = yeelight.discover_bulbs()
    if bulbs:
        bulb = yeelight.Bulb(bulbs[0]['ip'])
        if state is 'on':
            bulb.turn_on()
        elif state is 'off':
            bulb.turn_off()
        elif state is 'brightness':
            bulb.set_brightness(int(param))
        elif state is 'state':
            if bulbs[0]['capabilities']['power'] == 'on':
                pass
    else:
        exit(1)