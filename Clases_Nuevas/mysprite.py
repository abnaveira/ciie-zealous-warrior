
# --------------------------
# MySprite Class
import pygame


class MySprite(pygame.sprite.Sprite):
    "Sprites for the game"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = (0, 0)
        self.speed = (0, 0)
        self.scroll = (0, 0)

    def setPosition(self, position):
        self.position = position
        self.rect.left = self.position[0] - self.scroll[0]
        self.rect.bottom = self.position[1] - self.scroll[1]

    def setScreenPosition(self, sceneryScroll):
        self.scroll = sceneryScroll
        (scrollx, scrolly) = self.scroll
        (posx, posy) = self.position
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def increasePosition(self, increment):
        (posx, posy) = self.position
        (incrementx, incrementy) = increment
        self.setPosition((posx + incrementx, posy + incrementy))

    def update(self, time):
        incrementx = self.speed[0] * time
        incrementy = self.speed[1] * time
        self.increasePosition((incrementx, incrementy))