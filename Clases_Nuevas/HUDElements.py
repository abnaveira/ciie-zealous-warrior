import pygame
from characters import PLAYER_BASE_HEALTH
from resourcesManager import ResourcesManager
import time as timeLib
import math

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
DESCRIPTION_TEXT_POSITION_X = 300
DESCRIPTION_TEXT_POSITION_Y = 350
#-----------------------
ARROW_X = 320
ARROW_Y = 80
ARROW_WIDTH = 80
ARROW_HEIGHT = 60
#-----------------------
DIALOG_BOX_WIDTH = 750
DIALOG_BOX_HEIGHT = 409
#-----------------------
QUIT_TEXT_POSITION_X = 700
QUIT_TEXT_POSITION_Y = 500
#-----------------------
COUNTER_X = 430
COUNTER_Y = 67

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

class LastEnemyArrow(HUDElement):
    def __init__(self, enemies, player):
        self.image = ResourcesManager.loadImage("arrow.png", -1)
        self.image = pygame.transform.scale(self.image, (ARROW_WIDTH, ARROW_HEIGHT))
        HUDElement.__init__(self, self.image.get_rect())
        self.setScreenPosition((ARROW_X, ARROW_Y))
        self.enemies = enemies
        self.player = player

    def update(self):
        if self.enemies.__len__() > 0 :
            for sprite in self.enemies.sprites():
                enemy_pos = sprite.position
                player_pos = self.player.position
                # Vector between the player and the enemy
                vector = (enemy_pos[0] - player_pos[0], enemy_pos[1] - player_pos[1])
                # Calculates the angle over the horizontal vector (1,0)
                angle = math.acos( vector[0] / (math.sqrt(pow(vector[0],2) + pow(vector[1], 2))) )
                angle = angle*180/math.pi
                # Loads the image and scales it
                self.image = ResourcesManager.loadImage("arrow.png", -1)
                self.image = pygame.transform.scale(self.image, (ARROW_WIDTH, ARROW_HEIGHT))
                if vector[1]>=0:
                    # Arrow to left
                    if angle > 135:
                        self.image = pygame.transform.rotate(self.image, 180)
                    # Arrow to right
                    elif angle < 45:
                        return
                    # Arrow down
                    else:
                        self.image = pygame.transform.rotate(self.image, -90)
                else:
                    # Arrow to left
                    if angle > 135:
                        self.image = pygame.transform.rotate(self.image, 180)
                    # Arrow to right
                    elif angle < 45:
                        return
                    # Arrow up
                    else:
                        self.image = pygame.transform.rotate(self.image, 90)
                break

    def draw(self, screen):
        if self.enemies.__len__() > 0:
            screen.blit(self.image, self.rect)

class TextDialogBox(HUDElement):
    def __init__(self, image, position, width, height):
        self.image = ResourcesManager.loadImageWithAlpha(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        HUDElement.__init__(self, self.image.get_rect())
        self.setScreenPosition(position)

class GUIText(HUDElement):
    def __init__(self, font, color, text, position, time):
        # Creates the text image
        self.image = font.render(text, True, color)
        HUDElement.__init__(self, self.image.get_rect())
        # Sets text in position
        self.setScreenPosition(position)
        # Seconds in which the text is showed
        self.time = time
        self.last_time = 0

    def update(self):
        if self.time>0:
            if self.last_time == 0:
                self.last_time = timeLib.time()
            else:
                now = timeLib.time()
                self.time = self.time - (now - self.last_time)
                self.last_time = now

    def draw(self, screen):
        if self.time > 0:
            screen.blit(self.image, self.rect)

class EnemyCounter(HUDElement):
    def __init__(self, enemies):
        # Asks the resource manager for the font
        self.font = ResourcesManager.loadFont('arial', 30)
        self.enemies = enemies
        self.text = str(self.enemies.__len__())
        # Creates the text image
        self.image = self.font.render(self.text, True, (204, 153, 0))
        HUDElement.__init__(self, self.image.get_rect())
        # Sets text in position
        self.setScreenPosition((COUNTER_X, COUNTER_Y))

    def update(self):
        self.text = str(self.enemies.__len__())
        self.image = self.font.render(self.text, True, (204, 153, 0))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class QuitText(GUIText):
    def __init__(self):
        # Asks the resource manager for the font
        font = ResourcesManager.loadFont('arial', 17)
        GUIText.__init__(self, font, (255, 255, 255), "Presiona \"q\" para saltar",
                         (QUIT_TEXT_POSITION_X, QUIT_TEXT_POSITION_Y), 5)

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
    def __init__(self, spriteStructure, stageInfo, stageIntroStoryList, stageOutroStoryList, stageDeathStoryList):
        # Creates the HUD elements
        self.healthBar = HealthBar(spriteStructure.player)
        self.healthBarDecoration = HealthBarDecoration()
        self.stageText = StageText(stageInfo.title)
        self.descriptionText = DescriptionText(stageInfo.description)
        self.arrow = LastEnemyArrow(spriteStructure.enemyGroup, spriteStructure.player)
        self.quitText = QuitText()
        self.counter = EnemyCounter(spriteStructure.enemyGroup)
        # Initial text boxes
        self.initialBoxes = []
        for box in stageIntroStoryList:
            self.initialBoxes.append(TextDialogBox(box.file,(box.left, box.top), box.width, box.height))
        self.actualInitialBox = 0
        self.stop_initial_boxes = False
        self.actualTime = timeLib.time()
        # Final text boxes
        self.finalBoxes = []
        for box in stageOutroStoryList:
            self.finalBoxes.append(TextDialogBox(box.file,(box.left, box.top), box.width, box.height))
        self.actualFinalBox = 0
        self.stop_final_boxes = False
        # Death text boxes
        self.deathBoxes = []
        for box in stageDeathStoryList:
            self.deathBoxes.append(TextDialogBox(box.file, (box.left, box.top), box.width, box.height))
        self.actualDeathBox = 0
        self.stop_death_boxes = False

    def update(self):
        if self.stop_initial_boxes:
            # Updates the health bar
            self.healthBar.update()
            # Updates the stage title
            self.stageText.update()
            # Updates the description title
            self.descriptionText.update()
            # Updates the enemy arrow
            self.arrow.update()
            # Updates the enemy counter
            self.counter.update()

    def changeBox(self, keypressed, key, scapeKey):
        if keypressed[scapeKey]:
            self.stop_initial_boxes = True
        # Checks if there are more boxes
        if not self.stop_initial_boxes:
            time = timeLib.time() - self.actualTime
            # Only changes if the time is more than one second
            if time > 0.5:
                # Checks if the key is pressed
                if keypressed[key]:
                    self.actualInitialBox += 1
                    self.actualTime = timeLib.time()
        return self.stop_initial_boxes

    def changeFinalBox(self, keypressed, key, scapeKey):
        if keypressed[scapeKey]:
            self.stop_final_boxes = True
        # Checks if there are more boxes
        if not self.stop_final_boxes:
            time = timeLib.time() - self.actualTime
            # Only changes if the time is more than one second
            if time > 0.5:
                # Checks if the key is pressed
                if keypressed[key]:
                    self.actualFinalBox += 1
                    self.actualTime = timeLib.time()
        return self.stop_final_boxes

    def changeDeathBox(self, keypressed, key, scapeKey):
        if keypressed[scapeKey]:
            self.stop_death_boxes = True
        # Checks if there are more boxes
        if not self.stop_death_boxes:
            time = timeLib.time() - self.actualTime
            # Only changes if the time is more than one second
            if time > 0.5:
                # Checks if the key is pressed
                if keypressed[key]:
                    self.actualDeathBox += 1
                    self.actualTime = timeLib.time()
        return self.stop_death_boxes

    def draw(self, final, flagRaised, screen):
        # Checks if the initial boxes ended
        if self.stop_initial_boxes:
            # Checks if the phase is in the final
            if final:
                # Checks if the final boxes ended
                if not self.stop_final_boxes:
                    # Checks if there are more boxes
                    if self.actualFinalBox < self.finalBoxes.__len__():
                        self.finalBoxes[self.actualFinalBox].draw(screen)
                        self.quitText.draw(screen)
                    else:
                        self.stop_final_boxes = True
            else:
                # Draws in correct order the HUD
                self.healthBarDecoration.draw(screen)
                self.healthBar.draw(screen)
                self.stageText.draw(screen)
                self.descriptionText.draw(screen)
                # Only draws the flag if the player has reached the flag
                if flagRaised:
                    self.arrow.draw(screen)
                    self.counter.draw(screen)
        else:
            # Checks if there are more boxes
            if self.actualInitialBox < self.initialBoxes.__len__():
                self.initialBoxes[self.actualInitialBox].draw(screen)
                self.quitText.draw(screen)
            else:
                self.stop_initial_boxes = True

    def drawDeathBoxes(self, screen):
        if not self.stop_death_boxes:
            # Checks if there are more boxes
            if self.actualDeathBox < self.deathBoxes.__len__():
                self.deathBoxes[self.actualDeathBox].draw(screen)
                self.quitText.draw(screen)
            else:
                self.stop_death_boxes = True