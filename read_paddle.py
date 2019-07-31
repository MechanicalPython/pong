import RPi.GPIO as GPIO
import time
import math


left1 = 14
left2 = 15

right1 = 23
right2 = 24

GPIO.setmode(GPIO.BCM)


def switch(switch):
    if GPIO.input(switch) == GPIO.HIGH:
        print('ON')
        time.sleep(0.1)


def discharge(pin1, pin2):
    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.OUT)
    GPIO.output(pin2, False)
    time.sleep(0.01)


def charge_time(pin1, pin2):
    GPIO.setup(pin2, GPIO.IN)
    GPIO.setup(pin1, GPIO.OUT)
    GPIO.output(pin1, True)
    t1 = time.time()
    while not GPIO.input(pin2):
        pass
    t2 = time.time()
    return t2-t1


def move(pin1, pin2):
    """
    Return UP or DOWN.
    Bigger charge time is full left on both (probably)

    :param pin1:
    :param pin2:
    :return:
    """
    discharge(pin1, pin2)
    t = charge_time(pin1, pin2)
    discharge(pin1, pin2)
    GPIO.cleanup()
    return t


def move_left():
    return move(left1, left2)

def move_right():
    return move(right1, right2)

