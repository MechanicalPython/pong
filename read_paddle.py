#! /usr/bin/python3

import RPi.GPIO as GPIO
import time
import statistics as stats

left1 = 14
left2 = 15

right1 = 23
right2 = 24

# Time constant = resistance * capacitor


def switch(switch):
    if GPIO.input(switch) == GPIO.HIGH:
        print('ON')
        time.sleep(0.1)


def timer(func):
    def f(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        end = time.time()
        print('Time taken', end - start, ' for ', func.__name__)
        return rv
    return f


class PaddleMove:
    def __init__(self, side):
        if side == 'l':
            self.pin1, self.pin2 = left1, left2
        if side == 'r':
            self.pin1, self.pin2 = right1, right2

    @timer
    def discharge(self):           # Total 0.000122  Actual is 3-10 times longer.
        GPIO.setup(self.pin1, GPIO.IN)   # 0.00004
        GPIO.setup(self.pin2, GPIO.OUT)  # 0.00004
        GPIO.output(self.pin2, False)    # 0.000032
        time.sleep(0.00001)              # 0.00001

    @timer
    def charge_time(self):         # Total 0.000113
        GPIO.setup(self.pin2, GPIO.IN)   # 0.00004
        GPIO.setup(self.pin1, GPIO.OUT)  # 0.00004
        GPIO.output(self.pin1, True)     # 0.000033
        t1 = time.time()
        while not GPIO.input(self.pin2):  # Charge time
            pass
        t2 = time.time()
        return t2 - t1

    @timer
    def exact_time(self):  # Charge time for one capacitor
        self.discharge()
        t = self.charge_time()
        # self.discharge()
        return t

    @timer
    def avg_charge_time(self, iters=10):
        GPIO.setmode(GPIO.BCM)
        total = []
        for x in range(0, iters):
            total.append(self.exact_time())
        GPIO.cleanup()
        total.sort()
        total = total[int(iters/3):int(iters/3)*2]
        t = sum(total) / len(total)
        return round(t*1000000, 3)

    def stability(self):
        GPIO.setmode(GPIO.BCM)
        for x in range(100):
            print(self.exact_time())
        GPIO.cleanup()

    @timer
    def position(self):
        """
        Return a number between 0 and 1. 1 is max left (down) and 0 is max right (up). Refelcts y axis on pygame.
        Bigger charge time is full left on both (probably)
        """
        t = self.avg_charge_time()
        t = (t - 0.384) / (0.61 - 0.384) 
        return t
