import pygame
from characters import PLAYER_BASE_HEALTH
from resourcesManager import ResourcesManager

HEALTH_BAR_X = 78
HEALTH_BAR_Y = 52
HEALTH_BAR_WIDTH = 185
HEALTH_BAR_HEIGHT = 18
#-----------------------
HEALTH_BAR_DECORATION_X = 30
HEALTH_BAR_DECORATION_Y = 80
HEALTH_BAR_DECORATION_WIDTH = 250
HEALTH_BAR_DECORATION_HEIGHT = 80

# HUD elements for the level gameplay
class HUDElement:
    "Sprites for the game"

    def __init__(self, rectangle):
        # Store position
        self.position = (0,0)
        self.rect = rectangle

    def setScreenPosition(self, position):
        # Change position
        self.position = position
        self.rect.left = self.position[0]
        self.rect.bottom = self.position[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HealthBar(HUDElement):
    def __init__(self, player):
        # Set the position
        posX = HEALTH_BAR_X
        posY = HEALTH_BAR_Y
        self.player = player
        self.width = HEALTH_BAR_WIDTH
        self.height = HEALTH_BAR_HEIGHT
        # Creates the healthbar
        rectangle = pygame.Rect(posX, posY, self.width, self.height)
        HUDElement.__init__(self, rectangle)
        self.image = pygame.Surface((self.width, self.height))
        # Stores the positions
        self.setScreenPosition((posX,posY))
        # Adds color to the healthbar
        self.image.fill((255, 0, 0))
        # Creates the decoration
        self.decoration = HealthBarDecoration()

    def update(self):
        # Calculates proportion of health
        width = self.width * self.player.HP / PLAYER_BASE_HEALTH
        # If health greater than 0
        if (width>0):
            self.image = pygame.Surface((width, self.height))
            self.image.fill((179, 0, 0))
        # Otherwise set the bar to be invisible
        else:
            self.image = pygame.Surface((0, 0))


class HealthBarDecoration(HUDElement):
    def __init__(self):
        self.image = ResourcesManager.loadImage("health_bar.png", -1)
        self.image = pygame.transform.scale(self.image, (HEALTH_BAR_DECORATION_WIDTH, HEALTH_BAR_DECORATION_HEIGHT))
        HUDElement.__init__(self, self.image.get_rect())
        self.setScreenPosition((HEALTH_BAR_DECORATION_X, HEALTH_BAR_DECORATION_Y))

# Main class for the HUD
class HUD():
    def __init__(self, player):
        # Creates the HUD elements
        self.healthBar = HealthBar(player)
        self.healthBarDecoration = HealthBarDecoration()

    def update(self):
        # Updates the health bar
        self.healthBar.update()

    def draw(self, screen):
        # Draw in correct order the HUD
        self.healthBarDecoration.draw(screen)
        self.healthBar.draw(screen)