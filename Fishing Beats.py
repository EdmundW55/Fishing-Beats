import pygame
import os
from Game import Game
from States.MainMenu import MainMenu

def main():
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.init()
    except pygame.error as e:
        pygame.mixer.quit()
        os.environ["SDL_AUDIODRIVER"] = "directsound"
        pygame.mixer.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fishing Beats")
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.push_state(MainMenu(game))

    game.run()


if __name__ == "__main__":
    main()
