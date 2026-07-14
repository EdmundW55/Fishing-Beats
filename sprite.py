import pygame
import sys
import os

pygame.init()
pygame.font.init()
try:
    pygame.mixer.init()
except pygame.error as e:
    pygame.mixer.quit()
    os.environ["SDL_AUDIODRIVER"] = "directsound"
    pygame.mixer.init()

class button(pygame.sprite.Sprite):
    def __init__(self, x, y, action, text = None):
        super().__init__()
        self.image = pygame.Surface([120, 75])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [x, y]
        if action == "type":
            self.action = self.selectType
        elif action == "sprite":
            self.action = self.selectSprite
        elif action == "chest":
            self.action = self.chestEnter
        elif action == "clear":
            self.action = self.clear
        self.id = text
        if text is not None:
            self.text = smallFont.render(text, True, (0, 0, 0))
            w, h = smallFont.size(text)
            self.image.blit(self.text, (5, (self.rect.height - h) / 2))

    def handle_event(self, events):
        # if press mouse down
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if click button
                if pygame.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(event.pos):
                        self.action()

    def selectType(self):
        global sprTyp
        sprTyp = self.id
        button_group.reset(spriteType)
        self.image.fill((0, 0, 255))
        self.text = smallFont.render(self.id, True, (0, 0, 0))
        w, h = smallFont.size(self.id)
        self.image.blit(self.text, (5, (self.rect.height - h) / 2))


    def selectSprite(self):
        global spriteVariant
        spriteVariant = self.id
        button_group.reset(sprites)
        self.image.fill((0, 0, 255))
        self.text = smallFont.render(self.id, True, (0, 0, 0))
        w, h = smallFont.size(self.id)
        self.image.blit(self.text, (5, (self.rect.height - h) / 2))


    def chestEnter(self):
        global chest, opened, spritesCollected, spriteVariant, sprTyp
        chest = self.id
        button_group.reset(chestType)
        self.image.fill((0, 0, 255))
        self.text = smallFont.render(self.id, True, (0, 0, 0))
        w, h = smallFont.size(self.id)
        self.image.blit(self.text, (5, (self.rect.height - h) / 2))
        with open("sprites.txt", "a") as f:
            if sprTyp == "nothing":
                spriteVariant = "nothing"
            f.write(f'{sprTyp}, {spriteVariant}, {chest}\n')
        opened += 1
        if sprTyp != "nothing":
            spritesCollected += 1

        sprTyp = "nothing"
        spriteVariant = "nothing"
        chest = "chest"
        button_group.reset(spriteType)
        button_group.reset(sprites)
        button_group.reset(chestType)


    def reset(self, group):
        if self.id in group:
            self.image.fill((255, 255, 255))
            self.text = smallFont.render(self.id, True, (0, 0, 0))
            w, h = smallFont.size(self.id)
            self.image.blit(self.text, (5, (self.rect.height - h) / 2))

    def clear(self):
        global spritesCollected, opened
        try:
            with open("sprites.txt", "r+") as f:
                f.seek(0)
                f.truncate()
                spritesCollected = 0
                opened = 0
        except FileNotFoundError:
            pass


class buttonG(pygame.sprite.Group):#make a group
    def __init__(self, *args):
        super().__init__(*args)
        self.scrolling = False
        self.lastSprite = None

    def handle_event(self, event):
        for sprite in self:
            sprite.handle_event(event)

    def reset(self, group):
        for sprite in self:
            sprite.reset(group)


smallFont = pygame.font.SysFont("gadugi", 25)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Fishing Beats")
clock = pygame.time.Clock()
running = True
button_group = buttonG()

spriteType = ["normal", "gold", "gummy", "galaxy", "holofoil", "nothing"]
sprites = ["water", "fire", "earth", "fishstick", "duck", "ghost", "demon", "king", "aura", "football", "dream", "punk",
           "boss", "peanut", "zero point", "grim"]
chestType = ["sprite chest", "rare chest", "chest", "elim", "wandering"]

sprTyp = "nothing"
spriteVariant = "nothing"
chest = "chest"


for count, x in enumerate(spriteType):
    b = button(20 + count * 140, 20, "type", x)
    button_group.add(b)
i = 0
for count, s in enumerate(sprites):
    if count > 10:
        i = 1
    b = button(20 + (count - (i * 11)) * 140, 140 + i*120, "sprite", s)
    button_group.add(b)

for count, c in enumerate(chestType):
    b = button(20 + count * 140, 380, "chest", c)
    button_group.add(b)

b = button(20, 500, "clear", "clear")
button_group.add(b)
spritesCollected = 0
opened = 0
spriteData = {"Source":{"chest": [0,0], "sprite chest": [0, 0], "rare chest": [0, 0], "elim": [0,0], "wandering": [0,0]},
              "Sprite": {"water": 0, "fire": 0, "earth": 0, "fishstick": 0, "duck": 0, "ghost": 0, "demon": 0, "king": 0,
                    "aura": 0, "football": 0, "dream": 0, "punk": 0, "boss": 0, "peanut": 0, "zero point": 0, "grim": 0}
              }
def updateData():
    global spritesCollected, opened
    try:
        with open("sprites.txt", "r+") as f:
            for count2, line in enumerate(f, 1):
                splitLine = line.split(",")
                splitLine = [item.strip() for item in splitLine]
                if splitLine[0] != "nothing":
                    spritesCollected += 1
                if "chest" in splitLine[2]:
                    opened += 1

                if splitLine[0] != "nothing":
                    spriteData["Source"][splitLine[2]][0] += 1
                else:
                    spriteData["Source"][splitLine[2]][1] += 1

                if splitLine[1] != "nothing":
                    spriteData["Sprite"][splitLine[1]] += 1
    except FileNotFoundError:
        pass
    print(spriteData)
updateData()


def draw():
    screen.fill((0, 0, 0))
    we = 0
    chestCountText = smallFont.render(f"Chest Opened: {opened}", True, (255, 255, 255))
    w, h = smallFont.size(f"Chest Opened: {opened}")
    spriteText = smallFont.render(f"Sprites: {spritesCollected}", True, (255, 255, 255))
    screen.blit(chestCountText, (5, 620))
    screen.blit(spriteText, (w+50, 620))
    counter = 0
    for name, value in spriteData["Source"].items():
        chestAnalysisText = smallFont.render(f"{name}: {value}\nSprite percentage:{value[0]/(value[0]+value[1])*100:.2f}",
                                          True, (255, 255, 255))
        screen.blit(chestAnalysisText, (5 + we + 40*counter, 670))
        counter += 1
        we += smallFont.size(f"Sprite percentage:{value[0]/(value[0]+value[1])*100:.2f}")[0]
    we = 0
    counter = 0
    for name, value in spriteData["Sprite"].items():
        if counter == 13:
            we = 0
        spriteCountText = smallFont.render(f"{name}: {value}", True, (255, 255, 255))
        if counter > 12:
            screen.blit(spriteCountText, (5 + we + 30 * (counter-13), 780))
        else:
            screen.blit(spriteCountText, (5 + we + 30*counter, 750))
        we += smallFont.size(f"{name}: {value}")[0]
        counter += 1

    button_group.draw(screen)


while running:
    events = pygame.event.get()
    button_group.handle_event(events)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(60) / 1000
    draw()

    pygame.display.flip()
pygame.quit()
sys.exit()