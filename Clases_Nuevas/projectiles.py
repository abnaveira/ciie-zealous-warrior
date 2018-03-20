
from gestorRecursos import *
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

SWORD_SLASH_ANIM_DELAY = 2
SWORD_MOVE_SPEED = 0.01

AXE_ANIM_DELAY = 1
AXE_MOVE_SPEED = 0.15

MELTYGOO_ANIM_DELAY = 16

GRAVITY = 0.0009

class Projectile(MySprite):
    # Any "hitting sprite" is a projectile, be it a crossbow bolt or a sword slash
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
        self.moveSpeed = moveSpeed
        self.animationDelay = animDelay


        self.rect = pygame.Rect(100, 100, self.sheetCoords[self.numStance][self.numImageStance][2],
                                self.sheetCoords[self.numStance][self.numImageStance][3])


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
    # A slash from the Player's sword
    def __init__(self, position, looking):
        Projectile.__init__(self, 'swordSlashes.png', 'coordSword.txt',
                           [9], SWORD_MOVE_SPEED, SWORD_SLASH_ANIM_DELAY, looking)
        self.position = position
        self.damage = 10
        self. knockback = (.2,-.4)
        self.ended = False

    def update(self, player, enemyGroup, platformGroup, projectileGroup, time):
        # The slash follows the player character
        self.position = player.position
        self.scroll = player.scroll
        # This compensates for the slash' starting position so the player doesn't attack from its back
        if (self.looking <> RIGHT):
            self.increasePosition((-55, 0))

        enemyCollision = pygame.sprite.spritecollide(self, enemyGroup, False)
        for enemy in iter(enemyCollision):
            #What we do when we hit an enemy
            if (self.looking == RIGHT):
                enemy.stun(self.knockback,self.damage)
            else:
                enemy.stun((-self.knockback[0], self.knockback[1]),self.damage)


        Projectile.update(self, platformGroup, projectileGroup, time)
        if self.ended:
            self.kill()

class axeProj(Projectile):
    def __init__(self, position, looking):
        Projectile.__init__(self, 'AxeKnight.png', 'coordAxeProj.txt',
                           [16], AXE_MOVE_SPEED, AXE_ANIM_DELAY, looking)
        self.position = position
        self.damage = 10
        self.knockback = (.2,-.4)
        self.ended = False
        self.collided = False
        if (looking == RIGHT):
            self.speed = (0.17, -0.45)
        else:
            self.speed = (-0.17, -0.45)


    def update(self, player, enemyGroup, platformGroup, projectileGroup, time):
        # A thrown axe describes a parabola
        self.scroll = player.scroll
        speedx, speedy = self.speed

        speedy += GRAVITY * time

        self.speed = (speedx, speedy)
        if self.rect.colliderect(player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                player.stun(self.knockback, self.damage)
            else:
                player.stun((-self.knockback[0], self.knockback[1]), self.damage)
        collision = pygame.sprite.spritecollideany(self, platformGroup)
        if collision is not None:
            self.collided = True

        Projectile.update(self, platformGroup, projectileGroup, time)
        if self.collided:
            self.kill()

class MeltyGoo(Projectile):
    def __init__(self, position, looking):
        Projectile.__init__(self, 'MeltyZombie.png', 'coordMeltyGoo.txt',
                           [16], 0, MELTYGOO_ANIM_DELAY, looking)
        self.position = position
        self.damage = 5
        self.knockback = (.1,-.3)
        self.ended = False
        self.collided = False

    def update(self, player, enemyGroup, platformGroup, projectileGroup, time):
        # Goo  stays on the platform
        self.scroll = player.scroll
        if self.rect.colliderect(player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                player.stun(self.knockback, self.damage)
            else:
                player.stun((-self.knockback[0], self.knockback[1]), self.damage)

        Projectile.update(self, platformGroup, projectileGroup, time)
        if self.ended:
            self.kill()