# -*- encoding: utf-8 -*-

import pygame, sys, os
import math
from pygame.locals import *
from escena import *
from gestorRecursos import *
from mysprite import MySprite
from projectiles import *
from resourcesManager import *
from potionSprites import *

#---------------------------
#---------Constants---------
#---------------------------

# Movement
STILL   = 0
LEFT    = 1
RIGHT   = 2
UP      = 3
DOWN    = 4
UPRIGHT = 5
UPLEFT  = 6
STUNNED = 7

# Sprite Animations
SPRITE_STILL = 0
SPRITE_WALK  = 1
SPRITE_JUMP  = 2

# Character constants
PLAYER_SPEED        = 0.2   # px / ms
PLAYER_JUMP_SPEED   = 0.37  # px / ms
PLAYER_ANIM_DELAY   = 5     # updates / image
PLAYER_BASE_JUMP    = 350   # time to "keep jumping" to go higher
PLAYER_ATTACK_DELAY = 400   # time between attacks
PLAYER_STUN_DELAY   = 400
PLAYER_INVUL_DELAY  = 1500
PLAYER_BASE_HEALTH  = 100


SKELETON_SPEED       = 0.08
SKELETON_JUMP_SPEED  = 0.3
SKELETON_ANIM_DELAY  = 7
SKELETON_STUN_DELAY  = 800
SKELETON_BASE_HEALTH = 20
SKELETON_HIT_DMG     = 8
SKELETON_HIT_KB      = (.1,-.3)

AXEKNIGHT_SPEED        = 0.04
AXEKNIGHT_JUMP_SPEED   = 0.1
AXEKNIGHT_ANIM_DELAY   = 5
AXEKNIGHT_ATTACK_DELAY = 2000
AXEKNIGHT_STUN_DELAY   = 300
AXEKNIGHT_BASE_HEALTH  = 60
AXEKNIGHT_HIT_DMG      = 20
AXEKNIGHT_HIT_KB       = (.3, -.4)

MELTYZOMBIE_SPEED        = 0.03
MELTYZOMBIE_JUMP_SPEED   = 0.1
MELTYZOMBIE_ANIM_DELAY   = 9
MELTYZOMBIE_ATTACK_DELAY = 1500
MELTYZOMBIE_STUN_DELAY   = 800
MELTYZOMBIE_BASE_HEALTH  = 35
MELTYZOMBIE_HIT_DMG      = 10
MELTYZOMBIE_HIT_KB       = (.15, -.25)

IMP_SPEED        = 0.19
IMP_JUMP_SPEED   = 0
IMP_ANIM_DELAY   = 4
IMP_ATTACK_DELAY = 750
IMP_STUN_DELAY   = 750
IMP_BASE_HEALTH  = 5
IMP_HIT_DMG      = 6
IMP_HIT_KB       = (.15, -.25)

ZEBESIAN_SPEED        = 0.12
ZEBESIAN_JUMP_SPEED   = 0.3
ZEBESIAN_ANIM_DELAY   = 9
ZEBESIAN_ATTACK_DELAY = 2000
ZEBESIAN_STUN_DELAY   = 1500
ZEBESIAN_BASE_HEALTH  = 25
ZEBESIAN_HIT_DMG      = 10
ZEBESIAN_HIT_KB       = (.15, -.25)

# World constants
GRAVITY = 0.0009    # px / ms^2

#---------------------------
#---------Classes-----------
#---------------------------


#------------------------------------
# Character classes

class Character(MySprite):


    # Parameters:
    #   Spritesheet file
    #   Coordinate file
    #   Array with number of images in each stance
    #   Run speed
    #   Jump speed
    #   Animation delay

    def __init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay):

        # First we call parent's constructor
        MySprite.__init__(self)

        # Loading the spritesheet.
        self.sheet = ResourcesManager.loadImage(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        # Starting movement
        self.movement = STILL
        self.looking = RIGHT

        # Reading the coordinates
        data = ResourcesManager.loadFileCoordinates(coordFile)
        data = data.split()
        self.numStance = 1
        self.numImageStance = 0

        counter = 0
        self.sheetCoords = []
        for line in range(0, 3):
            self.sheetCoords.append([])
            tmp = self.sheetCoords[line]
            for stance in range(1, nImages[line] + 1):
                tmp.append(pygame.Rect((int(data[counter]), int(data[counter + 1])),
                                       (int(data[counter + 2]), int(data[counter + 3]))))
                counter += 4



        # Default stance is standing
        self.numStance = STILL

        # TODO Define custom hitboxes
        self.rect = pygame.Rect(100,100, self.sheetCoords[self.numStance][self.numImageStance][2],
                                self.sheetCoords[self.numStance][self.numImageStance][3])

        # Default running and jumping speed
        self.runSpeed = runSpeed
        self.jumpSpeed = jumpSpeed
        # Constant to reset sprite change
        self.animationDelay = animDelay
        # Counter to delay sprite change
        self.movementDelay = 0;
        self.jumpTime = PLAYER_BASE_JUMP  # Time you can keep jumping to increase height
        self.attackTime = 0  # If this is larger than 0 character has to wait to attack
        self.attacking = False
        self.dead = False
        self.stunDelay = 0
        self.stunnedTime = 0  # If this is larger than 0 character is hitstunned
        self.invulTime = 0

        self.updateStance()

    # move determines which movement the character will perform based on
    # intention and status
    def move(self, movement):
        # If character has been hit, it will be hitstunned and unable to move.
        if self.stunnedTime >= 0:
            self.numStance = SPRITE_JUMP
            self.movement = STUNNED

        else:
            # If trying to jump:
            # First check if we are standing or on the air
            #   If we are on the air, we will be able to keep jumping as long
            #   as we still have jumpTime
            #   If we are grounded we can simply jump
            if movement == UP:
                if self.numStance == SPRITE_JUMP:
                    if self.jumpTime <= 0:
                        self.movement = STILL
                else:
                    self.movement = UP
            # These cases allow diagonal jumps
            elif movement == UPRIGHT:
                if self.numStance == SPRITE_JUMP:
                    if self.jumpTime <= 0:
                        self.movement = RIGHT
                else:
                    self.movement = UPRIGHT
            elif movement == UPLEFT:
                if self.numStance == SPRITE_JUMP:
                    if self.jumpTime <= 0:
                        self.movement = LEFT
                else:
                    self.movement = UPLEFT
            else:
                self.movement = movement

    # updateStance updates the sprite to be shown
    # (makes characters animate)
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
            # TODO I don't like this, it implies all sprites must be facing the same way on the spritesheet
            if self.looking == RIGHT:
                self.image = self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance])
            elif self.looking == LEFT:
                self.image = pygame.transform.flip(
                    self.sheet.subsurface(self.sheetCoords[self.numStance][self.numImageStance]), 1, 0)

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

    def checkCeiling(self, platforms):
        for platform in iter(platforms):
            if (self.rect.top > platform.rect.top) and (self.rect.bottom < platform.rect.bottom)\
                    and (self.rect.left > platform.rect.left) and (self.rect.right < platform.rect.right):
                return True
        return False

    # update is run every frame to move and change the characters
    # it is the "important" procedure in every cycle
    def update(self, spriteStructure, time):
        # Separate speed into components for code legibility
        # these are local and are set to the character at the end of the procedure
        (speedx, speedy) = self.speed
        platforms = pygame.sprite.spritecollide(self, spriteStructure.platformGroup, False)
        if self.dead:
            self.onDeath(spriteStructure, time)

        if self.invulTime >= 0:
            self.invulTime -= time
        # If character is hitstunned, decrease the hitstun counter
        if self.movement == STUNNED:
            self.stunnedTime -= time
            if (speedx > 0):
                if self.checkWall(RIGHT, platforms):
                    speedx = 0
            elif (speedx < 0):
                if self.checkWall(LEFT, platforms):
                    speedx = 0
        # If moving left or right
        elif (self.movement == LEFT) or (self.movement == RIGHT):
            # Set direction the character is facing
            self.looking = self.movement


            # Set movement speeds
            if self.movement == LEFT:
                if self.checkWall(LEFT, platforms):
                    speedx = 0
                else:
                    speedx = -self.runSpeed
            else:
                if self.checkWall(RIGHT, platforms):
                    speedx = 0
                else:
                    speedx = self.runSpeed

            if self.numStance != SPRITE_JUMP:
                # If player is standing on solid ground, reset jump timer
                self.jumpTime = PLAYER_BASE_JUMP
                self.numStance = SPRITE_WALK
                # If we've run out of solid ground (walking out of a platform), start falling
                if not platforms:
                    self.numStance = SPRITE_JUMP

        elif (self.movement == UP) or (self.movement == UPLEFT) or (self.movement == UPRIGHT):
            # If player is jumping, decrease time to keep jumping and set vert. speed accordingly
            self.jumpTime -= time
            self.numStance = SPRITE_JUMP
            if self.checkCeiling(platforms):
                speedy = 0
            else:
                speedy = -self.jumpSpeed
            # These allow diagonal jumps
            if (self.movement == UPLEFT):
                if self.checkWall(LEFT, platforms):
                    speedx = 0
                else:
                    speedx = -self.runSpeed
            elif (self.movement == UPRIGHT):
                if self.checkWall(RIGHT, platforms):
                    speedx = 0
                else:
                    speedx = self.runSpeed

        # If not doing anything, stand still and reset jump timer
        elif self.movement == STILL:
            self.jumpTime = PLAYER_BASE_JUMP
            if not self.numStance == SPRITE_JUMP:
                self.numStance = SPRITE_STILL
            speedx = 0

        # If on the air, we have to check if we are landing on a platform
        if self.numStance == SPRITE_JUMP:
            for platform in iter(platforms):
                if (speedy > 0) and (platform.rect.top < self.rect.bottom) \
                            and ((self.rect.bottom - self.rect.height/2) < platform.rect.top):
                    # Set y value to top of the platform and break fall
                    self.setPosition((self.position[0], platform.position[1]-platform.rect.height+1))
                    self.numStance = SPRITE_STILL
                    speedy = 0

            # Otherwise, keep falling accelerated by gravity
            if self.numStance != SPRITE_STILL:
                speedy += GRAVITY * time
        self.updateStance()
        self.speed = (speedx, speedy)
        MySprite.update(self, time)
        if(self.position[1] > 3000):
            self.kill()
        return

    def stun(self, speed, damage):
        if (self.invulTime <= 0):
            self.stunnedTime = self.stunDelay
            self.invulTime = self.invulDelay
            self.speed = speed
            self.HP -= damage
            if self.HP <= 0:
                self.dead = True

    def onDeath(self, spriteStructure, time):
        self.kill()

class Player(Character):
    # The player character
    def __init__(self):
        Character.__init__(self, 'Arthur.png', 'coordArthur.txt',
                    [1, 7, 4], PLAYER_SPEED, PLAYER_JUMP_SPEED, PLAYER_ANIM_DELAY)
        self.stunDelay = PLAYER_STUN_DELAY
        self.invulDelay = PLAYER_INVUL_DELAY
        self.HP = PLAYER_BASE_HEALTH

    # Defines movement intention
    # Whatever the player presses on their keyboard will set an intention that will
    # be checked on Character.move. All abilities should start here too.
    def move(self, pressedKeys, up, down, left, right, attack):
        if pressedKeys[up]:
            if pressedKeys[right]:
                Character.move(self, UPRIGHT)
            elif pressedKeys[left]:
                Character.move(self, UPLEFT)
            else:
                Character.move(self, UP)
        elif pressedKeys[left]:
            Character.move(self, LEFT)
        elif pressedKeys[right]:
            Character.move(self, RIGHT)
        else:
            Character.move(self, STILL)
        if pressedKeys[attack]:
            if self.attackTime <= 0:
                self.attacking = True


    # Player's update deals mainly with spawning attacks
    def update(self, spriteStructure, time):
        # If player is attacking, start cooldown and spawn a projectile.
        if self.attacking:
            self.attacking = False
            self.attackTime = PLAYER_ATTACK_DELAY
            # Otherwise character attacks from its back
            if (self.looking == RIGHT):
                spriteStructure.projectileGroup.add(swordSlash(self.position, self.looking))
            else :
                spriteStructure.projectileGroup.add(swordSlash((self.position[0] - 50, self.position[1]), self.looking))
        elif self.attackTime > 0:
            self.attackTime -= time
        Character.update(self, spriteStructure, time)


class NPC(Character):

    # Mainly enemies
    def __init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay):
        Character.__init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay)
        self.stunDelay = 0
        self.invulDelay = 0
        self.attackTime = 0
        self.hitPlayer = None
        self.damage = 0
        self.knockback = (0,0)

    # This parent function checks if the player has bumped into an enemy.
    def move_cpu(self, spriteStructure):
        if self.rect.colliderect(spriteStructure.player.rect):
            self.hitPlayer = spriteStructure.player
        return

    # This parent function damages a player that has bumped into an enemy.
    def update(self, spriteStructure, time):
        if self.hitPlayer is not None:
            if self.stunnedTime <= 0:
                if (self.hitPlayer.looking == RIGHT):
                    self.hitPlayer.stun(self.knockback, self.damage)
                else:
                    self.hitPlayer.stun((-self.knockback[0], self.knockback[1]), self.damage)
            self.hitPlayer = None
        Character.update(self, spriteStructure, time)

    def onDeath(self, spriteStructure, time):
        # Npc's hace a chance to drop a potion on kill
        # Potion spawn percentages chan be changed on potionSprites
        potion = getRandomPotion()
        if (potion != None):
            # Put the potion in the place the enemy is before killing it
            potion.setPosition(self.position)
            # Add to potions group
            spriteStructure.potionsGroup.add(potion)
        self.kill()

# The skeleton walks towards the player (if on view) and tries to bump into him, jumping to match the player's jumps
class Skeleton(NPC):
    def __init__(self):
        NPC.__init__(self, 'Skeletons.png', 'coordSkeletons.txt', [1, 8, 2],
                     SKELETON_SPEED, SKELETON_JUMP_SPEED, SKELETON_ANIM_DELAY)
        self.stunDelay = SKELETON_STUN_DELAY
        self.invulDelay = SKELETON_STUN_DELAY
        self.HP = SKELETON_BASE_HEALTH
        self.knockback = SKELETON_HIT_KB
        self.damage = SKELETON_HIT_DMG


    def move_cpu(self, spriteStructure):
        # TODO make some real AI BS
        # Currently this enemy doesn't move if outside the screen
        if (self.rect.left > 0) and (self.rect.right < ANCHO_PANTALLA) \
                and (self.rect.bottom > 0) and (self.rect.top < ALTO_PANTALLA):
            if spriteStructure.player.position[0] < self.position[0]:
                if spriteStructure.player.position[1] < self.position[1]:
                    Character.move(self, UPLEFT)
                else:
                    Character.move(self, LEFT)
            else:
                if spriteStructure.player.position[1] < self.position[1]:
                    Character.move(self, UPRIGHT)
                else:
                    Character.move(self, RIGHT)

        else:
            Character.move(self, STILL)
        NPC.move_cpu(self, spriteStructure)


#Axeknight walks slowly towards the player (if he sees him) and throws axes in a parabola if on range.
class AxeKnight(NPC):
    def __init__(self):
        NPC.__init__(self, 'AxeKnight.png', 'coordAxeKnight.txt', [13, 16, 1],
                     AXEKNIGHT_SPEED, AXEKNIGHT_JUMP_SPEED, AXEKNIGHT_ANIM_DELAY)
        self.stunDelay = AXEKNIGHT_STUN_DELAY
        self.invulDelay = AXEKNIGHT_STUN_DELAY
        self.attackDelay = AXEKNIGHT_ATTACK_DELAY
        self.attacking = False
        self.HP = AXEKNIGHT_BASE_HEALTH
        self.knockback = AXEKNIGHT_HIT_KB
        self.damage = AXEKNIGHT_HIT_DMG


    def move_cpu(self, spriteStructure):
        diffPos = self.position[0] - spriteStructure.player.position[0]
        direction = LEFT
        if  diffPos < 0:
            direction = RIGHT
            diffPos = -diffPos
        if diffPos < 400:
            if diffPos < 200:
                if self.attackTime <= 0:
                    self.attacking = True
                else:
                    Character.move(self, direction)
            else:
                Character.move(self, direction)
        else:
            Character.move(self, STILL)
        NPC.move_cpu(self, spriteStructure)

    def update(self, spriteStructure, time):
        if self.attacking:
            self.attacking = False
            self.attackTime = self.attackDelay
            spriteStructure.projectileGroup.add(axeProj(self.position, self.looking))
        elif self.attackTime > 0:
            self.attackTime -= time
        NPC.update(self, spriteStructure, time)

# MeltyZombie stays on its platform, moves slowly towards the player and leaves a gooey trail that damages the player.
class MeltyZombie(NPC):
    def __init__(self):
        NPC.__init__(self, 'MeltyZombie.png', 'coordMeltyZombie.txt', [4, 8, 1],
                     MELTYZOMBIE_SPEED, MELTYZOMBIE_JUMP_SPEED, MELTYZOMBIE_ANIM_DELAY)
        self.stunDelay = MELTYZOMBIE_STUN_DELAY
        self.invulDelay = MELTYZOMBIE_STUN_DELAY
        self.HP = MELTYZOMBIE_BASE_HEALTH
        self.attackDelay = MELTYZOMBIE_ATTACK_DELAY
        self.attacking = False
        self.knockback = MELTYZOMBIE_HIT_KB
        self.damage = MELTYZOMBIE_HIT_DMG

    def move_cpu(self, spriteStructure):
        diffPos = self.position[0] - spriteStructure.player.position[0]
        direction = LEFT
        edge = False
        if diffPos < 0:
            direction = RIGHT
            diffPos = -diffPos
        if diffPos < 500:
            platform = pygame.sprite.spritecollideany(self, spriteStructure.platformGroup)
            if (platform is not None) and (platform.rect.top >= self.rect.bottom - 2 ):
                if ((direction == RIGHT) and (platform.rect.right < self.rect.right)) \
                        or ((direction == LEFT) and (platform.rect.left > self.rect.left)):
                    edge = True
            if edge :
                Character.move(self, STILL)
            else:
                Character.move(self, direction)
                if self.numStance != SPRITE_JUMP:
                    if self.attackTime <= 0:
                        self.attacking = True
        else: Character.move(self, STILL)
        NPC.move_cpu(self, spriteStructure)

    def update(self, spriteStructure, time):
        if self.attacking:
            self.attacking = False
            self.attackTime = self.attackDelay
            spriteStructure.projectileGroup.add(MeltyGoo((self.position[0],self.position[1] + 22), self.looking))
        elif self.attackTime > 0:
            self.attackTime -= time
        NPC.update(self, spriteStructure, time)

# The imp is able to fly through platforms toward the player. It is very fast.
class Imp(NPC):
    def __init__(self):
        NPC.__init__(self, 'Imp.png', 'coordImp.txt', [6, 6, 6],
                     IMP_SPEED, IMP_JUMP_SPEED, IMP_ANIM_DELAY)
        self.stunDelay = IMP_STUN_DELAY
        self.invulDelay = IMP_STUN_DELAY
        self.HP = IMP_BASE_HEALTH
        self.attackDelay = IMP_ATTACK_DELAY
        self.attacking = False
        self.direction = (0,0)
        self.numStance = SPRITE_JUMP
        self.knockback = IMP_HIT_KB
        self.damage = IMP_HIT_DMG

    def move_cpu(self, spriteStructure):
        distx = self.position[0] - spriteStructure.player.position[0]
        disty = self.position[1] - spriteStructure.player.position[1]
        #If total distance from player is less than 500
        if(distx*distx + disty*disty) < 250000:
            #Set direction towards player
            angle = math.atan(disty/distx)
            facAngle = 1
            if distx > 0:
                facAngle = -1
            self.direction = (facAngle * self.runSpeed*math.cos(angle), facAngle * self.runSpeed*math.sin(angle))
        else:
            self.direction = (0,0)
        NPC.move_cpu(self, spriteStructure)


    def update(self, spriteStructure, time):
        self.updateStance()
        if (self.stunnedTime <= 0):
            self.speed = self.direction
            if self.attackTime > 0:
                self.attackTime -= time
            if self.hitPlayer is not None and (self.attackTime <= 0):
                if (self.hitPlayer.looking == LEFT):
                    self.hitPlayer.stun(self.knockback, self.damage)
                else:
                    self.hitPlayer.stun((-self.knockback[0], self.knockback[1]), self.damage)
                self.attackTime = IMP_ATTACK_DELAY
                self.stunnedTime = IMP_STUN_DELAY
            self.hitPlayer = None
        else:
            self.stunnedTime -= time
        MySprite.update(self, time)
        if self.dead:
            self.onDeath(spriteStructure, time)

# The Zebesian tries to keep at a controlled distance from the player, getting close if it is too far and
# fleeing if the player gets too close. It fires when at an optimal distance if it has the player in front of him.
class Zebesian(NPC):
    def __init__(self):
        NPC.__init__(self, 'Zebesian.png', 'coordZebesian.txt', [12, 5, 4],
                     ZEBESIAN_SPEED, ZEBESIAN_JUMP_SPEED, ZEBESIAN_ANIM_DELAY)
        self.stunDelay = ZEBESIAN_STUN_DELAY
        self.invulDelay = ZEBESIAN_STUN_DELAY
        self.HP = ZEBESIAN_BASE_HEALTH
        self.attackDelay = ZEBESIAN_ATTACK_DELAY
        self.attacking = False
        self.knockback = ZEBESIAN_HIT_KB
        self.damage = ZEBESIAN_HIT_DMG

    def move_cpu(self, spriteStructure):
        diffPos = self.position[0] - spriteStructure.player.position[0]
        directionP = LEFT
        directionM = RIGHT
        jump = False
        if diffPos < 0:
            directionP = RIGHT
            directionM = LEFT
            diffPos = -diffPos
        if diffPos < 700:
            #Move enemy towards player
            platforms = pygame.sprite.spritecollide(self, spriteStructure.platformGroup, False)
            for platform in iter(platforms):
                if (self.rect.bottom - 5 > platform.rect.top):
                    jump = True
            if diffPos < 200:
                if jump:
                    Character.move(self, directionM + 4)
                else:
                    Character.move(self, directionM)
            elif diffPos < 500:
                if (self.attackTime <= 0) and (abs(self.position[1] - spriteStructure.player.position[1]) < 50):
                    self.attacking = True
                self.looking = directionP
                Character.move(self, STILL)
            elif jump:
                Character.move(self, directionP + 4)
            else:
                Character.move(self, directionP)
        NPC.move_cpu(self, spriteStructure)

    def update(self, spriteStructure, time):
        if self.attacking:
            self.attacking = False
            self.attackTime = self.attackDelay
            spriteStructure.projectileGroup.add(ZebesianBeam((self.position[0], self.position[1] - 25), self.looking))
        elif self.attackTime > 0:
            self.attackTime -= time
        NPC.update(self, spriteStructure, time)