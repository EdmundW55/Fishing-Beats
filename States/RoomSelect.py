from Entities.Button import *
from States.BaseState import state
from States.Room import Room
import pygame
import json

class RoomSelect(state):
    def __init__(self, game):
        super().__init__(game)
        self.buttonGroup = buttonG()


    def enter(self):
        back = button(self.game, self.back, 0, self.game.screenHeight - 75, False, self.game.assets.backButton)
        self.buttonGroup.add(back)
        self.game.network.send_data(1)

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
                roomButton = button(self.game, self.join_room, 0, 10 + 100 * count, False, text = room["code"],
                                    extraData=room["code"], textColour=(0, 0, 0))
                self.buttonGroup.add(roomButton)
        elif operation == 3:
            decoded = self.game.network.decode_data("B", data)[0]
            if not decoded:
                self.game.push_state(Room(self.game))

    def join_room(self, room):
        dataFormat = f'!BI{len(room)}s'
        self.game.network.send_data(3, len(room), room.encode("utf-8"), addedData=dataFormat)






