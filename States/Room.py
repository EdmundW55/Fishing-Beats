from Entities.Button import *
from States.BaseState import state
import json

class Room(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()


    def enter(self):
        back = button(self.game, self.back, 0, self.game.screenHeight - 75, False, self.game.assets.backButton)
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

    def online(self, operation, data):
        if operation == 1:
            decoded = data.decode()
            room_info = json.loads(decoded)
            rooms = room_info["rooms"]
            for count, room in enumerate(rooms):
                roomButton = button(self.game, self.back, 0, 10 + 100 * count, False, text = room["code"])
                self.buttonGroup.add(roomButton)



