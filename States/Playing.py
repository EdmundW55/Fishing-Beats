from States.BaseState import state
from Entities.Fish import *
import pygame

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

class FishPoleGroup(pygame.sprite.Group):  # make a group
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

class Playing(state):
    def __init__(self, game):
        super().__init__(game)
        self.score = 0
        self.combo = 0
        self.accuracy = 100

        self.hitnum = 0
        self.earlyNum = 0
        self.lateNum = 0

        self.pole = FishPoleGroup()
        self.fishGroup = fishG()

    def enter(self):
        FishingP = FishingPole(2, self.game)
        self.pole.add(FishingP)
        fish1 = fish(0, 1, 1, 1, self.game.screenWidth)
        self.fishGroup.add(fish1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("q")
                if event.key == pygame.K_w:
                    print("w")

    def update(self, dt):
        self.fishGroup.update()

    def draw(self, screen):
        screen.fill((0,0,0))
        self.pole.draw(screen)
        self.fishGroup.draw(screen)

