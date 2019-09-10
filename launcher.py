#! /usr/bin/env python3


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def switch_is_pressed(input_pin=7, power_pin=8):
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(power_pin, GPIO.OUT)
    GPIO.output(power_pin, True)

    if GPIO.input(input_pin) == GPIO.HIGH:
        GPIO.cleanup()
        return True
    else:
        GPIO.cleanup()
        return False


if __name__ == '__main__':
    while True:
        if switch_is_pressed():
            import pong2
            pong2.board()
        else:
            time.sleep(0.5)

