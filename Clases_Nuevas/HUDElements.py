import pygame
from characters import PLAYER_BASE_HEALTH
from resourcesManager import ResourcesManager

HEALTH_BAR_X = 40
HEALTH_BAR_Y = 55
HEALTH_BAR_WIDTH = 250
HEALTH_BAR_HEIGHT = 40

# HUD elements for the level gameplay
class HUDElement(pygame.sprite.Sprite):
    "Sprites for the game"

    def __init__(self):
        # Call the parent constructor
        pygame.sprite.Sprite.__init__(self)
        # Store position
        self.position = (0,0)

    def setScreenPosition(self, position):
        # Change position
        self.position = position
        self.rect.left = self.position[0]
        self.rect.bottom = self.position[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HealthBar(HUDElement):
    def __init__(self, player):
        HUDElement.__init__(self)
        # Set the position
        posX = HEALTH_BAR_X
        posY = HEALTH_BAR_Y
        self.player = player
        self.width = HEALTH_BAR_WIDTH
        self.height = HEALTH_BAR_HEIGHT
        # Creates the healthbar
        rectangle = pygame.Rect(posX, posY, self.width, self.height)
        self.rect = rectangle
        self.image = pygame.Surface((rectangle.width, rectangle.height))
        # Stores the positions
        self.setScreenPosition((posX,posY))
        # Adds color to the healthbar
        self.image.fill((255, 0, 0))

    def update(self, time):
        # Calculates proportion of health
        width = self.width * self.player.HP / PLAYER_BASE_HEALTH
        if (width>0):
            self.image = pygame.Surface((width, self.height))
            self.image.fill((255, 0, 0))
        else:
            self.image = pygame.Surface((0, self.height))

class HealthBarDecoration(HUDElement):
    def __init__(self):
        HUDElement.__init__(self)
        posX = 0
        posY = 0
        self.width = HEALTH_BAR_WIDTH - 10
        self.height = HEALTH_BAR_HEIGHT - 20
        self.image = ResourcesManager.loadImage("health_bar.png", -1)
        rectangle = pygame.Rect(posX, posY, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (300, 100))
        self.rect = rectangle
        self.setScreenPosition((posX, posY))