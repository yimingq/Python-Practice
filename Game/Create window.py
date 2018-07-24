# -*- coding:utf-8 -*-

import pygame
import time
import random

from pygame.locals import *

class basePlane(object):
    def __init__(self,temp,x,y,load):
        self.x=x
        self.y=y
        self.planeimage = pygame.image.load(load)
        self.screen = temp
        self.allbullet=[]

    def display(self):
        self.screen.blit(self.planeimage,(self.x,self.y))


    # fire
        for bullet in self.allbullet:
            bullet.display()
            bullet.move()
            if bullet.y<-5 or bullet.y>840:
                self.allbullet.remove(bullet)

    def fire(self):
        pass
    def move(self):
        pass

class plane(basePlane):
    def __init__(self,temp):
        basePlane.__init__(self,temp,210,700,"./feiji/hero1.png")

    def move_left(self):
        self.x-=5
    def move_right(self):
        self.x+=5
    def move_up(self):
        self.y-=5
    def move_down(self):
        self.y+=5

    def fire(self):
        self.allbullet.append(bullet(self.screen,self.x,self.y))

class enemy(basePlane):
    def __init__(self, temp):
        basePlane.__init__(self, temp, 200, 0, "./feiji/enemy0.png")
        self.flag = True

    def fire(self):
        ranin = random.randint(0, 15)
        if ranin == 5:
            self.allbullet.append(enemybullet(self.screen, self.x, self.y))

    def move(self):
        if self.x > 430:
            self.flag = False
        if self.x < 0:
            self.flag = True
        if self.flag:
            self.x += 5
        else:
            self.x -= 5

class baseBullet(object):
    def __init__(self,temp,x,y,load):
        self.screen=temp
        self.x =x
        self.y =y
        self.bulletimage=pygame.image.load(load)

    def display(self):
        self.screen.blit(self.bulletimage,(self.x,self.y))

    def move(self):
        self.y-=10

class bullet(baseBullet):
    def __init__(self,temp,x,y):
        baseBullet.__init__(self,temp,x+40,y-20,"./feiji/bullet.png")
    def move(self):
        self.y-=10

class enemybullet(baseBullet):
    def __init__(self,temp,x,y):
        baseBullet.__init__(self, temp, x+20, y+20, "./feiji/bullet1.png")
    def move(self):
        self.y+=10


def keyboard(plane):
    for event in pygame.event.get():
        # quit botton
        if event.type == QUIT:
            print("exit")
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                plane.move_left()
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                plane.move_right()
            elif event.key == K_w or event.key == K_UP:
                print('up')
                plane.move_up()
            elif event.key == K_s or event.key == K_DOWN:
                print('down')
                plane.move_down()
            elif event.key == K_SPACE:
                print ('space')
                plane.fire()

def main():
    # create window
    screen = pygame.display.set_mode((480, 852), 0, 32)

    # create backgroud image
    backgroud = pygame.image.load("./feiji/background.png")

    # create plane
    plane1 = plane(screen)
    enemy1 = enemy(screen)

    fla=0
    while True:
        # image display
        screen.blit(backgroud,(0,0))

        # plane move

        # screen.blit(plane1.planeimage,(plane1.x,plane1.y))
        plane1.display()

        enemy1.display()
        enemy1.move()
        enemy1.fire()

        pygame.display.update()

        # get keyboard event
        keyboard(plane1)

        # # create quit event
        # event = pygame.event.poll()
        # if event.type == pygame.QUIT:
        #     pygame.quit()
        #     exit()

        time.sleep(0.01)

if __name__ == "__main__":
    main()