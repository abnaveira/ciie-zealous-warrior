# -*- encoding: utf-8 -*-

import pygame

# -------------------------------------------------
# Class scene with its abtract methods

class Scene:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("It has to be implemented")

    def events(self, *args):
        raise NotImplemented("It has to be implemented")

    def draw(self):
        raise NotImplemented("It has to be implemented")

# -------------------------------------------------
# Class for pygame scenes

class PygameScene(Scene):

    def __init__(self, director, window_width, window_height):
        Scene.__init__(self, director)
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
