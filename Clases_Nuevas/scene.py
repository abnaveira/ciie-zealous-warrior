# -*- encoding: utf-8 -*-

import pygame

#---------------------------
#---------Constants---------
#---------------------------

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# -------------------------------------------------
# Class scene with its abtract methods

class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("It has to be implemented")

    def eventos(self, *args):
        raise NotImplemented("It has to be implemented")

    def dibujar(self):
        raise NotImplemented("It has to be implemented")

# -------------------------------------------------
# Class for pygame scenes

class PygameScene(Scene):

    def __init__(self, director):
        Scene.__init__(self, director)
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# -------------------------------------------------
# Class for pygame scenes with one player

class PhaseScene(PygameScene):

    def __init__(self, director):
        PygameScene.__init__(self, director)
