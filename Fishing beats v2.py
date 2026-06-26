import base64
import time
import pygame
from pygame import mixer
import sys
import os
import struct
import time
import threading
import socket
import json
import random
import shutil

pygame.init()

try:
    pygame.mixer.init()
except pygame.error as e:
    pygame.mixer.quit()
    os.environ["SDL_AUDIODRIVER"] = "directsound"
    pygame.mixer.init()

pygame.font.init()
smallfont = pygame.font.SysFont("gadugi",30)
font = pygame.font.SysFont("gadugi",50)
bigfont = pygame.font.SysFont("gadugi",90)

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
blue2 = (111,187, 211)
selectedc = (16, 210, 224)
unselectedc = (2, 61, 87)

sx, sy = pygame.display.get_window_size()#1536 ,864

#sx, sy = 1536 ,864
resizex, resizey = sx/1536, sy/864
w = 0#mmmove * w = movement
px = 0

mapsList = os.listdir("Maps")

def ImgLoad(image,num):
    image = image + ".png"
    if num == 1:#things
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (180,75))
    elif num == 2:#stuff
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
    elif num == 3:#map buttons
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (600,75))
    elif num == 4:#50,50
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (50,50))
    return imgS

MMSlider = ImgLoad("Map_Maker_Slider",2)
MMSP = ImgLoad("MMSliderPart",2)
fishimg = ImgLoad("fish",2)
fishimg2 = ImgLoad("fish2",2)
fba = ImgLoad("fishbutton_active",2)
fbi = ImgLoad("fishbutton_inactive",2)
eba = ImgLoad("eelbutton_active",2)
ebi = ImgLoad("eelbutton_inactive",2)
eelfront = ImgLoad("eel_front",2)
eelmid = ImgLoad("eel_mid",2)
eelmid2 = ImgLoad("eel_mid2",2)
eelmid3 = ImgLoad("eel_mid3",2)
eelback = ImgLoad("eel_back",2)
feelimg = ImgLoad("eel",1)
box = ImgLoad("box",3)
boxs = ImgLoad("box_selected",3)
box2 = ImgLoad("box2",3)
box2s = ImgLoad("box2_selected",3)
lock_on = ImgLoad("Lock_on",2)
lock_off = ImgLoad("Lock_off",2)
playbut = ImgLoad("playbutton",4)
pausebut = ImgLoad("pause",4)
bin1 = ImgLoad("bin",2)
bin2 = ImgLoad("bin2",2)
PMenu = ImgLoad("PauseMenu",2)
exitimg = ImgLoad("ExitButton",2)
Pbutton = ImgLoad("Play_button",2)
MMbutton = ImgLoad("mapmakebutton",2)
Setbutton = ImgLoad("SettingsButton",2)
MenuExitbutton = ImgLoad("Menu_Exit",2)
backimg = ImgLoad("Backbutton",2)
resumeImg = ImgLoad("Resume", 2)
RetryImg = ImgLoad("Retry", 2)
ExitImg = ImgLoad("Exit", 2)
SaveImg = ImgLoad("Save", 2)
SaveExitImg = ImgLoad("SaveExit", 2)

SpeedAddimg = ImgLoad("SpeedAdd", 2)
SpeedSubimg = ImgLoad("SpeedMinus", 2)
LoadImg = ImgLoad("LoadButton", 2)
EnterImg = ImgLoad("EnterButton", 2)

PlayerDis = ImgLoad("PlayerDisplay", 2)
ReadyPlayerDis = ImgLoad("ReadyPlayerDisplay", 2)
MissingPlayerDis = ImgLoad("PlayerDisplayNoMap", 2)
ReadyUpButton = ImgLoad("ReadyButton", 2)
DisabledReadyUpButton = ImgLoad("DisabledReadyButton", 2)
UnreadyUpButton = ImgLoad("UnreadyButton", 2)
CrownDis = ImgLoad("Crown", 2)
CreateRoomButton = ImgLoad("CreateRoomButton", 2)


class text():
    def __init__(self, txt, posx, posy):
        self.text = font.render(txt,True,white)
        self.surf = pygame.Surface(self.text.get_size()).convert_alpha()
        self.alpha = 255
        self.surf.fill((255, 255, 255, self.alpha))
        self.text.blit(self.surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.txt = txt
        self.posx = posx
        self.posy = posy


    def alphachange(self):
        if self.alpha > 0:
            self.alpha -= 0.5
        self.surf = pygame.Surface(self.text.get_size()).convert_alpha()
        self.surf.fill((255, 255, 255, self.alpha))
        self.text.blit(self.surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def delete(self):
        if self.alpha <= 0:
            self.kill()


score = 0
combo = 0
saver = 0
change = 0

class accuracyText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text = font.render("100.0%", True, white)
        self.total = 0
        self.playerAcc = 0
        self.acc = 100

    def update(self, change):
        self.total += 1
        self.playerAcc += change
        self.acc = (self.playerAcc/self.total)*100

    def display(self, x, y):
        if self.total != 0:
            self.text = font.render((str((self.playerAcc/self.total)*100))[:5] + "%", True, white)
        screen.blit(self.text, (x, y))

    def reset(self):
        self.total = 0
        self.playerAcc = 0
        self.text = font.render("100.0%", True, white)

    def returnAcc(self, other = False):
        if other:
            return str(self.acc)[:5] + "%"
        else:
            try:
                return (str((self.playerAcc/self.total)*100))[:5] + "%"
            except ZeroDivisionError:
                return str(self.acc) + "%"

    def setAcc(self, acc):
        self.acc = acc




Accuracy = accuracyText()

class hpb(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.Surface([500, 20])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [x,y]
        self.hpgain = 10
        self.dead = False
        self.died = False

    def hpchange(self, gain):
        if not self.dead or menu == "playing multiplayer":
            if (self.rect.width + gain*self.hpgain) >= 500:
                self.rect.width = 500
                if self.dead and menu == "playing multiplayer":
                    self.dead = False
                    sendBigData(b'ALIVE')

            elif (self.rect.width + gain*self.hpgain) <= 0:
                self.rect.width = 0
            else:
                self.rect.width += gain*self.hpgain

        if self.rect.width <= 0 and self.dead == False:
            self.dead = True
            if menu == "playing multiplayer":
                sendBigData(b'DEAD')
                self.died = True

    def rectdraw(self):
        pygame.draw.rect(screen, white, self.rect)

class hpbargroup(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def hpchange(self,gain):
        for sprite in self:
            sprite.hpchange(gain)

    def rectdraw(self):
        for sprite in self:
            sprite.rectdraw()

    def check(self, died = False):
        for sprite in self:
            if died:
                return sprite.died
            else:
                if sprite.rect.width == 0:
                    return True
                else:
                    return False

hpbar = hpbargroup()

missnum = 0
latenum = 0
earlynum = 0
hitnum = 0




######################### Fish Functions ######################################
#map maker
class MMfishM(pygame.sprite.Sprite):
    def __init__(self, posx, lane, size, speed,test):#position,if it can shoot and what kind of enemy
        super().__init__()

        if test == False:
            if size == 1:
                self.image = fishimg
            elif size == 2:
                self.image = fishimg2
        else:
            self.image = pygame.Surface([75,75])


        self.rect = self.image.get_rect()
        if lockon == False:
            self.rect.x,self.rect.y = [posx,((lane*50) + (lane-1)*70 + 400)]
            self.posx = posx
        else:
            self.rect.x,self.rect.y = [sx - 400,((lane*50) + (lane-1)*70 + 400)]
            self.posx = sx - 400

        self.size = size
        self.lane = lane
        self.speed = speed
        self.test = test
        self.Mov3 = MMMove

        xs = pygame.sprite.spritecollide(self, MMfish_group, False)
        for count in xs:
            try:
                if count.test == False:
                    count.kill()
            except AttributeError:
                count.kill()
        if test == False:
            self.w = rewinder()
            if self.w > 1536 or self.w > self.rect.x:
                self.ini = self.w*-1 + self.posx#position of test fish
            else:
                if self.w == 0:
                    self.ini = self.posx
                else:
                    self.ini = self.rect.x-self.w
        else:
            self.ini = self.posx





    def update(self):
        global combo
        self.rect.x += self.speed

    def move(self):#slider move
        global change
        if self.test == True:
            dist = self.rect.x - self.posx
            if MMMovet == 0:
                ratio = 0
            else:
                ratio = dist/MMMovet

            change = ratio * (MMMove - MMMovet)



        self.rect.x = self.rect.x + change

    def check(self):
        global saver
        if self.test == True:
            saver = self.rect.x



    def btStart(self):
        self.rect.x = self.ini

    def reset(self):
        if self.test == False:
            testpos = rewinder()
            self.rect.x = self.ini+testpos
        else:
            self.rect.x = w*MMMove



    def delete(self):
        if self.test == False:
            if mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and mode == "Delete":
                self.kill()

    def tapmove(self,direct):#left and right
        self.rect.x += direct*w*10

    def filewrite(self):
        global FishcountNum
        if self.test == False:
            p = "fish" +" "+ str(self.ini) +" "+ str(self.lane) +" "+ str(self.size) +" "+ str(self.speed) + "\n"
            smap.write(p)
            FishcountNum += 1

    def testplay(self):
        if self.test == False:
            if self.rect.x <= sx-475:
                fish = fishM(self.rect.x, self.lane, self.size, self.speed)
                fish_group.add(fish)

FishcountNum = 0
EelcountNum = 0
def rewinder():
    MMfish_group.check()
    ini = saver
    return ini

fl = 0
class MMTfish(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface([75,75])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [0,(450)]
        self.speed = speed

    def update(self):
        global fl
        global original
        global MMMove
        global MMMovet
        global EngineerFish
        global w
        global mode
        self.rect.x += self.speed
        if self.rect.x >= sx:
            fl = MMMove
            mixer.music.pause()
            original = pygame.mixer.music.get_pos()
            MMMovet = MMMove
            pos = (MMMove * SongLength2 * 1000)/1485
            mixer.music.rewind()
            try:
                mixer.music.set_pos(0)
            except pygame.error:
                mixer.music.play()
                pos = 0

                original = pygame.mixer.music.get_pos()
            MMMove = 0
            MMfish_group.move()
            calc()
            w = posList[0]/MMMoveList[0]
            Tfish2 = MMfishM(0,1,1,speed, True)
            MMfish_group.add(Tfish2)
            mode = "Fish"
            EngineerFish = True
            if loadmap == True:
                MapLoad(mapmakesong+".mp3", directoryStore)

            self.kill()

    def move(self):
        pass

    def delete(self):
        pass

    def filewrite(self):
        pass

    def reset(self):
        pass

    def check(self):
        pass








class MMeelM(pygame.sprite.Sprite):
    def __init__(self, posx, lane, length, speed):
        super().__init__()

        if length <= 180:
            self.image = feelimg
            self.rect = self.image.get_rect()
            if lockon == False:
                self.rect.x,self.rect.y = [(posx-180),((lane*50) + (lane-1)*70 + 400)]
            else:
                self.rect.x,self.rect.y = [(sx-400-180),((lane*50) + (lane-1)*70 + 400)]
            self.length = 180
        else:
            self.image = pygame.Surface([length,75])
            self.image.fill((224,231,245))
            self.image.set_colorkey((224,231,245))
            self.rect = self.image.get_rect()
            if (length - 146) % 34 == 0:
                num = (length - 146)//34
                self.image.blit(eelback,(0,0))
                for x in range(num):
                    self.image.blit(eelmid,((34*x)+78,0))
                self.image.blit(eelfront,(length-68,0))
            else:
                #self.image.fill(white)
                num = (length - 146)//34
                self.image.blit(eelback,(0,0))
                for x in range(num):
                    self.image.blit(eelmid,((34*x)+78,0))
                if ((length-68)-((34*num)+78)) >= 26:
                    self.image.blit(eelmid3, ((34 * num) + 78, 0))
                    self.image.blit(eelmid2, ((34 * num) + 104, 0))
                #self.image.blit(eelmid,((34*num)+78,0))
                self.image.blit(eelfront,(length-68,0))
            if lockon == False:
                self.rect.x,self.rect.y = [(posx-length),((lane*50) + (lane-1)*70 + 400)]
            else:
                self.rect.x,self.rect.y = [(sx - 400-length),((lane*50) + (lane-1)*70 + 400)]

            self.length = length
        xs = pygame.sprite.spritecollide(self, MMfish_group, False)
        for count in xs:
            try:
                if count.test == False:
                    count.kill()
            except AttributeError:
                count.kill()

        self.lane = lane
        self.speed = speed
        self.comboL = False
        self.SBuffer = 0
        self.w = rewinder()
        if lockon == False:
            self.pon = posx
        else:
            self.pon = sx - 400


        if self.w > 1536 or self.w > self.rect.x:
            self.ini = self.w*-1 + self.pon - length
        else:
            if self.w == 0:
                self.ini = self.pon - length
            else:
                self.ini = self.rect.x-self.w






    def update(self):
        global combo#change this ty
        self.rect.x += self.speed

    def move(self):
        self.rect.x = self.rect.x + change

    def delete(self):
        if mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and mode == "Delete":
            self.kill()

    def tapmove(self,direct):
        self.rect.x += direct*w*speed*5

    def btStart(self):
        self.rect.x = self.ini

    def reset(self):
        testpos = rewinder()
        self.rect.x = self.ini+testpos

    def check(self):
        pass

    def filewrite(self):
        global EelcountNum
        p = "eel" +" "+ str(self.ini) +" "+ str(self.lane) +" "+ str(self.length) +" "+ str(self.speed) + "\n"
        smap.write(p)
        EelcountNum += 1

    def testplay(self):
        eel = eelM(self.rect.x, self.lane, self.length, self.speed) #(pos, lane, length, speed):
        fish_group.add(eel)






class fishMG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        for sprite in self:
            sprite.update()

    def move(self):
        for sprite in self:
            sprite.move()

    def delete(self):
        for sprite in self:
            sprite.delete()

    def check(self):
        for sprite in self:
            sprite.check()

    def btStart(self):
        for sprite in self:
            sprite.btStart()

    def tapmove(self,direct):
        for sprite in self:
            sprite.tapmove(direct)

    def filewrite(self):
        for sprite in self:
            sprite.filewrite()

    def reset(self):
        for sprite in self:
            sprite.reset()

    def testplay(self):
        for sprite in self:
            sprite.testplay()


MMfish_group = fishMG()

#game
class eelM(pygame.sprite.Sprite):
    def __init__(self, pos, lane, length, speed):
        super().__init__()


        if length <= 180:
            self.image = feelimg
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = [(pos),((lane*50) + (lane-1)*70 + 400)]
            self.length = 180
        else:
            self.image = pygame.Surface([length,75])
            self.image.fill((224,231,245))
            self.image.set_colorkey((224,231,245))
            self.rect = self.image.get_rect()
            if (length - 146) % 34 == 0:
                num = (length - 146)//34
                self.image.blit(eelback,(0,0))
                for x in range(num):
                    self.image.blit(eelmid,((34*x)+78,0))
                self.image.blit(eelfront,(length-68,0))
            else:
                #self.image.fill(white)
                num = (length - 146)//34
                self.image.blit(eelback,(0,0))
                for x in range(num):
                    self.image.blit(eelmid,((34*x)+78,0))
                #self.image.blit(eelmid,((34*num)+78,0))
                self.image.blit(eelfront,(length-68,0))

            self.rect.x,self.rect.y = [(pos),((lane*50) + (lane-1)*70 + 400)]
            self.length = length

        self.lane = lane
        self.speed = speed
        self.comboL = False
        self.SBuffer = 0

    def update(self):
        global combo#change this when remaking ty
        self.rect.x += self.speed
        if self.rect.x >= (sx - 320) and self.comboL == False:
            combo = 0
            self.comboL = True#combo lost

        if menu == "playing multiplayer":
            playerGroup.setSelf()

        if self.rect.x >= sx:
            self.kill()

    def disappear(self):
        global score
        global combo
        if keys[pygame.K_q] or keys[pygame.K_w] or keys[pygame.K_SPACE]:
            if self.SBuffer <= 0:
                combo += 1
                score += 100*combo

                self.SBuffer = round(75/self.speed)
            else:
                self.SBuffer -= 1
            if menu == "playing multiplayer":
                playerGroup.setSelf()
            if self.rect.x >= (sx-400):
                self.kill()


    def echeck(self):
        return True

maxcombo = 0
class fishM(pygame.sprite.Sprite):
    def __init__(self, pos, lane, size, speed):#position,if it can shoot and what kind of enemy
        super().__init__()
        if size == 1:
            self.image = fishimg
        elif size == 2:
            self.image = fishimg2
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [pos,((lane*50) + (lane-1)*70 + 400)]
        self.size = size
        self.tap = 0
        self.lane = lane
        self.speed = speed
        self.comboL = False

    def update(self):
        global combo
        global missnum
        global maxcombo
        self.rect.x += self.speed

        if self.rect.x >= (sx - 320) and self.comboL == False:
            if (maxcombo < combo) and testingMap == False:
                maxcombo = combo
            combo = 0
            self.comboL = True#combo lost
            missnum += int(1) # concat str (not int) to str error?
            hpbar.hpchange(-2)
            Accuracy.update(0)

        if menu == "playing multiplayer":
            playerGroup.setSelf()

        if self.rect.x >= sx:
            self.kill()



    def disappear(self):
        global score
        global combo
        global hitnum
        global earlynum
        global latenum

        if self.rect.topright[0] >= sx - 325:
            if self.rect.x == (sx - 400):
                combo += 1
                score += 120*combo
                hitnum += 1
                self.tap += 1
                hpbar.hpchange(0.65)
                Accuracy.update(1)

            elif self.rect.x <= (sx - 375):
                combo += 1
                score += 100 * combo
                hitnum += 1
                self.tap += 1
                hpbar.hpchange(0.5)
                Accuracy.update(1)

            elif self.rect.x <= (sx - 350):
                combo += 1
                score += 75 * combo
                latenum += 1
                self.tap += 1
                hpbar.hpchange(0.35)
                Accuracy.update(0.75)

            elif self.rect.x <= (sx - 325):
                combo += 1
                score += 25 * combo
                latenum += 1
                self.tap += 1
                hpbar.hpchange(0.15)
                Accuracy.update(0.5)

        else:
            if self.rect.topright[0] <= (sx - 390):
                combo = 0
                earlynum += 1
                self.tap += 1
                hpbar.hpchange(-0.3)
                Accuracy.update(0.1)

            elif self.rect.topright[0] <= (sx - 375):
                combo += 1
                score += 25 * combo
                earlynum += 1
                self.tap += 1
                hpbar.hpchange(0.15)
                Accuracy.update(0.5)

            elif self.rect.topright[0] <= (sx - 350):
                combo += 1
                score += 75 * combo
                earlynum += 1
                self.tap += 1
                hpbar.hpchange(0.35)
                Accuracy.update(0.75)

            elif self.rect.topright[0] <= (sx - 325):
                combo += 1
                score += 100 * combo
                hitnum += 1
                self.tap += 1
                hpbar.hpchange(0.5)
                Accuracy.update(1)

        if menu == "playing multiplayer":
            playerGroup.setSelf()
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


def poscheck(self):
    return self.rect.x
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
        self.hold = False
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


    def reset(self):
        self.lane = 2
        self.buffer = 0
        self.disable1 = False
        self.hold = False
        self.disable2 = False

    def click(self):
        global zd
        if mapmake == False or testingMap == True:
            if keys[pygame.K_q] or keys[pygame.K_SPACE]:
                if pygame.sprite.spritecollide(FishingP, fish_group, False) and self.disable1 == False:
                    fishlist = pygame.sprite.spritecollide(FishingP, fish_group, False)
                    for sprite in fishlist:
                        ec = sprite.echeck()
                        if ec == False:
                            self.disable1 = True
                            zd = "True"
                            if len(fishlist) >= 2:
                                posfish = list(map(poscheck,fishlist))
                                fishlist[posfish.index(max(posfish))].disappear()
                                fishlist.remove(fishlist[posfish.index(max(posfish))])
                            else:
                                sprite.disappear()
                        else:
                            sprite.disappear()


            elif not(keys[pygame.K_q] or keys[pygame.K_SPACE]):
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


        else:#mapmaker
            if (keys[pygame.K_q] or keys[pygame.K_w]) and self.hold == False and exitmenu == False:
                if self.lane == 1:
                    if mode == "Fish":
                        fish = MMfishM(mx, 1, sizestore, speed, False)
                        MMfish_group.add(fish)
                    elif mode == "Eel":
                        eel = MMeelM(mx, 1, int(lengthstore), speed)
                        MMfish_group.add(eel)


                elif self.lane == 2:
                    if mode == "Fish":
                        fish = MMfishM(mx, 2, sizestore, speed, False)
                        MMfish_group.add(fish)
                    elif mode == "Eel":
                        eel = MMeelM(mx, 2, int(lengthstore), speed)
                        MMfish_group.add(eel)

                elif self.lane == 3:
                    if mode == "Fish":
                        fish = MMfishM(mx, 3, sizestore, speed, False)
                        MMfish_group.add(fish)
                    elif mode == "Eel":
                        eel = MMeelM(mx, 3, int(lengthstore), speed)
                        MMfish_group.add(eel)

                self.hold = True
            elif not(keys[pygame.K_q]) and not(keys[pygame.K_w]):
                self.hold = False





class FishPole(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def movement(self):
        for sprite in self:
            sprite.movement()

    def click(self):
        for sprite in self:
            sprite.click()

    def reset(self):
        for sprite in self:
            sprite.reset()

Pole = FishPole()
FishingP = FishingPole(2)
Pole.add(FishingP)

fish_group = fishG()
#fish = fishM(1,1, 1)#lane, size 1 or 2, speed

#fish_group.add(fish)

posList = []
MMMoveList = []
def calc():
    num = 1485//fl#number of times it goes to the end
    num = int(num)
    for y in range(1,num+1):
        posList.append(1536*y)
        MMMoveList.append(fl*y)




######################### End of Fish Functions ######################################
MMMove = 0
hold = False
pos = 0
''''''''''''''''''''' Map maker Functions and other things '''''''''''''''''''''
def mmslider(spr):#map maker slider
    global MMMove
    global hold
    global pos
    global MMMovet
    mx,my = pygame.mouse.get_pos()
    if (pygame.mixer.music.get_busy() == False or hold == True) and EngineerFish == True:#checks if song is not playing
        if mos.colliderect(spr) and pygame.mouse.get_pressed()[0]:#if touching slider
            if not(sx-45 - (sx-45-mx) >= 1491) and not(sx-45 - (sx-45-mx)<= 6):#1536-45 - (1536-45-mx) so it stops at right of slider 1536-45 - (1536-45-mx) to check if it is at left side of screen
                MMfish_group.move()
                MMMovet = MMMove
                MMMove = sx-45-mx
                hold = True
        if pygame.mouse.get_pressed()[0] and hold == True:
            if not(sx-45 - (sx-45-mx) >= 1491) and not(sx-45 - (sx-45-mx)<= 6):#the same as top
                MMfish_group.move()
                MMMovet = MMMove
                MMMove = sx-45-mx
            else:
                if mx > 500:#idk
                    MMfish_group.move()
                    MMMovet = MMMove
                    MMMove = 0
                elif mx < 500:
                    MMfish_group.move()
                    MMMovet = MMMove
                    MMMove = sx - 51
        else:
            hold = False

        pos = (MMMove * SongLength2 * 1000)/1485





    elif pygame.mixer.music.get_busy() == True and hold == False:
        if (1485 * (((pygame.mixer.music.get_pos() - original + pos)/1000)/SongLength2)) < 1485:
            MMMovet = MMMove
            MMMove =(1485 * (((pygame.mixer.music.get_pos() - original + pos)/1000)/SongLength2))
        else:
            MMMove = 1485




def scoredisplay():
    scd = font.render("Score:" + str(score), True, white)
    w, h = font.size("Score:" + str(score))
    screen.blit(scd, (0, 170-h))

    ph = font.render("Perfect:" + str(hitnum), True, white)
    w, h = font.size("Perfect:" + str(hitnum))
    screen.blit(ph, (0, 200))

    eh = font.render("Early:" + str(earlynum), True, white)
    w2, h2 = font.size("Early:" + str(earlynum))
    hi = h + h2
    screen.blit(eh, (0, 230+h))

    lh = font.render("Late:" + str(latenum), True, white)
    w, h = font.size("Late:" + str(latenum))
    screen.blit(lh, (0, 260+hi))
    hi += h

    mh = font.render("Miss:" + str(missnum), True, white)
    w, h = font.size("Miss:" + str(missnum))
    screen.blit(mh, (0, 290 + hi))
    hi += h

    mh = font.render("Max Combo:" + str(maxcombo), True, white)
    screen.blit(mh, (0, 320 + hi))
    if menu == "playing multiplayer":
        acc = Accuracy.returnAcc(True)
    else:
        acc = Accuracy.returnAcc()
    mh = font.render("Accuracy:" + acc, True, white)
    w, h = font.size("Max Combo:" + str(maxcombo))
    screen.blit(mh, (10 + w, 320 + hi))



spr= pygame.Rect(sx-45-MMMove, 382.5,39,39)
menu_done = False
def menuMake():
    global menu_done
    PlayButton = buttons("Play", sx/2-100,100,200,100)
    button_group.add(PlayButton)

    PlayButton = buttons("Multiplayer", sx / 2 - 100, 250, 200, 100)
    button_group.add(PlayButton)

    Mapmakerbutton = buttons("MMake", sx/2-100,400,200,100)
    button_group.add(Mapmakerbutton)

    SettingsButton = buttons("Settings", sx/2-100,550,200,100)
    button_group.add(SettingsButton)

    LeaveButton = buttons("Leave", sx/2-100,700,200,100)
    button_group.add(LeaveButton)
    menu_done = True

def screenDraw():
    global menu_done
    global spr
    global cdc
    global start_time
    screen.fill(black)

    '''pygame.draw.line(screen, blue, (sx - 400, 0), (sx - 400, sy), 1)#Shows segments of fishing rod
    pygame.draw.line(screen, green, (sx - 375, 0), (sx - 375, sy), 1)
    pygame.draw.line(screen, blue2, (sx - 350, 0), (sx - 350, sy), 1)
    pygame.draw.line(screen,white,(sx - 325,0),(sx - 325,sy),1)'''

    if menu == True:#menu
        if menu_done == False:
            menuMake()


        button_group.draw(screen)
    elif mapmake == False and menu == "name" and playing == False: # set name
        name = font.render("Name: " + player_name, True, white)
        width, height = font.size("Name: " + player_name)
        characters = ""
        name_segments = []
        if width > sx:
            for char in ("Name: " + player_name):
                characters += char
                width2, height2 = font.size(characters)
                if width2 > sx:
                    name_segments.append(characters)
                    characters = ""
            if characters != "":
                name_segments.append(characters)
            print(name_segments)
            name_segments = [font.render(line, True, white) for line in name_segments]
            for line in name_segments:
                screen.blit(line, (0, 100 + height * name_segments.index(line)))
        else:
            screen.blit(name, (0, 100))

        button_group.draw(screen)
        button_group.buttontext()
    elif mapmake == False and menu == "multiplayer" and playing == False:  # multiplayer menu
        button_group.draw(screen)
        button_group.buttontext()
        MultiplayerRooms.draw(screen)
    elif mapmake == False and menu == "room" and playing == False:  # multiplayer room
        button_group.draw(screen)
        button_group.buttontext()

        playerGroup.draw(screen)
        playerGroup.playerText()
    elif menu == "roomMapSelect":
        button_group.draw(screen)
        button_group.buttontext()
    elif mapmake == False and menu == False and playing == False:#map menu
        ScoreButton_Group.draw(screen)
        button_group.draw(screen)
        button_group.buttontext()
        if songstore != "":
            mapName = font.render(songstore[:-4], True, white)
            w, h = font.size(songstore[:-4])
            screen.blit(mapName, (0,0))

            MapLength = font.render("Length:"+str(LengthOfSong), True, white)
            screen.blit(MapLength, (0,h - 5))
            w2, h2 = font.size("Length:"+str(LengthOfSong))

            FishCount = font.render("Fish:"+str(FishcountNum), True, white)
            screen.blit(FishCount, (0,h+h2-5))
            wf, hf = font.size("Fish:"+str(FishcountNum))

            EelCount = font.render("Eels:"+str(EelcountNum), True, white)
            screen.blit(EelCount, (wf+5,h+h2-5))

            DifficultyDis = font.render("Difficulty:", True, white)
            #screen.blit(DifficultyDis, (w2,h+h2))

    elif (mapmake == False and menu == "playing multiplayer" and playing == True) or (mapmake == False and menu == False and playing == True) or (lc == True and EngineerFish == True and testingMap == True):#playing map
        ScoreButton_Group.empty()
        if finish == False:
            scoreDis = font.render(str(score),True,white)
            za = font.render(zd,True,white)
            comboDis = font.render("x"+str(combo),True,white)

            screen.blit(scoreDis, (0,0))
            screen.blit(comboDis, (0,100))
            screen.blit(za, (0,200))
            Accuracy.display(comboDis.get_width() + 20, 100)
            fish_group.draw(screen)
            Pole.draw(screen)
            if menu == "playing multiplayer":
                playerGroup.draw(screen)

            if testingMap == False:
                hpbar.rectdraw()

        if testingMap == True:  # map maker
            mmslider(spr)
        if cdc == False:#before countdown
            numss = 3#how many seconds

            for x in range(4):
                screen.fill(black)
                scoreDis = font.render(str(score),True,white)
                za = font.render(zd,True,white)
                comboDis = font.render("x"+str(combo),True,white)

                screen.blit(scoreDis, (0,0))
                screen.blit(comboDis, (0,100))
                screen.blit(za, (0,200))
                Accuracy.display(comboDis.get_width()+20, 100)
                fish_group.draw(screen)
                hpbar.rectdraw()
                Pole.draw(screen)
                if numss != 0:
                    numdis = bigfont.render(str(numss),True,white)
                    w, h = bigfont.size(str(numss))
                else:
                    numdis = bigfont.render("Go",True,white)
                    w, h = bigfont.size("Go")

                screen.blit(numdis, (768 - w/2,400 - h/2))#1536, 864
                numss -= 1
                pygame.display.update()
                pygame.time.delay(1000)
            start_time = pygame.time.get_ticks()
            cdc = True
            if not testingMap:
                mixer.music.play()
            else:
                mixer.music.rewind()
                MMfish_group.reset()
                try:
                    mixer.music.set_pos((pos/1000))
                    mixer.music.unpause()
                except pygame.error:
                    mixer.music.play()
                    mixer.music.set_pos((pos/1000))
                    MMfish_group.reset()
                    original = pygame.mixer.music.get_pos()
                    mixer.music.unpause()
        elif (cdc == True and pygame.mixer.music.get_busy() == False) or (cdc == True and menu == "playing multiplayer" and len(button_group) > 0):
            if finish == False:
                screen.blit(PMenu, (sx/2 - 250, sy/2-269))
            button_group.draw(screen)

            if finish == True:
                playerGroup.draw(screen)
                scoredisplay()


    elif mapmake == True and testingMap == False:#map maker
        if mapmakeSettings == False:
            screen.blit(MMSlider, (0,376.5))

            screen.blit(MMSP, (sx -45 - MMMove,382.5))
            spr = pygame.Rect(sx-45-MMMove, 382.5,39,39)
            mmslider(spr)#1524 space 192 second song 4 fish 300 pixels MMMove_max = 1485
            if mode == "Eel":
                Eellen = font.render("Length:" + lengthstore2,True,white)
                screen.blit(Eellen, (200,120))
            button_group.draw(screen)

            selected()
            Pole.draw(screen)
            MMfish_group.draw(screen)
        else:
            speedDis = font.render("Speed:"+str(speed),True,white)
            screen.blit(speedDis, (0,0))
            fish_group.update()
            fish_group.draw(screen)
            button_group.draw(screen)
            button_group.buttontext()

    ScoreButton_Group.click()
    button_group.click()
    MultiplayerRooms.click()
    pygame.display.update()

mode = "Fish"
smap = 0
mapmakeSettings = False
songstore = ""
directoryStore = ""
songStorage = ["",""]
lockon = False
lockonbuffer = 0
mbhold = False
mapmakesong = ""
stopper = False
loadmap = False
testingMap = False
class buttons(pygame.sprite.Sprite):
    def __init__(self, key, posx, posy, width, height, song = None, unum = None, directory = None, disabled = False):
        super().__init__()
        # print(key, menu)
        if key == "map":
            if loadmap == False:
                self.image = box
            else:
                self.image = box2
            self.text = smallfont.render(song,True,white)
        elif key == "Resume":
            self.image = resumeImg
        elif key == "Retry":
            self.image = RetryImg
        elif key == "ExitMM" or key == "ExitM":#mapmaker
            self.image = ExitImg
        elif key == "Save":
            self.image = SaveImg
        elif key == "SaveExit":
            self.image = SaveExitImg

        elif key == "Speed+":
            self.image = SpeedAddimg
        elif key == "Speed-":
            self.image = SpeedSubimg
        elif key == "LoadToggle":
            self.image = LoadImg
        elif key == "Enter" or key == "setName":
            self.image = EnterImg


        elif key == "lock":
            self.image = lock_off
        elif key == "Exit" and mapmake == True and mapmakeSettings == False:
            self.image = exitimg
        elif key == "Exit" or key == "exit" or key == "ExitRoom":
            self.image = backimg
        elif key == "Leave":#menu buttons
            self.image = MenuExitbutton
        elif key == "Play":
            self.image = Pbutton
        elif key == "Multiplayer":
            self.image = Pbutton
        elif key == "Settings":
            self.image = Setbutton
        elif key == "MMake":#last menu button
            self.image = MMbutton
        elif key == "size1":
            self.image = pygame.Surface([width,height])
            if sizestore == 1:
                self.image.fill(selectedc)
            else:
                self.image.fill(unselectedc)
            self.image.blit(fishimg,(0,0))
        elif key == "size2":
            self.image = pygame.Surface([width,height])
            if sizestore == 1:
                self.image.fill(unselectedc)
            else:
                self.image.fill(selectedc)
            self.image.blit(fishimg2, (0, 0))
        elif key == "createRoom":
            self.image = CreateRoomButton
        elif key == "readyUp":
            if songstore == "":
                self.image = DisabledReadyUpButton
            else:
                self.image = ReadyUpButton
        elif key == "multiplayerMap":
            self.image = box#pygame.Surface([width, height])
            #self.image.fill(white)
            if songstore == "":
                self.text = smallfont.render("Select a song", True, white)
            else:
                self.text = smallfont.render(songstore[:-4], True, white)
        elif key == "start":
            self.image = pygame.Surface([width, height])
            self.image.fill(white)
            pygame.draw.rect(self.image, blue, self.image.get_rect(), 4)
        else:
            self.image = pygame.Surface([width, height])
            if key != "Pause" and key != "score":
                self.image.fill(red)
                self.image.blit(playbut, (0, 0))
            elif key == "score":
                self.image.fill(white)
                pygame.draw.rect(self.image, blue, self.image.get_rect(), 4)

        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [posx, posy]
        self.originy = posy
        self.key = key#Fish, eel, exit, play etc
        self.buffer = 0
        self.song = song
        self.buttonclicked = False
        self.unum = unum
        self.directory = directory
        self.disable = disabled


    def click(self):
        global mode
        global original
        global MMMove
        global MMMovet
        global pos
        global mapmake
        global lc
        global hold2
        global EngineerFish
        global smap
        global run
        global main
        global menu
        global mapmakeSettings
        global speed
        global typing
        global lengthstore
        global lengthstore2
        global sizestore
        global menu_done
        global songstore
        global directoryStore
        global playing
        global lockon
        global lockonbuffer
        global mbhold
        global mapmenuload
        global mapmakesong
        global mmsonglist
        global mmsongload
        global original
        global posList
        global MMMoveList
        global loaded
        global cdc
        global fishes
        global EelcountNum
        global FishcountNum
        global exitmenu
        global stopper
        global loadmap
        global testingMap
        global combo
        global score
        global missnum
        global latenum
        global earlynum
        global hitnum
        global maxcombo
        global finish
        global kill
        global sock
        global connect
        global multiplayerMenuLoad
        global songStorage

        if not(pygame.mouse.get_pressed()[0]) and self.buffer > 0:
            self.buffer -= 1
        if not self.disable:
            if mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and mapmake == True and mapmakeSettings == False:#mapmaker
                if self.key == "Fish" and EngineerFish == True:
                    if mode == "Eel":
                        button_group.gone("input")

                    size1 = buttons("size1", 20, 130, 75, 75)
                    button_group.add(size1)

                    size2 = buttons("size2", 120, 130, 75, 75)
                    button_group.add(size2)

                    mode = "Fish"
                elif self.key == "Eel" and EngineerFish == True:
                    if mode == "Fish":
                        button_group.gone("size1")
                        button_group.gone("size2")
                    mode = "Eel"
                    inputbutton = buttons("input", 40, 130, 50,50)
                    button_group.add(inputbutton)



                elif self.key == "Pause":
                    if self.buffer <= 0:
                        if pygame.mixer.music.get_busy() == True and EngineerFish == True:
                            mixer.music.pause()
                            original = pygame.mixer.music.get_pos()
                            self.buffer = 30
                            MMMovet = MMMove
                        elif pygame.mixer.music.get_busy() == False:
                            mixer.music.rewind()
                            MMfish_group.move()
                            try:
                                mixer.music.set_pos((pos/1000))
                            except pygame.error:
                                mixer.music.play()
                                pos = 0
                                original = pygame.mixer.music.get_pos()
                            mixer.music.unpause()
                            self.buffer = 30
                elif self.key == "Delete" and EngineerFish == True:
                    if mode == "Fish":
                        button_group.gone("size1")
                        button_group.gone("size2")
                    elif mode == "Eel":
                        button_group.gone("input")

                    mode = "Delete"
                elif self.key == "Exit" and EngineerFish == True:
                    MapMakeExit()
                elif self.key == "Save":
                    smap = open((os.path.join(directoryStore, currentFile)), "w")
                    MMfish_group.filewrite()
                    smap.write(str(FishcountNum)+" "+str(EelcountNum)+" "+str(int(SongLength2)))
                    smap.close()
                    FishcountNum = 0
                    EelcountNum = 0
                    button_group.gone("SaveExit")
                    button_group.gone("ExitMM")
                    button_group.gone("Save")
                    exitmenu = False
                elif self.key == "SaveExit" or self.key == "ExitMM":
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    original = 0 #pygame.mixer.music.get_pos() ########################changed#################
                    MMMove = 0
                    MMMovet = 0
                    pos = 0
                    hold2 = False
                    if self.key == "SaveExit":
                        smap = open((os.path.join(directoryStore, currentFile)), "w")
                        MMfish_group.filewrite()
                        smap.write(str(FishcountNum)+" "+str(EelcountNum)+" "+str(int(SongLength2)))
                        smap.close()
                    lc = False#when the map maker starts
                    EngineerFish = False
                    button_group.empty()
                    MMfish_group.empty()
                    fish_group.empty()
                    fishes = []
                    mapmake = False
                    menu = True
                    typing = False
                    FishcountNum = 0
                    EelcountNum = 0
                    menu_done = False
                    lengthstore = "180"
                    lengthstore2 = "180"
                    sizestore = 1
                    posList = []
                    MMMoveList = []
                    speed = 2
                    Pole.reset()
                    mapmakesong = ""
                    directoryStore = ""
                    mmsonglist = []
                    mmsongload = False
                    lockon = False
                    pygame.time.delay(400)
                    stopper = True
                    loadmap = False

                elif self.key == "input":
                    if self.buffer <= 0:
                        typing = True
                        lengthstore2 = ""

                elif self.key == "size1" and EngineerFish == True:
                    sizestore = 1
                    button_group.resetclick()
                    self.image.fill(selectedc)
                    self.image.blit(fishimg,(0,0))

                elif self.key == "size2" and EngineerFish == True:
                    sizestore = 2
                    button_group.resetclick()
                    self.image.fill(selectedc)
                    self.image.blit(fishimg2,(0, 0))
                elif self.key == "lock" and EngineerFish == True:
                    if lockonbuffer <= 0:
                        lockon = not(lockon)
                        if lockon == False:
                            self.image = lock_off
                        else:
                            self.image = lock_on
                        lockonbuffer = 50
                elif self.key == "maptest" and EngineerFish == True and pygame.mixer.music.get_busy() == False:
                    MMfish_group.testplay()
                    testingMap = True

            elif mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and menu == True:#main menu
                if self.key == "Leave" and stopper == False:
                    run = False
                    main = False
                    kill = False
                    pygame.quit()
                    sys.exit()
                elif self.key == "MMake":
                    mapmake = True
                    menu = False
                    exitmenu = False
                    button_group.empty()

                    #fish way

                    mapmakeSettings = True
                    speedplusButton = buttons("Speed+", 300,0,50,50)
                    button_group.add(speedplusButton)

                    speedminusButton = buttons("Speed-", 400,0,50,50)
                    button_group.add(speedminusButton)

                    Togglebutton = buttons("LoadToggle", 600,0,200,75)
                    button_group.add(Togglebutton)

                    enterMMButton = buttons("Enter", 0,100,200,75)
                    button_group.add(enterMMButton)

                    exitMMButton = buttons("Exit", 0,sy-75,200,75)
                    button_group.add(exitMMButton)
                    songselect()

                elif self.key == "Settings":
                    pass
                elif self.key == "Play":
                    mapmake = False
                    menu = False
                    button_group.empty()
                elif self.key == "Multiplayer":
                    mapmake = False
                    typing = True
                    menu = "name"
                    button_group.empty()
                    exitMMButton = buttons("setName", sx-200, sy - 75, 200, 75)
                    button_group.add(exitMMButton)
                    exitMMButton = buttons("Exit", 0, sy - 75, 200, 75)
                    button_group.add(exitMMButton)

            # map/multiplayer menu
            elif mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and (menu == False or menu == "multiplayer" or menu == "room" or menu == "roomMapSelect" or menu == "name") and mapmake == False and mbhold == False and playing == False:
                if self.key == "map" and self.buttonclicked == False:
                    ScoreButton_Group.gone("score")
                    button_group.resetclick()
                    songstore = self.song + ".mp3"
                    directoryStore = self.directory
                    if menu != "room" and menu != "roomMapSelect":
                        scoremenu((songstore[:-4] + "-scores.txt"), directoryStore)
                    self.buttonclicked = True
                    mbhold = True
                    mapstats(self.song, self.directory)
                    self.image = boxs#waypoint
                    mixer.music.unload()
                    mixer.music.load(os.path.join(self.directory, songstore))
                    mixer.music.set_volume(0.5)
                    mixer.music.play(-1)
                    print("pressed a song")

                elif self.key == "setName":
                    menu = "multiplayer"
                    button_group.empty()
                    mbhold = True

                elif self.key == "map" and self.buttonclicked == True and songstore == (self.song + ".mp3") and directoryStore == self.directory and menu != "roomMapSelect":
                    button_group.empty()
                    playing = True

                elif self.key == "map" and self.buttonclicked == True and songstore == (self.song + ".mp3") and directoryStore == self.directory and menu == "roomMapSelect":
                    button_group.gone("map")
                    button_group.gone("Exit")
                    menu = "room"
                    backButton = buttons("ExitRoom", 0, sy - 75, 200, 75)
                    multiplayerMap = buttons("multiplayerMap", sx - 600, sy / 2 - 75, 600, 75)
                    readyUpButton = buttons("readyUp", sx - 410, sy - 75, 200, 75)
                    startButton = buttons("start", sx - 200, sy - 75, 200, 75)
                    button_group.add(startButton)
                    button_group.add(readyUpButton)
                    button_group.add(multiplayerMap)
                    button_group.add(backButton)
                    mapmenuload = False
                    mbhold = True
                    sendMap()
                    playerGroup.unreadyAll()
                    print("pressed", self.song)

                elif self.key == "score" and self.buttonclicked == False and songstore[:-4]+".txt" == (self.song+".txt"):
                    scoreget(self.song, self.unum, self.directory)
                    mixer.music.unload()
                    button_group.empty()
                    ScoreButton_Group.empty()
                    b = buttons("exit", 0, sy - 75, 200, 75)
                    stopper = False
                    button_group.add(b)
                    cdc = True
                    finish = True
                    menu = False
                    playing = True
                elif self.key == "createRoom" and mbhold == False:
                    create_room()
                    mbhold = True
                    print("create room")
                elif self.key == "readyUp" and mbhold == False and (directoryStore != "" and songstore != ""):
                    playerGroup.readyNotify()
                    mbhold = True
                elif self.key == "start" and mbhold == False:
                    all_ready = all(player.ready for player in playerGroup)
                    mbhold = True
                    if all_ready and songstore != "" and directoryStore != "":
                        start_game()

                elif self.key == "multiplayerMap" and mbhold == False:
                    # open map selector but instead of playing it will choose it
                    leader_exists = any(player.leader and player.isSelf for player in playerGroup)
                    songStorage = [songstore, directoryStore]
                    if leader_exists:
                        button_group.gone("ExitRoom")
                        menu = "roomMapSelect"
                        button_group.gone("multiplayerMap")
                        button_group.gone("readyUp")
                        button_group.gone("start")
                        mapmenu()
                        mbhold = True
                    else:
                        getMapData()
                        mbhold = True

                elif self.key == "ExitRoom" and mbhold == False:
                    songstore = ""
                    directoryStore = ""
                    button_group.resetclick()
                    mixer.music.unload()
                    FishcountNum = 0
                    EelcountNum = 0
                    mapmake = False
                    mapmakeSettings = False
                    menu = "multiplayer"
                    menu_done = False
                    mapmenuload = False
                    multiplayerMenuLoad = False
                    stopper = True
                    leave_room()
                    button_group.empty()
                    ScoreButton_Group.empty()
                    playerGroup.empty()
                    mbhold = True
                    print("leav")
                elif self.key == "Exit":
                    print("exiting", menu)
                    if stopper == False:
                        if menu == "multiplayer":
                            disconnect_from_server()
                        button_group.resetclick()
                        FishcountNum = 0
                        EelcountNum = 0
                        mapmake = False
                        mapmakeSettings = False

                        if menu == "roomMapSelect":
                            menu = "room"

                            if songstore != songStorage[0] and directoryStore != songStorage[1] and songStorage != ["", ""]:
                                print(songstore, directoryStore, songStorage)
                                songstore, directoryStore = songStorage
                                mixer.music.load(os.path.join(directoryStore, songstore))
                                mixer.music.set_volume(0.5)
                                mixer.music.play(-1)
                            elif songStorage == ["", ""]:
                                songstore = ""
                                directoryStore = ""
                            button_group.gone("map")
                            backButton = buttons("ExitRoom", 0, sy - 75, 200, 75)
                            multiplayerMap = buttons("multiplayerMap", sx - 600, sy / 2 - 75, 600, 75)
                            readyUpButton = buttons("readyUp", sx - 410, sy - 75, 200, 75)
                            startButton = buttons("start", sx - 200, sy - 75, 200, 75)
                            button_group.add(startButton)
                            button_group.add(readyUpButton)
                            button_group.add(multiplayerMap)
                            button_group.add(backButton)
                            button_group.gone("Exit")
                            mbhold = True
                        else:
                            songstore = ""
                            directoryStore = ""
                            mixer.music.unload()
                            menu = True
                            button_group.empty()
                            ScoreButton_Group.empty()
                            multiplayerMenuLoad = False
                            menu_done = False

                        mapmenuload = False


            elif mos.colliderect(self.rect) and not(pygame.mouse.get_pressed()[0]) and (menu == False or menu == "room" or menu == "roomMapSelect" or menu == "multiplayer") and mapmake == False and mbhold == True:#map menu
                mbhold = False

            elif mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and (menu == False or menu == "playing multiplayer") and mapmake == False and playing == True and cdc == True:#playing map
                if self.key == "Resume":
                    button_group.empty()
                    mixer.music.unpause()
                elif self.key == "Retry" and loaded == True and cdc == True:
                    button_group.empty()
                    fish_group.empty()
                    loaded = False
                    cdc = False
                    fishes = []
                    mixer.music.unload()
                    score = 0
                    combo = 0
                    missnum = 0
                    latenum = 0
                    earlynum = 0
                    hitnum = 0
                    maxcombo = 0
                    Accuracy.reset()
                    hpbar.empty()
                elif self.key == "ExitM":
                    mixer.music.unload()
                    fish_group.empty()
                    loaded = False
                    cdc = False
                    fishes = []
                    songstore = ""
                    directoryStore = ""
                    button_group.empty()
                    menu_done = False
                    mapmenuload = False
                    playing = False
                    score = 0
                    combo = 0
                    missnum = 0
                    latenum = 0
                    earlynum = 0
                    hitnum = 0
                    maxcombo = 0
                    Accuracy.reset()
                    hpbar.empty()
                    if menu == "playing multiplayer":
                        FishcountNum = 0
                        EelcountNum = 0
                        menu = "multiplayer"
                        multiplayerMenuLoad = False
                        stopper = True
                        leave_room()
                        ScoreButton_Group.empty()
                        playerGroup.empty()
                    else:
                        mapmenu()
                    mbhold = True
                elif self.key == "exit":
                    if menu == "playing multiplayer":
                        finish_song(True)
                    else:
                        finish_song()

                    mbhold = True
                    Accuracy.reset()

            elif mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and mapmakeSettings == True:#mapmaker settings
                if (self.key == "Speed+" or self.key == "Speed-") and loadmap == False:
                    if self.buffer <= 0:
                        if self.key == "Speed+":
                            if speed != 15:
                                speed += 1

                        elif self.key == "Speed-":
                            if speed != 1:
                                speed -= 1
                        self.buffer = 10
                    else:
                        self.buffer -= 1

                    fish_group.empty()
                    fish = fishM(0,2,1,speed)
                    fish_group.add(fish)
                elif self.key == "LoadToggle":
                    if self.buffer <= 0:
                        loadmap = not(loadmap)
                        mixer.music.unload()
                        button_group.gone("map")
                        songselect()
                        mapmakesong = ""
                        self.buffer = 30
                    else:
                        self.buffer -= 1



                elif self.key == "Enter" and mapmakesong != "":
                    fish_group.empty()
                    mapmakeSettings = False
                    button_group.empty()
                    mixer.music.unload()
                    print(directoryStore)
                elif self.key == "map" and self.song != mapmakesong:
                    button_group.resetclick()
                    mapmakesong = self.song
                    directoryStore = self.directory
                    if loadmap == False:
                        self.image = boxs
                    else:
                        self.image = box2s

                        mapfish = open((os.path.join(self.directory, mapmakesong+".txt")), "r")
                        cactus = mapfish.readlines()
                        pablo = cactus[0].split()
                        speed = int(pablo[-1])
                        mapfish.close()

                    mixer.music.unload()
                    mixer.music.load(os.path.join(self.directory, mapmakesong+".mp3"))
                    mixer.music.set_volume(0.5)
                    mixer.music.play(-1)

                elif self.key == "Exit":
                    print("yo")
                    mixer.music.unload()
                    button_group.empty()
                    mapmakeSettings = False
                    loadmap = False
                    mapmakesong = ""
                    directoryStore = ""
                    mapmake = False
                    menu = True
                    menu_done = False

    def gone(self,key):
        if self.key == key:
            self.kill()

    def scroll(self, amount):
        if self.key == "map" and (mapmakeSettings == True or (mapmake == False and menu == False and playing == False)):
            if (self.rect.y - (amount*20)) < self.originy:
                self.rect.y -= amount*20
            else:
                self.rect.y = self.originy

    def ready(self):
        if self.key == "readyUp":
            if self.image == ReadyUpButton:
                self.image = UnreadyUpButton
            else:
                self.image = ReadyUpButton

    def buttontext(self):
        if self.key == "map" or self.key == "multiplayerMap":
            screen.blit(self.text, (self.rect.x + 10, self.rect.y))

    def changeText(self, key, newtxt):
        if self.key == key:
            self.text = smallfont.render(newtxt, True, white)

    def resetclick(self):
        if self.key == "map":
            if loadmap == False:
                self.image = box
            else:
                self.image = box2
            self.buttonclicked = False
        elif self.key == "size1" or self.key == "size2":
            if self.key == "size1":
                self.image.fill(unselectedc)
                self.image.blit(fishimg,(0,0))
            elif self.key == "size2":
                self.image.fill(unselectedc)
                self.image.blit(fishimg2,(0,0))

    def toggleDisable(self, id, specific = None):
        if self.key == id:
            if specific is not None:
                self.disable = specific
            else:
                self.disable = not self.disable

            if self.key == "readyUp" and self.disable == False:
                self.image = ReadyUpButton
                print("a")
            elif self.key == "readyUp" and self.disable == True:
                self.image = UnreadyUpButton
                print("b")





# get maps
def createMapFolder(directory_name):
    creating = True
    fails = 5
    while creating and fails > 0:
        MID = str(random.randint(0, 99999999))  # Generate a map id
        MID = MID.zfill(8)  # add 0's to the start
        directory = f'Maps/{MID}-{directory_name[:-4]}'
        try:
            os.mkdir(directory)
            print(f"Directory '{directory_name}' created successfully.")
            creating = False
        except FileExistsError:
            print(f"Directory '{directory_name}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_name}'.")
            fails -= 1
        except Exception as e:
            print(f"An error occurred: {e}")
            fails -= 1
    if fails <= 0:
        return False
    return directory

class multiplayerRoom(pygame.sprite.Sprite):
    def __init__(self, name, posx, posy):
        super().__init__()
        self.name = name
        self.posx = posx
        self.posy = posy
        self.width = sx/2
        self.height = 80
        self.buffer = 0
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [posx, posy]

    def click(self):
        if not(pygame.mouse.get_pressed()[0]) and self.buffer > 0:
            self.buffer -= 1
        if mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0] and self.buffer <= 0:
            join_room(self.name)
            self.buffer += 1

class playerDisplay(pygame.sprite.Sprite):
    def __init__(self, posx, posy, leader, isSelf, name, idx):
        super().__init__()
        self.image = pygame.Surface([650, 60])

        self.image.blit(PlayerDis, (0, 0))
        if leader:
            self.image.blit(CrownDis, (self.image.get_width() - CrownDis.get_width() - 20,
                                       self.image.get_height()/2 - CrownDis.get_height()/2))
        self.rect = self.image.get_rect()
        self.posx = posx
        self.posy = posy
        self.rect.x, self.rect.y = [posx, posy + 75 * len(playerGroup)]
        self.leader = leader
        self.isSelf = isSelf
        self.ready = False
        self.id = name
        self.text = smallfont.render(name, True, black)
        self.score = 0
        self.perfect = 0
        self.early = 0
        self.late = 0
        self.miss = 0
        self.combo = 0
        self.accuracy = 0
        self.index = idx

    def playerText(self):
        width, height = self.text.get_size()
        self.image.blit(self.text, (10, self.rect.height/2-height/2))

    def readyNotify(self):
        print("yooo")
        if self.isSelf:
            self.ready = not self.ready
            ready_up(self.ready)


    def readyToggle(self, identifier, indx, readyStatus):
        if self.id == identifier and self.index == indx:
            if readyStatus:
                self.image.blit(ReadyPlayerDis, (0,0))
                self.ready = True
            else:
                self.image.blit(PlayerDis, (0,0))
                self.ready = False
            if self.leader:
                self.image.blit(CrownDis, (self.image.get_width() - CrownDis.get_width() - 20,
                                           self.image.get_height() / 2 - CrownDis.get_height() / 2))
            if self.isSelf:
                button_group.ready()

    def setPlayerSlab(self, identifier, form):
        if identifier:
            if self.isSelf:
                if form == "missing":
                    self.image.blit(MissingPlayerDis, (0, 0))
                elif form == "map":
                    self.image.blit(PlayerDis, (0, 0))
        else:
            if identifier == self.id:
                if form == "missing":
                    self.image.blit(MissingPlayerDis, (0, 0))
                elif form == "map":
                    self.image.blit(PlayerDis, (0, 0))

    def reposition(self, position, multiplayer = False):
        if multiplayer:
            self.image.fill(white)
            self.rect.x, self.rect.y = [200, 20 + 120 * position]
            self.text = smallfont.render(self.id + f" score:{self.score} combo:{self.combo}", True, black)
            self.image.blit(self.text, (0, 0))
        else:
            self.rect.x, self.rect.y = [self.posx, self.posy + 120 * position]
            if self.leader:
                self.image.blit(CrownDis, (self.image.get_width() - CrownDis.get_width() - 20,
                                           self.image.get_height() / 2 - CrownDis.get_height() / 2))

    def unreadyAll(self):
        self.ready = False
        if self.ready:
            self.image.blit(ReadyPlayerDis, (0, 0))
        else:
            self.image.blit(PlayerDis, (0, 0))
        if self.leader:
            self.image.blit(CrownDis, (self.image.get_width() - CrownDis.get_width() - 20,
                                       self.image.get_height() / 2 - CrownDis.get_height() / 2))

        self.text = smallfont.render(self.id, True, black)

    def leave(self, identifier):
        if self.id == identifier:
            playerGroup.remove(self)
            return True

    def setScores(self, score, combo, i):
        print(self.index, i)
        if self.index == int(i):
            self.score = score
            self.combo = combo
            self.image.fill(white)
            self.text = smallfont.render(self.id + f" score:{self.score} combo:{self.combo}", True, black)
            self.image.blit(self.text, (0, 0))

    def setFinalScores(self, scores, i):
        if self.index == int(i):
            self.score, self.perfect, self.early, self.late, self.miss, self.combo, self.accuracy = struct.unpack('>IHHHHHf', scores)

    def setSelf(self):
        self.score = score
        self.perfect = hitnum
        self.early = earlynum
        self.late = latenum
        self.miss = missnum
        self.combo = combo
        self.accuracy = Accuracy.returnAcc()
        self.image.fill(white)
        self.text = smallfont.render(self.id + f" score:{self.score} combo:{self.combo}", True, black)
        self.image.blit(self.text, (0, 0))

    def click(self):
        global score, hitnum, earlynum, latenum, missnum, maxcombo
        if mos.colliderect(self.rect) and pygame.mouse.get_pressed()[0]:
            score = self.score
            hitnum = self.perfect
            earlynum = self.early
            latenum = self.late
            missnum = self.miss
            maxcombo = self.combo
            Accuracy.setAcc(self.accuracy)

    def multiplayerDisplay(self, room):
        if room == "score":
            self.image.fill(white)
            self.rect.x, self.rect.y = [sx-200, 50 + 120 * self.index]
            self.text = smallfont.render(self.id + f" score:{self.score} combo:{self.combo}", True, black)
            self.image.blit(self.text, (0, 0))
        elif room:
            self.image = pygame.Surface([650, 60])

            if self.ready:
                self.image.blit(ReadyPlayerDis, (0, 0))
            else:
                self.image.blit(PlayerDis, (0, 0))
            if self.leader:
                self.image.blit(CrownDis, (self.image.get_width() - CrownDis.get_width() - 20,
                                           self.image.get_height() / 2 - CrownDis.get_height() / 2))
            self.rect.x, self.rect.y = [self.posx, self.posy + 75 * self.index]
            self.text = smallfont.render(self.id, True, black)
        else:
            # in game
            self.image.fill(white)
            self.rect.x, self.rect.y = [200, 20 + 120 * self.index]
            self.text = smallfont.render(self.id + f" score:{self.score} combo:{self.combo}", True, black)
            self.image.blit(self.text, (0, 0))


class playerList(pygame.sprite.Group):  # make a group
    def __init__(self, *args):
        super().__init__(*args)

    def playerText(self):
        for sprite in self:
            sprite.playerText()

    def readyNotify(self):
        for sprite in self:
            sprite.readyNotify()

    def readyToggle(self, identifier, indx, readyStatus):
        for sprite in self:
            sprite.readyToggle(identifier, indx, readyStatus)

    def unreadyAll(self):
        for sprite in self:
            sprite.unreadyAll()

    def leave(self, identifier):
        removed = False
        leader = False
        for sprite in self:
            if not removed:
                leader = sprite.leader
                removed = sprite.leave(identifier)
            else:
                sprite.index -= 1
        if leader:
            newLeader = next(iter(playerGroup))
            newLeader.leader = True
            if newLeader.isSelf and menu != "playing multiplayer":
                button_group.empty()
                backButton = buttons("ExitRoom", 0, sy - 75, 200, 75)
                multiplayerMap = buttons("multiplayerMap", sx - 600, sy / 2 - 75, 600, 75)
                readyUpButton = buttons("readyUp", sx - 410, sy - 75, 200, 75)
                startButton = buttons("start", sx - 200, sy - 75, 200, 75)
                button_group.add(startButton)
                button_group.add(readyUpButton)
                button_group.add(multiplayerMap)
                button_group.add(backButton)

    def reposition(self, multiplayer = False):
        count = 0
        if multiplayer:
            sorted_players = sorted(self, key=lambda s: s.score, reverse=True)
            for sprite in sorted_players:
                sprite.reposition(count, True)
                count += 1

        else:
            for sprite in self:
                sprite.reposition(count)
                count += 1

    def setScores(self, score, combo, i):
        for sprite in self:
            sprite.setScores(score, combo, i)
            playerGroup.reposition(True)

    def setFinalScores(self, scores, i):
        for sprite in self:
            sprite.setFinalScores(scores, i)

    def multiplayerDisplay(self, room):
        for sprite in self:
            sprite.multiplayerDisplay(room)

    def setPlayerSlab(self, identifier, form):
        for sprite in self:
            sprite.setPlayerSlab(identifier, form)

    def setSelf(self):
        for sprite in self:
            if sprite.isSelf:
                sprite.setSelf()
                playerGroup.reposition(True)

    def click(self):
        for sprite in self:
            sprite.click()

    def isLeader(self):
        for sprite in self:
            if sprite.isSelf:
                return sprite.leader

playerGroup = playerList()

class rooms(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def click(self):
        for sprite in self:
            sprite.click()


MultiplayerRooms = rooms()

def scoreget(file, num, directory):
    global score
    global hitnum
    global earlynum
    global latenum
    global missnum
    global maxcombo
    openmap = open((os.path.join(directory, (file + "-scores.txt"))), "r")  # way
    lines = openmap.readlines()
    line = lines[num]
    Stats = line.split()

    score = Stats[0]
    hitnum = Stats[1]
    earlynum = Stats[2]
    latenum = Stats[3]
    missnum = Stats[4]
    maxcombo = Stats[5]
    Accuracy.setAcc(Stats[6])

    openmap.close()

def selected():
    if mode == "Fish":
        screen.blit(fba, (0,0))
    else:
        screen.blit(fbi, (0,0))
    if mode == "Eel":
        screen.blit(eba, (200,0))
    else:
        screen.blit(ebi, (200,0))

    if mode == "Delete":
        screen.blit(bin2, (1356,25))
    else:
        screen.blit(bin1, (1356,25))

    if mapmake == True and lc == True:
        if pygame.mixer.music.get_busy() == False:
            screen.blit(playbut, (450, 25))
        else:
            screen.blit(pausebut, (450, 25))





class buttonG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def click(self):
        for sprite in self:
            sprite.click()

    def gone(self,key):
        for sprite in self:
            sprite.gone(key)

    def scroll(self, amount):
        for sprite in self:
            sprite.scroll(amount)

    def buttontext(self):
        for sprite in self:
            sprite.buttontext()

    def changeText(self, key, text):
        for sprite in self:
            sprite.changeText(key, text)

    def resetclick(self):
        for sprite in self:
            sprite.resetclick()

    def ready(self):
        for sprite in self:
            sprite.ready()

    def toggleDisable(self, id, specific = None):
        for sprite in self:
            if specific is not None:
                sprite.toggleDisable(id, specific)
            else:
                sprite.toggleDisable(id)



button_group = buttonG()
ScoreButton_Group = buttonG()

clock = pygame.time.Clock()
main = True
SongLength2 = 0
hold2 = False
lc = False#when the map maker starts
EngineerFish = False
currentFile = ""
sizestore = 1
def MapMaker(song, directory):
    global lc
    global MMMovet
    global MMMove
    global SongLength2
    global hold2
    global currentFile
    global lockonbuffer
    global sizestore
    global exitmenu
    global cdc
    global fishes
    global testingMap
    global pos
    global original
    global mbuffer
    global directoryStore

    if lc == False:
        currentFile = song+".txt"
        song = song + ".mp3"
        if not loadmap:
            newDirectory = createMapFolder(currentFile)
            shutil.copy(f"{directoryStore}/{currentFile[:-4]}.mp3", newDirectory)
            directoryStore = newDirectory
        newDirectory = directory
        l = pygame.mixer.Sound(os.path.join(newDirectory, song))
        SongLength = round(l.get_length())#192
        SongLength2 = l.get_length()

        lc = True
        mixer.music.load(os.path.join(newDirectory, song))
        mixer.music.set_volume(0.5)
        mixer.music.play()
        mixer.music.pause()
        fishButton = buttons("Fish", 0,0,200,100)
        eelButton = buttons("Eel", 200,0,200,100)
        PauseButton = buttons("Pause", 450,25,50,50)
        DeleteButton = buttons("Delete", 1356,25,50,50)
        LockButton = buttons("lock", 550,25,50,50)
        ExitButton = buttons("Exit", sx - 100,25,50,50)
        maptestButton = buttons("maptest", 1276,25,50,50)
        size1 = buttons("size1", 20, 130, 75,75)
        button_group.add(size1)
        size2 = buttons("size2", 120, 130, 75,75)
        button_group.add(size2)
        button_group.add(fishButton)
        button_group.add(eelButton)
        button_group.add(PauseButton)
        button_group.add(DeleteButton)
        button_group.add(LockButton)
        button_group.add(ExitButton)
        button_group.add(maptestButton)
        Tfish = MMTfish(speed)
        MMfish_group.add(Tfish)
    if lc == True and EngineerFish == False and pygame.mixer.music.get_busy() == False:
        button_group.click()
    if lc == True and EngineerFish == False and pygame.mixer.music.get_busy() == True:
        MMfish_group.update()


    if lc == True and EngineerFish == True and testingMap == False:
        button_group.click()
        lane1 = pygame.Rect(0, 427.5, sx, 120)
        lane2 = pygame.Rect(0, 547.5, sx, 120)
        lane3 = pygame.Rect(0, 667.5, sx, 120)

        #pygame.display.update()
        MMfish_group.delete()
        if pygame.mouse.get_pressed()[0] and hold2 == False and exitmenu == False:
            if mos.colliderect(lane1):
                if mode == "Fish":
                    fish = MMfishM(mx, 1, sizestore, speed, False)
                    MMfish_group.add(fish)
                elif mode == "Eel":
                    eel = MMeelM(mx, 1, int(lengthstore), speed)
                    MMfish_group.add(eel)


            elif mos.colliderect(lane2):
                if mode == "Fish":
                    fish = MMfishM(mx, 2, sizestore, speed, False)
                    MMfish_group.add(fish)
                elif mode == "Eel":
                    eel = MMeelM(mx, 2, int(lengthstore), speed)
                    MMfish_group.add(eel)

            elif mos.colliderect(lane3):
                if mode == "Fish":
                    fish = MMfishM(mx, 3, sizestore, speed, False)
                    MMfish_group.add(fish)
                elif mode == "Eel":
                    eel = MMeelM(mx, 3, int(lengthstore), speed)
                    MMfish_group.add(eel)

            hold2 = True
        elif not(pygame.mouse.get_pressed()[0]):
            hold2 = False

        if lockonbuffer > 0:
            lockonbuffer -= 1

        Pole.movement()
        if lockon == True:
            Pole.click()

        if (keys[pygame.K_1] or keys[pygame.K_KP1]) and mode == "Fish":
            sizestore = 1
        elif (keys[pygame.K_2] or keys[pygame.K_KP2]) and mode == "Fish":
            sizestore = 2




        if pygame.mixer.music.get_busy() == True:
            MMfish_group.update()

    if lc == True and EngineerFish == True and testingMap == True:
        if cdc == True and pygame.mixer.music.get_busy() == True:#playing the game
            fish_group.update()
            Pole.movement()
            Pole.click()


            if keys[pygame.K_ESCAPE]:
                fish_group.empty()
                cdc = False
                fishes = []
                testingMap = False
                mixer.music.pause()
                original = pygame.mixer.music.get_pos()
                mbuffer = 40
                MMMovet = MMMove
            if len(fish_group) == 0:
                fish_group.empty()
                cdc = False
                fishes = []
                testingMap = False
                mixer.music.pause()
                original = pygame.mixer.music.get_pos()
                mbuffer = 40
                MMMovet = MMMove


        elif cdc == True and pygame.mixer.music.get_busy() == False:
            pass

    if keys[pygame.K_ESCAPE] and len(button_group)>8 and testingMap == False:
        button_group.gone("SaveExit")
        button_group.gone("ExitMM")
        button_group.gone("Save")
        exitmenu = False

speed = 2


playing = False
fishes = []
loaded = False
def mapPlay(song, directory):
    global loaded
    print(song, directory)
    file = ""
    split = song.split(".")
    if len(split) > 2:
        for x in split:
            if x != "mp3":
                file = file + x +"."
        file = file + "txt"
    else:
        file = split[0] + ".txt"
    smp = open((os.path.join(directory, file)), "r")
    content = smp.readlines()
    for count in content:
        entity = count.split()
        fishes.append(entity)
    for count in fishes:
        if count[0] == "fish":
            fish = fishM(int(count[1]), int(count[2]), int(count[3]), int(count[4]))   #(pos, lane, size, speed)
            fish_group.add(fish)
        elif count[0] == "eel":
            eel = eelM(int(count[1]), int(count[2]), int(count[3]), int(count[4])) #(pos, lane, length, speed):
            fish_group.add(eel)

    mixer.music.load(os.path.join(directory, song))
    mixer.music.set_volume(0.5)
    bar = hpb(sx-500,0)
    hpbar.add(bar)
    loaded = True


def MapLoad(song, directory):
    file = ""
    split = song.split(".")
    if len(split) > 2:
        for x in split:
            if x != "mp3":
                file = file + x +"."
        file = file + "txt"
    else:
        file = split[0] + ".txt"
    smp = open((os.path.join(directory, file)), "r")
    content = smp.readlines()
    for count in content:
        entity = count.split()
        fishes.append(entity)
    for count in fishes:
        if count[0] == "fish":
            fish = MMfishM(int(count[1]), int(count[2]), int(count[3]), int(count[4]), False)   #(posx, lane, size, speed,test)
            MMfish_group.add(fish)
        elif count[0] == "eel":
            eel = MMeelM(int(count[1]), int(count[2]), int(count[3]), int(count[4])) #posx, lane, length, speed)
            MMfish_group.add(eel)



def scoremenu(txtfile, directory):
    try:
        openmap = open((os.path.join(directory, (txtfile))), "r")#way
        lines = openmap.readlines()
        x = len(lines)
        for count in range(x):
            scorebut = buttons("score",0,(count*100)+200,200,100,txtfile[:-11],unum=count, directory=directory)
            ScoreButton_Group.add(scorebut)
        openmap.close()
    except FileNotFoundError:
        pass


cdc = False

mapmenulist = []
mapmenuload = False
def mapmenu():
    global mapsList
    global mapmenulist
    global mapmenuload
    if mapmenuload == False:
        mapmenulist = []
        mapsList = os.listdir("Maps")
        for folder in mapsList:
            content = os.listdir(f"Maps/{folder}")
            for maps in content:
                file = ""
                split = maps.split(".")
                split2 = maps.split("-")

                if split[len(split)-1] != "mp3" and split2[-1] != "scores.txt":
                    if len(split) > 2:
                        for x in split:
                            if x != "txt":
                                file = file + x + "."
                            else:
                                file = file[:-1]
                        mapmenulist.append(file)
                    else:
                        file = split[0]
                        mapmenulist.append(file)

                    mapmenulist.index(file)

                    mapbutton = buttons("map", sx-600,(len(button_group))*75,600,75,file, directory = f"Maps/{folder}")
                    button_group.add(mapbutton)
        exitbutton = buttons("Exit", 0, sy-75,200,75)
        button_group.add(exitbutton)
        mapmenuload = True
    else:
        pass
LengthOfSong = 0

def mapstats(song, directory):
    global FishcountNum
    global EelcountNum
    global LengthOfSong
    openmap = open((os.path.join(directory, (song+".txt"))), "r")
    lines = openmap.read().splitlines()
    if lines != []:
        last_line = lines[-1]
        openmap.close()
        splitstats = last_line.split(" ")
        FishcountNum = splitstats[0]
        EelcountNum = splitstats[1]
        LengthOfSong = splitstats[2]

multiplayerMenuLoad = False

def multiplayerMapMenu():
    global multiplayerMenuLoad
    if not multiplayerMenuLoad:
        backButton = buttons("Exit", 0, sy - 75, 200, 75)
        button_group.add(backButton)
        createButton = buttons("createRoom", sx-200, sy - 75, 200, 75)
        button_group.add(createButton)
        multiplayerMenuLoad = True

def pauseMenu(multiplayer = False):#sx/2 - 250, sy/2-269(163)
    if not multiplayer:
        mixer.music.pause()
        retrybut = buttons("Retry", sx / 2 - 200, sy / 2 - 69, 400, 100)
        button_group.add(retrybut)

    resumebut = buttons("Resume", sx/2-200, sy/2-219, 400,100)
    button_group.add(resumebut)#waypoint 2

    exitmapbut = buttons("ExitM", sx/2-200, sy/2+81, 400,100)
    button_group.add(exitmapbut)
exitmenu = False
def MapMakeExit():
    global exitmenu
    resumebut = buttons("Save", sx/2-200, sy/2-219, 400,100)
    button_group.add(resumebut)

    retrybut = buttons("SaveExit", sx/2-200, sy/2-69, 400,100)
    button_group.add(retrybut)

    exitmapbut = buttons("ExitMM", sx/2-200, sy/2+81, 400,100)
    button_group.add(exitmapbut)
    exitmenu = True


mmsonglist = []
mmsongload = False
def songselect():
    global mapsList
    global mmsonglist
    global mmsongload
    mmsonglist = []
    mapsList = os.listdir("Maps")
    for folder in mapsList:
        content = os.listdir(f"Maps/{folder}")
        for songs in content:
            file = ""
            split = songs.split(".")
            if loadmap == False:
                if split[len(split)-1] == "mp3":
                    if len(split) > 2:
                        for x in split:
                            if x != "mp3":
                                file = file + x + "."
                            else:
                                file = file[:-1]
                        mmsonglist.append(file)
                    else:
                        file = split[0]
                        mmsonglist.append(file)

                    mmsonglist.index(file)
                    songbutton = buttons("map", sx-600,(len(button_group)-5)*75, 600, 75, file, directory = f"Maps/{folder}")

                    button_group.add(songbutton)
            else:
                if split[len(split)-1] == "txt" and split[len(split)-2][-7:] != "-scores":
                    if len(split) > 2:
                        for x in split:
                            if x != "txt":
                                file = file + x + "."
                            else:
                                file = file[:-1]
                        mmsonglist.append(file)
                    else:
                        file = split[0]
                        mmsonglist.append(file)

                    mmsonglist.index(file)
                    songbutton = buttons("map",sx-600,(len(button_group)-5)*75,600,75,file, directory = f"Maps/{folder}")

                    button_group.add(songbutton)




''''''''''''''''''''' End of Map maker Functions and other things '''''''''''''''''''''

def finish_song(multiplayer = False):
    global loaded
    global cdc
    global fishes
    global songstore
    global directoryStore
    global menu_done
    global mapmenuload
    global playing
    global score
    global combo
    global finish
    global missnum
    global latenum
    global earlynum
    global hitnum
    global maxcombo
    global menu

    loaded = False
    cdc = False
    fishes = []
    fish_group.empty()
    menu_done = False
    mapmenuload = False
    playing = False
    score = 0
    combo = 0
    latenum = 0
    earlynum = 0
    hitnum = 0
    maxcombo = 0
    missnum = 0
    Accuracy.reset()
    finish = False
    hpbar.empty()
    button_group.empty()
    if not multiplayer:
        songstore = ""
        directoryStore = ""
        mapmenu()
    else:
        menu = "room"

        multiplayerMap = buttons("multiplayerMap", sx - 600, sy / 2 - 75, 600, 75)
        button_group.add(multiplayerMap)
        playerGroup.unreadyAll()
        playerGroup.multiplayerDisplay(True)
        backButton = buttons("ExitRoom", 0, sy - 75, 200, 75)
        button_group.add(backButton)

        if playerGroup.isLeader():
            readyUpButton = buttons("readyUp", sx - 410, sy - 75, 200, 75)
            startButton = buttons("start", sx - 200, sy - 75, 200, 75)
            button_group.add(startButton)
            button_group.add(readyUpButton)
        else:
            readyUpButton = buttons("readyUp", sx - 200, sy - 75, 200, 75)
            button_group.add(readyUpButton)
        mixer.music.load(os.path.join(directoryStore, songstore))
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
def scoresave():
    spot = "abc"
    orderscores = []
    try:
        savescore = open((os.path.join(directoryStore, songstore[:-4] + "-scores.txt")), "r")
        scores = savescore.readlines()
        for x in range(len(scores)):
            compare = scores[x].split()
            orderscores.append([int(compare[0]), float(compare[6])])
            orderscores = sorted(orderscores, reverse=True)
        savescore.close()

        for s in orderscores:
            if score > s[0] and spot == "abc":
                spot = orderscores.index(s)
            if score == s[0] and float(Accuracy.returnAcc()[:-1]) > s[1] and spot == "abc":
                spot = orderscores.index(s)


        savescore = open((os.path.join(directoryStore, songstore[:-4] + "-scores.txt")), "w")
        for x in range(len(orderscores)):
            if spot == x:
                savescore.write(f"{score} {hitnum} {earlynum} {latenum} {missnum} {maxcombo} {Accuracy.returnAcc()[:-1]}\n")
                savescore.write(scores[x])
            else:
                savescore.write(scores[x])
        if spot == "abc":
            savescore.write(f"{score} {hitnum} {earlynum} {latenum} {missnum} {maxcombo} {Accuracy.returnAcc()[:-1]}\n")
    except FileNotFoundError:
        savescore = open((os.path.join(directoryStore, songstore[:-4] + "-scores.txt")), "w")
        savescore.write(f"{score} {hitnum} {earlynum} {latenum} {missnum} {maxcombo} {Accuracy.returnAcc()[:-1]}\n")
        savescore.close()

    savescore.close()


mapmake = False
mouseMov = 0
menu = True
mbuffer = 0
original = 0
MMMovet = 0
sliderhold = False
typing = False
lengthstore = "180"
numberlist = "0123456789"
lengthstore2 = "180"
finish = False
keys = pygame.key.get_pressed()
mx, my = pygame.mouse.get_pos()
host = '172.237.96.131'
port = 62087
sock = None
connect = False
kill = False
opponent_score = 0
opponent_combo = 0
start_time = 0
player_name = ""

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            raise ConnectionResetError("Connection closed early")
        data += packet
    return data

def recv_message(sock):
    raw_length = recv_all(sock, 4)
    message_length = int.from_bytes(raw_length, byteorder='big')
    return recv_all(sock, message_length)

def ready_up(ready):
    if sock:
        try:
            print(ready)
            if ready:
                sendBigData(b'READY')
            else:
                sendBigData(b'UNREADY')
        except OSError:
            pass

def start_game():
    if sock:
        try:
            sendBigData(b'START')
        except OSError:
            pass

def get_rooms():
    if sock:
        try:
            sendBigData(b'GET ROOMS')
        except OSError:
            pass

def create_room():
    if sock:
        try:
            sendBigData(b'CREATE ROOM')
        except OSError:
            pass

def join_room(room_id):
    if sock:
        message = f"JOIN {room_id}"
        data = message.encode("utf-8")
        try:
            sendBigData(data)
        except OSError:
            pass

def leave_room():
    if sock:
        try:
            sendBigData(b'LEAVE ROOM')
        except OSError:
            pass

def disconnect_from_server():
    global sock, kill, connect

    kill = True
    connect = False
    if sock:
        try:
            sendBigData(b'LEAVE')
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            sock.close()
        except OSError:
            pass
        sock = None


def sendData():
    if sock:
        payload = struct.pack('>IH', score, combo)
        sendBigData(b'score' + payload)
        print("sending")

def sendFinalScores():
    if sock:
        payload = struct.pack('>IHHHHHf', score, hitnum, earlynum, latenum, missnum, maxcombo, float(Accuracy.returnAcc()[:-1]))
        sendBigData(b'final score' + payload)

        print("sending final")

def sendBigData(data_bytes):
    length = len(data_bytes)
    try:
        sock.sendall(length.to_bytes(4, byteorder='big') + data_bytes)
    except OSError as e:
        print("error:", e)

def getMapData():
    if sock:
        message = f"GET MAP"
        data = message.encode("utf-8")
        try:
            sendBigData(data)
        except OSError:
            pass

def sendName():
    if sock:
        print("sending?")
        message = f"NAME:{player_name}"
        data = message.encode("utf-8")
        try:
            sendBigData(data)
        except OSError:
            pass

def sendMap():
    if sock:
        file = ""
        split = songstore.split(".")
        if len(split) > 2:
            for x in split:
                if x != "mp3":
                    file = file + x + "."
            file = file + "txt"
        else:
            file = split[0] + ".txt"
        sendmap = open((os.path.join(directoryStore, file)), "r")
        content = sendmap.read()
        print("a")
        songFile = open((os.path.join(directoryStore, songstore)), "rb")
        song = songFile.read()
        song_b64 = base64.b64encode(song).decode('utf-8')

        mapJson = {
            "name": directoryStore[5:],
            "content": content,
            "song": song_b64
        }
        data = json.dumps(mapJson).encode()
        sendBigData(data)
        sendmap.close()
        songFile.close()

def deserialize(data):
    global opponent_score, opponent_combo, menu, songstore, directoryStore, playing
    position = 0
    update_format = '>IH'
    print(data)
    if data.startswith(b'JOINED '):
        menu = "room"
        print("yes")
        button_group.empty()
        MultiplayerRooms.empty()
        backButton = buttons("ExitRoom", 0, sy - 75, 200, 75)
        button_group.add(backButton)
        room_id = data[7:].decode().strip()
        message = f"ROOM {room_id}"
        data = message.encode("utf-8")
        try:
            sendBigData(data)
        except OSError:
            pass
        return
        # get room data (people + map)
    elif data == b'CREATED ROOM':
        menu = "room"
        print("created")
        button_group.empty()
        MultiplayerRooms.empty()
        backButton = buttons("ExitRoom", 0, sy - 75, 200, 75)
        button_group.add(backButton)
        player = playerDisplay(50, 50, True, True, player_name, 0)
        playerGroup.add(player)
        multiplayerMap = buttons("multiplayerMap", sx - 600, sy / 2 - 75, 600, 75)
        button_group.add(multiplayerMap)
        readyUpButton = buttons("readyUp", sx - 410, sy - 75, 200, 75)
        button_group.add(readyUpButton)
        startButton = buttons("start", sx - 200, sy - 75, 200, 75)
        button_group.add(startButton)

        return
    elif data.startswith(b'PLAYER JOINED:'):
        message = data.decode()
        name = message.split(":", 1)[1]
        player = playerDisplay(50, 50, False, False, name, len(playerGroup))
        playerGroup.add(player)
        return
    elif data.startswith(b'PLAYER LEFT:'):
        decoded = data.decode()
        name = decoded.split(":", 1)[1]
        playerGroup.leave(name)
        playerGroup.reposition()
        return
    elif data == b'START MATCH':
        menu = "playing multiplayer"
        playerGroup.multiplayerDisplay(False)
        playing = True
        button_group.empty()
        return
    try:
        decoded = data.decode()
        room_info = json.loads(decoded)
        print("Received JSON:", room_info)
        # getting map when changed
        if len(room_info) == 1 and "map" in room_info:
            if not room_info["map"] == "":
                if os.path.isdir(os.path.join("Maps", room_info["map"][0])):
                    mapFile = open(os.path.join("Maps", room_info["map"][0], f"{room_info['map'][0][9:]}.txt"), "r")
                    content = mapFile.read()
                    if content == room_info["map"][1]:
                        playerGroup.setPlayerSlab(True, "map")
                        directoryStore = f"Maps/{room_info['map'][0]}"
                        mixer.music.load(os.path.join("Maps", room_info["map"][0], f"{room_info['map'][0][9:]}.mp3"))
                        mixer.music.set_volume(0.5)
                        mixer.music.play(-1)
                        button_group.toggleDisable("readyUp", False)
                    else:
                        playerGroup.setPlayerSlab(True, "missing")
                        button_group.toggleDisable("readyUp", True)
                else:
                    playerGroup.setPlayerSlab(True, "missing")
                    button_group.toggleDisable("readyUp", True)

                songstore = room_info["map"][0][9:]+".mp3"
                button_group.changeText("multiplayerMap", songstore[:-4])
        elif len(room_info) == 1 and "READY" in room_info:
            name = room_info["READY"][0]
            indx = room_info["READY"][1]
            playerGroup.readyToggle(name, indx, room_info["READY"][2])
        # joining room
        elif len(room_info) == 3 and "players" in room_info:
            # add players
            print(room_info)
            indx = 0
            for p in room_info["players"]:
                if indx + 1 < len(room_info["players"]):
                    if indx == room_info["leader"]:
                        player = playerDisplay(50, 50, True, False, p, indx)
                    else:
                        player = playerDisplay(50, 50, False, False, p, indx)
                    playerGroup.add(player)
                    indx += 1
            player = playerDisplay(50, 50, False, True, player_name, indx)
            playerGroup.add(player)
            readyUpButton = buttons("readyUp", sx - 200, sy - 75, 200, 75)
            button_group.add(readyUpButton)
            if not room_info["map"] == "":
                if os.path.isdir(os.path.join("Maps", room_info["map"][0])):
                    mapFile = open(os.path.join("Maps", room_info["map"][0], f"{room_info['map'][0][9:]}.txt"), "r")
                    content = mapFile.read()
                    if content == room_info["map"][1]:
                        playerGroup.setPlayerSlab(True, "map")
                        directoryStore = f"Maps/{room_info['map'][0]}"
                        mixer.music.load(os.path.join("Maps", room_info["map"][0], f"{room_info['map'][0][9:]}.mp3"))
                        mixer.music.set_volume(0.5)
                        mixer.music.play(-1)
                        button_group.toggleDisable("readyUp", False)
                    else:
                        playerGroup.setPlayerSlab(True, "missing")
                        button_group.toggleDisable("readyUp", True)
                else:
                    playerGroup.setPlayerSlab(True, "missing")
                    button_group.toggleDisable("readyUp", True)

                songstore = room_info["map"][0][9:]+".mp3"
            multiplayerMap = buttons("multiplayerMap", sx-600, sy/2 - 75, 600, 75)
            button_group.add(multiplayerMap)
            # playing and activating song ready up and checking for duplicates
            # check if the map is installed

        # download map
        elif len(room_info) == 3 and "song" in room_info:
            # make a folder with text file
            try:
                folderPath = os.path.join("Maps", room_info["name"])
                os.makedirs(folderPath)

                song = open(os.path.join(folderPath, f"{room_info['name'][9:]}.mp3"), "wb")
                song_bytes = base64.b64decode(room_info["song"])
                song.write(song_bytes)
                song.close()

                mapFile = open(os.path.join(folderPath, f"{room_info['name'][9:]}.txt"), "w")
                print(f"{room_info['name'][9:]}.txt")
                mapFile.write(room_info["content"])
                mapFile.close()
                playerGroup.setPlayerSlab(True, "map")
            except FileExistsError:
                print("already exists")
        # when going into multiplayer
        else:
            sendName()
            MultiplayerRooms.empty()
            for r in room_info:
                room = multiplayerRoom(r, 0, 90 * position)
                position += 1
                MultiplayerRooms.add(room)
        return
    except (UnicodeDecodeError, json.JSONDecodeError):
        pass  # Not JSON
    if len(data):
        colon_index = data.find(b':')
        scoreInfo = data[colon_index + 1:]
        try:
            if data.startswith(b'final'):
                playerIndex = data[5:colon_index].decode()
                playerGroup.setFinalScores(scoreInfo, playerIndex)
            else:
                playerIndex = data[:colon_index].decode()
                opp_score, opp_combo = struct.unpack_from(update_format, scoreInfo, 0)
                opponent_score = opp_score
                opponent_combo = opp_combo
                playerGroup.setScores(opp_score, opp_combo, playerIndex)
                print("score:", opponent_score, opponent_combo, playerIndex)
            return
        except struct.error:
            pass

def run_listener():
    global sock
    global kill
    global connect
    connect = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.connect((host, port))
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        s.settimeout(1)
        print("connected", s)
        sock = s
        while not kill:
            try:
                data = recv_message(sock)
                if data:
                    deserialize(data)
            except socket.timeout:
                pass
            except OSError as e:
                print("Socket error:", e)
                break
            time.sleep(0.001)

def main():
    global mapmake
    global mouseMov
    global menu
    global mbuffer
    global original
    global MMMovet
    global sliderhold
    global typing
    global lengthstore
    global numberlist
    global lengthstore2
    global finish
    global run
    global main
    global mos
    global MMMove
    global sliderhold
    global EngineerFish
    global stopper
    global maxcombo
    global combo
    global keys
    global kill
    global mx, my
    global player_name
    run = True

    while run: # what to do new folder when making song in map maker
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                kill = True
                disconnect_from_server()
                run = False
                main = False
                pygame.quit()
            elif event.type == pygame.MOUSEWHEEL and (pygame.mouse.get_pos()[0] > sx/2 or mapmakeSettings == True):
                button_group.scroll(event.y)
            if typing and menu != "name":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            if int(lengthstore2) < 180 or lengthstore2 == "" or int(lengthstore2)>1000000:
                                lengthstore = "180"
                                lengthstore2 = "180"
                            else:
                                lengthstore = lengthstore2
                            typing = False
                        except ValueError:
                            lengthstore = "180"
                            lengthstore2 = "180"

                    elif event.key==pygame.K_BACKSPACE:
                        lengthstore2 = lengthstore2[:-1]
                    else:
                        if event.unicode in numberlist:
                            lengthstore2 += event.unicode
            elif typing and menu == "name":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass

                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode


        mx, my = pygame.mouse.get_pos()
        mos = pygame.Rect(mx, my, 15,15)


        if mapmake:#map maker
            if pygame.mixer.music.get_busy() == False and EngineerFish == True and sliderhold == False:
                MMfish_group.reset()
            if not(pygame.mixer.music.get_busy() == False and keys[pygame.K_RIGHT] and keys[pygame.K_LEFT] and EngineerFish == True):
                if pygame.mixer.music.get_busy() == False and keys[pygame.K_RIGHT] and EngineerFish == True and sliderhold == False:
                    if spr.x + 45 > 1530 or spr.x + 49 > 1530:
                        MMMove = 0
                        MMfish_group.btStart()
                    else:
                        MMMove -= 10
                        MMfish_group.tapmove(-1)
                    MMMovet = MMMove

                elif pygame.mixer.music.get_busy() == False and keys[pygame.K_LEFT] and EngineerFish == True and sliderhold == False:
                    if spr.x - 10 < 6:
                        MMMove = 1485
                        MMfish_group.move()
                    else:
                        MMMove += 10
                        MMfish_group.tapmove(1)
                    MMMovet = MMMove
                if not(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
                    sliderhold = False



            if mbuffer <= 0:
                if keys[pygame.K_p] and pygame.mixer.music.get_busy() == True and EngineerFish == True:
                    mixer.music.pause()
                    original = pygame.mixer.music.get_pos()
                    mbuffer = 40
                    MMMovet = MMMove
                elif keys[pygame.K_p] and pygame.mixer.music.get_busy() == False and MMMove != 1485 and mapmakeSettings == False and typing == False:
                    mixer.music.rewind()
                    MMfish_group.reset()
                    try:
                        mixer.music.set_pos((pos/1000))
                        mixer.music.unpause()
                    except pygame.error:
                        mixer.music.play()
                        mixer.music.set_pos((pos/1000))
                        MMfish_group.reset()
                        original = pygame.mixer.music.get_pos()
                        mixer.music.unpause()

                    mbuffer = 40
            else:
                mbuffer -= 1


        #map maker end
        if menu and menu != "playing multiplayer":
            if not(pygame.mouse.get_pressed()[0]):
                stopper = False
        elif mapmake == False and menu == False:#play
            if playing:
                if not loaded:
                    mapPlay(songstore, directoryStore)#sets everything up
                elif loaded:
                    if cdc == True and pygame.mixer.music.get_busy() == True and finish == False:#playing the game
                        fish_group.update()
                        Pole.movement()
                        Pole.click()
                        if keys[pygame.K_ESCAPE]:
                            pauseMenu()
                        if len(fish_group) == 0 or hpbar.check() == True:
                            screenDraw()
                            if maxcombo < combo:
                                maxcombo = combo
                            if hpbar.check() == False:
                                scoresave()
                            pygame.mixer.music.fadeout(2500)
                            mixer.music.unload()
                            button_group.empty()
                            b = buttons("exit", 0, sy - 75, 200, 75)
                            button_group.add(b)
                            finish = True

                    elif cdc == True and pygame.mixer.music.get_busy() == False and finish == False:
                        pass
                    elif cdc == True and finish == True:
                        pass

            else:
                mapmenu()
        elif menu == "playing multiplayer":
            if playing:
                if not cdc:
                    n = 1
                if not loaded:
                    mapPlay(songstore, directoryStore)#sets everything up
                elif loaded:
                    if cdc == True and pygame.mixer.music.get_busy() == True and finish == False:#playing the game
                        if pygame.time.get_ticks() - start_time > 2000*n:
                            sendData()
                            n += 1
                        fish_group.update()
                        Pole.movement()
                        Pole.click()
                        if keys[pygame.K_ESCAPE]:
                            pauseMenu(True)
                        if len(fish_group) == 0:
                            screenDraw()
                            if maxcombo < combo:
                                maxcombo = combo
                            if hpbar.check() == False and hpbar.check(True) == False:
                                scoresave()
                            pygame.mixer.music.fadeout(2500)
                            mixer.music.unload()
                            button_group.empty()
                            playerGroup.setSelf()
                            playerGroup.multiplayerDisplay("score")
                            b = buttons("exit", 0, sy - 75, 200, 75)
                            button_group.add(b)
                            sendFinalScores()
                            finish = True

                    elif cdc == True and pygame.mixer.music.get_busy() == False and finish == False:
                        pass
                    elif cdc == True and finish == True:
                        playerGroup.click()
        else:#map maker
            if not mapmakeSettings:
                MapMaker(mapmakesong, directoryStore)#music waypoint


            else:
                pass
        if mapmake == False and menu == "multiplayer":
            if sock is None and connect == False:
                threading.Thread(target=run_listener).start()
                kill = False
            multiplayerMapMenu()# create button and playing visualise song chosen send song to other players
        screenDraw()
        clock.tick(60)

main()