#! /usr/bin/python3

import time
import statistics as stats
import pigpio

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

pi = pigpio.pi()

class PaddleMove:
    def __init__(self, side):
        if side == 'l':
            self.pin1, self.pin2 = left1, left2
        if side == 'r':
            self.pin1, self.pin2 = right1, right2

    def discharge(self):           # Total 0.000122  Actual is 3-10 times longer.
        pi.set_mode(self.pin1, pigpio.INPUT)   # 0.00004
        pi.set_mode(self.pin2, pigpio.OUTPUT)  # 0.00004
        pi.write(self.pin2, 0)    # 0.000032
        time.sleep(0.00001)              # 0.00001

    def charge_time(self):         # Total 0.000113
        pi.set_mode(self.pin2, pigpio.INPUT)   # 0.00004
        pi.set_mode(self.pin1, pigpio.OUTPUT)  # 0.00004
        pi.write(self.pin1, 1)     # 0.000033
        t1 = time.time()
        while pi.read(self.pin2) != 1:  # Charge time
            pass
        t2 = time.time()
        return t2 - t1

    def exact_time(self):  # Charge time for one capacitor
        self.discharge()
        t = self.charge_time()
        # self.discharge()
        return t

    def avg_charge_time(self, iters=30):
        # Max is 250, min is 50
        # Convert to decimal by having (x*4)/1000
        total = []
        for x in range(0, iters):
            total.append(self.exact_time())
        total = [round(int(i*1000000), -1) for i in total]
        total = max(set(total), key=total.count)
        total = ((total-50)*5)/1000
        return round(total, 2) 

    def position(self):
        """
        Return a number between 0 and 1. 1 is max left (down) and 0 is max right (up). Refelcts y axis on pygame.
        Bigger charge time is full left on both (probably)
        """
        t = self.avg_charge_time()
        return t

print(PaddleMove('l').exact_time())
#import collections
#t= []
#for x in range(0, 1000):
#    t1 = time.time()
#    (PaddleMove('l').position())
#    PaddleMove('r').position()
#    t.append(time.time() - t1)

#print(sum(t)/len(t))
#print(collections.Counter(t))
