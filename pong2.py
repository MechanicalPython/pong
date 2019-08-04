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
            self.side = 'l'
        else:
            self.x = width - 1.5 * margin - self.w
            self.side = 'r'

        self.y = height / 2 - self.h / 2

    # Show the Paddle
    def show(self):
        pygame.draw.rect(display, white, (self.x, self.y, self.w, self.h))

    # Move the Paddle
    def move(self, ydir):
        # If self.y (current position) is more than paddleSpeed, add paddle
        if abs(self.y - ydir) > self.paddleSpeed * 10:
            self.y = ydir
        if abs(self.y - ydir) < self.h:
            self.y = self.y
        elif self.y + self.paddleSpeed > ydir:  # Want to go up.
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


paddle_spoof = ['0.30338750000000003',
 '0.2684208333333334',
 '0.26405',
 '0.27417916666666664',
 '0.2805375',
 '0.2729875',
 '0.2811333333333333',
 '0.27914583333333337',
 '0.27159583333333337',
 '0.26424583333333335',
 '0.2801416666666666',
 '0.26662916666666664',
 '0.2721958333333333',
 '0.271',
 '0.2618625',
 '0.2831208333333333',
 '0.27020833333333333',
 '0.27417916666666664',
 '0.27755833333333335',
 '0.2733875',
 '0.267225',
 '0.27358333333333335',
 '0.2861',
 '0.2765666666666667',
 '0.2614666666666666',
 '0.2719958333333333',
 '0.27318749999999997',
 '0.2765666666666667',
 '0.26424583333333335',
 '0.26067083333333335',
 '0.2717958333333333',
 '0.26861666666666667',
 '0.26643333333333336',
 '0.27398333333333336',
 '0.2725916666666667',
 '0.26822083333333335',
 '0.275175',
 '0.27040416666666667',
 '0.26782083333333334',
 '0.2960375',
 '0.2670291666666667',
 '0.26643333333333336',
 '0.267625',
 '0.2783541666666667',
 '0.28650000000000003',
 '0.27040416666666667',
 '0.28550416666666667',
 '0.2984208333333333',
 '0.2912666666666667',
 '0.2622583333333333',
 '0.2622583333333333',
 '0.2892791666666667',
 '0.27060416666666665',
 '0.26524166666666665',
 '0.28471250000000003',
 '0.26424583333333335',
 '0.27020833333333333',
 '0.2656375',
 '0.27537083333333334',
 '0.2690166666666666',
 '0.2714',
 '0.267425',
 '0.2799416666666667',
 '0.27914583333333337',
 '0.2658375',
 '0.27577083333333335',
 '0.2773583333333333',
 '0.267225',
 '0.2656375',
 '0.2656375',
 '0.2614666666666666',
 '0.2650416666666667',
 '0.2680208333333333',
 '0.2717958333333333',
 '0.2725916666666667',
 '0.26861666666666667',
 '0.27597083333333333',
 '0.2721958333333333',
 '0.26603333333333334',
 '0.2692125',
 '0.2714',
 '0.274775',
 '0.27616666666666667',
 '0.2769625',
 '0.26344999999999996',
 '0.26087083333333333',
 '0.2769625',
 '0.2692125',
 '0.2831208333333333',
 '0.260075',
 '0.2859041666666667',
 '0.27417916666666664',
 '0.2694125',
 '0.2916666666666667',
 '0.27895',
 '0.26484166666666664',
 '0.2614666666666666',
 '0.26861666666666667',
 '0.2924583333333333',
 '0.260075',
 '0.2729875',
 '0.2841166666666667',
 '0.289875',
 '0.2813333333333333',
 '0.26365',
 '0.2626583333333333',
 '0.27577083333333335',
 '0.2763666666666667',
 '0.2590791666666667',
 '0.267425',
 '0.2845125',
 '0.26464583333333336',
 '0.26424583333333335',
 '0.27795416666666667',
 '0.26344999999999996',
 '0.2632541666666667',
 '0.2668291666666667',
 '0.27755833333333335',
 '0.2654375',
 '0.2809375',
 '0.27318749999999997',
 '0.2809375',
 '0.27537083333333334',
 '0.2737833333333333',
 '0.2658375',
 '0.27616666666666667',
 '0.28510833333333335',
 '0.2725916666666667',
 '0.2668291666666667',
 '0.2680208333333333',
 '0.267625',
 '0.26405',
 '0.26344999999999996',
 '0.2781541666666667',
 '0.2813333333333333',
 '0.26087083333333333',
 '0.27040416666666667',
 '0.2725916666666667',
 '0.2781541666666667',
 '0.271',
 '0.26484166666666664',
 '0.2956375',
 '0.29722916666666666',
 '0.2799416666666667',
 '0.2614666666666666',
 '0.2908708333333333',
 '0.27457916666666665',
 '0.2658375',
 '0.274975',
 '0.2763666666666667',
 '0.2708041666666666',
 '0.27060416666666665',
 '0.27934583333333335',
 '0.26385',
 '0.2763666666666667',
 '0.27000833333333335',
 '0.2626583333333333',
 '0.2692125',
 '0.2892791666666667',
 '0.2696125',
 '0.2721958333333333',
 '0.2688166666666667',
 '0.2680208333333333',
 '0.2622583333333333',
 '0.26405',
 '0.28550416666666667',
 '0.26424583333333335',
 '0.26405',
 '0.26067083333333335',
 '0.275175',
 '0.274975',
 '0.27597083333333333',
 '0.27239166666666664',
 '0.2805375',
 '0.2912666666666667',
 '0.27597083333333333',
 '0.27020833333333333',
 '0.2996125',
 '0.27159583333333337',
 '0.267425',
 '0.2582875',
 '0.267225',
 '0.2696125',
 '0.2694125',
 '0.267625',
 '0.2614666666666666',
 '0.2670291666666667',
 '0.26365',
 '0.2708041666666666']
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
    # read_left = read_paddle.PaddleMove('l')
    # read_right = read_paddle.PaddleMove('r')
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
        # print(paddle_spoof[l_item])
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
