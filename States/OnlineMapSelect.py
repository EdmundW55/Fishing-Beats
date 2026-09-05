from Game import Game
from States.BaseState import state
from Entities.Button import *
from States.Playing import Playing
import os
from pygame import mixer

class OnlineMapSelect(state):
    def __init__(self, game, OnlineRoom):
        super().__init__(game)
        self.buttonGroup = buttonG()
        self.songStore = ["", ""]
        self.pressed = None
        self.fishCountNum = 0
        self.eelCountNum = 0
        self.lengthOfSong = 0
        self.room = OnlineRoom
        self.newSong = False

    def enter(self):
        box = self.game.assets.box
        selectedBox = self.game.assets.boxSelected
        mapsList = os.listdir("Maps")
        for folder in mapsList:
            # only show songs with a map
            song = folder.split("-", 1)[1]
            path = "Maps/"+folder+"/"+song+".txt"
            if os.path.isfile(path):
                mapButton = button(self.game, self.play_map, self.game.screenWidth-self.game.assets.size(box)[0], 100 +
                                   len(self.buttonGroup)*75, True, box, folder, selectedBox)
                self.buttonGroup.add(mapButton)
        self.buttonGroup.lastSpriteCheck()
        back = button(self.game, self.back, 0, self.game.screenHeight-75, False, self.game.assets.backButton)
        self.buttonGroup.add(back)

    def exit(self):
        if self.room.songSelector is not None and self.songStore != ["", ""]:
            if self.songStore != self.game.songStore:
                mixer.music.load(os.path.join(self.game.songStore[0], self.game.songStore[1] + ".mp3"))
                mixer.music.set_volume(0.5)
                mixer.music.play(-1)
            else:
                self.room.songSelector.change_text(self.songStore[1])
                self.game.network.send_map()

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)

    def update(self, dt):
        pass

    def draw(self, screen):
        font = self.game.text.font
        screen.fill((0, 0, 0))
        self.buttonGroup.draw(screen)
        if self.songStore[1] != "":
            mapName = font.render(self.songStore[1], True, (255, 255, 255))
            w, h = font.size(self.songStore[1])
            screen.blit(mapName, (0, 0))

            MapLength = font.render("Length:"+str(self.lengthOfSong), True, (255, 255, 255))
            screen.blit(MapLength, (0, h - 5))
            w2, h2 = font.size("Length:"+str(self.lengthOfSong))

            FishCount = font.render("Fish:"+str(self.fishCountNum), True, (255, 255, 255))
            screen.blit(FishCount, (0, h+h2-5))
            wf, hf = font.size("Fish:"+str(self.fishCountNum))

            EelCount = font.render("Eels:"+str(self.eelCountNum), True, (255, 255, 255))
            screen.blit(EelCount, (wf+5, h+h2-5))


    def play_map(self, entity):
        if self.pressed == entity:
            self.pressed = None
            if self.game.songStore != self.songStore:
                self.game.songStore = self.songStore
                self.newSong = True
            self.game.pop_state()
            print(f"playing {self.songStore[0], self.songStore[1]}.mp3")
        else:
            self.pressed = entity
            self.play_song(entity)


    def scroll_maps(self, amount):
        self.buttonGroup.scroll(amount)

    def play_song(self, entity):
        song = entity.directory.split("-", 1)[1]
        directory = "Maps/"+entity.directory
        self.songStore = [directory, song]
        self.buttonGroup.swap_image(entity)
        openMap = open((os.path.join(directory, (song + ".txt"))), "r")
        lines = openMap.read().splitlines()
        if lines != []:
            last_line = lines[-1]
            openMap.close()
            splitStats = last_line.split(" ")
            self.fishCountNum = splitStats[0]
            self.eelCountNum = splitStats[1]
            self.lengthOfSong = splitStats[2]

        mixer.music.load(os.path.join("Maps/"+entity.directory, song+".mp3"))
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        print(f"playing {entity.directory, song}.mp3")