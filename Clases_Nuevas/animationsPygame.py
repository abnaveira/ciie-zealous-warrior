# -*- encoding: utf-8 -*-

import pyganim

# We extend Pyganimation class to give it a postion
class Animation(pyganim.PygAnimation):
    def __init__(self, *args):
        pyganim.PygAnimation.__init__(self, args)
        # Posicion que tendra esta animacion
        self.positionx = 0
        self.positiony = 0

    def move(self, distancex, distancey):
        self.positionx += distancex
        self.positiony += distancey

    def draw(self, screen):
        self.blit(screen, (self.positionx, self.positiony))


# Animations can be charged from a tuple of frames + milliseconds of duration
class AnimationFromList(Animation):
    def __init__(self, framesList):
        pyganim.PygAnimation.__init__(self, framesList)
