# -*- encoding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from mysprite import MySprite
from projectiles import *

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

SNIPER_SPEED        = 0.12  # px / ms
SNIPER_JUMP_SPEED   = 0.27  # px / ms
SNIPER_ANIM_DELAY   = 5     # updates / image
SNIPER_STUN_DELAY    = 350

# World constants
GRAVITY = 0.0009    # px / ms^2

#---------------------------
#---------Classes-----------
#---------------------------


#------------------------------------
# Character classes

class Character(MySprite):

    jumpTime = PLAYER_BASE_JUMP  # Time you can keep jumping to increase height
    attackTime = 0               # If this is larger than 0 character has to wait to attack
    attacking = False
    stunnedTime = 0              # Time left in stun
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
        self.sheet = GestorRecursos.CargarImagen(imageFile, -1)
        self.sheet = self.sheet.convert_alpha()
        # Starting movement
        self.movement = STILL
        self.looking = RIGHT

        # Reading the coordinates
        data = GestorRecursos.CargarArchivoCoordenadas(coordFile)
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

        # Delay when changing sprite image
        self.movementDelay = 0;

        self.numStance = STILL

        self.rect = pygame.Rect(100,100, self.sheetCoords[self.numStance][self.numImageStance][2],
                                self.sheetCoords[self.numStance][self.numImageStance][3])

        self.runSpeed = runSpeed
        self.jumpSpeed = jumpSpeed

        self.animationDelay = animDelay

        self.updateStance()

    def move(self, movement):
        if self.stunnedTime >= 0:
            self.movement = STUNNED
        else:
            if movement == UP:
                if self.numStance == SPRITE_JUMP:
                    if self.jumpTime <= 0:
                        self.movement = STILL
                else:
                    self.movement = UP
            elif movement == UPRIGHT:
                if self.numStance == SPRITE_JUMP:
                    if self.jumpTime <= 0:
                        self.movement = RIGHT
                else: self.movement = UPRIGHT
            elif movement == UPLEFT:
                if self.numStance == SPRITE_JUMP:
                    if self.jumpTime <= 0:
                        self.movement = LEFT
                else:
                    self.movement = UPLEFT
            else:
                self.movement = movement



    def updateStance(self):
        self.movementDelay -= 1
        if (self.movementDelay < 0):
            self.movementDelay = self.animationDelay
            self.numImageStance += 1
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


    def update(self, platformGroup, projectileGroup, time):

        (speedx, speedy) = self.speed

        if (self.movement == LEFT) or (self.movement == RIGHT):
            self.looking = self.movement

            if self.movement == LEFT:
                speedx = -self.runSpeed
            else:
                speedx = self.runSpeed

            if self.numStance != SPRITE_JUMP:
                # if player is standing on solid ground, reset jump timer
                self.jumpTime = PLAYER_BASE_JUMP
                self.numStance = SPRITE_WALK
                if pygame.sprite.spritecollideany(self, platformGroup) is None:
                    self.numStance = SPRITE_JUMP

        elif (self.movement == UP) or (self.movement == UPLEFT) or (self.movement == UPRIGHT):
            # if player is jumping, decrease time to keep jumping
            self.jumpTime -= time
            self.numStance = SPRITE_JUMP
            speedy = -self.jumpSpeed
            if (self.movement == UPLEFT):
                speedx = -self.runSpeed
            elif (self.movement == UPRIGHT):
                speedx = self.runSpeed

        elif self.movement == STILL:
            self.timejumping = PLAYER_BASE_JUMP
            if not self.numStance == SPRITE_JUMP:
                self.numStance = SPRITE_STILL
            speedx = 0

        if self.movement == STUNNED:
            self.stunnedTime -= time


        if self.numStance == SPRITE_JUMP:

            platform = pygame.sprite.spritecollideany(self, platformGroup)
            # if falling onto a platform
            if (platform is not None) and (speedy > 0) and (platform.rect.bottom>self.rect.bottom):
                # set y value to top of the platform and break fall
                self.setPosition((self.position[0], platform.position[1]-platform.rect.height+1))
                self.numStance = SPRITE_STILL
                speedy = 0

            else:
                speedy += GRAVITY * time
        self.updateStance()
        self.speed = (speedx, speedy)
        MySprite.update(self, time)

        return




class Player(Character):
    # Any player character
    def __init__(self):
        Character.__init__(self, 'Soma.png', 'coordSoma.txt',
                    [5, 12, 5], PLAYER_SPEED, PLAYER_JUMP_SPEED, PLAYER_ANIM_DELAY)

    #def move(self, pressedKeys, up, down, left, right):
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



    def update(self, platformGroup, projectileGroup, time):

        if self.attacking:
            self.attackTime = PLAYER_ATTACK_DELAY

            if (self.looking == RIGHT):
                projectileGroup.add(swordSlash(self.position, self.looking))
            else :
                projectileGroup.add(swordSlash((self.position[0] , self.position[1]), self.looking))
            self.attacking = False
        elif self.attackTime > 0:
            self.attackTime -= time
        Character.update(self, platformGroup, projectileGroup, time)


class NPC(Character):

    def __init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay):
        Character.__init__(self, imageFile, coordFile, nImages, runSpeed, jumpSpeed, animDelay)

#    def move_cpu(self, player1, player2):
    def move_cpu(self, player):
        return

class Sniper(NPC):
    def __init__(self):

        NPC.__init__(self, 'Sniper.png', 'coordSniper.txt', [5, 10, 6],
                     SNIPER_SPEED, SNIPER_JUMP_SPEED, SNIPER_ANIM_DELAY)

    def move_cpu(self, player1):

        if (self.rect.left > 0) and (self.rect.right < ANCHO_PANTALLA) \
                and (self.rect.bottom > 0) and (self.rect.top < ALTO_PANTALLA):
            if player1.position[0] <  self.position[0]:
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

    def stun(self, speedx, speedy, damage):
        self.stunnedTime = SNIPER_STUN_DELAY
        self.speedx = speedx
        self.speedy = speedy