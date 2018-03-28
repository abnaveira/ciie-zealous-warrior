# -*- encoding: utf-8 -*-
import pygame

import pyganim

# We extend Pyganimation class to give it a postion
class Animation(pyganim.PygAnimation):
    def __init__(self, *args):
        pyganim.PygAnimation.__init__(self, args)
        # Posicion global que tendra esta animacion
        self.positionX = 0
        self.positionY = 0
        #posicion local
        self.posX =0
        self.posY= 0

    def move(self, distanceX, distanceY):
        self.positionX += distanceX
        self.positionY += distanceY

    def draw(self, screen):
        self.blit(screen, (self.posX, self.posY))


    def setScreenPosition(self, position):
        # Change position
        self.posX=self.positionX-position[0]
        self.posY=self.positionY+position[1]



# Animations can be charged from a tuple of frames + milliseconds of duration
class AnimationFromList(Animation):
    def __init__(self, framesList):
        pyganim.PygAnimation.__init__(self, framesList)
