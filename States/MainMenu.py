from States.BaseState import state
from Entities.Button import *
from States.MapSelect import MapSelect
from States.MapMaker import MapMaker
from States.OnlineStart import OnlineStart
from States.Settings import Settings



class MainMenu(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()

    def enter(self):
        spacing = (self.game.screenHeight-200)/5

        playButton = self.game.assets.playButton
        size = self.game.assets.size(playButton)
        play = button(self.game, self.play, (self.game.screenWidth-size[0])/2, spacing, image=playButton)
        self.buttonGroup.add(play)

        size = self.game.assets.size(playButton)
        playOnlineButton = button(self.game, self.play_online, (self.game.screenWidth - size[0]) / 2, spacing*2,
                                  image=playButton)
        self.buttonGroup.add(playOnlineButton)

        mapMakerButton = self.game.assets.mapMaker
        size = self.game.assets.size(mapMakerButton)
        mapMake = button(self.game, self.mapmake, (self.game.screenWidth - size[0]) / 2, spacing*3,
                         image=mapMakerButton)
        self.buttonGroup.add(mapMake)

        settingsButton = self.game.assets.settingsButton
        size = self.game.assets.size(settingsButton)
        settings = button(self.game, self.settings, (self.game.screenWidth - size[0]) / 2, spacing*4,
                          image=settingsButton)
        self.buttonGroup.add(settings)

        exitButton = self.game.assets.exitButton
        size = self.game.assets.size(exitButton)
        exit = button(self.game, self.quit_game, (self.game.screenWidth - size[0]) / 2, spacing*5, image=exitButton)
        self.buttonGroup.add(exit)

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

    def play_online(self):
        self.game.push_state(OnlineStart(self.game))

    def mapmake(self):
        self.game.push_state(MapMaker(self.game))

    def settings(self):
        self.game.push_state(Settings(self.game))

    def quit_game(self):
        self.game.pop_state()