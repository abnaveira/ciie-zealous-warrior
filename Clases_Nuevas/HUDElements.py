import pygame
from characters import PLAYER_BASE_HEALTH
from resourcesManager import ResourcesManager
import time as timeLib

HEALTH_BAR_X = 78
HEALTH_BAR_Y = 52
HEALTH_BAR_WIDTH = 185
HEALTH_BAR_HEIGHT = 18
#-----------------------
HEALTH_BAR_DECORATION_X = 30
HEALTH_BAR_DECORATION_Y = 80
HEALTH_BAR_DECORATION_WIDTH = 250
HEALTH_BAR_DECORATION_HEIGHT = 80
#-----------------------
STAGE_TEXT_POSITION_X = 300
STAGE_TEXT_POSITION_Y = 300
#-----------------------
DESCRIPTION_TEXT_POSITION_X = 400
DESCRIPTION_TEXT_POSITION_Y = 350

# HUD elements for the level gameplay
class HUDElement:

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

class GUIText(HUDElement):
    def __init__(self, font, color, text, position, time):
        # Creates the text image
        self.image = font.render(text, True, color)
        HUDElement.__init__(self, self.image.get_rect())
        # Sets text in position
        self.setScreenPosition(position)
        # Seconds in which the text is showed
        self.time = time
        self.last_time = timeLib.time()

    def update(self):
        if self.time>0:
            now = timeLib.time()
            self.time = self.time - (now - self.last_time)
            self.last_time = now

    def draw(self, screen):
        if self.time > 0:
            screen.blit(self.image, self.rect)



class StageText(GUIText):
    def __init__(self, text):
        # Asks the resource manager for the font
        font = ResourcesManager.loadFont('arial', 100)
        GUIText.__init__(self, font, (255, 255, 255), text, (STAGE_TEXT_POSITION_X, STAGE_TEXT_POSITION_Y), 5)

class DescriptionText(GUIText):
    def __init__(self, text):
        # Asks the resource manager for the font
        font = ResourcesManager.loadFont('arial', 40)
        GUIText.__init__(self, font, (255, 255, 255), text, (DESCRIPTION_TEXT_POSITION_X, DESCRIPTION_TEXT_POSITION_Y), 5)

# Main class for the HUD
class HUD():
    def __init__(self, player, title, description):
        # Creates the HUD elements
        self.healthBar = HealthBar(player)
        self.healthBarDecoration = HealthBarDecoration()
        self.stageText = StageText(title)
        self.descriptionText = DescriptionText(description)

    def update(self):
        # Updates the health bar
        self.healthBar.update()
        self.stageText.update()
        self.descriptionText.update()

    def draw(self, screen):
        # Draw in correct order the HUD
        self.healthBarDecoration.draw(screen)
        self.healthBar.draw(screen)
        self.stageText.draw(screen)
        self.descriptionText.draw(screen)