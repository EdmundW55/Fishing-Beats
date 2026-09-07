from pygame import mixer
import os

class MusicManager:
    def __init__(self, game):
        self.game = game
        self.directory = ""
        self.song = ""

    def set_song(self, directory, song):
        self.directory = "Maps/" + directory
        self.song = song + ".mp3"

    def play(self):
        mixer.music.load(os.path.join(self.directory, self.song))
        mixer.music.set_volume(0.5)
        mixer.music.play()