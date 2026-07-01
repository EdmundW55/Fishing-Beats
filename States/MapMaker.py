from Entities.Button import *
from States.BaseState import state
import pygame
class MapSelect(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()

    def enter(self):
        play = button(self.game, self.play, 0, 0)
        self.buttonGroup.add(play)

    def exit(self):
        pass

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)

    def update(self, dt):
        pass

    def draw(self, screen):
        self.buttonGroup.draw(screen)