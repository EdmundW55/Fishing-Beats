from States.BaseState import state
from Entities.Fish import *
from Entities.Button import *
import pygame
from pygame import mixer
import os

from States.ScoreScreen import ScoreScreen


class FishingPole(pygame.sprite.Sprite):
    def __init__(self, lane, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([75,75])
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = [game.screenWidth - 400,((lane*50) + (lane-1)*70 + 400)]
        self.lane = lane
        self.buffer = 0
        self.disable1 = False
        self.hold = False
        self.disable2 = False
        self.buffer = 0

    def update(self, up):
        if up:
            if self.lane != 1:
                self.lane -= 1
                self.buffer = 12
        else:
            if self.lane != 3:
                self.lane += 1
                self.buffer = 12

        self.rect.x,self.rect.y = [self.game.screenWidth - 400,((self.lane*50) + (self.lane-1)*70 + 400)]

    def click(self, fish):
        if pygame.sprite.spritecollide(self, fish, False):
            fishlist = pygame.sprite.spritecollide(self, fish, False)
            for sprite in fishlist:
                ec = sprite.echeck() # eel check
                if not ec:
                    if len(fishlist) >= 2:
                        posfish = list(map(poscheck, fishlist))
                        idx = posfish.index(max(posfish))
                        fishlist[idx].disappear()
                        fishlist.remove(fishlist[idx])
                    else:
                        sprite.disappear()
                else:
                    sprite.disappear()



def poscheck(self):
    return self.rect.x

class FishPoleGroup(pygame.sprite.Group):  # make a group
    def __init__(self, *args):
        super().__init__(*args)

    def update(self, direction):
        for sprite in self:
            sprite.update(direction)

    def click(self, fish):
        for sprite in self:
            sprite.click(fish)

    def reset(self):
        for sprite in self:
            sprite.reset()

class Playing(state):
    def __init__(self, game, song, directory):
        super().__init__(game)
        self.score = 0
        self.combo = 0
        self.accuracy = 100

        self.hitNum = 0
        self.earlyNum = 0
        self.lateNum = 0
        self.missNum = 0
        self.maxCombo = 0

        self.pole = FishPoleGroup()
        self.fishGroup = fishG()
        self.buttonGroup = buttonG()

        self.directory = directory
        self.song = song

    def enter(self):
        FishingP = FishingPole(2, self.game)
        exitmap = button(self.game, self.quit, 200, 200)
        self.buttonGroup.add(exitmap)

        self.pole.add(FishingP)
        self.mapPlay(self.song + ".mp3", "Maps/"+self.directory)

    def quit(self):
        self.game.pop_state()

    def exit(self):
        if len(self.fishGroup) <= 0:
            scores = [self.score, self.hitNum, self.earlyNum, self.lateNum, self.missNum, self.maxCombo, self.accuracy]
            self.game.push_state(ScoreScreen(self.game, scores))
        else:
            mixer.music.unload()


    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.pole.click(self.fishGroup)
                if event.key == pygame.K_w:
                    self.pole.click(self.fishGroup)

                if event.key == pygame.K_UP:
                    self.pole.update(True)
                if event.key == pygame.K_DOWN:
                    self.pole.update(False)

    def update(self, dt):
        self.fishGroup.update()
        if len(self.fishGroup) <= 0:
            self.game.updateScreen()
            pygame.mixer.music.fadeout(2500)
            mixer.music.unload()
            self.quit()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        scoreDis = self.game.text.font.render(str(self.score), True, (255, 255, 255))
        comboDis = self.game.text.font.render("x" + str(self.combo), True, (255, 255, 255))

        screen.blit(scoreDis, (0, 0))
        screen.blit(comboDis, (0, 100))
        self.fishGroup.draw(screen)
        self.pole.draw(screen)
        self.buttonGroup.draw(screen)

    def getScore(self, result):
        earlyLate = result[0]
        result = result[1:]
        if result == "Perfect":
            self.combo += 1
            self.score += 120 * self.combo
            self.hitNum += 1

        elif result == "Good":
            self.combo += 1
            self.score += 100 * self.combo
            self.hitNum += 1

        elif result == "Ok":
            self.combo += 1
            self.score += 75 * self.combo

        elif result == "Eh":
            self.combo += 1
            self.score += 25 * self.combo

        elif result == "Bad":
            self.maxCombo = self.combo
            self.combo = 0

        elif result == "Miss":
            self.maxCombo = self.combo
            self.combo = 0
            self.missNum += 1

        if earlyLate == "E":
            self.earlyNum += 1
        elif earlyLate == "L":
            self.lateNum += 1

    def mapPlay(self, song, directory):
        # e.g. Jamie Paige - BIRDBRAIN (Cover By Evil).mp3, Maps/53508563-Jamie Paige - BIRDBRAIN (Cover By Evil)
        fishes = []
        print(song, directory)
        file = ""
        split = song.split(".")
        # finds the txt file for the level
        if len(split) > 2:
            for x in split:
                if x != "mp3":
                    file = file + x + "."
            file = file + "txt"
        else:
            file = split[0] + ".txt"
        # reads file and gets content
        print(directory, file)
        smp = open((os.path.join(directory, file)), "r")
        content = smp.readlines()
        # gets all the fish
        for count in content:
            entity = count.split()
            fishes.append(entity)
        for count in fishes:
            if count[0] == "fish":
                fishEntity = fish(int(count[1]), int(count[2]), int(count[3]), int(count[4]), self.game.screenWidth, self)  # (pos, lane, size, speed)
                self.fishGroup.add(fishEntity)

        mixer.music.load(os.path.join(directory, song))
        mixer.music.set_volume(0.5)
        mixer.music.play()

