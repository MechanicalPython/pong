#! /usr/bin/python

import RPi.GPIO as GPIO
import time
import statistics as stats

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
        time.sleep(0.00001)

    def charge_time(self):
        GPIO.setup(self.pin2, GPIO.IN)
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.output(self.pin1, True)
        t1 = time.time()
        while not GPIO.input(self.pin2):
            pass
        t2 = time.time()
        return t2-t1

    def exact_time(self):  # Charge time for one capacitor
        self.discharge()
        t = self.charge_time()
        self.discharge()
        return t

    def avg_charge_time(self, iters=100):
        total = []
        GPIO.setmode(GPIO.BCM)
        for x in range(0, iters):
            total.append(self.exact_time())
        GPIO.cleanup()
        total = total[80:120]
        return sum(total) / len(total)

    def stability(self):
        t = []
        for x in range(60):
            time.sleep(0.0000001)
            t.append(self.avg_charge_time())
        return stats.stdev(t), stats.mean(t)

    def position(self):
        """
        Return a number between 0 and 1. 1 is max left (down) and 0 is max right (up). Refelcts y axis on pygame.
        Bigger charge time is full left on both (probably)
        """
        t = self.avg_charge_time()
        t = t * 10000
        return t

while True:
    #print(PaddleMove('l').position())
    print(PaddleMove('r').avg_charge_time())


