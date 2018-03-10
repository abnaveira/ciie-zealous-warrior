# -*- coding: utf-8 -*-

from scene import PygameScene
from xmlLevelParser import *
from characters import *
from scrollControl import *

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

        # Stores all the platforms of the level
        self.platformsGroup = pygame.sprite.Group.empty()
        for platform in platformList:
            self.platformsGroup.add(platform)

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

    def update(self, time):

        # Update dinamic sprites
        self.dinamicSpritesGroup.update(self.platformsGroup, time)

        # Update scroll
        self.controlScroll.updateScroll(self.player, self.spritesGroup)

        # Update the background if it is necessary
        self.background.update(time)

    def draw(self, screen):
        self.background.draw(screen)
        self.scenery.draw(screen)
        self.spritesGroup.draw(screen)

    def events(self, events_list):
        # Miramos a ver si hay algun evento de salir del programa
        for event in events_list:
            # Si se quiere salir, se le indica al director
            if event.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.player.move(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

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
        self.image = GestorRecursos.CargarImagen(sceneryObj.file, -1)
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



