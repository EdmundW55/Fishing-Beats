from Entities.Button import *
from Game import Game
from States.BaseState import state
import pygame

from States.RoomSelect import RoomSelect


class OnlineStart(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()
        self.playerName = ""
        self.typing = False
        self.typingBox = pygame.rect.Rect(0, 0, 1, 1)


    def enter(self):
        back = button(self.game, self.back, 0, self.game.screenHeight - 75, False, self.game.assets.backButton)
        enter = button(self.game, self.connect, self.game.screenWidth - 200, self.game.screenHeight - 75, False, self.game.assets.enterButton)
        self.buttonGroup.add(back)
        self.buttonGroup.add(enter)

    def exit(self):
        pass

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)
        for event in events:
            if event.type == pygame.KEYDOWN and self.typing:
                if event.key == pygame.K_RETURN:
                    self.typing = False
                elif event.key == pygame.K_BACKSPACE:
                    self.playerName = self.playerName[:-1]
                else:
                    self.playerName += event.unicode

    def update(self, dt):
        if self.typingBox.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.typing = True

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.buttonGroup.draw(screen)

        nameDis = self.game.text.font.render(f"Name: {self.playerName}", (0, 0, 0), True)
        w, h = self.game.text.font.size(f"Name: {self.playerName}")
        self.typingBox = pygame.rect.Rect(0, 90, self.game.screenWidth, h + 20)
        pygame.draw.rect(screen, (255, 255, 255), self.typingBox)
        screen.blit(nameDis, (0, 100))

    def connect(self):
        # go to room select
        self.game.push_state(RoomSelect(self.game))


