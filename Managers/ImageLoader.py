import pygame
import os
# old code
def ImgLoad(image,num):
    image = image + ".png"
    if num == 1: #things
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
    elif num == 2: #stuff
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (180, 75))
    elif num == 3: #map buttons
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (600,75))
    elif num == 4: #50,50
        imgS = pygame.image.load(os.path.join('Assets', image)).convert_alpha()
        imgS = pygame.transform.scale(imgS, (50,50))
    return imgS

# stores all assets
class Assets():
    def __init__(self):
        self.playButton = ImgLoad("Play_button", 1)
        self.mapMaker = ImgLoad("mapmakebutton", 1)
        self.settingsButton = ImgLoad("SettingsButton", 1)
        self.exitButton = ImgLoad("Menu_Exit", 1)
        self.backButton = ImgLoad("Backbutton", 1)
        self.enterButton = ImgLoad("EnterButton", 1)
        self.fish = ImgLoad("fish", 1)
        self.fish2 = ImgLoad("fish2", 1)
        self.box = ImgLoad("box", 1)
        self.boxSelected = ImgLoad("box_selected", 1)
        self.box2 = ImgLoad("box2", 1)

    def size(self, image):
        return image.get_size()
