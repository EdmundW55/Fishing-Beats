import pygame

class fish(pygame.sprite.Sprite):
    def __init__(self, pos, lane, size, speed, sx):#position,if it can shoot and what kind of enemy
        super().__init__()
        if size == 1:
            self.image = pygame.surface.Surface([75, 75])
        elif size == 2:
            self.image = pygame.surface.Surface([75, 75])
        self.image.fill((0,255,255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [pos, ((lane * 50) + (lane - 1) * 70 + 400)]
        self.size = size
        self.lane = lane
        self.speed = speed
        self.sx = sx

    def update(self):
        self.rect.x += self.speed

        if self.rect.x >= self.sx:
            self.kill()

    '''def disappear(self):
        if self.rect.topright[0] >= sx - 325:
            if self.rect.x == (sx - 400):
                combo += 1
                score += 120 * combo
                hitnum += 1
                self.tap += 1

            elif self.rect.x <= (sx - 375):
                combo += 1
                score += 100 * combo
                hitnum += 1
                self.tap += 1

            elif self.rect.x <= (sx - 350):
                combo += 1
                score += 75 * combo
                latenum += 1
                self.tap += 1

            elif self.rect.x <= (sx - 325):
                combo += 1
                score += 25 * combo
                latenum += 1
                self.tap += 1

        else:
            if self.rect.topright[0] <= (sx - 390):
                combo = 0
                earlynum += 1
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 375):
                combo += 1
                score += 25 * combo
                earlynum += 1
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 350):
                combo += 1
                score += 75 * combo
                earlynum += 1
                self.tap += 1

            elif self.rect.topright[0] <= (sx - 325):
                combo += 1
                score += 100 * combo
                hitnum += 1
                self.tap += 1

        if self.size == self.tap:
            self.kill()'''

class fishG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        for sprite in self:
            sprite.update()

