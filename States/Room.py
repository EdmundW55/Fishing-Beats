from Entities.Button import *
from Entities.PlayerDisplay import *
from States.BaseState import state
import json
from States.OnlineMapSelect import OnlineMapSelect


class Room(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()
        self.playerGroup = PlayerDisplayG()
        self.ready = False
        self.songSelector = None
        self.song = ""
        self.host = False
        self.download = False

    def enter(self):
        buttonWidth, buttonHeight = self.game.assets.size(self.game.assets.box)
        self.songSelector = button(self.game, self.SelectSong, self.game.screenWidth - buttonWidth, (self.game.screenHeight - buttonHeight)/2,
                        False, self.game.assets.box, secondImage=self.game.assets.box2, text="Select Song")
        ready = button(self.game, self.readyUp, self.game.screenWidth - 410, self.game.screenHeight - 75, False,
                       self.game.assets.readyButton, secondImage=self.game.assets.unreadyButton)
        back = button(self.game, self.back, 0, self.game.screenHeight - 75, False, self.game.assets.backButton)
        self.buttonGroup.add(self.songSelector)
        self.buttonGroup.add(ready)
        self.buttonGroup.add(back)
        self.game.network.send_data(4)

    def exit(self):
        pass

    def handle_events(self, events):
        self.buttonGroup.handle_event(events, self.buttonGroup)

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.buttonGroup.draw(screen)
        self.playerGroup.draw(screen)

    def readyUp(self):
        self.ready = not self.ready
        self.game.network.send_data(7, self.ready.to_bytes())

    def back(self):
        self.game.network.send_data(5)
        self.game.pop_state()

    def SelectSong(self):
        if self.host:
            self.game.push_state(OnlineMapSelect(self.game, self))
        else:
            if self.download:
                self.game.network.send_data(6)

    def online(self, operation, data):
        if operation == 3:
            decoded = data.decode()
            player = json.loads(decoded)
            playerDis = PlayerDisplay(self.game, 50, 50 + 75 * len(self.playerGroup), 650, 60, False,
                                   player["player"][0], player["player"][1])
            self.playerGroup.add(playerDis)
        elif operation == 4:
            decoded = data.decode()
            roomInfo = json.loads(decoded)
            print(roomInfo)
            roomData = roomInfo["room"]
            for count, player in enumerate(roomData["players"]):#
                playerDis = PlayerDisplay(self.game, 50, 50 + 75 * count, 650, 60, player["id"] == roomData["host"],
                              player["id"], player["username"], player["ready"])
                self.playerGroup.add(playerDis)
            if roomData["host"] != self.game.playerID:
                if self.songSelector:
                    self.host = False
            else:
                self.host = True
        elif operation == 5:
            decoded = data.decode()
            data = json.loads(decoded)
            player = data["player"]
            host = data["host"]
            self.playerGroup.Leave(player, host)
            if host == self.game.playerID:
                self.host = True
        elif operation == 7:
            decoded = data.decode()
            data = json.loads(decoded)
            player = data["player"]
            self.playerGroup.Set_Display(player)
        elif operation == 13:
            decoded = data.decode()
            data = json.loads(decoded)
            dir = data["map"]
            print(dir)
            self.song = dir
            self.game.file.Check_File(dir)
        elif operation == 14:
            decoded = self.game.network.decode_data("!?", data)[0]
            if decoded:
                songName = self.song.split("-", 1)[1]
                self.songSelector.change_text(songName)
                self.game.music.set_song(self.song, songName)
                self.game.music.play()
            else:
                self.download = True
                self.songSelector.change_text("Missing Map", 1)




