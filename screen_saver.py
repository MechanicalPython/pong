#! /usr/bin/env python3

import pygame
import pygame.freetype
import sys
import time
import os
from math import *
import read_paddle


def move_pong(x, y, angle):
    speed = 10
    x += int(speed * cos(radians(angle)))
    y += int(speed * sin(radians(angle)))

    if x + img_x >= width:  # hit right side
        angle = 180 - angle
    if x <= 0:  # hit left side
        angle = 180 - angle
    if y < 0:   # hit top
        angle = - angle
    if y + img_y >= height:  # hit bottom
        angle = - angle

    display.blit(pong_img, (x, y))
    return x, y, angle


def screensaver():
    pygame.init()
    global display, width, height

    width = 1920
    height = 1080
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("ScreenSaver")
    clock = pygame.time.Clock()

    black = (0, 0, 0)
    white = (236, 240, 241)
    d = os.path.dirname(__file__)
    global img_x, img_y, pong_img
    pong_img = pygame.image.load(f'{d}/splash.png')  # x, y = (800, 400)
    img_x , img_y = pong_img.get_size()
    x, y, angle = 0, 0, 45
    pressed = False
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_0:
                    cont = False

        if read_paddle.auto is False:
            if read_paddle.switch_is_pressed():
                time.sleep(0.1)
                cont = False
        display.fill(black)

        x, y, angle = move_pong(x, y, angle)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    screensaver()

