import pygame
from sympy import false


class button(pygame.sprite.Sprite):
    def __init__(self, game, action, x, y, scroll = False, image = None, directory = None, secondImage = None, text = None):
        super().__init__()
        self.game = game
        if image is not None:
            # make all images independent
            self.image = image.copy()
            self.imageStore = [image.copy()]
            if secondImage is not None:
                self.imageStore.append(secondImage.copy())
            else:
                self.imageStore.append(image.copy())
        else:
            self.image = pygame.Surface([75, 75])
            self.image.fill((255, 255, 255))
            self.imageStore = [pygame.Surface([75, 75]), pygame.Surface([75, 75])]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [x, y]
        self.swap = 0
        self.originalY = self.rect.y
        self.action = action
        self.scrollToggle = scroll
        self.directory = directory

        if self.directory is not None:
            song = self.directory.split("-", 1)[1]
            self.text = self.game.text.smallFont.render(song, True, (255, 255, 255))
            w, h = self.game.text.smallFont.size(song)
            self.image.blit(self.text, (10, (self.rect.height-h)/2))
        elif text is not None:
            self.text = self.game.text.smallFont.render(text, True, (255, 255, 255))
            w, h = self.game.text.smallFont.size(text)
            self.image.blit(self.text, (10, (self.rect.height - h) / 2))

        self.textStore = text

    def handle_event(self, events, group):
        # if press mouse down
        for event in events:
            if not self.rect.collidepoint(pygame.mouse.get_pos()) and self.scroll:
                group.scrolling = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if click button
                if pygame.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(event.pos):
                        if self.directory is not None:
                            self.action(self.directory, self)
                        else:
                            self.action()
            elif event.type == pygame.MOUSEWHEEL and self.scrollToggle:
                if pygame.mouse.get_pos()[0] > pygame.display.get_window_size()[0]/2:
                    # scroll up and down
                    group.scrolling = True
                    group.scroll(event.y)




    def scroll(self, amount, top = False):
        if not top:
            if self.scrollToggle:
                if self.rect.y + (amount*10) < self.originalY:
                    self.rect.y += amount*10
                else:
                    self.rect.y = self.originalY
        else:
            if self.scrollToggle:
                self.rect.y -= amount

    def swap_image(self, img):
        self.image = self.imageStore[img]
        if self.directory is not None:
            song = self.directory.split("-", 1)[1]
            self.text = self.game.text.smallFont.render(song, True, (255, 255, 255))
            w, h = self.game.text.smallFont.size(song)
            self.image.blit(self.text, (10, (self.rect.height-h)/2))


class buttonG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)
        self.scrolling = False
        self.lastSprite = None

    def handle_event(self, event, group):
        for sprite in self:
            sprite.handle_event(event, group)

    def scroll(self, amount):
        for sprite in self:
            if self.lastSprite.rect.y + amount*10 > 0:
                sprite.scroll(amount)
            elif self.lastSprite.rect.y + amount*10 < 0 and self.lastSprite.rect.y != 0:
                sprite.scroll(self.lastSprite.rect.y, True)

    def lastSpriteCheck(self):
        self.lastSprite = self.sprites()[-1]
        for sprite in reversed(self.sprites()):
            if sprite.scrollToggle:
                self.lastSprite = sprite
                break

    def swap_image(self, entity):
        for sprite in self:
            if sprite == entity:
                sprite.swap_image(1)
            else:
                sprite.swap_image(0)
