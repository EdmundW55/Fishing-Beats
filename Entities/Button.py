import pygame
from sympy import false


class button(pygame.sprite.Sprite):
    def __init__(self, game, action, x, y, scroll = False):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([75, 75])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [x, y]
        self.originalY = self.rect.y
        self.action = action
        self.scrollToggle = scroll

    def handle_event(self, events, group):
        # if press mouse down
        for event in events:
            if not self.rect.collidepoint(pygame.mouse.get_pos()) and self.scroll:
                group.scrolling = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if click button
                if pygame.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(event.pos):
                        # run function
                        self.action()
            elif event.type == pygame.MOUSEWHEEL and self.scrollToggle:
                if pygame.mouse.get_pos()[0] > pygame.display.get_window_size()[0]/2:
                    # scroll up and down
                    group.scrolling = True
                    group.scroll(event.y)




    def scroll(self, amount, top = False):
        if not top:
            if self.scrollToggle:
                if self.rect.y + (amount*20) < self.originalY:
                    self.rect.y += amount*20
                else:
                    self.rect.y = self.originalY
        else:
            if self.scrollToggle:
                self.rect.y -= amount


class buttonG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)
        self.scrolling = False

    def handle_event(self, event, group):
        for sprite in self:
            sprite.handle_event(event, group)

    def scroll(self, amount):
        last_sprite = self.sprites()[-1]
        for sprite in self:
            if last_sprite.rect.y + amount*20 > 0:
                sprite.scroll(amount)
            elif last_sprite.rect.y + amount*20 < 0 and last_sprite.rect.y != 0:
                sprite.scroll(last_sprite.rect.y, True)
