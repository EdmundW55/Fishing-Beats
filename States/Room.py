from Entities.Button import *
from Entities.PlayerDisplay import *
from Managers.ImageLoader import Assets
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

    def enter(self):
        buttonWidth, buttonHeight = self.game.assets.size(self.game.assets.box)
        self.songSelector = button(self.game, self.SelectSong, self.game.screenWidth - buttonWidth, (self.game.screenHeight - buttonHeight)/2,
                        False, self.game.assets.box, text="Select Song")
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
        self.game.push_state(OnlineMapSelect(self.game, self))

    def online(self, operation, data):
        decoded = data.decode()
        if operation == 3:
            player = json.loads(decoded)
            playerDis = PlayerDisplay(self.game, 50, 50 + 75 * len(self.playerGroup), 650, 60, False,
                                   player["player"][0], player["player"][1])
            self.playerGroup.add(playerDis)
        elif operation == 4:
            roomInfo = json.loads(decoded)
            print(roomInfo)
            roomData = roomInfo["room"]
            for count, player in enumerate(roomData["players"]):#
                playerDis = PlayerDisplay(self.game, 50, 50 + 75 * count, 650, 60, player["id"] == roomData["host"],
                              player["id"], player["username"], player["ready"])
                self.playerGroup.add(playerDis)
        elif operation == 5:
            data = json.loads(decoded)
            player = data["player"]
            host = data["host"]
            self.playerGroup.Leave(player, host)
        elif operation == 7:
            data = json.loads(decoded)
            player = data["player"]
            self.playerGroup.Set_Display(player)







