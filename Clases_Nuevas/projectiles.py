
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
SWORD_KB        = (.1,-.3)

AXE_ANIM_DELAY = 1
AXE_MOVE_SPEED = 0.15

BARREL_ANIM_DELAY = 6
BARREL_MOVE_SPEED = 0.22
BARREL_DAMAGE     = 18
BARREL_KB         = (.4, -.25)

MELTYGOO_ANIM_DELAY = 16

ZEBESIANBEAM_ANIM_DELAY = 5
ZEBESIANBEAM_MOVE_SPEED = 0.4
ZEBESIANBEAM_DAMAGE     = 15
ZEBESIANBEAM_KB         = (.3,-.35)

FIREBALL_ANIM_DELAY = 2
FIREBALL_MOVE_SPEED = 0.2
FIREBALL_DAMAGE = 15
FIREBALL_KB = (.2, -.25)

PILLAR_ANIM_DELAY = 8
PILLAR_DAMAGE = 20
PILLAR_KB = (0, -.4)

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

    def update(self, spriteStructure, time):

        self.updateStance()
        MySprite.update(self, time)

        return


    # A slash from the Player's sword
class swordSlash(Projectile):

    def __init__(self, position, looking):
        Projectile.__init__(self, 'swordSlashes.png', 'coordSword.txt',
                           [9], SWORD_MOVE_SPEED, SWORD_SLASH_ANIM_DELAY, looking)
        self.position = position
        self.damage = 10
        self. knockback = SWORD_KB
        self.ended = False

    def update(self, spriteStructure, time):
        # The slash follows the player character
        self.position = spriteStructure.player.position
        self.scroll = spriteStructure.player.scroll
        # This compensates for the slash' starting position so the player doesn't attack from its back
        if (self.looking <> RIGHT):
            self.increasePosition((-55, 0))

        enemyCollision = pygame.sprite.spritecollide(self, spriteStructure.enemyGroup, False)
        for enemy in iter(enemyCollision):
            #What we do when we hit an enemy
            if (self.looking == RIGHT):
                enemy.stun(self.knockback,self.damage)
            else:
                enemy.stun((-self.knockback[0], self.knockback[1]),self.damage)


        Projectile.update(self, spriteStructure, time)
        if self.ended:
            self.kill()

class Barrel(Projectile):
    def __init__(self, position, looking):
        Projectile.__init__(self, 'VariousEnemies.png', 'coordBarrel.txt',
                           [4], BARREL_MOVE_SPEED, BARREL_ANIM_DELAY, looking)
        self.position = position
        self.damage = BARREL_DAMAGE
        self.knockback = BARREL_KB
        self.ended = False
        self.collided = False
        self.falling = True
        self.hitGround = False

        speedy = -0.25
        if (looking == RIGHT):
            self.speed = (BARREL_MOVE_SPEED, speedy)
        else:
            self.speed = (-BARREL_MOVE_SPEED, speedy)


    def update(self, spriteStructure, time):
        self.scroll = spriteStructure.player.scroll
        speedx, speedy = self.speed
        if self.rect.colliderect(spriteStructure.player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                spriteStructure.player.stun(self.knockback, self.damage)
            else:
                spriteStructure.player.stun((-self.knockback[0], self.knockback[1]), self.damage)
        platforms = pygame.sprite.spritecollide(self, spriteStructure.platformGroup, False)
        if platforms:
            speedy = 0

            # Play thump sound first time it hits the floor
            if not self.hitGround:
                self.hitGround = True
                # Play the thump sound
                spriteStructure.soundEffects.thumpSound.play()

            if self.checkWall(self.looking, platforms):
                self.collided = True
        else:
            speedy += GRAVITY * time
        self.speed = (speedx, speedy)




        Projectile.update(self, spriteStructure, time)
        if self.collided:
            self.kill()

    def checkWall(self, direction, platforms):
        if direction == LEFT:
            for platform in iter(platforms):
                if (platform.rect.top + 5 < self.rect.bottom) and (
                        platform.rect.right - 5 < self.rect.left):
                    return True
            return False
        elif direction == RIGHT:
            for platform in iter(platforms):
                if (platform.rect.top + 5 < self.rect.bottom) and (
                        platform.rect.left + 5 > self.rect.right):
                    return True
            return False


# An AxeKnight's projectile is a throwing axe that describes a parabola through the air
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


    def update(self, spriteStructure, time):
        # Set current scroll
        self.scroll = spriteStructure.player.scroll

        # Adjust for gravity
        speedx, speedy = self.speed
        speedy += GRAVITY * time
        self.speed = (speedx, speedy)

        # Check for colisions
        if self.rect.colliderect(spriteStructure.player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                spriteStructure.player.stun(self.knockback, self.damage)
            else:
                spriteStructure.player.stun((-self.knockback[0], self.knockback[1]), self.damage)
        collision = pygame.sprite.spritecollideany(self, spriteStructure.platformGroup)
        if collision is not None:
            self.collided = True

        Projectile.update(self, spriteStructure, time)
        if self.collided:
            self.kill()

# MeltyGoo is a puddle of substance MeltyZombies leave on the floor they squirm along
class MeltyGoo(Projectile):
    def __init__(self, position, looking):
        Projectile.__init__(self, 'MeltyZombie.png', 'coordMeltyGoo.txt',
                           [16], 0, MELTYGOO_ANIM_DELAY, looking)
        self.position = position
        self.damage = 5
        self.knockback = (.1,-.3)
        self.ended = False
        self.collided = False

    def update(self, spriteStructure, time):
        # Goo  stays on the platform
        self.scroll = spriteStructure.player.scroll
        if self.rect.colliderect(spriteStructure.player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                spriteStructure.player.stun(self.knockback, self.damage)
            else:
                spriteStructure.player.stun((-self.knockback[0], self.knockback[1]), self.damage)

        Projectile.update(self, spriteStructure, time)
        if self.ended:
            self.kill()

# Zebesians fire a beam that moves in a straight line until it collides against something
class ZebesianBeam(Projectile):
    def __init__(self, position, looking):
        Projectile.__init__(self, 'Zebesian.png', 'coordBeam.txt',
                           [2], ZEBESIANBEAM_MOVE_SPEED, ZEBESIANBEAM_ANIM_DELAY, looking)
        self.position = position
        self.damage = ZEBESIANBEAM_DAMAGE
        self.knockback = ZEBESIANBEAM_KB
        self.ended = False
        self.collided = False
        if (looking == RIGHT):
            self.speed = (ZEBESIANBEAM_MOVE_SPEED, 0)
        else:
            self.speed = (-ZEBESIANBEAM_MOVE_SPEED, 0)


    def update(self, spriteStructure, time):
        # Zebesian beam goes straight
        self.scroll = spriteStructure.player.scroll
        if self.rect.colliderect(spriteStructure.player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                spriteStructure.player.stun(self.knockback, self.damage)
            else:
                spriteStructure.player.stun((-self.knockback[0], self.knockback[1]), self.damage)
        collision = pygame.sprite.spritecollideany(self, spriteStructure.platformGroup)
        if collision is not None:
            self.collided = True
        Projectile.update(self, spriteStructure, time)
        if self.collided:
            self.kill()

# Fireballs are spawned from the top of the final boss, they fall.
class Fireball(Projectile):
    def __init__(self, position, looking, up):
        Projectile.__init__(self, 'KingSoma.png', 'coordFireball.txt',
                           [8], FIREBALL_MOVE_SPEED, FIREBALL_ANIM_DELAY, looking)
        self.position = position
        self.damage = FIREBALL_DAMAGE
        self.knockback = FIREBALL_KB
        self.ended = False
        self.collided = False
        speedy = -0.05
        if up:
            speedy = -0.20
        if (looking == RIGHT):
            self.speed = (FIREBALL_MOVE_SPEED, speedy)
        else:
            self.speed = (-FIREBALL_MOVE_SPEED, speedy)


    def update(self, spriteStructure, time):
        self.scroll = spriteStructure.player.scroll
        speedx, speedy = self.speed
        speedy += GRAVITY * time
        self.speed = (speedx, speedy)
        if self.rect.colliderect(spriteStructure.player.rect):
            self.collided = True
            if (self.looking == RIGHT):
                spriteStructure.player.stun(self.knockback, self.damage)
            else:
                spriteStructure.player.stun((-self.knockback[0], self.knockback[1]), self.damage)
        collision = pygame.sprite.spritecollideany(self, spriteStructure.platformGroup)
        if collision is not None:
            self.collided = True

        Projectile.update(self, spriteStructure, time)
        if self.collided:
            self.kill()

# These pillars appear in front of the boss when close, they throw the player upwards.
class Pillar(Projectile):
    def __init__(self, position, looking):
        Projectile.__init__(self, 'KingSoma.png', 'coordPillar.txt',
                           [10], 0, PILLAR_ANIM_DELAY, looking)
        self.position = position
        self.damage = PILLAR_DAMAGE
        self.knockback = PILLAR_KB
        self.ended = False
        self.collided = False

    def update(self, spriteStructure, time):
        self.scroll = spriteStructure.player.scroll
        if self.rect.colliderect(spriteStructure.player.rect):
            self.collided = True
            spriteStructure.player.stun(self.knockback, self.damage)

        Projectile.update(self, spriteStructure, time)
        if self.ended:
            self.kill()