# -*- coding: utf-8 -*-

from scene import PygameScene
from xmlLevelParser import *
from characters import *
from scrollControl import *
from animationsPygame import *
from miscSprites import *

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

        # Initializes the enemy sprites group
        self.enemiesGroup = pygame.sprite.Group()

        # Initializes the projectiles sprites group
        self.projectilesGroup = pygame.sprite.Group()

        # Stores all the platforms of the level
        self.platformsGroup = pygame.sprite.Group()
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

        # Creates a list for all the group sprites
        self.spritesList = [self.playersGroup, self.enemiesGroup, self.projectilesGroup,
                            self.platformsGroup, self.frontAnimations, self.backAnimations]

        # Creates the class that will control the scroll
        self.controlScroll = scrollControl(self.scroll, sceneryObj.leftMin, sceneryObj.windowWidth - sceneryObj.leftMin,
                                           sceneryObj.topMin, sceneryObj.windowHeight - sceneryObj.topMin, sceneryObj.windowHeight, \
                                           sceneryObj.windowWidth, self.scenery)

    # Allows to add enemies to the phase
    def addEnemies(self, enemySprite):
        self.enemiesGroup.add(enemySprite)
        self.dinamicSpritesGroup.add(enemySprite)

    def update(self, time):
        # Executes enemy AI
        for enemy in self.enemiesGroup:
            enemy.move_cpu(self.player)

        # Updates the player
        self.player.update(self.platformsGroup, self.projectilesGroup, time)

        # Updates the enemies
        self.enemiesGroup.update(self.platformsGroup, self.projectilesGroup, time)

        # Updates the projectiles
        self.projectilesGroup.update(self.player, self.enemiesGroup, self.platformsGroup, self.projectilesGroup, time)

        # Updates the platforms
        self.platformsGroup.update(time)

        # Update scroll
        self.controlScroll.updateScroll(self.player, self.spritesList)

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
        for group in self.spritesList:
            group.draw(screen)
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
        self.player.move(keysPressed, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
