import pygame
import sys
import os
import random
from random import randint
import math


pygame.init()
pygame.font.init()
pygame.mixer.init()

font = pygame.font.SysFont("gadugi",50)

screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#screen = pygame.display.set_mode((1236,564))
pygame.display.set_caption("Fishing Beats")

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255,0)
orange = (255, 165, 0)
dorange = (255, 64, 0)

sx, sy = pygame.display.get_window_size()
px = 0
def ImgLoad(image,num):
    image = image + ".png"
    if num == 1:#character
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (width,height))
    return imgS

score = 0
combo = 0
class fishM(pygame.sprite.Sprite):
    def __init__(self, lane, size, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        self.image = pygame.Surface([75,75])
        if size == 2:    
            self.image.fill(dorange)
        else:
            self.image.fill(orange)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [0,((lane*50) + (lane-1)*70 + 350)]
        self.size = size
        self.tap = 0
        self.lane = lane
        self.speed = speed
        self.comboL = False

    def update(self):
        global combo
        self.rect.x += self.speed
        if self.rect.x >= (sx - 320) and self.comboL == False:
            combo = 0
            self.comboL = True#combo lost
            
        if self.rect.x >= sx:
            self.kill()

    def disappear(self):
        global score
        global combo
        if self.rect.topright[0] >= sx - 325:
            if self.rect.x == (sx - 400):
                combo += 1
                score += 320*combo
                self.tap += 1
                

            elif self.rect.x <= (sx - 375):
                combo += 1
                score += 300 * combo
                self.tap += 1

            elif self.rect.x <= (sx - 350):
                combo += 1
                score += 200 * combo
                self.tap += 1

            elif self.rect.x <= (sx - 325):
                combo += 1
                score += 100 * combo
                self.tap += 1

        else:
            if self.rect.topright[0] <= (sx - 390):
                combo = 0
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 375):
                combo += 1
                score += 100 * combo
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 350):
                combo += 1
                score += 200 * combo
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 325):
                combo += 1
                score += 300 * combo
                self.tap += 1

        
            
        if self.size == self.tap:
            self.kill()


class fishMs(pygame.sprite.Sprite):
    def __init__(self, posx, lane, size, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        self.image = pygame.Surface([75,75])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [posx,((lane*50) + (lane-1)*70 + 350)]
        self.size = size
        self.tap = 0
        self.lane = lane
        self.speed = speed
        self.comboL = False

    def update(self):
        global combo
        self.rect.x += self.speed
        if self.rect.x >= (sx - 320) and self.comboL == False:
            combo = 0
            self.comboL = True#combo lost
            
        if self.rect.x >= sx:
            self.kill()

    def disappear(self):
        global score
        global combo
        if self.rect.topright[0] >= sx - 325:
            if self.rect.x == (sx - 400):
                combo += 1
                score += 320*combo
                self.tap += 1

            elif self.rect.x <= (sx - 375):
                combo += 1
                score += 300 * combo
                self.tap += 1

            elif self.rect.x <= (sx - 350):
                combo += 1
                score += 200 * combo
                self.tap += 1

            elif self.rect.x <= (sx - 325):
                combo += 1
                score += 100 * combo
                self.tap += 1

        else:
            if self.rect.topright[0] <= (sx - 390):
                combo = 0
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 375):
                combo += 1
                score += 100 * combo
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 350):
                combo += 1
                score += 200 * combo
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 325):
                combo += 1
                score += 300 * combo
                self.tap += 1

        
            
        if self.size == self.tap:
            self.kill()
            
class fishG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        for sprite in self:
            sprite.update()
            

buffer = 0
zd = "False"
class FishingPole(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.image = pygame.Surface([75,75])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [sx - 400,((lane*50) + (lane-1)*70 + 350)]
        self.lane = lane
        self.buffer = 0
        self.disable1 = False
        self.disable2 = False

    def movement(self):
        global buffer
        global px

        if buffer <= 0:
            if not(keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
                if keys[pygame.K_RIGHT]:
                    if self.lane != 1:
                        self.lane -= 1
                        buffer = 20

                if keys[pygame.K_LEFT]:
                    if self.lane != 3:
                        self.lane += 1
                        buffer = 20

            self.rect.x,self.rect.y = [sx - 400,((self.lane*50) + (self.lane-1)*70 + 350)]
            
        else:
            buffer -= 1

            

    def click(self):
        global zd
        if keys[pygame.K_w]:
            if pygame.sprite.spritecollide(FishingP, fish_group, False) and self.disable1 == False:
                for sprite in pygame.sprite.spritecollide(FishingP, fish_group, False):
                    sprite.disappear()
                    self.disable1 = True
                    zd = "True"
        elif not(keys[pygame.K_w]):
            self.disable1 = False
            zd = "False"

        if keys[pygame.K_e]:
            if pygame.sprite.spritecollide(FishingP, fish_group, False) and self.disable2 == False:
                for sprite in pygame.sprite.spritecollide(FishingP, fish_group, False):
                    sprite.disappear()
                    self.disable2 = True
                    zd = "True"
        elif not(keys[pygame.K_e]):
            self.disable2 = False
            zd = "False"
                    
                
            
        
class FishPole(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def movement(self):
        for sprite in self:
            sprite.movement()

    def click(self):
        for sprite in self:
            sprite.click()

Pole = FishPole()
FishingP = FishingPole(2)
Pole.add(FishingP)

     
fish_group = fishG()
'''
fish = fishMs(0, 1, 1, 10)#lane, size 1 or 2, speed
fish2 = fishMs(-800, 2, 1, 10)
fish3 = fishMs(-1600, 3, 1, 10)
fish4 = fishMs(-2400, 3, 1, 10)
fish_group.add(fish)
fish_group.add(fish2)
fish_group.add(fish3)
fish_group.add(fish4)

idk = pygame.Rect((sx - 405), 400, 15, 75)
idk2 = pygame.Rect((sx - 400), 400, 25, 75)
idk3 = pygame.Rect((sx - 375), 400, 25, 75)
idk4 = pygame.Rect((sx - 350), 400, 25, 75)
pygame.draw.rect(screen,white,idk)
pygame.draw.rect(screen,green,idk2)
pygame.draw.rect(screen,blue,idk3)
pygame.draw.rect(screen,red,idk4)
'''
espeed = 3

def check():
    for sprite in fish_group:
        if sprite.rect.topleft[0] < 300:
            return True
def newf():
    fish = fishM(randint(1,3),randint(1,2), espeed)
    fish_group.add(fish)
    
def endless():
    if len(fish_group) < 4:
        c = check()
        if c != True:
            newf()
        
        

    
def screenDraw():
    scoreDis = font.render(str(score),True,white)
    za = font.render(zd,True,white)
    sp = font.render(("speed = " + str(espeed)),True,white)
    comboDis = font.render("x"+str(combo),True,white)
    screen.fill(black)
    
    screen.blit(scoreDis, (0,0))
    screen.blit(comboDis, (0,100))
    screen.blit(za, (0,200))
    screen.blit(sp, (200,0))
    fish_group.draw(screen)
    Pole.draw(screen)
    
    pygame.display.update()
    

    

clock = pygame.time.Clock()
main = True

#def MapMaker():
    
inputbuffer = 0   

while main:
    
    run = True
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                main = False
                pygame.quit()

        if inputbuffer <= 0:
            if keys[pygame.K_o]:
                espeed += 1
                inputbuffer = 40
            elif keys[pygame.K_p]:
                if (espeed - 1) != 0:
                    espeed -= 1
                    inputbuffer = 40
        else:
            inputbuffer -= 1
                
        fish_group.update()
        Pole.movement()
        Pole.click()
        endless()
        screenDraw()
        
        clock.tick(120)
