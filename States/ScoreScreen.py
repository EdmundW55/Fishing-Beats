from States.BaseState import state
from Entities.Button import *


class ScoreScreen(state):
    def __init__(self, game, scores):
        super().__init__(game)
        self.buttonGroup = buttonG()
        self.scores = scores

    def enter(self):
        back = button(self.game, self.back, 0, self.game.screenHeight - 75, False, self.game.assets.backButton)
        self.buttonGroup.add(back)

    def exit(self):
        pass

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        font = self.game.text.font
        scd = font.render("Score:" + str(self.scores[0]), True, (255, 255, 255))
        w, h = font.size("Score:" + str(self.scores[0]))
        screen.blit(scd, (0, 170 - h))

        ph = font.render("Perfect:" + str(self.scores[1]), True, (255, 255, 255))
        w, h = font.size("Perfect:" + str(self.scores[1]))
        screen.blit(ph, (0, 200))

        eh = font.render("Early:" + str(self.scores[2]), True, (255, 255, 255))
        w2, h2 = font.size("Early:" + str(self.scores[2]))
        hi = h + h2
        screen.blit(eh, (0, 230 + h))

        lh = font.render("Late:" + str(self.scores[3]), True, (255, 255, 255))
        w, h = font.size("Late:" + str(self.scores[3]))
        screen.blit(lh, (0, 260 + hi))
        hi += h

        mh = font.render("Miss:" + str(self.scores[4]), True, (255, 255, 255))
        w, h = font.size("Miss:" + str(self.scores[4]))
        screen.blit(mh, (0, 290 + hi))
        hi += h

        mh = font.render("Max Combo:" + str(self.scores[5]), True, (255, 255, 255))
        screen.blit(mh, (0, 320 + hi))

        mh = font.render("Accuracy:" + str(self.scores[6]), True, (255, 255, 255))
        w, h = font.size("Max Combo:" + str(self.scores[5]))
        screen.blit(mh, (10 + w, 320 + hi))
        self.buttonGroup.draw(screen)