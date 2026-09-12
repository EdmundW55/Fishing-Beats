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
        self.readyButton = None
        self.song = ""
        self.host = False
        self.download = False

    def enter(self):
        buttonWidth, buttonHeight = self.game.assets.size(self.game.assets.box)
        self.songSelector = button(self.game, self.SelectSong, self.game.screenWidth - buttonWidth, (self.game.screenHeight - buttonHeight)/2,
                        False, self.game.assets.box, secondImage=self.game.assets.box2, text="Select Song")
        self.readyButton = button(self.game, self.readyUp, self.game.screenWidth - 410, self.game.screenHeight - 75, False,
                       self.game.assets.readyButton, secondImage=self.game.assets.unreadyButton)
        w, _ = self.game.assets.size(self.game.assets.playButton)
        play = button(self.game, self.readyUp, self.game.screenWidth - w, self.game.screenHeight - 75, False,
                      self.game.assets.playButton, secondImage=self.game.assets.playButton)
        back = button(self.game, self.back, 0, self.game.screenHeight - 75, False, self.game.assets.backButton)
        self.buttonGroup.add(self.songSelector)
        self.buttonGroup.add(self.readyButton)
        self.buttonGroup.add(play)
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
        if self.ready:
            self.readyButton.swap_image(1)
        else:
            self.readyButton.swap_image(0)
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

    def downloaded(self):
        songName = self.song.split("-", 1)[1]
        self.songSelector.change_text(songName)
        self.game.music.set_song(self.song, songName)
        self.game.music.play()
        data = {
            "player": self.game.playerID,
            "operation": 0,
            "data": {
                "missing": False
            }
        }

        jsonData = json.dumps(data).encode("utf-8")
        self.game.network.send_data(15, jsonData)

    def play(self):
        pass
        # send message to sever to start game
        # send message to server to start
        # players send data back when map is loaded?

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
        elif operation == 11:
            self.game.file.Start_File(data)
        elif operation == 12:
            self.game.file.Get_Chunk(data)
        elif operation == 13:
            decoded = data.decode()
            if decoded == "":
                self.game.file.End_File(self)
                return

            data = json.loads(decoded)
            dir = data["map"]
            print(dir)
            self.song = dir
            check = self.game.file.Check_File(dir)
            if not check:
                self.download = True
                self.songSelector.change_text("Missing Map", 1)
                data = {
                    "player": self.game.playerID,
                    "operation": 0,
                    "data": {
                        "missing": True
                    }
                }
                print(data)
                jsonData = json.dumps(data).encode("utf-8")
                self.game.network.send_data(15, jsonData)
        elif operation == 14:
            decoded = self.game.network.decode_data("!?", data)[0]
            if decoded:
                songName = self.song.split("-", 1)[1]
                self.songSelector.change_text(songName)
                self.game.music.set_song(self.song, songName)
                self.game.music.play()
            else:
                self.download = True
                data = {
                    "player": self.game.playerID,
                    "operation": 0,
                    "data": {
                        "missing": True
                    }
                }

                jsonData = json.dumps(data).encode("utf-8")
                self.game.network.send_data(15, jsonData)
                self.songSelector.change_text("Missing Map", 1)
        elif operation == 15:
            decoded = data.decode()
            jsonData = json.loads(decoded)
            self.game.player.Use(jsonData, self)









