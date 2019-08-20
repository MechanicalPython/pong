#! /usr/bin/python3


import pygame
import pygame.freetype
import sys
import read_paddle


pygame.init()

width = 900
height = 1000

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()

background = (0, 0, 0)
white = (236, 240, 241)
gray = (128, 128, 128)
font = pygame.freetype.Font('SF Atarian System Extended Bold.ttf', 60)


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
    pygame.event.set_allowed([pygame.KEYDOWN])
    pygame.mouse.set_visible(False)
    display.set_alpha(None)
    read_left = read_paddle.PaddleMove('l')
    read_right = read_paddle.PaddleMove('r')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        display.fill(background)

        dot = Dot(110)
        pos = read_left.position()
        start = 100
        for item in menu_items:
            font.render_to(display, (width / 2, start), item, white)
            start += 100

        if pos < 0.5:
            dot.move(110)
            return 'Quit'
            # if read_paddle.switch_is_pressed():
            #     return
        elif 0.5 < pos:
            dot.move(210)
            return 'Reset'
            # if read_paddle.switch_is_pressed():
            #     reset()

        dot.show_dot()
        pygame.display.update()
        clock.tick(30)

