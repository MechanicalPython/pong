#! /usr/bin/python

import RPi.GPIO as GPIO
import time

left1 = 14
left2 = 15

right1 = 23
right2 = 24

def switch(switch):
    if GPIO.input(switch) == GPIO.HIGH:
        print('ON')
        time.sleep(0.1)


class PaddleMove:
    def __init__(self, side):
        if side == 'l':
            self.pin1, self.pin2 = left1, left2
        if side == 'r':
            self.pin1, self.pin2 = right1, right2

    def discharge(self):
        GPIO.setup(self.pin1, GPIO.IN)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.output(self.pin2, False)
        time.sleep(0.01)

    def charge_time(self):
        GPIO.setup(self.pin2, GPIO.IN)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.output(self.pin1, True)
        t1 = time.time()
        while not GPIO.input(self.pin2):
            pass
        t2 = time.time()
        return t2-t1

    def position(self):
        """
        Return a number between 0 and 1. 1 is max left (down) and 0 is max right (up). Refelcts y axis on pygame.
        Bigger charge time is full left on both (probably)

        :param pin1:
        :param pin2:
        :return:
        """
        GPIO.setmode(GPIO.BCM)
        self.discharge()
        t = self.charge_time()
        self.discharge()
        GPIO.cleanup()
        return t/0.14
