import pygame
from pygame import mixer
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

mixer.music.load("Creo-Dimension.mp3")
mixer.music.set_volume(0.5)

sx, sy = pygame.display.get_window_size()#1536 ,864
px = 0
def ImgLoad(image,num):
    image = image + ".png"
    if num == 1:#things
        imgS = pygame.image.load(os.path.join('../Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (width,height))
    elif num == 2:#stuff
        imgS = pygame.image.load(os.path.join('../Assets', image)).convert_alpha()
    return imgS
MMSlider = ImgLoad("Map_Maker_Slider",2)
MMSP = ImgLoad("MMSliderPart",2)
score = 0
combo = 0

class MMfishM(pygame.sprite.Sprite):
    def __init__(self, posx, lane, size, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        self.image = pygame.Surface([75,75])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [posx,((lane*50) + (lane-1)*70 + 400)]
        self.size = size
        self.posx = posx
        self.lane = lane
        self.speed = speed

    def update(self):
        global combo
        self.rect.x += self.speed
        
    def move(self):
        dist = self.rect.x - self.posx
        if MMMovet == 0:
            ratio = 0
        else:
            ratio = dist/MMMovet
        change = ratio * (MMMove - MMMovet)
        self.rect.x = self.rect.x + change
        
class MMTfish(pygame.sprite.Sprite):
    def __init__(self, posx, lane, size, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        self.image = pygame.Surface([75,75])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [posx,((lane*50) + (lane-1)*70 + 400)]
        self.size = size
        self.posx = posx
        self.lane = lane
        self.speed = speed

    def update(self):
        global combo
        pygame.time.set_timer()
        self.rect.x += self.speed
     
        

        


class MMeelM(pygame.sprite.Sprite):
    def __init__(self, posx, lane, length, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        
        if length < 100:
            self.image = pygame.Surface([100,75])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = [(-100),((lane*50) + (lane-1)*70 + 400)]
            self.length = 100
        else:
            self.image = pygame.Surface([length,75])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = [(-length),((lane*50) + (lane-1)*70 + 400)]
            self.length = length
        self.lane = lane
        self.speed = speed
        self.comboL = False
        self.SBuffer = 0

    def update(self):
        global combo#change this ty
        self.rect.x += self.speed
            
        if self.rect.x >= sx:
            self.kill()


class fishMG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        for sprite in self:
            sprite.update()

    def move(self):
        for sprite in self:
            sprite.move()

MMfish_group = fishMG()
            
class eelM(pygame.sprite.Sprite):
    def __init__(self, lane, length, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        
        if length < 100:
            self.image = pygame.Surface([100,75])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = [(-100),((lane*50) + (lane-1)*70 + 400)]
            self.length = 100
        else:
            self.image = pygame.Surface([length,75])
            self.image.fill(white)
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = [(-length),((lane*50) + (lane-1)*70 + 400)]
            self.length = length
        self.lane = lane
        self.speed = speed
        self.comboL = False
        self.SBuffer = 0

    def update(self):
        global combo#change this ty
        self.rect.x += self.speed
        if self.rect.x >= (sx - 320) and self.comboL == False:
            combo = 0
            self.comboL = True#combo lost
            
        if self.rect.x >= sx:
            self.kill()

    def disappear(self):
        global score
        global combo
        if keys[pygame.K_q] or keys[pygame.K_w]:
            if self.SBuffer <= 0:
                combo += 1
                score += 100*combo
                
                self.SBuffer = round(75/self.speed)
            else:
                self.SBuffer -= 1
                
            if self.rect.x >= (sx-400):
                self.kill()
            

    def echeck(self):
        return True
            

class fishM(pygame.sprite.Sprite):
    def __init__(self, lane, size, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        self.image = pygame.Surface([75,75])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [0,((lane*50) + (lane-1)*70 + 400)]
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
    def echeck(self):
        return False

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
        self.rect.x,self.rect.y = [sx - 400,((lane*50) + (lane-1)*70 + 400)]
        self.lane = lane
        self.buffer = 0
        self.disable1 = False
        self.disable2 = False

    def movement(self):
        global buffer
        global px

        if buffer <= 0:
            if not(keys[pygame.K_UP] and keys[pygame.K_DOWN]):
                if keys[pygame.K_UP]:
                    if self.lane != 1:
                        self.lane -= 1
                        buffer = 12

                if keys[pygame.K_DOWN]:
                    if self.lane != 3:
                        self.lane += 1
                        buffer = 12

            self.rect.x,self.rect.y = [sx - 400,((self.lane*50) + (self.lane-1)*70 + 400)]
            
        else:
            buffer -= 1

            

    def click(self):
        global zd
        if keys[pygame.K_q]:
            if pygame.sprite.spritecollide(FishingP, fish_group, False) and self.disable1 == False:
                for sprite in pygame.sprite.spritecollide(FishingP, fish_group, False):
                    ec = sprite.echeck()
                    if ec == False:
                        self.disable1 = True
                        zd = "True"
                    sprite.disappear()
        elif not(keys[pygame.K_q]):
            self.disable1 = False
            zd = "False"

        if keys[pygame.K_w]:
            if pygame.sprite.spritecollide(FishingP, fish_group, False) and self.disable2 == False:
                for sprite in pygame.sprite.spritecollide(FishingP, fish_group, False):
                    ec = sprite.echeck()
                    if ec == False:
                        self.disable2 = True
                        zd = "True"
                    if not(keys[pygame.K_w] and keys[pygame.K_q]) or (ec == False):
                        sprite.disappear()
        elif not(keys[pygame.K_w]):
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
#fish = fishM(1,1, 1)#lane, size 1 or 2, speed
#fish2 = fishM(2,1, 2)
#fish3 = fishM(3,1,3)
#fish4 = fishM(3,2, 8)
e = eelM(3,300, 2)
print(e)
#fish_group.add(fish)
#fish_group.add(fish2)
#fish_group.add(fish3)
#fish_group.add(fish4)
fish_group.add(e)
'''
idk = pygame.Rect((sx - 405), 400, 15, 75)
idk2 = pygame.Rect((sx - 400), 400, 25, 75)
idk3 = pygame.Rect((sx - 375), 400, 25, 75)
idk4 = pygame.Rect((sx - 350), 400, 25, 75)
pygame.draw.rect(screen,white,idk)
pygame.draw.rect(screen,green,idk2)
pygame.draw.rect(screen,blue,idk3)
pygame.draw.rect(screen,red,idk4)
'''
MMMove = 0
hold = False
pos = 0
def mmslider(spr):#map maker slider
    global MMMove
    global hold
    global pos
    mx,my = pygame.mouse.get_pos()
    if pygame.mixer.music.get_busy() == False or hold == True:
        if mos.colliderect(spr) and pygame.mouse.get_pressed()[0]:
            if not(sx-45 - (sx-45-mx) >= 1491) and not(sx-45 - (sx-45-mx)<= 6):
                MMMove = sx-45-mx
                hold = True
        if pygame.mouse.get_pressed()[0] and hold == True:
            if not(sx-45 - (sx-45-mx) >= 1491) and not(sx-45 - (sx-45-mx)<= 6):
                MMMove = sx-45-mx
            else:
                if mx > 500:
                    MMMove = 0
                elif mx < 500:
                    MMMove = sx - 51 
        else:
            hold = False

        pos = (MMMove * SongLength2 * 1000)/1491

        
            
        
    
    elif pygame.mixer.music.get_busy() == True and hold == False:
        if (1491 * (((pygame.mixer.music.get_pos() - original + pos)/1000)/SongLength2)) < 1485:       
            MMMove =(1491 * (((pygame.mixer.music.get_pos() - original + pos)/1000)/SongLength2))
        else:
            MMMove = 1485

        


    
        
    

def screenDraw():
    screen.fill(black)
    if mapmake == False:
        scoreDis = font.render(str(score),True,white)
        za = font.render(zd,True,white)
        comboDis = font.render("x"+str(combo),True,white)       
        
        screen.blit(scoreDis, (0,0))
        screen.blit(comboDis, (0,100))
        screen.blit(za, (0,200))
        fish_group.draw(screen)
        Pole.draw(screen)
        
    elif mapmake == True:
        screen.blit(MMSlider, (0,376.5))
        screen.blit(MMSP, (sx -45 - MMMove,382.5))
        spr = pygame.Rect(sx-45-MMMove, 382.5,39,39)
        mmslider(spr)#1524 space 192 second song 4 fish 300 pixels MMMove_max = 1485
        
        
        MMfish_group.draw(screen)
        

        
        
        
        
        
        
    
    pygame.display.update()
    

    

clock = pygame.time.Clock()
main = True
SongLength2 = 0
hold2 = False
lc = False#when the map maker starts
def MapMaker(song):
    global lc
    global SongLength2
    global hold2
    
    if lc == False:
        song = song + ".mp3"
        l = pygame.mixer.Sound(song)
        SongLength = round(l.get_length())#192
        SongLength2 = l.get_length()
        lc = True
        mixer.music.load(song)
        mixer.music.set_volume(0.5)
        mixer.music.play()
        mixer.music.pause()
        
    if lc == True:
        lane1 = pygame.Rect(0, 427.5, sx, 120)
        lane2 = pygame.Rect(0, 547.5, sx, 120)
        lane3 = pygame.Rect(0, 667.5, sx, 120)
        if pygame.mouse.get_pressed()[0] and hold2 == False:
            if mos.colliderect(lane1):
                fish = MMfishM(mx, 1, 1, 2)
                MMfish_group.add(fish)
                
            elif mos.colliderect(lane2):   
                fish = MMfishM(mx, 2, 1, 2)
                MMfish_group.add(fish)
                
            elif mos.colliderect(lane3):
                fish = MMfishM(mx, 3, 1, 2)
                MMfish_group.add(fish)
                
            hold2 = True
        elif not(pygame.mouse.get_pressed()[0]):
            hold2 = False

        if pygame.mixer.music.get_busy() == True:
            MMfish_group.update()
            

    
    
    

   
    
    
mapmake = True
mbuffer = 0
original = pygame.mixer.music.get_pos()
MMMovet = 0
while main:
    
    run = True
    
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False
                main = False
                pygame.quit()
                
        mx,my = pygame.mouse.get_pos()
        mos = pygame.Rect(mx,my,15,15)
        
        if mbuffer <= 0:
            if keys[pygame.K_p] and pygame.mixer.music.get_busy() == True:
                mixer.music.pause()
                original = pygame.mixer.music.get_pos()
                mbuffer = 40
                MMMovet = MMMove
            elif keys[pygame.K_p] and pygame.mixer.music.get_busy() == False:
                mixer.music.rewind()
                MMfish_group.move()
                try:
                    mixer.music.set_pos((pos/1000))
                except pygame.error:
                    mixer.music.play()
                    pos = 0
                    original = pygame.mixer.music.get_pos()
                
                mixer.music.unpause()
                
                mbuffer = 40
        else:
            mbuffer -= 1
        
        if mapmake == False:
            fish_group.update()
            Pole.movement()
            Pole.click()
        else:
            MapMaker("Creo-Dimension")
            
        screenDraw()
        
        clock.tick(60)
