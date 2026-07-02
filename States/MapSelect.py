from States.BaseState import state
from Entities.Button import *
from States.Playing import Playing
import os
from pygame import mixer

class MapSelect(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()


    def enter(self):
        box = self.game.assets.box
        selectedBox = self.game.assets.box2
        mapsList = os.listdir("Maps")
        for folder in mapsList:
            # only show songs with a map
            song = folder.split("-", 1)[1]
            path = "Maps/"+folder+"/"+song+".txt"
            if os.path.isfile(path):
                mapButton = button(self.game, self.play_map, self.game.screenWidth-self.game.assets.size(box)[0], len(self.buttonGroup)*75,
                                   True, box, folder)
                self.buttonGroup.add(mapButton)

        back = button(self.game, self.back, 0, self.game.screenHeight-75, False)
        self.buttonGroup.add(back)

    def exit(self):
        pass

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))

        self.buttonGroup.draw(screen)

    def play_map(self, directory):
        song = directory.split("-", 1)[1]
        self.game.push_state(Playing(self.game, song, directory))

    def scroll_maps(self, amount):
        self.buttonGroup.scroll(amount)

    def play_song(self, entity):
        song = entity.directory.split("-", 1)[1]
        self.buttonGroup.reset(entity)
        print(song, entity.directory)
        mixer.music.load(os.path.join("Maps/"+entity.directory, song+".mp3"))
        mixer.music.set_volume(0.5)
        mixer.music.play()