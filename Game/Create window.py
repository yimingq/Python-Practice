# -*- coding:utf-8 -*-

import pygame
import time

from pygame.locals import *

def main():
    # create window
    screen = pygame.display.set_mode((480, 852), 0, 32)

    # create backgroud image
    backgroud = pygame.image.load("./feiji/background.png")

    # create plane
    plane = pygame.image.load("./feiji/hero1.png")
    x = 210
    y = 700


    while True:
        # image display
        screen.blit(backgroud,(0,0))

        # plane move
        screen.blit(plane,(x,y))

        pygame.display.update()

        # get keyboard event
        for event in pygame.event.get():
        # quit botton
            if event.type == QUIT:
                print("exit")
                exit()
            elif event.type ==KEYDOWN:
                if event.key == K_a or event.key ==K_LEFT:
                   print('left')
                   x-=5

                elif event.key == K_d or event.key == K_RIGHT:
                    print('right')
                    x+=5
                elif event.key == K_w or event.key == K_UP:
                    print('right')
                    y-=5
                elif event.key == K_s or event.key == K_DOWN:
                    print('right')
                    y+=5
                elif event.key == K_SPACE:
                    print ('space')


        # # create quit event
        # event = pygame.event.poll()
        # if event.type == pygame.QUIT:
        #     pygame.quit()
        #     exit()

        time.sleep(0.01)

if __name__ == "__main__":
    main()