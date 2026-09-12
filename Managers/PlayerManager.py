
class PlayerManager:
    def __init__(self, game):
        self.game = game
        self.manager = {
            0: self.Change_Player_Display,
        }

    def Use(self, data, state):
        print("yhes")
        func = self.manager.get(data["operation"])
        func(data, state)

    def Change_Player_Display(self, data, room):
        print("a")
        playerID = data["player"]
        playerInfo = data["data"]
        print(playerInfo)
        if playerInfo["missing"]:
            room.playerGroup.Set_Display_Map(playerID, "No Map")
        else:
            room.playerGroup.Set_Display_Map(playerID, False)