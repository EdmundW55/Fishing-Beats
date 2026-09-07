import pygame
import sys
from Managers import ImageLoader, TextManager, NetworkManager, FileManager, MusicManager


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.states = []
        self.songStore = []
        self.screenWidth, self.screenHeight = pygame.display.get_window_size()
        self.assets = ImageLoader.Assets()
        self.text = TextManager.TextManager()
        self.network = NetworkManager.NetworkManager(self)
        self.file = FileManager.FileManager(self)
        self.music = MusicManager.MusicManager(self)
        self.running = True

        self.playerID = -1
        self.playerUsername = ""

    def push_state(self, state):
        self.states.append(state)
        state.enter()

    def pop_state(self):
        state = self.states.pop()
        state.exit()

    def updateScreen(self):
        self.states[-1].draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            dt = self.clock.tick(60) / 1000
            try:
                self.states[-1].handle_events(events)
                self.states[-1].update(dt)
                self.states[-1].draw(self.screen)
            except IndexError as e:
                print(e)
                self.running = False

            pygame.display.flip()
        print("a")
        pygame.quit()
        sys.exit()

