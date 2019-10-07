#! /usr/bin/env python3

# Pong
# Language - Python
# Modules - pygame, sys, random, math
#
import pygame
import pygame.freetype
import sys
import time
import os
import read_paddle as read_paddle

pygame.mixer.init(22100, -16, 2, 2**7)
pygame.init()

width = 900
height = 1000

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()

background = (0, 0, 0)
white = (236, 240, 241)
gray = (128, 128, 128)

d = os.path.dirname(__file__)
font = pygame.freetype.Font(f'{d}/SF Atarian System Extended Bold.ttf', 60)


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
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()

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


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

        while read_paddle.switch_is_pressed() is True:
            time.sleep(0.1)
        time.sleep(0.1)
        menu_items = ['Pong', 'Breakout', 'Quit']
        event = menu(menu_items)
        if event == 'Pong':
            import pong2
            pong2.board()
        elif event == 'Breakout':
            import breakout
            breakout.Breakout().main()
        elif event == 'Quit':
            sys.exit()


if __name__ == '__main__':
    main()
