# -*- coding: utf-8 -*-

from scene import PygameScene
from xmlLevelParser import *
from characters import *
from scrollControl import *
from resourcesManager import *
from animationsPygame import *

# -------------------------------------------------
# Class for pygame scenes with one player

class PhaseScene(PygameScene):

    def __init__(self, director, levelFile):
        # It reads the file with the level paramethers
        sceneryObj, frontImagesList, frontAnimationsList, backAnimationsList, \
        platformList, playerX, playerY, spawnPointList = loadLevelData(levelFile)

        PygameScene.__init__(self, director, sceneryObj.windowWidth, sceneryObj.windowHeight)

        # Creates the scenary and background
        self.scenery= Scenary(sceneryObj)
        self.background = Background(sceneryObj)

        # Set scroll to (0,0)
        self.scroll = (0, 0)

        # Creates the player and adds it to the group of players
        self.player = Player()
        self.playersGroup = pygame.sprite.Group(self.player)

        # Set the player in its initial position
        self.player.setPosition((playerX, playerY))

        # Initialize the enemy sprites group
        self.enemiesGroup = pygame.sprite.Group()

        # Stores all the platforms of the level
        self.platformsGroup = pygame.sprite.Group.empty()
        for platform in platformList:
            self.platformsGroup.add(platform)

        # Loads the animations in the front
        self.frontAnimations = []
        for frontAnimation in frontAnimationsList:
            for scaleAndPlacement in frontAnimation.scaleAndPlacementList:
                animation = AnimationFromList(frontAnimation.frameList)
                if ((scaleAndPlacement.scaleX != 0) and (scaleAndPlacement.scaleY != 0)):
                    animation.scale((scaleAndPlacement.scaleX, scaleAndPlacement.scaleY))
                animation.positionX = scaleAndPlacement.x
                animation.positionY = scaleAndPlacement.y
                animation.play()
                self.frontAnimations.append(animation)

        # Loads the animations in the back
        self.backAnimations = []
        for backAnimation in backAnimationsList:
            for scaleAndPlacement in backAnimation.scaleAndPlacementList:
                animation = AnimationFromList(backAnimation.frameList)
                if ((scaleAndPlacement.scaleX != 0) and (scaleAndPlacement.scaleY != 0)):
                    animation.scale((scaleAndPlacement.scaleX, scaleAndPlacement.scaleY))
                animation.positionX = scaleAndPlacement.x
                animation.positionY = scaleAndPlacement.y
                animation.play()
                # Animation next frame?
                self.backAnimations.append(animation)

        # Creates a group for the dinamic sprites
        self.dinamicSpritesGroup = pygame.sprite.Group(self.player)

        # Creates a group for all the sprites
        self.spritesGroup = pygame.sprite.Group()
        for sprite in self.platformsGroup.sprites():
            self.spritesGroup.add(sprite)
        for sprite in self.dinamicSpritesGroup.sprites():
            self.spritesGroup.add(sprite)

        # Creates the class that will control the scroll
        self.controlScroll = scrollControl(self.scroll, sceneryObj.leftMin, sceneryObj.windowWidth - sceneryObj.leftMin,
                                           sceneryObj.topMin, sceneryObj.windowHeight - sceneryObj.topMin, sceneryObj.windowHeight, \
                                           sceneryObj.windowWidth, self.scenery)

    # Allows to add enemies to the phase
    def addEnemies(self, enemySprite):
        self.enemiesGroup.add(enemySprite)
        self.dinamicSpritesGroup.add(enemySprite)
        self.spritesGroup.add(enemySprite)

    def update(self, time):

        # Update dinamic sprites
        self.dinamicSpritesGroup.update(self.platformsGroup, time)

        # Update scroll
        self.controlScroll.updateScroll(self.player, self.spritesGroup)

        # Update the background if it is necessary
        self.background.update(time)

    def draw(self, screen):
        # Background
        self.background.draw(screen)
        # Back animations
        for animation in self.backAnimations:
            animation.dibujar(screen)
        # Scenery
        self.scenery.draw(screen)
        # Sprites
        self.spritesGroup.draw(screen)
        # Front animations
        for animation in self.frontAnimations:
            animation.dibujar(screen)

    def events(self, events_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        keysPressed = pygame.key.get_pressed()
        self.player.move(keysPressed, K_UP, K_DOWN, K_LEFT, K_RIGHT)

# -------------------------------------------------
# Class created for the scenery platforms

class Platform(MySprite):
    def __init__(self, rectangle):
        MySprite.__init__(self)
        # The platforms will be rectangles
        self.rect = rectangle
        # The position will be set as the size of the platform
        self.setPosition((self.rect.left, self.rect.bottom))
        # The platforms are invisible
        self.image = pygame.Surface((0, 0))


# -------------------------------------------------
# Class for the background

class Background:
    def __init__(self, sceneryObj):
        self.color = (sceneryObj.red, sceneryObj.green, sceneryObj.blue)

    # It has to be implmented if there is some variations over time in the background
    def update(self, time):
        return

    def draw(self, screen):
        screen.fill(self.color)


# -------------------------------------------------
# Class for the scenary

class Scenary:
    def __init__(self, sceneryObj):
        self.image = ResourcesManager.LoadImage(sceneryObj.file, -1)
        self.image = pygame.transform.scale(self.image, (sceneryObj.scaleX, sceneryObj.scaleY))

        self.rect = self.image.get_rect()

        # The subimage that we see
        self.rectSubimage = pygame.Rect(0, 0, sceneryObj.windowWidth, sceneryObj.windowHeight)
        self.rectSubimage.left = 0  # Starts on the left
        self.rectSubimage.bottom = self.rect.bottom # Starts on the bottom

    def update(self, scroll):
        self.rectSubimage.left = scroll[0]
        self.rectSubimage.bottom = self.rect.bottom - scroll[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.rectSubimage)



