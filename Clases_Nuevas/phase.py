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
        sceneryObj, platformList, playerX, playerY, spawnPointList = loadLevelData(levelFile)

        PygameScene.__init__(self, director, sceneryObj.windowWidth, sceneryObj.windowHeight)

        # Creamos el decorado y el fondo
        self.scenery= Scenary()
        self.fondo = Cielo()

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

        # Actualizamos el fondo:
        #  la posicion del sol y el color del cielo
        self.fondo.update(time)

    def draw(self, screen):
        # Ponemos primero el fondo
        self.fondo.dibujar(screen)
        # Después el decorado
        self.scenery.draw(screen)
        # Luego los Sprites
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
# Clase Cielo

class Cielo:
    def __init__(self):
        self.sol = GestorRecursos.CargarImagen('sol.png', -1)
        self.sol = pygame.transform.scale(self.sol, (200, 200))

        self.rect = self.sol.get_rect()
        self.posicionx = 0  # El lado izquierdo de la subimagen que se esta visualizando
        self.update(0)

    def update(self, tiempo):
        self.posicionx += 0.2 * tiempo
        if (self.posicionx - self.rect.width >= ANCHO_PANTALLA):
            self.posicionx = 0
        self.rect.right = self.posicionx
        # Calculamos el color del cielo
        if self.posicionx >= ((self.rect.width + ANCHO_PANTALLA) / 2):
            ratio = 2 * ((self.rect.width + ANCHO_PANTALLA) - self.posicionx) / (self.rect.width + ANCHO_PANTALLA)
        else:
            ratio = 2 * self.posicionx / (self.rect.width + ANCHO_PANTALLA)
        self.colorCielo = (100 * ratio, 200 * ratio, 255)

    def dibujar(self, pantalla):
        # Dibujamos el color del cielo
        pantalla.fill(self.colorCielo)
        # Y ponemos el sol
        pantalla.blit(self.sol, self.rect)


# -------------------------------------------------
# Clase Decorado

class Scenary:
    def __init__(self, windowHeight, windowWidth):
        self.image = GestorRecursos.CargarImagen('decorado.png', -1)
        self.image = pygame.transform.scale(self.image, (1200, 700)) # 1200, 300

        self.rect = self.image.get_rect()

        # La subimagen que estamos viendo
        self.rectSubimage = pygame.Rect(0, 0, windowWidth, windowHeight)
        self.rectSubimage.left = 0  # Starts on the left
        self.rectSubimage.bottom = self.rect.bottom # Starts on the bottom

    def update(self, scroll):
        self.rectSubimage.left = scroll[0]
        self.rectSubimage.bottom = self.rect.bottom - scroll[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.rectSubimage)



