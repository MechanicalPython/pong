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

left = 4  # Pin1

right = 24  # Pin1


# Time constant = resistance * capacitor
def timer(func):
    def f(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        end = time.time()
        print('Time taken', end - start, ' for ', func.__name__)
        return rv
    return f


def switch_is_pressed(input_pin=7, power_pin=8):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(power_pin, GPIO.OUT)
    GPIO.output(power_pin, True)

    if GPIO.input(input_pin) == GPIO.HIGH:
        GPIO.cleanup()
        return True
    else:
        GPIO.cleanup()
        return False


class PaddleMove:
    def __init__(self, side):
        if side == 'l':
            self.pin = left
        if side == 'r':
            self.pin = right

    def exact_time(self):  
        GPIO.setmode(GPIO.BCM)
        # Discharge capacitor
        GPIO.setup(self.pin, GPIO.OUT) 
        GPIO.output(self.pin, GPIO.LOW) 
        time.sleep(0.0001)
        GPIO.setup(self.pin, GPIO.IN) 
        t = time.time()
        while (GPIO.input(self.pin) == GPIO.LOW): 
            pass
        t = time.time() - t
        GPIO.cleanup()
        return int(t*1000000)

    def avg_charge_time(self, iters=20):
        # Max is 250, min is 50
        # Convert to decimal by having (x*4)/1000 
        total = [] 
        for x in range(0, iters):
            total.append(self.exact_time())
        total = stats.median(total)
        return total

    def position(self, iters=20):
        """
        Return a number between 0 and 1. 1 is max left (down) and 0 is max right (up). Refelcts y axis on pygame.
        Bigger charge time is full left on both (probably)
        """
        t = self.avg_charge_time(iters)
        t = round((t-50)/430, 5)
        return t

if __name__ == '__main__':
    import sys
    lp = PaddleMove('l')
    rp = PaddleMove('r')
    if len(sys.argv) > 1:
        i = int(sys.argv[1])
    else:
        i = 20
    print('Iters = ', i)
    t = time.time()
    print(lp.position(i))
    print('Time taken: ', time.time() - t)
    t = time.time()
    print(rp.position(i))
    print('Time taken: ', time.time() - t)
