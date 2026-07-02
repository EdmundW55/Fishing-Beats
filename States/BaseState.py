class state():
    def __init__(self, game):
        self.game = game

    def enter(self):
        """
        Updates when first entering state
        """
        pass

    def exit(self):
        """
        Updates when exiting state
        """
        pass

    def back(self):
        self.game.pop_state()

    def handle_events(self, events):
        """
        Key presses in this state
        """
        pass

    def update(self, dt):
        """
        Key presses in this state
        """
        pass

    def draw(self, screen):
        """
        Drawing on screen
        """
        pass
