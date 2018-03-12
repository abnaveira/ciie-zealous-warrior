
from gestorRecursos import *
from mysprite import MySprite
from resourcesManager import *

STILL   = 0
LEFT    = 1
RIGHT   = 2
UP      = 3
DOWN    = 4
UPRIGHT = 5
UPLEFT  = 6

SWORD_SLASH_ANIM_DELAY = 2
SWORD_MOVE_SPEED = 0.01

class Projectile(MySprite):

    def __init__(self, imageFile, coordFile, nImages, moveSpeed, animDelay, looking):

        # First we call parent's constructor
        MySprite.__init__(self)

        # Loading the spritesheet.
        self.sheet = ResourcesManager.loadImage(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        # Starting movement
        self.movement = looking
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

        self.rect = pygame.Rect(100, 100, self.sheetCoords[self.numStance][self.numImageStance][2],
                                self.sheetCoords[self.numStance][self.numImageStance][3])

        self.moveSpeed = moveSpeed
        self.animationDelay = animDelay

        self.updateStance()

    def updateStance(self):
        self.movementDelay -= 1
        if self.movementDelay < 0:
            self.movementDelay = self.animationDelay
            self.numImageStance += 1
            if self.numImageStance >= len(self.sheetCoords[self.numStance]):
                self.ended = True
                self.numImageStance = 0
            if self.numImageStance < 0:
                self.numImageStance = len(self.sheetCoords[self.numStance]) - 1
            self.image = self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance])

            if self.looking == RIGHT:
                self.image = self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance])
            elif self.looking == LEFT:
                self.image = pygame.transform.flip(
                    self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance]), 1, 0)

    def update(self, platformGroup, projectileGroup, time):


        self.updateStance()
        MySprite.update(self, time)

        return

class swordSlash(Projectile):
    ended = False
    def __init__(self, position, looking):
        Projectile.__init__(self, 'swordSlashes.png', 'coordSword.txt',
                           [8], SWORD_MOVE_SPEED, SWORD_SLASH_ANIM_DELAY, looking)
        self.position = position

    def update(self, player, enemyGroup, platformGroup, projectileGroup, time):
        self.position = player.position
        if (self.looking <> RIGHT):
            self.increasePosition((-50, 0))
        enemyCollision = pygame.sprite.spritecollide(self, enemyGroup, False)
        for enemy in iter(enemyCollision):
            #What do we do when we hit an enemy
            enemyGroup.remove(enemy)


        Projectile.update(self, platformGroup, projectileGroup, time)
        if self.ended:
            projectileGroup.remove(self)
