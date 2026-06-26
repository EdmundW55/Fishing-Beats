import pygame

class fish(pygame.sprite.Sprite):
    def __init__(self, pos, lane, size, speed, sx, play):#position,if it can shoot and what kind of enemy
        super().__init__()
        if size == 1:
            self.image = play.game.assets.fish
        elif size == 2:
            self.image = play.game.assets.fish2
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [pos, ((lane * 50) + (lane - 1) * 70 + 400)]
        self.size = size
        self.lane = lane
        self.speed = speed
        self.sx = sx
        self.tap = 0
        self.comboL = False
        self.play = play

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= (self.sx - 320) and self.comboL == False:
            self.play.getScore("AMiss")
            self.comboL = True

        if self.rect.x >= self.sx:
            self.kill()



    def disappear(self):
        result = None
        if self.rect.topright[0] >= self.sx - 325:
            print("a")
            if self.rect.x == (self.sx - 400):
                self.tap += 1
                result = "APerfect"

            elif self.rect.x <= (self.sx - 365):
                self.tap += 1
                result = "AGood"

            elif self.rect.x <= (self.sx - 340):
                self.tap += 1
                result = "LOk"

            elif self.rect.x <= (self.sx - 325):
                self.tap += 1
                result = "LEh"

        else:
            print("buh")
            if self.rect.topright[0] <= (self.sx - 390):
                self.tap += 1
                result = "EBad"

            elif self.rect.topright[0] <= (self.sx - 375):
                self.tap += 1
                result = "EEh"

            elif self.rect.topright[0] <= (self.sx - 350):
                self.tap += 1
                result = "EOk"

            elif self.rect.topright[0] <= (self.sx - 325):
                self.tap += 1
                result = "AGood"

        self.play.getScore(result)
        if self.size == self.tap:
            self.kill()

    def echeck(self):
        # Eel check
        return False

class fishG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        for sprite in self:
            sprite.update()

