# -*- encoding: utf-8 -*-

import pyganim

# We extend Pyganimation class to give it a postion
class Animation(pyganim.PygAnimation):
    def __init__(self, *args):
        pyganim.PygAnimation.__init__(self, args)
        # Posicion que tendra esta animacion
        self.positionX = 0
        self.positionY = 0

    def move(self, distanceX, distanceY):
        self.positionX += distanceX
        self.positionY += distanceY

    def draw(self, screen):
        self.blit(screen, (self.positionX, self.positionY))


# Animations can be charged from a tuple of frames + milliseconds of duration
class AnimationFromList(Animation):
    def __init__(self, framesList):
        pyganim.PygAnimation.__init__(self, framesList)
