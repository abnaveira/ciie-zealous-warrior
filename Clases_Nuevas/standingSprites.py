
from mysprite import MySprite
from resourcesManager import *

# These are here mostly for consistence
STILL   = 0
LEFT    = 1
RIGHT   = 2
UP      = 3
DOWN    = 4
UPRIGHT = 5
UPLEFT  = 6
STUNNED = 7

FLAG_ANIM_DELAY = 6
AXE_MOVE_SPEED = 0.15

GRAVITY = 0.0009

class StandingSprites(MySprite):
    # StandingSprites don't move
    def __init__(self, imageFile, coordFile, nImages, animDelay, looking):

        # First we call parent's constructor
        MySprite.__init__(self)

        # Loading the spritesheet.
        self.sheet = ResourcesManager.loadImage(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        # Where is the image looking
        self.looking = looking

        # Reading the coordinates
        data = ResourcesManager.loadFileCoordinates(coordFile)
        data = data.split()
        self.numStance = 1
        self.numImageStance = 0
        counter = 0
        self.sheetCoords = []
        line = 0
        self.sheetCoords.append([])
        tmp = self.sheetCoords[line]
        for stance in range(1, nImages[line] + 1):
            tmp.append(pygame.Rect((int(data[counter]), int(data[counter + 1])),
                                   (int(data[counter + 2]), int(data[counter + 3]))))
            counter += 4

        # Delay when changing sprite image
        self.movementDelay = 0
        self.numStance = STILL
        self.animationDelay = animDelay


        self.rect = pygame.Rect(100, 100, self.sheetCoords[self.numStance][self.numImageStance][2],
                                self.sheetCoords[self.numStance][self.numImageStance][3])


        self.updateStance()

    def updateStance(self):
        # Every frame a counter is decreased
        self.movementDelay -= 1
        # If it runs out, it's time to change the sprite shown.
        if (self.movementDelay < 0):
            self.movementDelay = self.animationDelay
            self.numImageStance += 1
            # If we run out of stances, the loop is reset
            if self.numImageStance >= len(self.sheetCoords[self.numStance]):
                self.numImageStance = 0
            if self.numImageStance < 0:
                self.numImageStance = len(self.sheetCoords[self.numStance])-1
            self.image = self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance])
            if self.looking == RIGHT:
                self.image = self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance])
            elif self.looking == LEFT:
                self.image = pygame.transform.flip(
                    self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance]), 1, 0)

    def update(self, time):
        self.updateStance()
        MySprite.update(self, time)

        return

class Banner(StandingSprites):
    # The banner sprite
    def __init__(self, position):
        StandingSprites.__init__(self, 'banner.png', 'coordBanner.txt',
                    [10], FLAG_ANIM_DELAY, LEFT)
        self.position = position

    def update(self, player, time):
        self.scroll = player.scroll
        StandingSprites.update(self, time)