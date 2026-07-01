from Game import Game
from States.BaseState import state
from Entities.Button import *
import pygame
from States.Playing import Playing

class MapSelect(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()

    def enter(self):
        play = button(self.game, self.play_map, 0, 0, True)
        play2 = button(self.game, self.play_map, 0, 50, True)
        back = button(self.game, self.back, 0, self.game.screenHeight-50, True)
        self.buttonGroup.add(play)
        self.buttonGroup.add(play2)
        self.buttonGroup.add(back)

    def exit(self):
        pass

    def back(self):
        self.game.pop_state()

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.buttonGroup.draw(screen)

    def play_map(self):
        self.game.push_state(Playing(self.game))

    def scroll_maps(self, amount):
        self.buttonGroup.scroll(amount)