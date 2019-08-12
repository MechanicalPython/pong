#! /usr/bin/python3

#  Pin1----- -------Paddle
#                       |
#                       |
#  pin2 -- Capacitor-----  
#            |
# Ground ----         



import time
import statistics as stats
import RPi.GPIO as GPIO

left1 = 14  # Pin1
left2 = 15  # Pin2

right1 = 23  # Pin1
right2 = 24  # Pin2

# Time constant = resistance * capacitor


class Switch:
    def __init__(self, input_pin):
        GPIO.setmode(GPIO.BCM)
        self.input_pin = input_pin
        GPIO.setup(self.input_pin, GPIO.IN)

    def is_pressed(self):
        if GPIO.input(self.input_pin) == GPIO.HIGH:
            return True


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
        
    def discharge(self):           # Total 0.000122  Actual is 3-10 times longer.
        GPIO.setup(self.pin1, GPIO.IN)   # 0.00004
        GPIO.setup(self.pin2, GPIO.OUT)  # 0.00004
        GPIO.output(self.pin2, False)    # 0.000032
        time.sleep(0.00001)              # 0.00001

    def charge_time(self):         # Total 0.000113
        GPIO.setup(self.pin2, GPIO.IN)   # 0.00004
        GPIO.setup(self.pin1, GPIO.OUT)  # 0.00004
        GPIO.output(self.pin1, True)     # 0.000033
        t1 = time.time()
        while not GPIO.input(self.pin2):  # Charge time
            pass
        t2 = time.time()
        return t2 - t1

    def exact_time(self):  # Charge time for one capacitor
        self.discharge()
        t = self.charge_time()
        #print('{0:.10f}'.format(t))
        # self.discharge()
        return t

    def avg_charge_time(self, iters=30):
        # Max is 250, min is 50
        # Convert to decimal by having (x*4)/1000 
        GPIO.setmode(GPIO.BCM)
        total = []
        for x in range(0, iters):
            total.append(self.exact_time())
        total = stats.median(total)
        GPIO.cleanup()
        return round(total*1000000, 2)

    def position(self):
        """
        Return a number between 0 and 1. 1 is max left (down) and 0 is max right (up). Refelcts y axis on pygame.
        Bigger charge time is full left on both (probably)
        """
        t = self.avg_charge_time()
        t = (t-50)/200
        return round(t, 4)

# print(PaddleMove('l').position())
#t = []
#pl = PaddleMove('l')
#pr = PaddleMove('r')
#for x in range(0, 1000):
    #t1 = time.time()
#    print(pl.position(), pr.position())
    #t.append(time.time() - t1)

#print(sum(t)/len(t))
