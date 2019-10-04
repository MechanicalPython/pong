#! /usr/bin/env python3

# Pong
# Language - Python
# Modules - pygame, sys, random, math
#
import pygame
import pygame.freetype
import sys
import random
from math import *
import time
import os
import pong.c_read_paddle as read_paddle

pygame.mixer.init(22100, -16, 2, 2**7)
pygame.init()

width = 900
height = 1000

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

background = (0, 0, 0)
white = (236, 240, 241)
gray = (128, 128, 128)

top = white
bottom = white
left = white
right = white

margin = 4

scoreLeft = 0
scoreRight = 0
maxScore = 11

d = os.path.dirname(__file__)
font = pygame.freetype.Font(f'{d}/SF Atarian System Extended Bold.ttf', 60)

beep = pygame.mixer.Sound(f"{d}/beep.wav")
boop = pygame.mixer.Sound(f"{d}/boop.wav")


def timer(func):
    def f(*args, **kwargs):
        start = time.time()
        rv = func(*args, **kwargs)
        end = time.time()
        print('Time taken', end - start, ' for ', func.__name__)
        return rv
    return f


# Draw the Boundary of Board
def boundary():
    global top, bottom, left, right
    pygame.draw.rect(display, left, (0, 0, margin, height))
    pygame.draw.rect(display, top, (0, 0, width, margin))
    pygame.draw.rect(display, right, (width - margin, 0, margin, height))
    pygame.draw.rect(display, bottom, (0, height - margin, width, margin))

    dash_height = 15
    dash_width = 1

    number_of_dashes = int(height/(dash_height*2))
    x = width / 2 - margin / 2
    y = 0
    for dash in range(number_of_dashes):
        pygame.draw.rect(display, white, (x, y, dash_width, dash_height))  # screen, colour, (x, y, width, height)
        y += dash_height*2


# Paddle Class
class Paddle:
    def __init__(self, position):
        self.w = 10
        self.h = self.w * 8
        self.paddleSpeed = 6

        if position == -1:
            self.x = 1.5 * margin
            self.side = 'l'
        else:
            self.x = width - 1.5 * margin - self.w
            self.side = 'r'

        self.y = height / 2 - self.h / 2
        self.moving_avg = []
        self.last_minute = []

    # Show the Paddle
    def show_paddle(self):
        pygame.draw.rect(display, white, (self.x, self.y, self.w, self.h))

    # Move the Paddle
    def move_paddle(self, ydir):  # ydir is the raw value given by read_paddle.position()
        self.moving_avg.append(ydir)
        #self.last_minute.append(ydir)
        ydir = int(sum(self.moving_avg)/len(self.moving_avg))
        self.y = ydir
        if len(self.moving_avg) > 15:  # 1/2 of a second. 
            self.moving_avg.pop(0)
        #if len(self.last_minute) > 30*60:
        #    self.last_minute.pop(0)

        # Collision control
        if self.y < 0:
            self.y = 0
        elif self.y + self.h > height:
            self.y = height - self.h


leftPaddle = Paddle(-1)
rightPaddle = Paddle(1)


# Ball Class
class Ball:
    def __init__(self, color):
        self.r = 20
        self.x = width / 2 - self.r / 2
        self.y = height / 2 - self.r / 2
        self.color = color
        self.angle = random.randint(-75, 75)
        if random.randint(0, 1):
            self.angle += 180

        self.speed = 5

    # Show the Ball
    def show_ball(self):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.r, self.r))

    # Move the Ball
    def move_ball(self):
        global scoreLeft, scoreRight
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if self.x + self.r > width - margin:
            beep.play()
            self.angle = 180 - self.angle
            if not leftPaddle.y < ball.x < leftPaddle.y + leftPaddle.h:  # Point left, so hit right side. 
                scoreLeft += 1
                time.sleep(0.5)
                ball.x = width / 2 - self.r / 2
                ball.y = height / 2 - self.r / 2
                ball.angle = random.randint(-75, 75)
                ball.angle += 180

        if self.x < margin:  # Point right
            beep.play()
            self.angle = 180 - self.angle
            if not rightPaddle.y < ball.x < rightPaddle.y + rightPaddle.h:
                scoreRight += 1
                time.sleep(0.5)
                ball.x = width / 2 - self.r / 2
                ball.y = height / 2 - self.r / 2
                ball.angle = random.randint(-75, 75)

        if self.y < margin:
            beep.play()
            self.angle = - self.angle
        if self.y + self.r >= height - margin:
            beep.play()
            self.angle = - self.angle

    # Check and Reflect the Ball when it hits the paddle
    def checkForPaddle(self):
        if self.x < width / 2:  # If on left side
            if leftPaddle.x < self.x < leftPaddle.x + leftPaddle.w:  # Ball is near the paddle (between paddle x and paddle x + 20
                if leftPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r < leftPaddle.y + 10:
                    boop.play()
                    self.angle = -45
                if leftPaddle.y + 10 < self.y < leftPaddle.y + 20 or leftPaddle.y + 10 < self.y + self.r < leftPaddle.y + 20:
                    boop.play()
                    self.angle = -30
                if leftPaddle.y + 20 < self.y < leftPaddle.y + 30 or leftPaddle.y + 20 < self.y + self.r < leftPaddle.y + 30:
                    boop.play()
                    self.angle = -15
                if leftPaddle.y + 30 < self.y < leftPaddle.y + 40 or leftPaddle.y + 30 < self.y + self.r < leftPaddle.y + 40:
                    boop.play()
                    self.angle = -10
                if leftPaddle.y + 40 < self.y < leftPaddle.y + 50 or leftPaddle.y + 40 < self.y + self.r < leftPaddle.y + 50:
                    boop.play()
                    self.angle = 10
                if leftPaddle.y + 50 < self.y < leftPaddle.y + 60 or leftPaddle.y + 50 < self.y + self.r < leftPaddle.y + 60:
                    boop.play()
                    self.angle = 15
                if leftPaddle.y + 60 < self.y < leftPaddle.y + 70 or leftPaddle.y + 60 < self.y + self.r < leftPaddle.y + 70:
                    boop.play()
                    self.angle = 30
                if leftPaddle.y + 70 < self.y < leftPaddle.y + 80 or leftPaddle.y + 70 < self.y + self.r < leftPaddle.y + 80:
                    boop.play()
                    self.angle = 45
        else:
            if rightPaddle.x + rightPaddle.w > self.x + self.r > rightPaddle.x:
                if rightPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r < leftPaddle.y + 10:
                    boop.play()
                    self.angle = -135
                if rightPaddle.y + 10 < self.y < rightPaddle.y + 20 or rightPaddle.y + 10 < self.y + self.r < rightPaddle.y + 20:
                    boop.play()
                    self.angle = -150
                if rightPaddle.y + 20 < self.y < rightPaddle.y + 30 or rightPaddle.y + 20 < self.y + self.r < rightPaddle.y + 30:
                    boop.play()
                    self.angle = -165
                if rightPaddle.y + 30 < self.y < rightPaddle.y + 40 or rightPaddle.y + 30 < self.y + self.r < rightPaddle.y + 40:
                    boop.play()
                    self.angle = 170
                if rightPaddle.y + 40 < self.y < rightPaddle.y + 50 or rightPaddle.y + 40 < self.y + self.r < rightPaddle.y + 50:
                    boop.play()
                    self.angle = 190
                if rightPaddle.y + 50 < self.y < rightPaddle.y + 60 or rightPaddle.y + 50 < self.y + self.r < rightPaddle.y + 60:
                    boop.play()
                    self.angle = 165
                if rightPaddle.y + 60 < self.y < rightPaddle.y + 70 or rightPaddle.y + 60 < self.y + self.r < rightPaddle.y + 70:
                    boop.play()
                    self.angle = 150
                if rightPaddle.y + 70 < self.y < rightPaddle.y + 80 or rightPaddle.y + 70 < self.y + self.r < rightPaddle.y + 80:
                    boop.play()
                    self.angle = 135


# Show the Score
def showScore():
    font.render_to(display, ((width/4, 20)), str(scoreLeft), white)
    font.render_to(display, (((width / 4)*3, 20)), str(scoreRight), white)


# Game Over
def gameOver():
    if scoreLeft == maxScore or scoreRight == maxScore:
        t = time.time()
        while t+5 > time.time():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        reset()
            font.render_to(display, (width / 2 - 185, height / 2), "GAME OVER", white)
            pygame.display.update()
        reset()


def reset():
    global scoreLeft, scoreRight
    scoreLeft = 0
    scoreRight = 0
    board()


def close():
    pygame.quit()
    sys.exit()


def auto_paddle(paddle, side):
    move = False
    ball_angle = abs(ball.angle)
    if side == 'left' and ball_angle > 90:
        move = True
    elif side == 'right' and ball_angle < 90:
        move = True
    pc = paddle.y + (paddle.h/2)
    move_distance = ball.speed * 10 * iters
    if move is True:
        if abs(pc - ball.y) < 10:
            move_distance = int(abs(pc - ball.y)/2)
        if pc > ball.y:  # paddle further down
            return paddle.y - move_distance
        else:
            return paddle.y + move_distance
    return paddle.y


class Dot:
    def __init__(self, y):
        self.x = (width / 2 - 50)
        self.y = y
        self.w = 20
        self.h = 20

    def show_dot(self):
        pygame.draw.rect(display, white, (self.x, self.y, self.w, self.h))

    def move(self, y):
        self.y = y


def menu(menu_items):
    read_left = read_paddle.PaddleMove('l')
    n = len(menu_items)
    while True:
        # p = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        display.fill(background)

        dot = Dot(110)
        pos = read_left.position()
        start = 1
        for item in menu_items:
            font.render_to(display, (width / 2, start*100), item, white)
            if (start - 1)/n < pos < start/n:
                dot.move(start*100 + 10)
                if read_paddle.switch_is_pressed():
                    time.sleep(0.5)
                    return menu_items[start - 1]
            start += 1
        dot.show_dot()
        pygame.display.update()
        clock.tick(30)


def board():
    pygame.event.set_allowed([pygame.KEYDOWN])
    pygame.mouse.set_visible(False)
    display.set_alpha(None)
    global ball
    ball = Ball(white)

    global iters
    iters = 4
    read_left = read_paddle.PaddleMove('l')
    read_right = read_paddle.PaddleMove('r')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()

        if read_paddle.switch_is_pressed() is True:
            while read_paddle.switch_is_pressed() is True:
                time.sleep(0.1)
            time.sleep(0.1)
            menu_items = ['Quit', 'Reset', 'Continue', 'Ball Speed']
            event = menu(menu_items)
            if event == 'Quit':
                close()
            elif event == 'Reset':
                reset()
            elif event == 'Continue':
                pass
            elif event == 'Ball Speed':
                options = {'Slow': 2, 'Medium (Recommended)': 4, 'High': 6, 'Very High': 8, 'Insane': 10}
                event = menu(list(options.keys()))
                iters = options[event]

        left_event = int((height - leftPaddle.h) * read_left.position(10))
        right_event = int((height - rightPaddle.h) * read_right.position(10))
        leftChange = left_event
        rightChange = right_event


        # leftChange = auto_paddle(leftPaddle, 'left')
        # rightChange = auto_paddle(rightPaddle, 'right')

        #if len(leftPaddle.last_minute) >= 30*60 and abs(max(leftPaddle.last_minute) - min(leftPaddle.last_minute)) < 100:
        #    leftChange = auto_paddle(leftPaddle, 'left')
        #    leftPaddle.colour = gray
        #else:
        #    leftChange = left_event
        #    leftPaddle.colour = white
        #if len(rightPaddle.last_minute) >= 30*60 and abs(max(rightPaddle.last_minute) - min(rightPaddle.last_minute)) < 100:
        #    rightChange = auto_paddle(rightPaddle, 'right')
        #    rightPaddle.colour = gray
        #else:
        #    rightChange = right_event
        #    rightPaddle.colour = white
        leftPaddle.move_paddle(leftChange)
        rightPaddle.move_paddle(rightChange)

        for x in range(iters):
            ball.move_ball()
            ball.checkForPaddle()


        display.fill(background)
        showScore()

        ball.show_ball()
        leftPaddle.show_paddle()
        rightPaddle.show_paddle()

        boundary()

        gameOver()

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    board()

# todo sound delay still there.
