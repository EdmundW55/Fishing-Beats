from Game import Game
from States.BaseState import state
import pygame
from Entities.Button import *
from States.MapSelect import MapSelect


class MainMenu(state):
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
        screen.fill((0, 0, 0))
        self.buttonGroup.draw(screen)

    def play(self):
        self.game.push_state(MapSelect(self.game))