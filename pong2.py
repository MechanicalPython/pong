#! /usr/bin/python3

# Pong
# Language - Python
# Modules - pygame, sys, random, math
#
# Controls - Arrow Keys for Right Paddle and WASD Keys for Left Paddle

import pygame
import pygame.freetype
import sys
import random
from math import *
import time

# import read_paddle

pygame.init()

width = 900
height = 1000

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

background = (0, 0, 0)
white = (236, 240, 241)

top = white
bottom = white
left = white
right = white

margin = 4

scoreLeft = 0
scoreRight = 0
maxScore = 11

font = pygame.freetype.Font('SF Atarian System Extended Bold.ttf', 60)
point_score_sound = pygame.mixer.Sound("Point score.wav")  # Works
hit_paddle_sound = pygame.mixer.Sound("Hit Paddle.wav")  # Works
hit_wall_sound = pygame.mixer.Sound("Hit wall.wav")


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
        else:
            self.x = width - 1.5 * margin - self.w

        self.y = height / 2 - self.h / 2

    # Show the Paddle
    def show(self):
        pygame.draw.rect(display, white, (self.x, self.y, self.w, self.h))

    # Move the Paddle
    def move(self, ydir):
        # If self.y (current position) is more than paddleSpeed, add paddle
        if self.y + self.paddleSpeed > ydir:  # Want to go up.
            self.y -= self.paddleSpeed
        elif self.y - self.paddleSpeed < ydir:
            self.y += self.paddleSpeed
        else:
            self.y = ydir
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

        self.speed = 8

    # Show the Ball
    def show(self):
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.r, self.r))

    # Move the Ball
    def move(self):
        global scoreLeft, scoreRight
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if self.x + self.r > width - margin:  # Point left
            scoreLeft += 1
            point_score_sound.play()
            self.angle = 180 - self.angle
        if self.x < margin:  # Point right
            scoreRight += 1
            point_score_sound.play()
            self.angle = 180 - self.angle

        if self.y < margin:
            self.angle = - self.angle
            hit_wall_sound.play()
        if self.y + self.r >= height - margin:
            self.angle = - self.angle
            hit_wall_sound.play()

    # Check and Reflect the Ball when it hits the padddle
    def checkForPaddle(self):
        if self.x < width / 2:
            if leftPaddle.x < self.x < leftPaddle.x + leftPaddle.w:
                hit_paddle_sound.play()
                if leftPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r < leftPaddle.y + 10:
                    self.angle = -45
                if leftPaddle.y + 10 < self.y < leftPaddle.y + 20 or leftPaddle.y + 10 < self.y + self.r < leftPaddle.y + 20:
                    self.angle = -30
                if leftPaddle.y + 20 < self.y < leftPaddle.y + 30 or leftPaddle.y + 20 < self.y + self.r < leftPaddle.y + 30:
                    self.angle = -15
                if leftPaddle.y + 30 < self.y < leftPaddle.y + 40 or leftPaddle.y + 30 < self.y + self.r < leftPaddle.y + 40:
                    self.angle = -10
                if leftPaddle.y + 40 < self.y < leftPaddle.y + 50 or leftPaddle.y + 40 < self.y + self.r < leftPaddle.y + 50:
                    self.angle = 10
                if leftPaddle.y + 50 < self.y < leftPaddle.y + 60 or leftPaddle.y + 50 < self.y + self.r < leftPaddle.y + 60:
                    self.angle = 15
                if leftPaddle.y + 60 < self.y < leftPaddle.y + 70 or leftPaddle.y + 60 < self.y + self.r < leftPaddle.y + 70:
                    self.angle = 30
                if leftPaddle.y + 70 < self.y < leftPaddle.y + 80 or leftPaddle.y + 70 < self.y + self.r < leftPaddle.y + 80:
                    self.angle = 45
        else:
            if rightPaddle.x + rightPaddle.w > self.x + self.r > rightPaddle.x:
                hit_paddle_sound.play()
                if rightPaddle.y < self.y < leftPaddle.y + 10 or leftPaddle.y < self.y + self.r < leftPaddle.y + 10:
                    self.angle = -135
                if rightPaddle.y + 10 < self.y < rightPaddle.y + 20 or rightPaddle.y + 10 < self.y + self.r < rightPaddle.y + 20:
                    self.angle = -150
                if rightPaddle.y + 20 < self.y < rightPaddle.y + 30 or rightPaddle.y + 20 < self.y + self.r < rightPaddle.y + 30:
                    self.angle = -165
                if rightPaddle.y + 30 < self.y < rightPaddle.y + 40 or rightPaddle.y + 30 < self.y + self.r < rightPaddle.y + 40:
                    self.angle = 170
                if rightPaddle.y + 40 < self.y < rightPaddle.y + 50 or rightPaddle.y + 40 < self.y + self.r < rightPaddle.y + 50:
                    self.angle = 190
                if rightPaddle.y + 50 < self.y < rightPaddle.y + 60 or rightPaddle.y + 50 < self.y + self.r < rightPaddle.y + 60:
                    self.angle = 165
                if rightPaddle.y + 60 < self.y < rightPaddle.y + 70 or rightPaddle.y + 60 < self.y + self.r < rightPaddle.y + 70:
                    self.angle = 150
                if rightPaddle.y + 70 < self.y < rightPaddle.y + 80 or rightPaddle.y + 70 < self.y + self.r < rightPaddle.y + 80:
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
    move_distance = ball.speed
    if move is True:
        if abs(pc - ball.y) < 10:
            move_distance = int(abs(pc - ball.y)/2)
        if pc > ball.y:  # paddle further down
            return paddle.y - move_distance
        else:
            return paddle.y + move_distance
    return paddle.y


paddle_spoof = ['0.995',
 '0.970',
 '0.959',
 '0.999',
 '0.935',
 '0.989',
 '0.966',
 '0.922',
 '0.950',
 '0.951',
 '0.919',
 '0.946',
 '0.899',
 '0.936',
 '0.892',
 '0.913',
 '0.877',
 '0.864',
 '0.886',
 '0.866',
 '0.865',
 '0.846',
 '0.827',
 '0.836',
 '0.836',
 '0.811',
 '0.855',
 '0.789',
 '0.818',
 '0.800',
 '0.810',
 '0.816',
 '0.811',
 '0.781',
 '0.775',
 '0.769',
 '0.746',
 '0.737',
 '0.721',
 '0.763',
 '0.719',
 '0.738',
 '0.701',
 '0.728',
 '0.723',
 '0.700',
 '0.694',
 '0.704',
 '0.688',
 '0.669',
 '0.676',
 '0.640',
 '0.646',
 '0.646',
 '0.636',
 '0.618',
 '0.609',
 '0.599',
 '0.596',
 '0.590',
 '0.603',
 '0.616',
 '0.593',
 '0.607',
 '0.589',
 '0.544',
 '0.548',
 '0.593',
 '0.547',
 '0.546',
 '0.557',
 '0.542',
 '0.524',
 '0.519',
 '0.504',
 '0.511',
 '0.497',
 '0.508',
 '0.466',
 '0.460',
 '0.429',
 '0.468',
 '0.442',
 '0.435',
 '0.425',
 '0.416',
 '0.411',
 '0.428',
 '0.414',
 '0.385',
 '0.387',
 '0.368',
 '0.378',
 '0.361',
 '0.344',
 '0.343',
 '0.342',
 '0.340',
 '0.313',
 '0.337',
 '0.311',
 '0.334',
 '0.315',
 '0.301',
 '0.285',
 '0.286',
 '0.289',
 '0.289',
 '0.300',
 '0.262',
 '0.284',
 '0.264',
 '0.264',
 '0.242',
 '0.247',
 '0.250',
 '0.245',
 '0.248',
 '0.227',
 '0.206',
 '0.211',
 '0.210',
 '0.204',
 '0.186',
 '0.199',
 '0.189',
 '0.158',
 '0.168',
 '0.160',
 '0.164',
 '0.153',
 '0.152',
 '0.145',
 '0.125',
 '0.118',
 '0.114',
 '0.108',
 '0.098',
 '0.067',
 '0.069',
 '0.061',
 '0.069',
 '0.063',
 '0.060',
 '0.056',
 '0.062',
 '0.031',
 '0.017',
 '0.035',
 '0.010',
 '0.017',
 '0.008',
 '0.011',
 '0.000',
 '0.008',
 '0.012',
 '0.005',
 '0.008',
 '0.009',
 '0.006',
 '0.010',
 '0.007',
 '0.015',
 '0.013',
 '0.005',
 '0.008',
 '0.008',
 '0.008',
 '0.011',
 '0.010',
 '0.012',
 '0.005',
 '0.006',
 '0.007',
 '0.006',
 '0.005',
 '0.008',
 '0.011',
 '0.006',
 '0.008',
 '0.015',
 '0.011',
 '0.011',
 '0.010']
paddle_spoof = [float(i) for i in paddle_spoof]


def board():
    pygame.event.set_allowed([pygame.KEYDOWN])
    pygame.mouse.set_visible(False)
    display.set_alpha(None)
    loop = True
    leftChange = 0
    rightChange = 0
    global ball
    ball = Ball(white)
    left_last_position = 0
    right_last_position = 0
    left_paddle_change_track = 0
    right_paddle_change_track = 0
    read_left = read_paddle.PaddleMove('l')
    read_right = read_paddle.PaddleMove('r')
    l_item = 92
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                        close()

        # left_paddle_event = (height - leftPaddle.h) *  #read_left.position()
        # right_paddle_event = (height - rightPaddle.h) * 0.5#read_right.position()

        if l_item == len(paddle_spoof):
            l_item = 0
        print(paddle_spoof[l_item])
        left_paddle_event = int((height - leftPaddle.h) * paddle_spoof[l_item])
        right_paddle_event = int((height - leftPaddle.h) * paddle_spoof[l_item])
        l_item += 1

        if round(left_paddle_event, 1) == left_last_position:
            left_paddle_change_track += 1

        if round(right_paddle_event, 1) == right_last_position:
            right_paddle_change_track += 1

        if left_paddle_change_track > 60*1:
            leftChange = auto_paddle(leftPaddle, 'left')
        else:
            left_paddle_change_track = 0
            leftChange = left_paddle_event

        if right_paddle_change_track > 60*1:
            rightChange = auto_paddle(rightPaddle, 'right')

        else:
            rightChange = right_paddle_event
            right_paddle_change_track = 0

        left_last_position = round(left_paddle_event, 1)
        right_last_position = round(right_paddle_event, 1)

        leftPaddle.move(leftChange)
        rightPaddle.move(rightChange)
        ball.move()
        ball.checkForPaddle()

        display.fill(background)
        showScore()

        ball.show()
        leftPaddle.show()
        rightPaddle.show()

        boundary()

        gameOver()

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    board()
# todo reset button
# todo sound. Hit paddle, hit bottom/top, point score.
# todo menu button. Quit to cmd line, Change volume, Change ball speed.

# todo problems. Very gittery at the bottom of the screen. Need some kind of averaging system. So faster capacitors.
