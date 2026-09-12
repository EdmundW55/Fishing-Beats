import pygame


class PlayerDisplay(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, leader, playerID, text = None, ready = False):
        super().__init__()
        self.game = game

        # make all images independent
        self.image = self.game.assets.playerDisplay.copy()
        self.imageStore = [self.game.assets.playerDisplay.copy(), self.game.assets.playerDisplayReady.copy(),
                           self.game.assets.playerDisplayNoMap.copy()]
        if ready:
            self.image = self.imageStore[1]

        self.leader = leader
        if leader:
            self.image.blit(self.game.assets.crown, (self.image.get_width() - self.game.assets.crown.get_width() - 20,
                                       self.image.get_height() / 2 - self.game.assets.crown.get_height() / 2))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [x, y]

        self.text = self.game.text.smallFont.render(text, True, (255, 255, 255))
        w, h = self.game.text.smallFont.size(text)
        self.image.blit(self.text, (10, (self.rect.height - h) / 2))
        self.textStore = text

        self.playerID = playerID

    def Set_Display(self, state):
        print(state)
        if state == True:
            self.image = self.imageStore[1]
        elif not state:
            self.image = self.imageStore[0]
        elif state == "No Map":
            self.image = self.imageStore[2]

        if self.leader:
            self.image.blit(self.game.assets.crown, (self.image.get_width() - self.game.assets.crown.get_width() - 20,
                            self.image.get_height() / 2 - self.game.assets.crown.get_height() / 2))
        self.text = self.game.text.smallFont.render(self.textStore, True, (255, 255, 255))
        w, h = self.game.text.smallFont.size(self.textStore)
        self.image.blit(self.text, (10, (self.rect.height - h) / 2))

    def Reorder(self, index, host = None):
        self.rect.x, self.rect.y = [50, 50 + 75 * index]
        if host is not None:
            print(host)
            if self.playerID == host:
                self.leader = True
                self.image.blit(self.game.assets.crown,(self.image.get_width() - self.game.assets.crown.get_width() - 20,
                                 self.image.get_height() / 2 - self.game.assets.crown.get_height() / 2))

    def Leave(self, group, host):
        self.kill()
        group.Reorder(host)


class PlayerDisplayG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)

    def Set_Display(self, player):
        for sprite in self:
            if sprite.playerID == player[0]:
                state = bool.from_bytes(player[1].encode('utf-8'), byteorder='big')
                sprite.Set_Display(state)

    def Set_Display_Map(self, player, state):
        for sprite in self:
            if sprite.playerID == player:
                sprite.Set_Display(state)

    def Reorder(self, host = None):
        for count, sprite in enumerate(self):
            sprite.Reorder(count, host)

    def Leave(self, player, host):
        for sprite in self:
            if sprite.playerID == player[0]:
                sprite.Leave(self, host)
