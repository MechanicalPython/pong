#! /usr/bin/env python3


import sys
import pygame
from pygame import *
from pygame.locals import *
import c_read_paddle as read_paddle

white = (236, 240, 241)
background = (0, 0, 0)
clock = pygame.time.Clock()

width = 1000
height = 600

class Dot:
    def __init__(self, y):
        self.x = 200
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


class Breakout:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 600))
        self.blocks = []
        self.paddle = [[pygame.Rect(300, 500, 20, 10), 120],
                       [pygame.Rect(320, 500, 20, 10), 100],
                       [pygame.Rect(340, 500, 20, 10), 80],
                       [pygame.Rect(360, 500, 20, 10), 45],
                       ]
        self.ball = pygame.Rect(300, 490, 5, 5)
        self.direction = -1
        self.yDirection = -1
        self.angle = 80
        self.speeds = {
            120: (-10, -3),
            100: (-10, -8),
            80: (10, -8),
            45: (10, -3),
        }
        self.swap = {
            120: 45,
            45: 120,
            100: 80,
            80: 100,
        }
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 25)
        self.score = 0

    def createBlocks(self):
        self.blocks = []
        y = 50
        for __ in range(20):
            x = 50
            for _ in range(33):
                block = pygame.Rect(x, y, 25, 10)
                self.blocks.append(block)
                x += 27
            y += 12

    def ballUpdate(self):
        for _ in range(2):
            speed = self.speeds[self.angle]
            xMovement = True
            if _:
                self.ball.x += speed[0] * self.direction
            else:
                self.ball.y += speed[1] * self.direction * self.yDirection
                xMovement = False
            if self.ball.x <= 0 or self.ball.x >= 800:
                self.angle = self.swap[self.angle]
                if self.ball.x <= 0:
                    self.ball.x = 1
                else:
                    self.ball.x = 799
            if self.ball.y <= 0:
                self.ball.y = 1
                self.yDirection *= -1

            for paddle in self.paddle:
                if paddle[0].colliderect(self.ball):
                    self.angle = paddle[1]
                    self.direction = -1
                    self.yDirection = -1
                    break
            check = self.ball.collidelist(self.blocks)
            if check != -1:
                block = self.blocks.pop(check)
                if xMovement:
                    self.direction *= -1
                self.yDirection *= -1
                self.score += 1
            if self.ball.y > 600:
                self.createBlocks()
                self.score = 0
                self.ball.x = self.paddle[1][0].x
                self.ball.y = 490
                self.yDirection = self.direction = -1

    def paddleUpdate(self):

        pos = read_right.position(10) * 1000
        # pos = pygame.mouse.get_pos()
        on = 0
        for p in self.paddle:
            p[0].x = pos[0] + 20 * on
            on += 1

    def main(self):
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        self.createBlocks()
        global read_right
        read_right = read_paddle.PaddleMove('r')
        speed = 60
        while True:
            clock.tick(speed)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if read_paddle.switch_is_pressed() is True:
                while read_paddle.switch_is_pressed() is True:
                    time.sleep(0.1)
                time.sleep(0.1)
                menu_items = ['Quit', 'Continue', 'Ball Speed']
                event = menu(menu_items)
                if event == 'Quit':
                    pygame.quit()
                elif event == 'Continue':
                    pass
                elif event == 'Ball Speed':
                    options = {'Slow': 30, 'Fast': 60}
                    event = menu(list(options.keys()))
                    speed = options[event]

            self.screen.fill((0, 0, 0))
            self.paddleUpdate()
            self.ballUpdate()

            for block in self.blocks:
                pygame.draw.rect(self.screen, (255, 255, 255), block)
            for paddle in self.paddle:
                pygame.draw.rect(self.screen, (255, 255, 255), paddle[0])
            pygame.draw.rect(self.screen, (255, 255, 255), self.ball)
            self.screen.blit(self.font.render(str(self.score), -1, (255, 255, 255)), (400, 550))
            pygame.display.update()


if __name__ == "__main__":
    Breakout().main()
