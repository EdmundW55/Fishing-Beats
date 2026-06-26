import pygame
import sys
from Managers import ImageLoader

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.states = []
        self.screenWidth, self.screenHeight = pygame.display.get_window_size()
        self.assets = ImageLoader.Assets()

    def push_state(self, state):
        self.states.append(state)
        state.enter()

    def pop_state(self):
        state = self.states.pop()
        state.exit()

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            dt = self.clock.tick(60) / 1000
            self.states[-1].handle_events(events)
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

