# -*- encoding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from mysprite import MySprite
from projectiles import *
from resourcesManager import *

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
PLAYER_BASE_HEALTH = 100


SKELETON_SPEED      = 0.08
SKELETON_JUMP_SPEED = 0.3
SKELETON_ANIM_DELAY = 7
SKELETON_STUN_DELAY = 800
SKELETON_BASE_HEALTH = 20

AXEKNIGHT_SPEED      = 0.04
AXEKNIGHT_JUMP_SPEED = 0.1
AXEKNIGHT_ANIM_DELAY = 5
AXEKNIGHT_ATTACK_DELAY = 1500
AXEKNIGHT_STUN_DELAY = 300
AXEKNIGHT_BASE_HEALTH = 60

MELTYZOMBIE_SPEED = 0.03
MELTYZOMBIE_JUMP_SPEED = 0.1
MELTYZOMBIE_ANIM_DELAY = 9
MELTYZOMBIE_ATTACK_DELAY = 1500
MELTYZOMBIE_STUN_DELAY = 800
MELTYZOMBIE_BASE_HEALTH = 35

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
        self.stunnedTime = 0  # If this is larger than 0 character is hitstunned

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
    def update(self, platformGroup, projectileGroup, time):
        # Separate speed into components for code legibility
        # these are local and are set to the character at the end of the procedure
        (speedx, speedy) = self.speed
        platforms = pygame.sprite.spritecollide(self, platformGroup, False)
        if self.dead:
            self.onDeath(platformGroup, projectileGroup, time)
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

        return

    def stun(self, speed, damage):
        if (self.stunnedTime <= 0):
            self.stunnedTime = self.stunDelay
            self.speed = speed
            self.HP -= damage
            if self.HP <= 0:
                self.dead = True

    def onDeath(self, platformGroup, projectileGroup, time):
        self.kill()

class Player(Character):
    # The player character
    def __init__(self):
        Character.__init__(self, 'Arthur.png', 'coordArthur.txt',
                    [1, 7, 4], PLAYER_SPEED, PLAYER_JUMP_SPEED, PLAYER_ANIM_DELAY)
        self.stunDelay = PLAYER_STUN_DELAY
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
    def update(self, platformGroup, projectileGroup, time):
        # If player is attacking, start cooldown and spawn a projectile.
        if self.attacking:
            self.attacking = False
            self.attackTime = PLAYER_ATTACK_DELAY
            # Otherwise character attacks from its back
            if (self.looking == RIGHT):
                projectileGroup.add(swordSlash(self.position, self.looking))
            else :
                projectileGroup.add(swordSlash((self.position[0] - 50, self.position[1]), self.looking))
        elif self.attackTime > 0:
            self.attackTime -= time
        Character.update(self, platformGroup, projectileGroup, time)


class NPC(Character):

    # Mainly enemies
    def __init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay):
        Character.__init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay)
        self.stunDelay = 0

    def move_cpu(self, player, platformGroup):
        return



class Skeleton(NPC):
    def __init__(self):
        NPC.__init__(self, 'Skeletons.png', 'coordSkeletons.txt', [1, 8, 2],
                     SKELETON_SPEED, SKELETON_JUMP_SPEED, SKELETON_ANIM_DELAY)
        self.stunDelay = SKELETON_STUN_DELAY
        self.HP = SKELETON_BASE_HEALTH


    def move_cpu(self, player1, platformGroup):
        # TODO make some real AI BS
        # Currently enemies don't move if outside the screen
        print(self.HP)
        if (self.rect.left > 0) and (self.rect.right < ANCHO_PANTALLA) \
                and (self.rect.bottom > 0) and (self.rect.top < ALTO_PANTALLA):
            if player1.position[0] < self.position[0]:
                if player1.position[1] < self.position[1]:
                    Character.move(self, UPLEFT)
                else:
                    Character.move(self, LEFT)
            else:
                if player1.position[1] < self.position[1]:
                    Character.move(self, UPRIGHT)
                else:
                    Character.move(self, RIGHT)

        else:
            Character.move(self, STILL)


class AxeKnight(NPC):
    def __init__(self):
        NPC.__init__(self, 'AxeKnight.png', 'coordAxeKnight.txt', [13, 16, 1],
                     AXEKNIGHT_SPEED, AXEKNIGHT_JUMP_SPEED, AXEKNIGHT_ANIM_DELAY)
        self.stunDelay = AXEKNIGHT_STUN_DELAY
        self.attackDelay = AXEKNIGHT_ATTACK_DELAY
        self.attacking = False
        self.HP = AXEKNIGHT_BASE_HEALTH


    def move_cpu(self, player, platformGroup):
        diffPos = self.position[0] - player.position[0]
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

    def update(self, platformGroup, projectileGroup, time):
        if self.attacking:
            self.attacking = False
            self.attackTime = AXEKNIGHT_ATTACK_DELAY
            projectileGroup.add(axeProj(self.position, self.looking))
        elif self.attackTime > 0:
            self.attackTime -= time
        Character.update(self, platformGroup, projectileGroup, time)

class MeltyZombie(NPC):
    def __init__(self):
        NPC.__init__(self, 'MeltyZombie.png', 'coordMeltyZombie.txt', [4, 8, 1],
                     MELTYZOMBIE_SPEED, MELTYZOMBIE_JUMP_SPEED, MELTYZOMBIE_ANIM_DELAY)
        self.stunDelay = MELTYZOMBIE_STUN_DELAY
        self.HP = MELTYZOMBIE_BASE_HEALTH

    def move_cpu(self, player, platformGroup):
        diffPos = self.position[0] - player.position[0]
        direction = LEFT
        edge = False
        if diffPos < 0:
            direction = RIGHT
            diffPos = -diffPos
        if diffPos < 500:
            platform = pygame.sprite.spritecollideany(self, platformGroup)
            if (platform is not None) and (platform.rect.top >= self.rect.bottom - 2 ):
                if (direction == RIGHT) and (platform.rect.right < self.rect.right):
                    edge = True
                elif (direction == LEFT) and (platform.rect.left > self.rect.left):
                    edge = True
            if edge :
                Character.move(self, STILL)
            else:
                Character.move(self, direction)
        else: Character.move(self, STILL)

    def onDeath(self, platformGroup, projectileGroup, time):
        projectileGroup.add(MeltyGoo(self.position, self.looking))
        Character.onDeath(self, platformGroup, projectileGroup, time)