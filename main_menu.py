#! /usr/bin/env python3

# Pong
# Language - Python
# Modules - pygame, sys, random, math
# Splash screen at /usr/share/plymouth/themes/pix/splash.png
# Test commit
import pygame
import pygame.freetype
import sys
import time
import os
import read_paddle as read_paddle

pygame.mixer.init(22100, -16, 2, 2**7)
pygame.init()
pygame.mouse.set_visible(False)

width = 1920
height = 1080

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (236, 240, 241)
gray = (128, 128, 128)

d = os.path.dirname(__file__)
font = pygame.freetype.Font(f'{d}/SF Atarian System Extended Bold.ttf', 60)


class Dot:
    def __init__(self, x, y):
        self.x = x
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
    background = pygame.image.load(f'{d}/background_image.png')
    pressed = False
    pos = 0.2
    start_time = time.time()
    while True:
        if time.time() > start_time + 5*60:
            import screen_saver
            screen_saver.screensaver()
            start_time = time.time()
            time.sleep(0.2)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_0:
                    pressed = True
                if event.key == pygame.K_1:
                    pos = 0.2
                if event.key == pygame.K_2:
                    pos = 0.4
                if event.key == pygame.K_3:
                    pos = 0.6
                if event.key == pygame.K_4:
                    pos = 0.9
        if read_paddle.auto is False:
            if read_paddle.switch_is_pressed():
                pressed = True

        display.blit(background, [0, 0])

        dot = Dot(100, 250)
        if read_paddle.auto is False:
            pos = read_left.position()

        item_x = 150
        item_y = 250
        item_number = 0
        for item in menu_items:
            font.render_to(display, (item_x, item_y), item, white)
            if item_number/len(menu_items) < pos <= (item_number+1)/len(menu_items):
                dot.move(item_y + 10)
                if pressed:
                    time.sleep(0.5)
                    return menu_items[item_number]
            item_y += 100
            item_number += 1

        dot.show_dot()
        pygame.display.flip()
        clock.tick(30)


def main():
    while True:
        pygame.display.set_mode((width, height))
        menu_items = ['Pong', 'Reboot', 'Quit']
        event = menu(menu_items)
        if event == 'Pong':
            import pong2
            pong2.board()
        elif event == 'Update':
            if read_paddle.auto is True:
                print('Well done')
                sys.exit()
            else:
                os.system('sudo reboot')
                sys.exit()
        elif event == 'Breakout':
            import breakout
            breakout.Breakout().main()

        elif event == 'Quit':
            sys.exit()


if __name__ == '__main__':
    main()
